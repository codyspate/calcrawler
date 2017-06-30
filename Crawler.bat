CALL ./venv/scripts/activate.bat
echo "Activating Python Environment..."
python --version
start pythonw %~dp0main.py
