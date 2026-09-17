#!/bin/bash
#
# Phase 3 仓库清理脚本
# 用途：删除不必要的生成文件和临时目录
#
# 执行方式：
#   bash cleanup.sh
#
# 作者: Claude Opus 5
# 日期: 2026-09-17

echo "========================================"
echo "Phase 3 仓库清理"
echo "========================================"
echo ""

# 1. 删除生成的报告文件
echo "[1/7] 删除生成的HTML报告..."
rm -f output/*.html
echo "✅ output/*.html"

# 2. 删除execution目录（执行日志）
echo ""
echo "[2/7] 删除execution目录..."
if [ -d "execution" ]; then
    rm -rf execution
    echo "✅ execution/"
else
    echo "ℹ️  execution/ 不存在"
fi

# 3. 删除outputs目录（旧的输出）
echo ""
echo "[3/7] 删除outputs目录..."
if [ -d "outputs" ]; then
    rm -rf outputs
    echo "✅ outputs/"
else
    echo "ℹ️  outputs/ 不存在"
fi

# 4. 删除output/output目录（重复）
echo ""
echo "[4/7] 删除output/output目录..."
if [ -d "output/output" ]; then
    rm -rf output/output
    echo "✅ output/output/"
else
    echo "ℹ️  output/output/ 不存在"
fi

# 5. 删除output/octopus_energy目录（示例输出）
echo ""
echo "[5/7] 删除output/octopus_energy目录..."
if [ -d "output/octopus_energy" ]; then
    rm -rf output/octopus_energy
    echo "✅ output/octopus_energy/"
else
    echo "ℹ️  output/octopus_energy/ 不存在"
fi

# 6. 删除测试生成的文件
echo ""
echo "[6/7] 删除测试生成的文件..."
rm -f test_*.html test_*.docx test_*.md test_report.html
echo "✅ test_*.html test_*.docx test_*.md"

# 7. 删除Python缓存
echo ""
echo "[7/7] 删除Python缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✅ __pycache__/ *.pyc"

echo ""
echo "========================================"
echo "✅ 清理完成"
echo "========================================"
echo ""
echo "保留的文件："
echo "  - test_exporter.py（测试脚本，可手动删除）"
echo "  - test_phase3_integration.py（集成测试，可手动删除）"
echo ""
echo "下一步："
echo "  git add .gitignore"
echo "  git commit -m 'chore: 清理不必要的文件和优化.gitignore'"
echo "  git push"
