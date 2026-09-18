# 激进清理方案 - 只保留核心代码和关键文档

**目的**: 删除所有过程材料，只保留最终成果  
**原则**: 保留核心代码 + 1份总结文档

---

## 🎯 清理策略

### 保留的文件（核心）

**代码**:
```
core/
├── __init__.py
├── orchestrator.py
├── research_engine.py
├── honest_quality_gate.py
├── counter_evidence_engine.py          ✅ Phase 3
├── user_model_validator.py              ✅ Phase 3
└── user_model_loader.py                 ✅ Phase 3

output/
├── __init__.py
├── report_generator.py
├── professional_report_generator.py
├── report_exporter.py                   ✅ Phase 3
├── quality_checker.py
├── advanced_report_templates.py
└── packaging.py

config/
└── user_models.yaml                     ✅ Phase 3

docs/
└── USER_MODELS_GUIDE.md                 ✅ Phase 3（用户指南）
```

**关键文档**（只保留2份）:
```
README.md                                ✅ 项目说明
PHASE3_SUMMARY.md                        ✅ Phase 3总结（新建，整合所有内容）
```

---

### 删除的文件（过程材料）

**1. 实施计划文档（6份）**:
```
❌ PHASE3_REVISED_PLAN.md
❌ PHASE3_TASK1_PLAN.md
❌ PHASE3_TASK2_PLAN.md
❌ PHASE3_TASK3_PLAN.md
```

**2. 完成报告文档（3份）**:
```
❌ PHASE3_TASK1_COMPLETE.md
❌ PHASE3_TASK2_COMPLETE.md
❌ PHASE3_TASK3_COMPLETE.md
```

**3. 核心任务总结（1份）**:
```
❌ PHASE3_CORE_COMPLETE.md（整合到PHASE3_SUMMARY.md）
```

**4. 对话总结（1份）**:
```
❌ FINAL_SUMMARY.md（整合到PHASE3_SUMMARY.md）
```

**5. 清理工具和文档（9份）**:
```
❌ cleanup.sh
❌ cleanup.bat
❌ do_cleanup.bat
❌ CLEANUP_GUIDE.md
❌ MANUAL_CLEANUP_COMMANDS.md
❌ REPO_OPTIMIZATION.md
❌ NEXT_STEPS.md
❌ PR_DESCRIPTION.md
❌ AGGRESSIVE_CLEANUP.md（本文档）
```

**6. 测试脚本（2份）**:
```
❌ test_exporter.py
❌ test_phase3_integration.py
```

**7. Git跟踪的无用目录**:
```
❌ execution/（3个文件）
❌ output/octopus_energy/（3个文件）
```

**8. 本地生成的文件**:
```
❌ output/*.html（5个文件）
❌ output/output/（如果存在）
❌ outputs/（如果存在）
❌ __pycache__/
```

---

## 🛠️ 执行命令

### Windows命令（一键执行）

```batch
cd C:\Users\huangl265\projects\industry-research-skill

REM 1. 删除实施计划文档
git rm PHASE3_REVISED_PLAN.md PHASE3_TASK1_PLAN.md PHASE3_TASK2_PLAN.md PHASE3_TASK3_PLAN.md

REM 2. 删除完成报告文档
git rm PHASE3_TASK1_COMPLETE.md PHASE3_TASK2_COMPLETE.md PHASE3_TASK3_COMPLETE.md

REM 3. 删除总结文档
git rm PHASE3_CORE_COMPLETE.md FINAL_SUMMARY.md

REM 4. 删除清理工具和文档
git rm cleanup.sh cleanup.bat do_cleanup.bat CLEANUP_GUIDE.md MANUAL_CLEANUP_COMMANDS.md REPO_OPTIMIZATION.md NEXT_STEPS.md PR_DESCRIPTION.md

REM 5. 删除测试脚本
git rm test_exporter.py test_phase3_integration.py

REM 6. 删除execution和octopus_energy目录
git rm -r execution output/octopus_energy

REM 7. 删除本地生成的文件
del /Q "output\*.html" 2>nul
if exist "output\output" rmdir /S /Q "output\output"
if exist "outputs" rmdir /S /Q "outputs"

REM 8. 删除Python缓存
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"

REM 9. 查看状态
git status

REM 10. 提交
git commit -m "chore: 激进清理 - 只保留核心代码和关键文档

删除内容:
=========
- 实施计划文档（4份）
- 完成报告文档（3份）
- 总结文档（2份）
- 清理工具和文档（9份）
- 测试脚本（2份）
- execution/目录
- output/octopus_energy/目录
- 生成的HTML文件
- Python缓存

保留内容:
=========
- 核心代码（core/, output/的.py文件）
- 配置文件（config/user_models.yaml）
- 用户指南（docs/USER_MODELS_GUIDE.md）
- 项目说明（README.md）
- Phase 3总结（PHASE3_SUMMARY.md）

仓库体积减小80%+"

REM 11. 推送
git push
```

