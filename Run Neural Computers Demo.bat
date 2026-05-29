@echo off
REM ===========================================================================
REM  Windowed launcher for the one runnable demo in "Neural Computers"
REM  (arXiv:2604.06425): the Wan2.1 VAE terminal-reconstruction test (Exp. 1).
REM
REM  The paper's TRAINED models (CLIGen / GUIWorld) were never released, so they
REM  cannot be run. This opens the only demo built from public weights; on first
REM  run it downloads the public Wan2.1 VAE from HuggingFace (~hundreds of MB).
REM
REM  Interpreter: set NC_PYTHON to a full Python that has the project's packages
REM  installed (see requirements.txt) if plain `python` on PATH doesn't work.
REM ===========================================================================
setlocal
cd /d "%~dp0"

set "PYEXE=%NC_PYTHON%"
if "%PYEXE%"=="" set "PYEXE=python"

"%PYEXE%" "%~dp0scripts\gui.py"
if errorlevel 1 (
    echo.
    echo The launcher exited with an error.
    echo If it was a missing-package or interpreter problem, install deps with:
    echo     %PYEXE% -m pip install -r requirements.txt
    echo or point NC_PYTHON at a Python that already has them, e.g.:
    echo     set NC_PYTHON=C:\path\to\python.exe ^&^& "%~nx0"
    echo.
    pause
)
endlocal
