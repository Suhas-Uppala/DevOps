# Test API Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Student Feedback API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check API Status
Write-Host "[TEST 1] Checking API Status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/" -Method Get
    Write-Host "✅ API is running!" -ForegroundColor Green
    Write-Host "Message: $($response.message)" -ForegroundColor White
} catch {
    Write-Host "❌ API is NOT running!" -ForegroundColor Red
    Write-Host "Please run START_BACKEND.bat first" -ForegroundColor Red
    exit
}

Write-Host ""

# Test 2: Get all feedback
Write-Host "[TEST 2] Getting all feedback..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/feedback" -Method Get
    Write-Host "✅ Retrieved feedback successfully!" -ForegroundColor Green
    Write-Host "Total feedback: $($response.count)" -ForegroundColor White
} catch {
    Write-Host "❌ Failed to get feedback" -ForegroundColor Red
}

Write-Host ""

# Test 3: Add new feedback
Write-Host "[TEST 3] Adding new feedback..." -ForegroundColor Yellow
try {
    $body = @{
        student_name = "Test Student"
        comment = "This is a test feedback from PowerShell script!"
        rating = 5
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/feedback" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ Feedback added successfully!" -ForegroundColor Green
    Write-Host "Feedback ID: $($response.data.id)" -ForegroundColor White
    Write-Host "Student: $($response.data.student_name)" -ForegroundColor White
} catch {
    Write-Host "❌ Failed to add feedback" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""

# Test 4: Get all feedback again
Write-Host "[TEST 4] Getting updated feedback list..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/feedback" -Method Get
    Write-Host "✅ Retrieved feedback successfully!" -ForegroundColor Green
    Write-Host "Total feedback: $($response.count)" -ForegroundColor White
    
    Write-Host "`nAll Feedback:" -ForegroundColor Cyan
    foreach ($feedback in $response.data) {
        Write-Host "  - ID: $($feedback.id) | $($feedback.student_name) | Rating: $($feedback.rating)/5" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Failed to get feedback" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All tests completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now open: D:\projects\DevOps\student-feedback\frontend\index.html" -ForegroundColor Yellow
Write-Host "in your browser to see the beautiful UI!" -ForegroundColor Yellow