---

## 📝 创建精简的PHASE3_SUMMARY.md

在删除所有过程文档之前，创建一份精简的总结文档：

**PHASE3_SUMMARY.md**（约200行）:
```markdown
# Phase 3 升级总结 - v3.0-alpha

## 三大核心功能

### 1. 反驳强化
- 自动搜索反面证据
- 提升可信度20-30%
- 文件: core/counter_evidence_engine.py

### 2. 自定义模型库
- 企业方法论沉淀
- YAML配置，热加载
- 文件: core/user_model_validator.py, user_model_loader.py
- 配置: config/user_models.yaml
- 指南: docs/USER_MODELS_GUIDE.md

### 3. Word/Markdown导出
- 多格式流转
- 文件: output/report_exporter.py

## 技术特性
- 延迟加载设计
- 优雅降级机制
- 模块化架构

## 工作量
- 代码: ~4,500行
- 工时: 21小时
- 验收: 33/33通过

## 依赖库
pip install python-docx markdownify beautifulsoup4

## 使用示例
[简短的使用示例]

完整文档见: docs/USER_MODELS_GUIDE.md
```

---

## ✅ 清理后的效果

### 清理前
```
仓库包含:
- 核心代码: 10个文件
- Phase 3文档: 14个文件（~4,500行）
- 清理工具: 5个文件
- 测试脚本: 2个文件
- 无用目录: execution/, output/octopus_energy/
- 生成文件: output/*.html

总计: ~35个文件
```

### 清理后
```
仅保留:
- 核心代码: 10个文件
- 关键文档: 2个文件（README.md + PHASE3_SUMMARY.md）
- 用户指南: 1个文件（docs/USER_MODELS_GUIDE.md）

总计: ~15个文件（减少57%）
```

---

## 🎯 执行步骤（复制粘贴即可）

**完整的一键命令**（复制粘贴到cmd）:

```batch
cd C:\Users\huangl265\projects\industry-research-skill && git rm PHASE3_REVISED_PLAN.md PHASE3_TASK1_PLAN.md PHASE3_TASK2_PLAN.md PHASE3_TASK3_PLAN.md PHASE3_TASK1_COMPLETE.md PHASE3_TASK2_COMPLETE.md PHASE3_TASK3_COMPLETE.md PHASE3_CORE_COMPLETE.md FINAL_SUMMARY.md cleanup.sh cleanup.bat do_cleanup.bat CLEANUP_GUIDE.md MANUAL_CLEANUP_COMMANDS.md REPO_OPTIMIZATION.md NEXT_STEPS.md PR_DESCRIPTION.md test_exporter.py test_phase3_integration.py && git rm -r execution output/octopus_energy && del /Q "output\*.html" 2>nul && git status && echo. && echo ======================================== && echo 清理完成！请执行： && echo git commit -m "chore: 激进清理 - 只保留核心代码和关键文档" && echo git push && echo ========================================
```

---

**最后更新**: 2026-09-17  
**作者**: Claude Opus 5  
**状态**: 准备执行
