@echo off
REM PTC - Windows Start Script
REM Just run this and you're connected to the global PTC network!

echo 🌐 Starting PTC (Private Coin)...
echo 🔄 Connecting to global PTC network...
echo.

REM Start PTC daemon (connects automatically to global network)
echo Starting PTC daemon...
start /B python ptc_mainnet_daemon.py

REM Wait for daemon to start
timeout /t 3 /nobreak >nul

REM Start web wallet
echo Starting PTC wallet...
start /B python ptc_web_wallet.py

echo.
echo ✅ PTC is now running!
echo 🌐 Wallet: http://127.0.0.1:8888
echo 📊 Dashboard: http://127.0.0.1:8080
echo.
echo Press any key to stop PTC...
pause >nul

echo.
echo 🛑 Stopping PTC...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq ptc*" 2>nul
echo ✅ PTC stopped
pause