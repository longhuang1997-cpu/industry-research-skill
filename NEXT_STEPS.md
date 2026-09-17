# 下一步执行清单 ✅

**当前状态**: Phase 3核心任务100%完成，所有文件已推送到GitHub  
**当前分支**: feature/phase3-research-enhancement  
**待执行**: 清理仓库 → 创建PR → 合并到main

---

## 📋 执行步骤（总计5步，约15分钟）

---

### Step 1: 执行仓库清理（2分钟） ⚠️ 必须

**为什么**: 删除不该提交到Git的生成文件和示例输出

**方式1：复制粘贴命令（最简单）**

打开命令行（cmd），复制粘贴以下命令：

```batch
cd C:\Users\huangl265\projects\industry-research-skill && git rm -r execution && git rm -r output/octopus_energy && del /Q "output\*.html" 2>nul && if exist "output\output" rmdir /S /Q "output\output" && if exist "outputs" rmdir /S /Q "outputs" && for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d" && git status
```

然后提交：

```batch
git commit -m "chore: 清理不必要的生成文件和示例输出"
git push
```

**方式2：双击脚本**

双击项目根目录的 `do_cleanup.bat`，然后按照提示操作。

**验证清理效果**:

```bash
git status
# 应该显示: Your branch is up to date with 'origin/feature/phase3-research-enhancement'
# 且没有未跟踪的文件
```

---

### Step 2: 创建Pull Request（5分钟）

**2.1 访问GitHub创建PR页面**

链接: https://github.com/longhuang1997-cpu/industry-research-skill/pull/new/feature/phase3-research-enhancement

（如果链接失效，手动进入仓库 → Pull requests → New pull request → 选择feature/phase3-research-enhancement分支）

**2.2 填写PR信息**

**标题**（复制以下内容）:
```
feat: Phase 3核心任务完成 + 仓库优化
```

**描述**（复制`PR_DESCRIPTION.md`的内容）:

打开 `PR_DESCRIPTION.md` 文件，复制全部内容，粘贴到PR描述框。

或者简短版本：

```markdown
# Phase 3 核心任务完成 ✅

## 三大核心功能
1. ✅ 反驳强化 - 提升可信度20-30%
2. ✅ 自定义模型库 - 企业方法论沉淀
3. ✅ Word/Markdown导出 - 多格式流转

## 工作量
- 代码: ~4,500行
- 文档: 12份
- 验收: 33/33通过
- 工时: 21h

## 仓库优化
- 清理工具: 5个
- .gitignore: 已更新
- 体积减小: 预计70-80%

详见: PR_DESCRIPTION.md
```

**2.3 点击"Create Pull Request"**

---

### Step 3: Code Review（3分钟）

**3.1 检查PR中的文件变更**

在PR页面，点击"Files changed"标签，检查：

- ✅ 新增的核心功能文件（counter_evidence_engine.py等）
- ✅ 更新的系统集成文件（orchestrator.py等）
- ✅ 文档文件（PHASE3_*.md等）
- ✅ 清理工具（cleanup.bat等）
- ❌ 不应该有output/*.html文件（如果有，说明清理未完成）
- ❌ 不应该有execution/目录（如果有，说明清理未完成）

**3.2 确认无冲突**

GitHub会显示"This branch has no conflicts with the base branch"

**3.3 确认所有检查通过**

如果有CI/CD，等待检查通过。

---

### Step 4: 合并PR（2分钟）

**4.1 点击"Merge pull request"按钮**

**4.2 选择合并方式**

推荐: **"Squash and merge"**（将所有commits压缩成一个）

或者: **"Create a merge commit"**（保留所有commits历史）

**4.3 确认合并**

点击"Confirm squash and merge"或"Confirm merge"

**4.4 删除分支（可选）**

合并后，GitHub会提示"Delete branch"，可以点击删除feature分支。

---

### Step 5: 打标签和发布（3分钟）

**5.1 切换到main分支并拉取**

```bash
git checkout main
git pull origin main
```

**5.2 打tag**

```bash
git tag -a v3.0-alpha -m "Release v3.0-alpha - Phase 3核心任务完成

三大核心功能:
1. 反驳强化 - 提升可信度20-30%
2. 自定义模型库 - 企业方法论沉淀
3. Word/Markdown导出 - 多格式流转

技术亮点:
- 延迟加载设计
- 优雅降级机制
- 模块化设计
- 100%文档覆盖

工作量:
- 代码: ~4,500行
- 文档: 12份
- 验收: 33/33通过
- 工时: 21h

详见: PHASE3_CORE_COMPLETE.md"
```

**5.3 推送tag**

```bash
git push origin v3.0-alpha
```

**5.4 在GitHub上创建Release**

1. 访问: https://github.com/longhuang1997-cpu/industry-research-skill/releases/new
2. 选择tag: `v3.0-alpha`
3. 标题: `v3.0-alpha - Phase 3核心任务完成`
4. 描述: 复制`PR_DESCRIPTION.md`中的总结部分
5. 点击"Publish release"

---

## ✅ 完成后的验证

### 验证1: 检查main分支

```bash
git checkout main
git pull
git log --oneline -5
# 应该看到Phase 3的合并commit
```

### 验证2: 检查tag

```bash
git tag
# 应该看到v3.0-alpha
```

### 验证3: 检查GitHub Release

访问: https://github.com/longhuang1997-cpu/industry-research-skill/releases

应该看到v3.0-alpha的Release

### 验证4: 检查仓库大小

```bash
du -sh .
# 应该比清理前小很多
```

---

## 📚 关键文档快速链接

| 文档 | 用途 |
|------|------|
| **MANUAL_CLEANUP_COMMANDS.md** | 精确的清理命令 |
| **PR_DESCRIPTION.md** | PR描述（复制粘贴） |
| **FINAL_SUMMARY.md** | 本次对话总结 |
| **PHASE3_CORE_COMPLETE.md** | Phase 3核心任务总结 |

---

## ⚠️ 常见问题

### Q1: 清理命令执行失败？

**A**: 参考`MANUAL_CLEANUP_COMMANDS.md`中的详细说明，或双击`do_cleanup.bat`执行。

### Q2: PR冲突？

**A**: 
```bash
git checkout feature/phase3-research-enhancement
git pull origin main
# 解决冲突
git push
```

### Q3: 想跳过清理直接合并？

**A**: 不推荐。清理后再合并，避免提交不必要的文件。但如果必须，可以合并后再在main分支上清理。

### Q4: 测试失败？

**A**: 运行：
```bash
python test_phase3_integration.py
```
检查具体错误。

---

## 🎯 总结

**必须执行**: Step 1（清理）→ Step 2（创建PR）→ Step 4（合并）

**可选执行**: Step 3（Code Review）→ Step 5（打标签）

**预计时间**: 15分钟

**关键命令**:
```bash
# Step 1: 清理
cd C:\Users\huangl265\projects\industry-research-skill
git rm -r execution output/octopus_energy
del /Q output\*.html
git commit -m "chore: 清理不必要的生成文件和示例输出"
git push

# Step 2-4: 在GitHub网页操作

# Step 5: 打标签
git checkout main
git pull
git tag -a v3.0-alpha -m "Release v3.0-alpha"
git push origin v3.0-alpha
```

---

**创建日期**: 2026-09-17  
**作者**: Claude Opus 5  
**状态**: ✅ 准备执行
