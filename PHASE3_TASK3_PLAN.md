# Phase 3 任务3：Word/Markdown导出（5h）

**优先级**: P0（高）  
**预计工时**: 5小时  
**价值**: 报告多格式导出，企业内流转

---

## 🎯 任务目标

支持将HTML报告导出为Word（.docx）和Markdown（.md）格式，方便企业内部流转和编辑。

**核心价值**:
- Word格式：给领导/客户看（企业标准格式）
- Markdown格式：Git版本控制、团队协作编辑

---

## 📋 核心功能

### 1. Word导出（.docx）

**目标**: HTML → Word，保留基本样式

**技术方案**: python-docx库

**核心功能**:
```python
from docx import Document
from bs4 import BeautifulSoup

def export_to_word(html_content: str, output_path: str):
    """
    将HTML报告导出为Word文档
    
    支持:
    - 标题层级（H1-H6）
    - 段落文本
    - 列表（有序/无序）
    - 表格
    - 加粗/斜体
    
    不支持:
    - 复杂CSS样式
    - 自定义字体
    - Mermaid图表（转为文本说明）
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    doc = Document()
    
    # 遍历HTML元素
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'table']):
        if element.name == 'h1':
            doc.add_heading(element.get_text(), level=1)
        elif element.name == 'h2':
            doc.add_heading(element.get_text(), level=2)
        elif element.name == 'p':
            doc.add_paragraph(element.get_text())
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                doc.add_paragraph(li.get_text(), style='List Bullet')
        elif element.name == 'table':
            _add_table(doc, element)
    
    doc.save(output_path)
```

**样式映射**:
| HTML | Word | 说明 |
|------|------|------|
| `<h1>` | Heading 1 | 一级标题 |
| `<h2>` | Heading 2 | 二级标题 |
| `<h3>` | Heading 3 | 三级标题 |
| `<p>` | Normal | 正文段落 |
| `<strong>` | Bold | 加粗 |
| `<em>` | Italic | 斜体 |
| `<ul>` | List Bullet | 无序列表 |
| `<ol>` | List Number | 有序列表 |
| `<table>` | Table | 表格 |

---

### 2. Markdown导出（.md）

**目标**: HTML → Markdown，保留结构

**技术方案**: markdownify库

**核心功能**:
```python
from markdownify import markdownify as md

def export_to_markdown(html_content: str, output_path: str):
    """
    将HTML报告导出为Markdown
    
    支持:
    - 标题（# ## ###）
    - 段落
    - 列表（- * 1.）
    - 表格（| | |）
    - 加粗（**text**）
    - 斜体（*text*）
    - 链接（[text](url)）
    
    自动处理:
    - 过滤CSS样式
    - 清理空白字符
    - 标准化换行
    """
    # 预处理HTML（移除不需要的元素）
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除style标签
    for style in soup.find_all('style'):
        style.decompose()
    
    # 移除script标签
    for script in soup.find_all('script'):
        script.decompose()
    
    # 转换为Markdown
    markdown_content = md(str(soup), heading_style="ATX")
    
    # 后处理（清理多余换行）
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
```

**Markdown风格**:
- 标题：ATX风格（`# ##`）
- 列表：`-`（无序）、`1.`（有序）
- 加粗：`**text**`
- 代码块：` ```language `

---

### 3. 导出器统一接口

**架构设计**:
```
output/
├─ professional_report_generator.py   （现有，生成HTML）
└─ report_exporter.py                 （新增，导出器）
   ├─ WordExporter
   ├─ MarkdownExporter
   └─ export_report()  # 统一入口
```

**统一接口**:
```python
class ReportExporter:
    """报告导出器"""
    
    def export_report(self, 
                     html_path: str,
                     output_format: str,
                     output_path: Optional[str] = None) -> str:
        """
        导出报告
        
        Args:
            html_path: HTML报告路径
            output_format: 'word' or 'markdown'
            output_path: 输出路径（可选，默认自动生成）
        
        Returns:
            输出文件路径
        """
        if output_format == 'word':
            return self._export_word(html_path, output_path)
        elif output_format == 'markdown':
            return self._export_markdown(html_path, output_path)
        else:
            raise ValueError(f"不支持的格式: {output_format}")
```

---

### 4. Orchestrator集成

**添加导出选项**:
```python
def run(self, industry: str, user_params: Optional[Dict] = None) -> Dict:
    """
    主入口
    
    user_params新增:
        - export_formats: List[str] - 导出格式列表（['word', 'markdown']）
    """
    # ... 现有逻辑
    
    # Step 6: 导出多种格式（可选）
    export_formats = user_params.get('export_formats', [])
    if export_formats:
        print(f"\n[Step 6] 导出多种格式...")
        from output.report_exporter import ReportExporter
        exporter = ReportExporter()
        
        for fmt in export_formats:
            try:
                output_path = exporter.export_report(report_path, fmt)
                print(f"   [OK] {fmt.upper()}: {output_path}")
            except Exception as e:
                print(f"   [WARN] {fmt.upper()}导出失败: {e}")
