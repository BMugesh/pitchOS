# Test script for PitchOS backend
Write-Host "Testing PitchOS Backend..." -ForegroundColor Green

# Test health endpoint
Write-Host "`nTesting health endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host "Health check: " -NoNewline
    Write-Host "SUCCESS" -ForegroundColor Green
    $health | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Health check: " -NoNewline
    Write-Host "FAILED" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

# Test analyzer endpoint
Write-Host "`nTesting analyzer initialization..." -ForegroundColor Yellow
try {
    $test = Invoke-RestMethod -Uri "http://localhost:8000/api/test" -Method Get
    Write-Host "Analyzer test: " -NoNewline
    if ($test.success) {
        Write-Host "SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "FAILED" -ForegroundColor Red
    }
    $test | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Analyzer test: " -NoNewline
    Write-Host "FAILED" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

# Test analysis endpoint
Write-Host "`nTesting analysis endpoint..." -ForegroundColor Yellow
try {
    $body = @{
        content = "We are building a revolutionary AI-powered startup that will change the world."
        mode = "expert"
        source_type = "text"
    } | ConvertTo-Json

    $analysis = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Analysis test: " -NoNewline
    if ($analysis.success) {
        Write-Host "SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "FAILED" -ForegroundColor Red
    }
    Write-Host "Response: $($analysis.error)"
} catch {
    Write-Host "Analysis test: " -NoNewline
    Write-Host "FAILED" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

Write-Host "`nTest completed!" -ForegroundColor Green
