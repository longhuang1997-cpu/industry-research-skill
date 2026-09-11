#!/bin/bash

# Industry Research Skill - 快速启动脚本

echo "======================================================================"
echo "  Industry Research Skill - 项目初始化"
echo "======================================================================"

# 进入项目目录
cd "$(dirname "$0")"

echo ""
echo "📂 检查项目结构..."
if [ -f "skill.md" ] && [ -f "config.yaml" ] && [ -f "requirements.txt" ]; then
    echo "✅ 核心配置文件存在"
else
    echo "❌ 核心配置文件缺失"
    exit 1
fi

echo ""
echo "📦 检查Python环境..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "✅ Python已安装: $PYTHON_VERSION"
else
    echo "❌ Python未安装，请先安装Python 3.8+"
    exit 1
fi

echo ""
echo "🔧 安装依赖..."
pip install -r requirements.txt

echo ""
echo "🧪 运行测试..."
python tests/test_basic.py

echo ""
echo "======================================================================"
echo "✅ 项目初始化完成!"
echo "======================================================================"
echo ""
echo "使用方法:"
echo "  快速模式: python orchestrator/orchestrator.py 医疗陪护"
echo "  全量模式: python orchestrator/orchestrator.py 医疗陪护 --mode full"
echo ""
