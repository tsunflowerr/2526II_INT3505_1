$running = Get-Process mongod -ErrorAction SilentlyContinue

if (-not $running) {
    Write-Output "MongoDB khong dang chay."
    exit 0
}

$running | Stop-Process -Force
Write-Output "MongoDB da duoc tat."
