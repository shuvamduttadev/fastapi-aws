# deploy.ps1
Write-Host "=== FastAPI Lambda CloudFormation Deployment ===" -ForegroundColor Green
Write-Host ""

# Configuration
$StackName = "fastapi-lambda-infrastructure"
$TemplateFile = "lambda-infrastructure.yaml"
$ParametersFile = "lambda-parameters.json"
$Region = "ap-south-1"
$ProjectRoot = "..\..\..\"

# Check AWS CLI
try {
    aws --version | Out-Null
} catch {
    Write-Host "ERROR: AWS CLI not found!" -ForegroundColor Red
    Write-Host "Install from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "AWS CLI: OK" -ForegroundColor Green
Write-Host ""

# Validate template
Write-Host "Validating CloudFormation template..." -ForegroundColor Cyan
aws cloudformation validate-template `
    --template-body file://$TemplateFile `
    --region $Region 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Template validation failed!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Template is valid!" -ForegroundColor Green
Write-Host ""

# Check if stack exists
Write-Host "Checking if stack exists..." -ForegroundColor Cyan
$stackExists = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region 2>$null

if ($stackExists) {
    $action = "update"
    Write-Host "Stack exists - will UPDATE" -ForegroundColor Yellow
} else {
    $action = "create"
    Write-Host "Stack does not exist - will CREATE" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Stack Name: $StackName" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host "Action: $action" -ForegroundColor Cyan
Write-Host ""

# Check if Lambda package exists
$lambdaZipPath = Join-Path $ProjectRoot "lambda-deployment-package.zip"

if (Test-Path $lambdaZipPath) {
    $zipSize = [math]::Round((Get-Item $lambdaZipPath).Length / 1MB, 2)
    $zipDate = (Get-Item $lambdaZipPath).LastWriteTime
    
    Write-Host "Lambda package found:" -ForegroundColor Green
    Write-Host "  Location: $lambdaZipPath" -ForegroundColor Gray
    Write-Host "  Size: $zipSize MB" -ForegroundColor Gray
    Write-Host "  Last modified: $zipDate" -ForegroundColor Gray
    Write-Host ""
    
    $repackage = Read-Host "Repackage Lambda function? (yes/no) [default: no]"
    
    if ($repackage -eq "yes") {
        Write-Host ""
        Write-Host "Repackaging Lambda function..." -ForegroundColor Cyan
        .\package.ps1
        
        if (-not (Test-Path $lambdaZipPath)) {
            Write-Host "ERROR: Lambda package not created!" -ForegroundColor Red
            pause
            exit 1
        }
        
        Write-Host "Lambda package updated!" -ForegroundColor Green
    } else {
        Write-Host "Using existing Lambda package" -ForegroundColor Yellow
    }
} else {
    Write-Host "Lambda package not found. Creating..." -ForegroundColor Yellow
    Write-Host ""
    .\package.ps1
    
    if (-not (Test-Path $lambdaZipPath)) {
        Write-Host "ERROR: Lambda package not found!" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host "Lambda package created!" -ForegroundColor Green
}

Write-Host ""

# Confirm deployment
$confirm = Read-Host "Deploy stack? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Deployment cancelled" -ForegroundColor Yellow
    pause
    exit 0
}

Write-Host ""

# Deploy stack
if ($action -eq "create") {
    Write-Host "Creating CloudFormation stack..." -ForegroundColor Cyan
    
    aws cloudformation create-stack `
        --stack-name $StackName `
        --template-body file://$TemplateFile `
        --parameters file://$ParametersFile `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Stack creation failed!" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host ""
    Write-Host "Waiting for stack creation (10-15 minutes)..." -ForegroundColor Yellow
    Write-Host "This may take a while. Please be patient..." -ForegroundColor Yellow
    
    aws cloudformation wait stack-create-complete `
        --stack-name $StackName `
        --region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Stack creation failed or timed out!" -ForegroundColor Red
        Write-Host "Check AWS Console for details" -ForegroundColor Yellow
        pause
        exit 1
    }
    
    Write-Host "Stack created successfully!" -ForegroundColor Green
    
} else {
    Write-Host "Updating CloudFormation stack..." -ForegroundColor Cyan
    
    aws cloudformation update-stack `
        --stack-name $StackName `
        --template-body file://$TemplateFile `
        --parameters file://$ParametersFile `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region 2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        $errorMsg = $Error[0].Exception.Message
        if ($errorMsg -like "*No updates*") {
            Write-Host "No updates to perform" -ForegroundColor Yellow
        } else {
            Write-Host "ERROR: Stack update failed!" -ForegroundColor Red
            pause
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Waiting for stack update..." -ForegroundColor Yellow
        
        aws cloudformation wait stack-update-complete `
            --stack-name $StackName `
            --region $Region
        
        Write-Host "Stack updated successfully!" -ForegroundColor Green
    }
}

# Upload Lambda package to S3
Write-Host ""
Write-Host "Uploading Lambda package to S3..." -ForegroundColor Cyan

$bucket = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='LambdaCodeBucket'].OutputValue" `
    --output text

if ($bucket -and $bucket -ne "None") {
    Write-Host "S3 Bucket: $bucket" -ForegroundColor Gray
    
    # Change to project root to access the zip file
    Push-Location $ProjectRoot
    
    aws s3 cp lambda-deployment-package.zip s3://$bucket/ --region $Region
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Lambda package uploaded!" -ForegroundColor Green
        
        # Update Lambda function code
        Write-Host ""
        Write-Host "Updating Lambda function..." -ForegroundColor Cyan
        
        aws lambda update-function-code `
            --function-name fastapi-lambda-function `
            --s3-bucket $bucket `
            --s3-key lambda-deployment-package.zip `
            --region $Region | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Lambda function updated!" -ForegroundColor Green
        } else {
            Write-Host "Warning: Lambda update failed" -ForegroundColor Yellow
        }
    }
    
    Pop-Location
} else {
    Write-Host "Warning: Could not find S3 bucket in stack outputs" -ForegroundColor Yellow
}

# Get stack outputs
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Stack Outputs:" -ForegroundColor Cyan
aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs[*].[OutputKey,OutputValue]" `
    --output table

Write-Host ""

# Get CloudFront URL
$cloudfrontUrl = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" `
    --output text

if ($cloudfrontUrl) {
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "Your API is deployed!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "CloudFront URL: $cloudfrontUrl" -ForegroundColor White
    Write-Host "Health Check: ${cloudfrontUrl}/health" -ForegroundColor White
    Write-Host "API Docs: ${cloudfrontUrl}/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: CloudFront takes 10-20 minutes to fully deploy globally" -ForegroundColor Yellow
}

Write-Host ""
pause