# package.ps1 - Docker-based Lambda packaging
Write-Host "=== Packaging FastAPI Lambda Function with Docker ===" -ForegroundColor Green
Write-Host ""

# Configuration
$ProjectRoot = "..\..\..\"
$PackageDir = "lambda_package"
$ZipFile = "lambda-deployment-package.zip"
$DockerfileName = "Dockerfile.lambda"

# Change to project root
Push-Location $ProjectRoot

Write-Host "Working directory: $((Get-Location).Path)" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan
Write-Host ""

# Check Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker not found!" -ForegroundColor Red
    Write-Host "Install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Docker daemon
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker daemon not running!" -ForegroundColor Red
    Write-Host "Start Docker Desktop and try again" -ForegroundColor Yellow
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Docker daemon: Running" -ForegroundColor Green
Write-Host ""

# Check required files
$allFound = $true

if (Test-Path "requirements.txt") {
    Write-Host "requirements.txt: Found" -ForegroundColor Green
} else {
    Write-Host "requirements.txt: NOT FOUND" -ForegroundColor Red
    $allFound = $false
}

if (Test-Path "handler.py") {
    Write-Host "handler.py: Found" -ForegroundColor Green
} else {
    Write-Host "handler.py: NOT FOUND" -ForegroundColor Red
    $allFound = $false
}

if (Test-Path "app") {
    Write-Host "app/: Found" -ForegroundColor Green
} else {
    Write-Host "app/: NOT FOUND" -ForegroundColor Red
    $allFound = $false
}

if (-not $allFound) {
    Write-Host ""
    Write-Host "ERROR: Required files missing!" -ForegroundColor Red
    Write-Host "Current directory: $((Get-Location).Path)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Files in directory:" -ForegroundColor Yellow
    Get-ChildItem | Select-Object Name, Length | Format-Table
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "All prerequisites OK!" -ForegroundColor Green
Write-Host ""

# Clean up old files
Write-Host "Cleaning up old package..." -ForegroundColor Cyan
if (Test-Path $PackageDir) {
    Remove-Item -Recurse -Force $PackageDir
}
if (Test-Path $ZipFile) {
    Remove-Item -Force $ZipFile
}
if (Test-Path $DockerfileName) {
    Remove-Item -Force $DockerfileName
}
Write-Host "Cleanup complete" -ForegroundColor Green
Write-Host ""

# Create Dockerfile
Write-Host "Creating Dockerfile..." -ForegroundColor Cyan
@"
FROM public.ecr.aws/lambda/python:3.11

# Install zip utility
RUN yum install -y zip && yum clean all

# Set working directory
WORKDIR /package

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -t .

# Copy application code
COPY app ./app/
COPY handler.py .

# Clean up unnecessary files
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find . -type f -name "*.pyc" -delete 2>/dev/null || true && \
    find . -type f -name "*.pyo" -delete 2>/dev/null || true && \
    rm -rf boto3 botocore pip setuptools wheel tests test 2>/dev/null || true

# Create ZIP package
RUN cd /package && zip -r9q /lambda.zip .

# Default command (not used, just for documentation)
CMD ["echo", "Lambda package created"]
"@ | Out-File -FilePath $DockerfileName -Encoding utf8 -NoNewline

Write-Host "Dockerfile created" -ForegroundColor Green
Write-Host ""

# Show what will be packaged
Write-Host "Dependencies to install:" -ForegroundColor Yellow
Get-Content requirements.txt | Select-Object -First 10 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
if ((Get-Content requirements.txt).Count -gt 10) {
    Write-Host "  ... and $((Get-Content requirements.txt).Count - 10) more" -ForegroundColor Gray
}
Write-Host ""

# Build Docker image
Write-Host "Building Docker image (this may take 3-5 minutes)..." -ForegroundColor Cyan
Write-Host "Please wait..." -ForegroundColor Yellow
Write-Host ""

docker build -f $DockerfileName -t lambda-packager:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Docker build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Docker image built successfully!" -ForegroundColor Green
Write-Host ""

# Extract package from container (using docker cp method)
Write-Host "Extracting Lambda package from container..." -ForegroundColor Cyan

# Create temporary container
$containerId = docker create lambda-packager:latest 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to create container!" -ForegroundColor Red
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Temporary container: $containerId" -ForegroundColor Gray

# Copy file from container
docker cp "${containerId}:/lambda.zip" "./$ZipFile" 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to copy package!" -ForegroundColor Red
    docker rm $containerId 2>&1 | Out-Null
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Package copied from container" -ForegroundColor Green

# Remove temporary container
docker rm $containerId 2>&1 | Out-Null
Write-Host "Temporary container removed" -ForegroundColor Gray
Write-Host ""

# Verify package was created
if (Test-Path $ZipFile) {
    $size = (Get-Item $ZipFile).Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "Package: $ZipFile" -ForegroundColor White
    Write-Host "Size: $sizeMB MB" -ForegroundColor White
    Write-Host "Location: $((Get-Location).Path)\$ZipFile" -ForegroundColor White
    Write-Host "Method: Docker (Linux-compatible)" -ForegroundColor White
    Write-Host "Runtime: Python 3.11 (AWS Lambda)" -ForegroundColor White
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    
    if ($size -gt 52428800) {
        Write-Host "Warning: Package exceeds 50 MB Lambda direct upload limit" -ForegroundColor Yellow
        Write-Host "Will use S3 upload method" -ForegroundColor Yellow
        Write-Host ""
    }
    
    # Clean up Dockerfile
    Write-Host "Cleaning up temporary files..." -ForegroundColor Cyan
    if (Test-Path $DockerfileName) {
        Remove-Item -Force $DockerfileName
    }
    Write-Host "Cleanup complete" -ForegroundColor Green
    
} else {
    Write-Host "=========================================" -ForegroundColor Red
    Write-Host "ERROR: ZIP file was not created!" -ForegroundColor Red
    Write-Host "=========================================" -ForegroundColor Red
}

# Return to cloudformation directory
Pop-Location

Write-Host ""
Read-Host "Press Enter to exit"