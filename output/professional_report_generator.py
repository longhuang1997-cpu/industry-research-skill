"""
专业级报告生成器：生成咨询公司水准的可视化报告

特性:
1. 专业排版（类似麦肯锡/BCG的报告样式）
2. 图表集成（matplotlib生成的SVG图表）
3. 数据表格
4. 结构化章节
5. PDF导出（可选）
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json


class ProfessionalReportGenerator:
    """
    专业级报告生成器

    生成咨询公司水准的HTML/PDF报告
    """

    def __init__(self, output_dir: str = None):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录（可选）
                - None: 自动选择（优先桌面，其次当前目录，最后skill目录）
                - 相对路径: 相对于当前工作目录
                - 绝对路径: 使用指定路径
        """
        # 智能选择输出目录（零硬编码）
        if output_dir is None:
            # 优先级1: 桌面（如果存在且可写）
            desktop = Path.home() / "Desktop"
            if desktop.exists() and desktop.is_dir():
                self.output_dir = desktop / "industry_research_reports"
                self.output_dir.mkdir(exist_ok=True)
                print(f"[ReportGenerator] 输出目录: {self.output_dir} (桌面)")
            # 优先级2: 当前工作目录
            else:
                self.output_dir = Path.cwd() / "output"
                self.output_dir.mkdir(exist_ok=True)
                print(f"[ReportGenerator] 输出目录: {self.output_dir} (当前目录)")
        else:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(exist_ok=True, parents=True)
            print(f"[ReportGenerator] 输出目录: {self.output_dir} (指定路径)")

    def generate_report(self,
                       industry: str,
                       research_data: Dict,
                       report_type: str = "full") -> str:
        """
        生成专业报告

        Args:
            industry: 行业名称
            research_data: 研究数据
            report_type: 报告类型 (quick, standard, full)

        Returns:
            output_path: 生成的报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{industry}_report_{timestamp}.html"

        # 生成HTML内容
        html_content = self._generate_html(industry, research_data, report_type)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_file)

    def _generate_html(self,
                      industry: str,
                      research_data: Dict,
                      report_type: str) -> str:
        """生成HTML内容"""

        # 专业样式CSS（类似麦肯锡报告）
        css = self._get_professional_css()

        # 封面页
        cover_page = self._generate_cover_page(industry)

        # 执行摘要
        executive_summary = self._generate_executive_summary(research_data)

        # 主体章节
        main_content = self._generate_main_content(research_data, report_type)

        # 附录
        appendix = self._generate_appendix(research_data)

        # 组装完整HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{industry} 行业研究报告</title>
    {css}
</head>
<body>
    {cover_page}
    {executive_summary}
    {main_content}
    {appendix}

    <div class="footer-note">
        <p>本报告由 Industry Research Skill 生成</p>
        <p>生成时间: {datetime.now().strftime("%Y年%m月%d日")}</p>
    </div>
</body>
</html>
"""
        return html

    def _get_professional_css(self) -> str:
        """获取专业样式CSS"""
        return """
<style>
    /* 全局样式 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
        line-height: 1.8;
        color: #333;
        background: #f8f9fa;
    }

    /* 页面容器 */
    .page {
        width: 210mm;
        min-height: 297mm;
        margin: 20px auto;
        background: white;
        padding: 20mm;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        page-break-after: always;
    }

    /* 封面页 */
    .cover-page {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 257mm;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }

    .cover-title {
        margin-top: 80mm;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .cover-subtitle {
        margin-top: 20px;
        font-size: 24px;
        opacity: 0.9;
    }

    .cover-footer {
        font-size: 18px;
        opacity: 0.8;
        margin-bottom: 20mm;
    }

    /* 执行摘要 */
    .executive-summary {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 30px;
        margin: 30px 0;
    }

    .executive-summary h2 {
        color: #856404;
        margin-bottom: 20px;
        font-size: 28px;
    }

    /* 章节标题 */
    h1 {
        font-size: 36px;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 15px;
        margin-bottom: 30px;
    }

    h2 {
        font-size: 28px;
        color: #34495e;
        margin-top: 40px;
        margin-bottom: 20px;
        border-left: 5px solid #3498db;
        padding-left: 15px;
    }

    h3 {
        font-size: 22px;
        color: #555;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* 段落 */
    p {
        margin-bottom: 15px;
        text-align: justify;
        font-size: 16px;
    }

    /* 关键指标卡片 */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 30px 0;
    }

    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #3498db;
        margin: 10px 0;
    }

    .metric-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
    }

    /* 表格样式 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14px;
    }

    thead {
        background: #3498db;
        color: white;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border: 1px solid #ddd;
    }

    tbody tr:nth-child(even) {
        background: #f8f9fa;
    }

    tbody tr:hover {
        background: #e9ecef;
    }

    /* 图表容器 */
    .chart-container {
        margin: 30px 0;
        text-align: center;
    }

    .chart-container img {
        max-width: 100%;
        height: auto;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }

    .chart-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #34495e;
    }

    /* 引用框 */
    .quote-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 20px;
        margin: 20px 0;
        font-style: italic;
    }

    /* 警告框 */
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 20px;
        margin: 20px 0;
    }

    /* 成功框 */
    .success-box {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 20px;
        margin: 20px 0;
    }

    /* 反事实检验区块（P0任务4新增） */
    .counter-argument-section {
        background: #f5f5f5;
        border: 2px solid #9e9e9e;
        border-radius: 8px;
        padding: 20px;
        margin: 30px 0;
    }

    .counter-argument-section h3 {
        color: #d32f2f;
        font-size: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #d32f2f;
        padding-bottom: 10px;
    }

    .counter-argument-section h4 {
        color: #333;
        font-size: 16px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .counter-argument-content {
        background: white;
        padding: 15px;
        border-radius: 4px;
    }

    /* 列表样式 */
    ul, ol {
        margin: 15px 0 15px 30px;
    }

    li {
        margin-bottom: 8px;
    }

    /* 质量分数徽章 */
    .quality-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-left: 10px;
    }

    .quality-excellent {
        background: #4caf50;
        color: white;
    }

    .quality-good {
        background: #2196f3;
        color: white;
    }

    .quality-fair {
        background: #ff9800;
        color: white;
    }

    /* 页脚 */
    .footer-note {
        text-align: center;
        color: #999;
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
    }

    /* 打印样式 */
    @media print {
        body {
            background: white;
        }

        .page {
            margin: 0;
            box-shadow: none;
        }
    }
</style>
"""

    def _generate_cover_page(self, industry: str) -> str:
        """生成封面页"""
        return f"""
<div class="page cover-page">
    <div></div>
    <div>
        <div class="cover-title">{industry}</div>
        <div class="cover-subtitle">行业深度研究报告</div>
    </div>
    <div class="cover-footer">
        <p>Industry Research Skill</p>
        <p>{datetime.now().strftime("%Y年%m月")}</p>
    </div>
</div>
"""

    def _generate_executive_summary(self, research_data: Dict) -> str:
        """生成执行摘要"""
        profile = research_data.get('profile', {})

        return f"""
<div class="page">
    <div class="executive-summary">
        <h2>📋 执行摘要</h2>
        <p>{profile.get('summary', '暂无数据')}</p>
    </div>
</div>
"""

    def _generate_main_content(self,
                              research_data: Dict,
                              report_type: str) -> str:
        """生成主体内容"""
        analysis = research_data.get('analysis', {})

        content = ""

        # 政策环境
        if 'policy' in analysis:
            content += self._generate_section(
                "政策环境分析",
                analysis['policy']
            )

        # 市场规模
        if 'market_size' in analysis:
            content += self._generate_section(
                "市场规模测算",
                analysis['market_size']
            )

        # 商业模式
        if 'business_model' in analysis:
            content += self._generate_section(
                "商业模式分析",
                analysis['business_model']
            )

        return content

    def _generate_section(self, title: str, section_data: Dict) -> str:
        """生成章节（含反事实检验）"""
        quality_score = section_data.get('quality_score', 0)
        content = section_data.get('content', '暂无数据')

        # 质量分数徽章
        if quality_score >= 0.8:
            badge_class = "quality-excellent"
            badge_text = "优秀"
        elif quality_score >= 0.6:
            badge_class = "quality-good"
            badge_text = "良好"
        else:
            badge_class = "quality-fair"
            badge_text = "一般"

        # 反事实检验小节（P0任务4）
        counter_argument_html = ""
        counter_arg = section_data.get('counter_argument', {})

        if counter_arg and counter_arg.get('rebuttal'):
            # 有反事实检验数据
            rebuttals = counter_arg.get('rebuttal', [])
            responses = counter_arg.get('response', [])
            verdict = counter_arg.get('verdict', '')

            rebuttals_html = "".join([f"<li>{r}</li>" for r in rebuttals])
            responses_html = "".join([f"<li>{r}</li>" for r in responses])

            counter_argument_html = f"""
<div class="counter-argument-section">
    <h3>【反方观点】本章结论的最强反驳</h3>

    <div class="counter-argument-content">
        <h4>反驳点：</h4>
        <ul>{rebuttals_html}</ul>

        <h4>我方回应：</h4>
        <ul>{responses_html}</ul>

        <h4>综合判断：</h4>
        <p>{verdict}</p>
    </div>
</div>
            """
        else:
            # Phase 3: 显示自动搜索的反面证据
            counter_evidences = analysis.get('counter_evidences', [])
            if counter_evidences:
                counter_argument_html = self._render_phase3_counter_evidences(counter_evidences)
            else:
                # 无反事实检验数据，显示提示
                counter_argument_html = """
<div class="warning-box">
    <strong>⚠️ 质量提示</strong>：本章未做反事实检验。建议补充反驳观点以增强论证严谨性。
</div>
            """

        return f"""
<div class="page">
    <h2>
        {title}
        <span class="quality-badge {badge_class}">
            质量分数: {quality_score:.2f} - {badge_text}
        </span>
    </h2>
    <p>{content}</p>

    {counter_argument_html}
</div>
"""

    def _generate_appendix(self, research_data: Dict) -> str:
        """生成附录"""
        return f"""
<div class="page">
    <h2>附录</h2>
    <h3>数据来源</h3>
    <ul>
        <li>国家统计局</li>
        <li>行业公开数据</li>
        <li>AI分析引擎</li>
    </ul>

    <h3>分析方法</h3>
    <ul>
        <li>PEST分析框架</li>
        <li>Top-down + Bottom-up市场测算</li>
        <li>四方决策链分析</li>
        <li>单位经济模型</li>
    </ul>
</div>
"""

    def _render_phase3_counter_evidences(self, counter_evidences: List[Dict]) -> str:
        """
        渲染Phase 3自动搜索的反面证据

        Args:
            counter_evidences: 反面证据列表

        Returns:
            HTML字符串
        """
        if not counter_evidences:
            return ""

        evidences_html = ""
        for i, evidence in enumerate(counter_evidences, 1):
            title = evidence.get('title', '未知标题')
            source = evidence.get('source', '#')
            snippet = evidence.get('snippet', '无摘要')

            evidences_html += f"""
        <div style="margin: 15px 0; padding-left: 10px; border-left: 3px solid #ffc107;">
            <strong>{i}. <a href="{source}" target="_blank" style="color: #1976d2;">{title}</a></strong>
            <blockquote style="margin: 8px 0; padding-left: 15px; border-left: 2px solid #ddd; color: #555;">
                {snippet}
            </blockquote>
        </div>
            """

        return f"""
<div class="counter-argument-section">
    <h3>【反方观点】本章结论的最强反驳</h3>

    <h4>🔍 AI自动搜索到的反面证据：</h4>
    <div class="counter-argument-content">
        {evidences_html}
    </div>

    <h4>💡 提示：</h4>
    <div class="warning-box" style="margin-top: 10px;">
        <p>以上反面证据由AI自动搜索发现。建议：</p>
        <ul>
            <li>补充<strong>【我方回应】</strong>：针对每条反面证据的回应</li>
            <li>给出<strong>【综合判断】</strong>：考虑反面证据后的最终结论</li>
        </ul>
    </div>
</div>
        """


def main():
    """测试专业报告生成器"""
    generator = ProfessionalReportGenerator()

    # 测试数据
    test_data = {
        'profile': {
            'summary': '医疗陪护行业是政府主导+高监管行业，长护险试点49城覆盖1.45亿人。'
        },
        'analysis': {
            'policy': {
                'content': '长护险试点是医疗陪护行业的核心政策红利...',
                'quality_score': 1.0
            },
            'market_size': {
                'content': '医疗陪护市场规模测算（2023年）...',
                'quality_score': 0.8
            }
        }
    }

    output_path = generator.generate_report('医疗陪护', test_data, 'full')
    print(f"✅ 专业报告已生成: {output_path}")


if __name__ == '__main__':
    main()
