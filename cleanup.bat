@echo off
REM
REM Phase 3 仓库清理脚本（Windows版本）
REM 用途：删除不必要的生成文件和临时目录
REM
REM 执行方式：
REM   cleanup.bat
REM
REM 作者: Claude Opus 5
REM 日期: 2026-09-17

echo ========================================
echo Phase 3 仓库清理（Windows）
echo ========================================
echo.

REM 1. 删除生成的HTML报告
echo [1/8] 删除生成的HTML报告...
del /Q output\*.html 2>nul
echo 完成 output\*.html
echo.

REM 2. 删除execution目录（执行日志）
echo [2/8] 删除execution目录...
if exist execution (
    rmdir /S /Q execution
    echo 完成 execution\
) else (
    echo 跳过 execution\ 不存在
)
echo.

REM 3. 删除outputs目录（旧的输出）
echo [3/8] 删除outputs目录...
if exist outputs (
    rmdir /S /Q outputs
    echo 完成 outputs\
) else (
    echo 跳过 outputs\ 不存在
)
echo.

REM 4. 删除output\output目录（重复）
echo [4/8] 删除output\output目录...
if exist output\output (
    rmdir /S /Q output\output
    echo 完成 output\output\
) else (
    echo 跳过 output\output\ 不存在
)
echo.

REM 5. 删除output\octopus_energy目录（示例输出）
echo [5/8] 删除output\octopus_energy目录...
if exist output\octopus_energy (
    rmdir /S /Q output\octopus_energy
    echo 完成 output\octopus_energy\
) else (
    echo 跳过 output\octopus_energy\ 不存在
)
echo.

REM 6. 删除测试生成的文件
echo [6/8] 删除测试生成的文件...
del /Q test_*.html test_*.docx test_*.md test_report.html 2>nul
echo 完成 test_*.html test_*.docx test_*.md
echo.

REM 7. 删除Python缓存（__pycache__）
echo [7/8] 删除Python缓存...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
del /S /Q *.pyc 2>nul
echo 完成 __pycache__\ *.pyc
echo.

REM 8. 从Git中移除（如果已跟踪）
echo [8/8] 从Git中移除已跟踪的文件...
git rm --cached -r execution outputs output\output output\octopus_energy 2>nul
git rm --cached output\*.html 2>nul
echo 完成（如果存在）
echo.

echo ========================================
echo 清理完成
echo ========================================
echo.
echo 保留的文件：
echo   - test_exporter.py（测试脚本，可手动删除）
echo   - test_phase3_integration.py（集成测试，可手动删除）
echo.
echo 下一步：
echo   git add .gitignore
echo   git commit -m "chore: 清理不必要的文件"
echo   git push
echo.

pause
