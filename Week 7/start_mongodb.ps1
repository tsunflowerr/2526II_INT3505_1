$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$mongod = Join-Path $root "mongodb-extract\mongodb-win32-x86_64-windows-8.2.6\bin\mongod.exe"
$data = Join-Path $root "mongodb\data"
$logDir = Join-Path $root "mongodb\log"
$log = Join-Path $logDir "mongodb.log"

New-Item -ItemType Directory -Force $data | Out-Null
New-Item -ItemType Directory -Force $logDir | Out-Null

$running = Get-Process mongod -ErrorAction SilentlyContinue
if ($running) {
    Write-Output "MongoDB da dang chay."
    exit 0
}

Start-Process -FilePath $mongod -ArgumentList "--bind_ip 127.0.0.1 --port 27017 --dbpath `"$data`" --logpath `"$log`" --logappend" -WindowStyle Hidden | Out-Null
Start-Sleep -Seconds 2
Write-Output "MongoDB da duoc bat tai localhost:27017"
