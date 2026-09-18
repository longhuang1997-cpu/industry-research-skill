@echo off
echo ========================================
echo 激进清理 - 只保留核心代码和关键文档
echo ========================================
echo.

cd /d "%~dp0"

echo 正在删除过程材料...
echo.

git rm PHASE3_REVISED_PLAN.md PHASE3_TASK1_PLAN.md PHASE3_TASK2_PLAN.md PHASE3_TASK3_PLAN.md PHASE3_TASK1_COMPLETE.md PHASE3_TASK2_COMPLETE.md PHASE3_TASK3_COMPLETE.md PHASE3_CORE_COMPLETE.md FINAL_SUMMARY.md cleanup.sh cleanup.bat do_cleanup.bat CLEANUP_GUIDE.md MANUAL_CLEANUP_COMMANDS.md REPO_OPTIMIZATION.md NEXT_STEPS.md PR_DESCRIPTION.md AGGRESSIVE_CLEANUP.md test_exporter.py test_phase3_integration.md 2>nul

git rm -r execution output/octopus_energy 2>nul

del /Q "output\*.html" 2>nul
if exist "output\output" rmdir /S /Q "output\output"
if exist "outputs" rmdir /S /Q "outputs"
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"

echo.
echo ========================================
echo 清理完成！
echo ========================================
echo.

git status

echo.
echo 下一步：
echo   git commit -m "chore: 激进清理 - 只保留核心代码和关键文档"
echo   git push
echo.

pause
