@echo off
cd /d "%~dp0"

start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 6; Start-Process 'http://127.0.0.1:8002'"

python -m uvicorn webapp:app --host 127.0.0.1 --port 8002

pause