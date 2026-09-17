@echo off
echo ========================================
echo 执行仓库清理
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] 从Git中移除生成的HTML报告...
git rm "output/医疗陪护_mock_report_20260917_114337.html" 2>nul
git rm "output/测试行业_report_20260916_162405.html" 2>nul
git rm "output/测试行业v1_report_20260916_163523.html" 2>nul
git rm "output/测试行业v2_empty_report_20260916_163523.html" 2>nul
git rm "output/测试行业v2_report_20260916_163523.html" 2>nul
echo 完成
echo.

echo [2/5] 从Git中移除示例输出目录...
git rm -r output/octopus_energy 2>nul
git rm -r output/output 2>nul
echo 完成
echo.

echo [3/5] 从Git中移除执行日志和废弃目录...
git rm -r execution 2>nul
git rm -r outputs 2>nul
echo 完成
echo.

echo [4/5] 删除Python缓存...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
del /S /Q *.pyc 2>nul
echo 完成
echo.

echo [5/5] 删除测试生成的文件（本地）...
del /Q test_*.html test_*.docx test_*.md 2>nul
echo 完成
echo.

echo ========================================
echo 清理完成！
echo ========================================
echo.
echo 下一步：
echo   1. git status（查看状态）
echo   2. git commit -m "chore: 清理不必要的文件"
echo   3. git push
echo.
pause