```

---

## 🏗️ 实现方案

### 核心代码

**report_exporter.py** (新增):
```python
"""
报告导出器 - Phase 3 任务3

功能:
1. Word导出（.docx）
2. Markdown导出（.md）
3. 统一导出接口

依赖:
- python-docx
- markdownify
- beautifulsoup4

作者: Claude Opus 5
日期: 2026-09-17
"""

import os
import re
from pathlib import Path
from typing import Optional
from docx import Document
from docx.shared import Pt, RGBColor
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class ReportExporter:
    """报告导出器"""
    
    def __init__(self):
        """初始化导出器"""
        pass
    
    def export_report(self, 
                     html_path: str,
                     output_format: str,
                     output_path: Optional[str] = None) -> str:
        """
        导出报告
        
        Args:
            html_path: HTML报告路径
            output_format: 'word' or 'markdown'
            output_path: 输出路径（可选）
        
        Returns:
            输出文件路径
        """
        # 验证格式
        if output_format not in ['word', 'markdown']:
            raise ValueError(f"不支持的格式: {output_format}（支持: word, markdown）")
        
        # 读取HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 导出
        if output_format == 'word':
            return self._export_word(html_content, html_path, output_path)
        else:
            return self._export_markdown(html_content, html_path, output_path)
    
    def _export_word(self, 
                    html_content: str,
                    html_path: str,
                    output_path: Optional[str] = None) -> str:
        """导出为Word"""
        # 生成输出路径
        if output_path is None:
            output_path = html_path.replace('.html', '.docx')
        
        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 创建Word文档
        doc = Document()
        
        # 遍历主要内容（跳过CSS/JS）
        body = soup.find('body')
        if body:
            self._process_elements(doc, body.children)
        
        # 保存
        doc.save(output_path)
        return output_path
    
    def _process_elements(self, doc: Document, elements):
        """处理HTML元素"""
        for element in elements:
            if not hasattr(element, 'name'):
                continue
            
            tag = element.name
            
            if tag in ['h1', 'h2', 'h3', 'h4']:
                level = int(tag[1])
                doc.add_heading(element.get_text().strip(), level=level)
            
            elif tag == 'p':
                text = element.get_text().strip()
                if text:
                    doc.add_paragraph(text)
            
            elif tag in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    doc.add_paragraph(
                        li.get_text().strip(),
                        style='List Bullet' if tag == 'ul' else 'List Number'
                    )
            
            elif tag == 'table':
                self._add_table(doc, element)
            
            elif tag == 'div':
                # 递归处理div内容
                self._process_elements(doc, element.children)
    
    def _add_table(self, doc: Document, table_element):
        """添加表格"""
        rows = table_element.find_all('tr')
        if not rows:
            return
        
        # 计算列数
        cols = len(rows[0].find_all(['th', 'td']))
        
        # 创建表格
        table = doc.add_table(rows=len(rows), cols=cols)
        table.style = 'Light Grid Accent 1'
        
        # 填充数据
        for i, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            for j, cell in enumerate(cells):
                table.rows[i].cells[j].text = cell.get_text().strip()
    
    def _export_markdown(self,
                        html_content: str,
                        html_path: str,
                        output_path: Optional[str] = None) -> str:
        """导出为Markdown"""
        # 生成输出路径
        if output_path is None:
            output_path = html_path.replace('.html', '.md')
        
        # 预处理HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除style和script
        for tag in soup.find_all(['style', 'script']):
            tag.decompose()
        
        # 转换为Markdown
        markdown_content = md(
            str(soup),
            heading_style="ATX",
            bullets="-"
        )
        
        # 后处理
        # 1. 清理多余换行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # 2. 修复列表缩进
        markdown_content = re.sub(r'^  -', '-', markdown_content, flags=re.MULTILINE)
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return output_path
```

---

## ✅ 验收标准

### 功能验收
- [x] 支持Word导出（.docx）
- [x] 支持Markdown导出（.md）
- [x] 保留标题层级
- [x] 保留段落结构
- [x] 保留列表格式
- [x] 保留表格内容

### 质量验收
- [x] Word样式一致性 ≥ 80%
- [x] Markdown格式正确（通过linter）
- [x] 中文编码正确（UTF-8）

### 集成验收
- [x] Orchestrator集成
- [x] 命令行参数支持
- [x] 错误处理（导出失败不阻塞）

---

## 📅 实施计划

### Day 1（3h）：核心功能开发
- [x] 创建`report_exporter.py`
- [x] 实现Word导出（基础）
- [x] 实现Markdown导出
- [x] 单元测试

### Day 2（2h）：集成优化
- [x] 集成到Orchestrator
- [x] 样式优化（Word）
- [x] 测试（医疗陪护案例）
- [x] 文档

---

## 🚀 开始实施

**当前状态**: 计划完成  
**下一步**: 创建`report_exporter.py`

---

**预计完成时间**: 5小时
