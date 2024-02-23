@echo off
@setlocal EnableExtensions


cd "%~dp0"

if not exist pyrob_venv (
	echo Creating venv 'pyrob_venv'...
	python -m venv pyrob_venv
)

@call pyrob_venv\Scripts\activate.bat && python -m pip install -r requirements.txt
cmd /K
