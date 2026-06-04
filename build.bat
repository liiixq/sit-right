@echo off
chcp 65001 >nul
setlocal
set PROJECT=%~dp0
set VENV=%PROJECT%.venv
set PYEXE=%VENV%\Scripts\python.exe

REM 隔离用户 site-packages，避免 Anaconda 牵连大库
set PYTHONNOUSERSITE=1

if not exist "%PYEXE%" (
    echo [1/3] 创建虚拟环境 .venv ...
    python -m venv "%VENV%"
    if errorlevel 1 (
        echo 创建 venv 失败，请确认已安装 Python 并加入 PATH。
        pause & exit /b 1
    )
)

echo [2/3] 安装依赖（pystray / Pillow / pyinstaller 5.13.2）...
"%PYEXE%" -m pip install --quiet --upgrade pip
"%PYEXE%" -m pip install --quiet pystray Pillow "pyinstaller==5.13.2"
if errorlevel 1 ( echo 安装依赖失败。 & pause & exit /b 1 )

echo [3/3] 打包 sit-right.exe ...
if exist "%PROJECT%build" rmdir /s /q "%PROJECT%build"
if exist "%PROJECT%dist" rmdir /s /q "%PROJECT%dist"
if exist "%PROJECT%sit-right.spec" del /q "%PROJECT%sit-right.spec"

"%PYEXE%" -m PyInstaller --noconsole --onefile --name sit-right ^
    --distpath "%PROJECT%dist" ^
    --workpath "%PROJECT%build" ^
    --specpath "%PROJECT%" ^
    "%PROJECT%sit_right.py"
if errorlevel 1 ( echo 打包失败。 & pause & exit /b 1 )

echo.
echo ============================================================
echo  打包完成！exe 路径：%PROJECT%dist\sit-right.exe
echo  发给别人时，把这个单文件发过去即可。
echo  退出方式：右键系统托盘图标 → 退出。
echo ============================================================
REM 仅在双击启动时暂停（命令行 / 脚本调用不暂停）
echo %CMDCMDLINE% | findstr /I /C:"/c " >nul && pause
endlocal
