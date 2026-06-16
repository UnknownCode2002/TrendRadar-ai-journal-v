@echo off
chcp 65001 >nul

REM ============================================================
REM  TrendRadar 计划任务一键安装脚本
REM  以管理员身份运行此脚本
REM ============================================================

set VBS_PATH=D:\Projects\project-p\TrendRadar-ai-journal-v\run_hidden.vbs

REM 检查 run_hidden.vbs 是否存在
if not exist "%VBS_PATH%" (
    echo [错误] 找不到文件: %VBS_PATH%
    echo 请修改本脚本中的 VBS_PATH 为实际路径后重试。
    pause
    exit /b 1
)

echo.
echo ========================================
echo  安装 TrendRadar 计划任务
echo ========================================
echo.

REM 任务1：到岗速览（08:35）
schtasks /create /tn "TrendRadar" ^
    /tr "wscript.exe \"%VBS_PATH%\"" ^
    /sc daily /st 08:35 /f
if %errorlevel% neq 0 (
    echo [失败] 到岗速览任务创建失败
) else (
    echo [成功] 到岗速览任务已创建 (08:35)
)
echo.

REM 任务2：采集（11:00 起每2小时，共4次）
schtasks /create /tn "TrendRadar 采集" ^
    /tr "wscript.exe \"%VBS_PATH%\"" ^
    /sc daily /st 11:00 /du 06:00 /ri 120 /f
if %errorlevel% neq 0 (
    echo [失败] 采集任务创建失败
) else (
    echo [成功] 采集任务已创建 (11:00/13:00/15:00/17:00)
)
echo.

REM 任务3：收工汇总（17:25）
schtasks /create /tn "TrendRadar 收工" ^
    /tr "wscript.exe \"%VBS_PATH%\"" ^
    /sc daily /st 17:25 /f
if %errorlevel% neq 0 (
    echo [失败] 收工汇总任务创建失败
) else (
    echo [成功] 收工汇总任务已创建 (17:25)
)
echo.

echo ========================================
echo  全部安装完成！
echo.
echo  任务列表：
echo    TrendRadar       - 08:35  到岗速览
echo    TrendRadar 采集  - 11/13/15/17 时  采集数据
echo    TrendRadar 收工  - 17:25  收工汇总
echo.
echo  如需删除，请运行：
echo    schtasks /delete /tn "TrendRadar" /f
echo    schtasks /delete /tn "TrendRadar 采集" /f
echo    schtasks /delete /tn "TrendRadar 收工" /f
echo ========================================
pause
