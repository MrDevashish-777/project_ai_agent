@echo off
cd /d "%~dp0"
echo Starting HTTP server on http://127.0.0.1:3000
python -m http.server 3000
pause
