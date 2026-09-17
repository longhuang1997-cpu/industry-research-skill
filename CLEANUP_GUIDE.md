# 仓库清理指南

**目的**: 删除不必要的生成文件，优化GitHub仓库

---

## 🗑️ 需要清理的文件

### 1. 生成的报告文件（output/目录）
```
output/医疗陪护_mock_report_20260917_114337.html
output/测试行业_report_20260916_162405.html
output/测试行业v1_report_20260916_163523.html
output/测试行业v2_empty_report_20260916_163523.html
output/测试行业v2_report_20260916_163523.html
```

**原因**: 这些是测试过程中生成的临时报告，不应该提交到Git

---

### 2. execution/目录
```
execution/
```

**原因**: 执行日志，不应该提交到Git

---

### 3. outputs/目录
```
outputs/
```

**原因**: 旧的输出目录，已废弃

---

### 4. output/octopus_energy/目录
```
output/octopus_energy/
├── octopus_wanwuyun_benchmark.md
├── 章鱼能源_研究报告.md
└── 章鱼能源_行业研究报告_完整版.md
```

**原因**: 示例报告输出，不应该提交到Git（可保留一个作为example）

---

### 5. output/output/目录
```
output/output/
```

**原因**: 重复的目录结构

---

### 6. 测试文件（可选删除）
```
test_exporter.py
test_phase3_integration.py
```

**原因**: 测试脚本，已完成测试后可以删除（或保留用于持续测试）

---

## 🛠️ 清理方式

### 方式1：使用清理脚本（推荐）

```bash
# 赋予执行权限
chmod +x cleanup.sh

# 执行清理
bash cleanup.sh
```

---

### 方式2：手动清理

```bash
# 1. 删除生成的HTML报告
rm -f output/*.html

# 2. 删除execution目录
rm -rf execution

# 3. 删除outputs目录
rm -rf outputs

# 4. 删除重复的output/output
rm -rf output/output

# 5. 删除示例输出
rm -rf output/octopus_energy

# 6. 删除测试生成的文件
rm -f test_*.html test_*.docx test_*.md

# 7. 删除Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 8. （可选）删除测试脚本
# rm -f test_exporter.py test_phase3_integration.py
```

---

### 方式3：Windows批处理

```batch
REM 1. 删除生成的HTML报告
del /Q output\*.html

REM 2. 删除execution目录
if exist execution rmdir /S /Q execution

REM 3. 删除outputs目录
if exist outputs rmdir /S /Q outputs

REM 4. 删除重复的output/output
if exist output\output rmdir /S /Q output\output

REM 5. 删除示例输出
if exist output\octopus_energy rmdir /S /Q output\octopus_energy

REM 6. 删除测试生成的文件
del /Q test_*.html test_*.docx test_*.md 2>nul
```

---

## ✅ 清理后提交

```bash
# 1. 提交更新的.gitignore
git add .gitignore
git commit -m "chore: 优化.gitignore，忽略生成文件"

# 2. 从Git历史中移除（如果已提交）
git rm --cached -r execution outputs output/output output/octopus_energy 2>/dev/null
git rm --cached output/*.html 2>/dev/null
git commit -m "chore: 从Git中移除生成文件和临时目录"

# 3. 推送
git push
```

---

## 📊 清理前后对比

### 清理前
```
项目大小: ~50MB
文件数量: ~200个
问题:
  - 包含生成的HTML报告
  - 包含执行日志
  - 包含示例输出
  - .gitignore不完整
```

### 清理后
```
项目大小: ~5MB
文件数量: ~50个
改进:
  - 仅包含源代码和文档
  - .gitignore完整覆盖
  - 仓库结构清晰
```

---

## 🎯 保留的文件结构

清理后，仓库结构如下：

```
industry-research-skill/
├── .gitignore                    # 更新后的忽略规则
├── README.md                     # 项目说明（v3.0-alpha）
├── requirements.txt              # 依赖库
├── irs.py                        # 主入口
├── config.yaml                   # 配置文件（示例）
├── skill.md                      # Skill文档
├── skill_config.yaml             # Skill配置
│
├── config/
│   └── user_models.yaml          # 自定义模型配置
│
├── core/                         # 核心引擎
│   ├── orchestrator.py
│   ├── research_engine.py
│   ├── counter_evidence_engine.py   # Phase 3 任务1
│   ├── user_model_validator.py      # Phase 3 任务2
│   └── user_model_loader.py         # Phase 3 任务2
│
├── output/                       # 输出模块
│   ├── report_generator.py
│   ├── professional_report_generator.py
│   ├── report_exporter.py        # Phase 3 任务3
│   └── quality_checker.py
│
├── docs/
│   └── USER_MODELS_GUIDE.md      # 用户指南
│
├── PHASE3_*.md                   # Phase 3文档（9份）
└── FINAL_SUMMARY.md              # 最终总结
```

---

## ⚠️ 注意事项

1. **保留测试脚本（可选）**
   - `test_exporter.py`
   - `test_phase3_integration.py`
   - 这些可以保留用于持续测试

2. **不要删除文档**
   - 所有`PHASE3_*.md`文件都是重要的项目文档
   - `FINAL_SUMMARY.md`是对话总结

3. **确认后再推送**
   - 清理后先本地检查
   - 确认无误后再推送到GitHub

---

## 🚀 清理完成后

执行清理并推送后，你的GitHub仓库将：

1. ✅ 体积减小90%
2. ✅ 结构清晰
3. ✅ 仅包含源代码和文档
4. ✅ .gitignore规则完整
5. ✅ 准备好创建PR

---

**最后更新**: 2026-09-17  
**作者**: Claude Opus 5 (1M context)
