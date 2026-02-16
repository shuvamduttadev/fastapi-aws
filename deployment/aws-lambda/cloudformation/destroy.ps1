# destroy.ps1 - Destroy FastAPI Lambda Infrastructure
Write-Host "=== FastAPI Lambda Infrastructure Destruction ===" -ForegroundColor Red
Write-Host ""

# Configuration
$StackName = "fastapi-lambda-infrastructure"
$Region = "ap-south-1"

# Check AWS CLI
try {
    aws --version | Out-Null
} catch {
    Write-Host "ERROR: AWS CLI not found!" -ForegroundColor Red
    pause
    exit 1
}

# Check if stack exists
Write-Host "Checking if stack exists..." -ForegroundColor Cyan
$stackExists = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region 2>$null

if (-not $stackExists) {
    Write-Host "Stack $StackName does not exist." -ForegroundColor Yellow
    Write-Host "Nothing to destroy." -ForegroundColor Green
    pause
    exit 0
}

Write-Host "Stack found: $StackName" -ForegroundColor Yellow
Write-Host ""

# Show what will be deleted
Write-Host "Resources that will be DESTROYED:" -ForegroundColor Red
Write-Host "  - Lambda Function" -ForegroundColor Gray
Write-Host "  - API Gateway" -ForegroundColor Gray
Write-Host "  - CloudFront Distribution" -ForegroundColor Gray
Write-Host "  - S3 Bucket (and all contents)" -ForegroundColor Gray
Write-Host "  - IAM Roles" -ForegroundColor Gray
Write-Host "  - CloudWatch Logs" -ForegroundColor Gray
Write-Host "  - CloudWatch Alarms" -ForegroundColor Gray
Write-Host ""

Write-Host "WARNING: This action cannot be undone!" -ForegroundColor Red
Write-Host ""

# Confirm destruction
$confirm = Read-Host "Type 'destroy' to confirm deletion"

if ($confirm -ne "destroy") {
    Write-Host ""
    Write-Host "Destruction cancelled." -ForegroundColor Yellow
    pause
    exit 0
}

Write-Host ""
Write-Host "Starting destruction process..." -ForegroundColor Yellow
Write-Host ""

# Empty S3 bucket first (required before deletion)
Write-Host "Step 1: Emptying S3 bucket..." -ForegroundColor Cyan

$bucket = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='LambdaCodeBucket'].OutputValue" `
    --output text 2>$null

if ($bucket -and $bucket -ne "None") {
    Write-Host "S3 Bucket: $bucket" -ForegroundColor Gray
    
    # Check if bucket has objects
    $objectCount = aws s3 ls s3://$bucket --recursive --summarize 2>$null | Select-String "Total Objects:" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }
    
    if ($objectCount -and $objectCount -gt 0) {
        Write-Host "Deleting $objectCount object(s)..." -ForegroundColor Gray
        aws s3 rm s3://$bucket --recursive --region $Region 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "S3 bucket emptied successfully" -ForegroundColor Green
        } else {
            Write-Host "Warning: Failed to empty S3 bucket (may cause stack deletion to fail)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "S3 bucket is already empty" -ForegroundColor Green
    }
} else {
    Write-Host "No S3 bucket found (or already deleted)" -ForegroundColor Yellow
}

Write-Host ""

# Delete CloudFormation stack
Write-Host "Step 2: Deleting CloudFormation stack..." -ForegroundColor Cyan
Write-Host "Stack: $StackName" -ForegroundColor Gray
Write-Host "Region: $Region" -ForegroundColor Gray
Write-Host ""

aws cloudformation delete-stack `
    --stack-name $StackName `
    --region $Region

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to initiate stack deletion!" -ForegroundColor Red
    Write-Host "Check AWS Console for details" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Stack deletion initiated" -ForegroundColor Green
Write-Host ""

# Wait for stack deletion
Write-Host "Step 3: Waiting for stack deletion (5-10 minutes)..." -ForegroundColor Cyan
Write-Host "This may take a while. Please be patient..." -ForegroundColor Yellow
Write-Host ""

# Show progress
$startTime = Get-Date
$dots = 0

# Wait with progress indicator
while ($true) {
    Start-Sleep -Seconds 5
    
    # Check if stack still exists
    $stackStatus = aws cloudformation describe-stacks `
        --stack-name $StackName `
        --region $Region `
        --query "Stacks[0].StackStatus" `
        --output text 2>$null
    
    if (-not $stackStatus) {
        # Stack no longer exists - deletion complete
        break
    }
    
    # Show progress
    $elapsed = (Get-Date) - $startTime
    $dots = ($dots + 1) % 4
    $progress = "." * $dots
    Write-Host "`rDeleting$progress Elapsed: $([math]::Round($elapsed.TotalMinutes, 1)) minutes" -NoNewline -ForegroundColor Yellow
}

Write-Host ""
Write-Host ""

# Verify deletion
$finalCheck = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region 2>$null

if ($finalCheck) {
    Write-Host "WARNING: Stack still exists (may be stuck)" -ForegroundColor Yellow
    Write-Host "Status: $stackStatus" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Check AWS CloudFormation Console for details:" -ForegroundColor Yellow
    Write-Host "https://console.aws.amazon.com/cloudformation/home?region=$Region" -ForegroundColor Gray
} else {
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "ALL RESOURCES DESTROYED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Stack Name: $StackName" -ForegroundColor Gray
    Write-Host "Region: $Region" -ForegroundColor Gray
    Write-Host "Deletion completed in: $([math]::Round($elapsed.TotalMinutes, 1)) minutes" -ForegroundColor Gray
}

Write-Host ""
pause