@echo off
title Push VeriVox App to GitHub
cd /d "%~dp0"

set "GIT_PATH=C:\Program Files\Git\cmd;C:\Users\Tanishq\AppData\Local\Programs\Git\cmd;%PATH%"
set "PATH=%GIT_PATH%"

echo ========================================================
echo   Pushing complete VeriVox App to your GitHub repository
echo ========================================================
echo.

git init
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/ta15spec/verivox_app.git
git add -A
git commit -m "Complete VeriVox Android app with updated assets and workflows"
echo.
echo Pushing to GitHub... Please sign in when prompted.
git push -u origin main --force

echo.
echo ========================================================
echo Done! Check your GitHub Actions tab to download the APK.
echo ========================================================
pause
