# ===========================================================================
#           TRIGGER RENDER DEPLOYMENT
# ===========================================================================
# This script triggers a manual deployment on Render
# ===========================================================================

$RENDER_API_KEY = "rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF"
$RENDER_SERVICE_ID = "srv-d3melk56ubrc73eo2180"

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "           TRIGGER RENDER DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

Write-Host "Service ID: $RENDER_SERVICE_ID" -ForegroundColor Cyan
Write-Host "Triggering deployment...`n" -ForegroundColor Yellow

try {
    $headers = @{
        "Authorization" = "Bearer $RENDER_API_KEY"
        "Content-Type" = "application/json"
    }
    
    $body = @{
        "clearCache" = $false
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" `
        -Method POST `
        -Headers $headers `
        -Body $body
    
    Write-Host "✅ Deployment triggered successfully!" -ForegroundColor Green
    Write-Host "`nDeploy ID: $($response.id)" -ForegroundColor Cyan
    Write-Host "Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "`nCheck status at: https://dashboard.render.com/web/$RENDER_SERVICE_ID`n" -ForegroundColor Yellow
    
    # Open dashboard
    Start-Process "https://dashboard.render.com/web/$RENDER_SERVICE_ID"
    
} catch {
    Write-Host "❌ Failed to trigger deployment!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)`n" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody`n" -ForegroundColor Yellow
    }
}

Write-Host "========================================================================`n" -ForegroundColor Cyan

