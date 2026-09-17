# 手动清理命令（精确版本）

**目的**: 精确清理不必要的文件  
**执行位置**: 项目根目录  
**时间**: 约2分钟

---

## 📋 需要清理的文件清单

### 1. Git已跟踪的文件（需要git rm）

```bash
# execution目录（3个文件）
execution/__init__.py
execution/consulting_ai_analyzer.py
execution/model_config.py

# output/octopus_energy/目录（3个文件）
output/octopus_energy/octopus_wanwuyun_benchmark.md
output/octopus_energy/章鱼能源_研究报告.md
output/octopus_energy/章鱼能源_行业研究报告_完整版.md
```

### 2. Git未跟踪的文件（需要直接删除）

```bash
# 生成的HTML报告（5个文件）
output/医疗陪护_mock_report_20260917_114337.html
output/测试行业_report_20260916_162405.html
output/测试行业v1_report_20260916_163523.html
output/测试行业v2_empty_report_20260916_163523.html
output/测试行业v2_report_20260916_163523.html

# output/output/目录（如果存在）
output/output/

# outputs/目录（如果存在）
outputs/
```

---

## 🛠️ 精确清理命令

### Windows命令（复制粘贴即可）

```batch
REM 进入项目目录
cd C:\Users\huangl265\projects\industry-research-skill

REM 1. 从Git中移除execution目录
git rm -r execution

REM 2. 从Git中移除output/octopus_energy目录
git rm -r output/octopus_energy

REM 3. 删除生成的HTML文件（未跟踪，直接删除）
del /Q "output\医疗陪护_mock_report_20260917_114337.html"
del /Q "output\测试行业_report_20260916_162405.html"
del /Q "output\测试行业v1_report_20260916_163523.html"
del /Q "output\测试行业v2_empty_report_20260916_163523.html"
del /Q "output\测试行业v2_report_20260916_163523.html"

REM 4. 删除其他不必要的目录（如果存在）
if exist "output\output" rmdir /S /Q "output\output"
if exist "outputs" rmdir /S /Q "outputs"

REM 5. 删除Python缓存
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
del /S /Q *.pyc

REM 6. 查看状态
git status

REM 7. 提交
git commit -m "chore: 清理不必要的生成文件和示例输出"

REM 8. 推送
git push
```

---

### Linux/Mac命令

```bash
# 进入项目目录
cd /path/to/industry-research-skill

# 1. 从Git中移除execution目录
git rm -r execution

# 2. 从Git中移除output/octopus_energy目录
git rm -r output/octopus_energy

# 3. 删除生成的HTML文件
rm -f output/*.html

# 4. 删除其他不必要的目录
rm -rf output/output outputs

# 5. 删除Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 6. 查看状态
git status

# 7. 提交
git commit -m "chore: 清理不必要的生成文件和示例输出"

# 8. 推送
git push
```

---

## 📊 清理效果预测

### 清理前
```
仓库包含:
✗ execution/ (3个.py文件)
✗ output/octopus_energy/ (3个.md示例)
✗ output/*.html (5个生成的报告)
✗ __pycache__/ (Python缓存)
```

### 清理后
```
仅保留:
✓ 核心代码（core/, output/的.py文件）
✓ 配置文件（config/user_models.yaml）
✓ 文档（docs/, PHASE3_*.md）
✓ 工具脚本（cleanup.bat, cleanup.sh）
✓ .gitignore（阻止未来提交生成文件）
```

---

## ⚠️ 重要说明

### 可以安全删除
- `execution/` - 模型配置和分析器（可以从其他地方获取）
- `output/octopus_energy/` - 示例报告（不是核心代码）
- `output/*.html` - 生成的临时报告
- `__pycache__/` - Python缓存（自动生成）

### 必须保留
- `core/` - 核心引擎
- `output/*.py` - 输出模块代码
- `config/` - 配置文件
- `docs/` - 文档
- `PHASE3_*.md` - Phase 3文档
- `test_*.py` - 测试脚本（可选）

---

## 🎯 执行步骤（复制粘贴即可）

**1. 打开命令行**（Windows: cmd 或 PowerShell）

**2. 复制粘贴以下命令**（完整的清理流程）:

```batch
cd C:\Users\huangl265\projects\industry-research-skill && git rm -r execution && git rm -r output/octopus_energy && del /Q "output\*.html" 2>nul && if exist "output\output" rmdir /S /Q "output\output" && if exist "outputs" rmdir /S /Q "outputs" && for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d" && git status && echo. && echo ========================================&& echo 清理完成，请执行：&& echo git commit -m "chore: 清理不必要的生成文件和示例输出"&& echo git push&& echo ========================================
```

**3. 查看Git状态**

```bash
git status
```

应该看到：
```
Changes to be committed:
  deleted: execution/__init__.py
  deleted: execution/consulting_ai_analyzer.py
  deleted: execution/model_config.py
  deleted: output/octopus_energy/...
```

**4. 提交并推送**

```bash
git commit -m "chore: 清理不必要的生成文件和示例输出

清理内容:
- 删除execution/目录（模型配置）
- 删除output/octopus_energy/（示例报告）
- 删除output/*.html（生成的报告）
- 删除Python缓存（__pycache__）

清理后:
- 仅保留核心代码和文档
- .gitignore已配置阻止未来提交生成文件
- 仓库体积减小，结构清晰"

git push
```

---

## ✅ 验证清理效果

```bash
# 检查Git状态
git status

# 查看仓库文件列表
git ls-files | wc -l

# 确认不再包含不必要的文件
git ls-files | grep -E "(execution|octopus_energy|\.html$)"
# 应该没有输出

# 查看仓库大小
du -sh .
```

---

**最后更新**: 2026-09-17  
**作者**: Claude Opus 5  
**状态**: ✅ 准备执行
