"""
高级专业报告模板生成器

提供可定制的高级报告模板
支持多种输出格式和可视化风格
"""

from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class ProfessionalReportTemplateGenerator:
    """
    专业报告模板生成器（增强版）

    新功能:
    - 多种预设模板（咨询风格、投资风格、学术风格）
    - 可定制的章节结构
    - 内置图表配色方案
    - 支持交互式HTML和静态PDF
    """

    def __init__(self):
        """初始化模板生成器"""
        self.templates = self._init_templates()
        self.chart_styles = self._init_chart_styles()

    def _init_templates(self) -> Dict:
        """
        初始化报告模板库

        Returns:
            templates: 模板定义字典
        """
        return {
            'consulting_style': {
                'name': '咨询风格（麦肯锡/贝恩）',
                'description': '金字塔原理，结论先行，数据支撑',
                'structure': [
                    {
                        'section': '执行摘要',
                        'subsections': [
                            '核心发现（3-5条）',
                            '关键建议',
                            '实施路径'
                        ],
                        'page_limit': 2
                    },
                    {
                        'section': '行业概览',
                        'subsections': [
                            '行业定义与范围',
                            '市场规模与增长',
                            '产业链结构',
                            '政策环境'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '竞争格局',
                        'subsections': [
                            '市场集中度',
                            '主要玩家分析',
                            'SWOT分析',
                            '竞争壁垒'
                        ],
                        'page_limit': 10
                    },
                    {
                        'section': '商业模式',
                        'subsections': [
                            '价值主张',
                            '收入模式',
                            '成本结构',
                            '盈利能力'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '机会与风险',
                        'subsections': [
                            '增长机会',
                            '关键风险',
                            '应对策略'
                        ],
                        'page_limit': 6
                    },
                    {
                        'section': '附录',
                        'subsections': [
                            '数据来源',
                            '研究方法',
                            '名词解释'
                        ],
                        'page_limit': 4
                    }
                ],
                'chart_density': 'high',  # 每2页至少1个图表
                'data_emphasis': 'high',
                'visual_style': 'professional'
            },

            'investment_style': {
                'name': '投资风格（PE/VC尽调）',
                'description': '投资视角，风险聚焦，量化分析',
                'structure': [
                    {
                        'section': '投资摘要',
                        'subsections': [
                            '投资亮点',
                            '关键风险',
                            '估值区间'
                        ],
                        'page_limit': 2
                    },
                    {
                        'section': '市场分析',
                        'subsections': [
                            '市场规模（TAM/SAM/SOM）',
                            '增长驱动因素',
                            '市场成熟度'
                        ],
                        'page_limit': 6
                    },
                    {
                        'section': '竞争分析',
                        'subsections': [
                            '竞争格局',
                            '护城河分析',
                            '市占率趋势'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '商业模式与财务',
                        'subsections': [
                            '商业模式画布',
                            '单位经济模型',
                            '财务预测（3-5年）',
                            '敏感性分析'
                        ],
                        'page_limit': 10
                    },
                    {
                        'section': '管理团队与执行',
                        'subsections': [
                            '核心团队背景',
                            '组织架构',
                            '执行能力评估'
                        ],
                        'page_limit': 4
                    },
                    {
                        'section': '风险因素',
                        'subsections': [
                            '政策风险',
                            '市场风险',
                            '运营风险',
                            '财务风险'
                        ],
                        'page_limit': 6
                    },
                    {
                        'section': '附录',
                        'subsections': [
                            '详细财务模型',
                            '行业对标',
                            '数据来源'
                        ],
                        'page_limit': 8
                    }
                ],
                'chart_density': 'very_high',
                'data_emphasis': 'very_high',
                'visual_style': 'data_driven'
            },

            'strategic_style': {
                'name': '战略风格（企业内部）',
                'description': '战略决策，落地导向，内部视角',
                'structure': [
                    {
                        'section': '战略背景',
                        'subsections': [
                            '当前业务现状',
                            '战略目标',
                            '研究问题'
                        ],
                        'page_limit': 3
                    },
                    {
                        'section': '外部环境分析',
                        'subsections': [
                            'PEST分析',
                            '行业趋势',
                            '客户需求变化'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '内部能力评估',
                        'subsections': [
                            '核心能力盘点',
                            '资源评估',
                            '差距分析'
                        ],
                        'page_limit': 6
                    },
                    {
                        'section': '战略选项',
                        'subsections': [
                            '可选战略方向',
                            '方案对比',
                            '推荐方案及理由'
                        ],
                        'page_limit': 10
                    },
                    {
                        'section': '实施计划',
                        'subsections': [
                            '关键举措',
                            '时间表',
                            '资源需求',
                            '里程碑'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '风险与应对',
                        'subsections': [
                            '关键风险',
                            '应对预案'
                        ],
                        'page_limit': 4
                    }
                ],
                'chart_density': 'medium',
                'data_emphasis': 'medium',
                'visual_style': 'clear_actionable'
            },

            'market_entry_style': {
                'name': '市场进入评估',
                'description': '新市场/新业务评估，决策导向',
                'structure': [
                    {
                        'section': '机会概述',
                        'subsections': [
                            '市场机会',
                            '战略契合度',
                            '初步结论'
                        ],
                        'page_limit': 2
                    },
                    {
                        'section': '市场吸引力',
                        'subsections': [
                            '市场规模与增长',
                            '盈利能力',
                            '竞争强度',
                            '吸引力评分'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '竞争定位',
                        'subsections': [
                            '现有玩家分析',
                            '我们的差异化',
                            '可防御性'
                        ],
                        'page_limit': 6
                    },
                    {
                        'section': '进入策略',
                        'subsections': [
                            '进入模式（自建/并购/合作）',
                            '目标客群',
                            'GTM策略',
                            '资源投入'
                        ],
                        'page_limit': 10
                    },
                    {
                        'section': '财务预测',
                        'subsections': [
                            '收入预测',
                            '成本结构',
                            '盈亏平衡',
                            'ROI分析'
                        ],
                        'page_limit': 8
                    },
                    {
                        'section': '风险与决策',
                        'subsections': [
                            '关键假设',
                            '风险因素',
                            'Go/No-Go建议'
                        ],
                        'page_limit': 4
                    }
                ],
                'chart_density': 'high',
                'data_emphasis': 'high',
                'visual_style': 'decision_oriented'
            }
        }

    def _init_chart_styles(self) -> Dict:
        """
        初始化图表配色方案

        Returns:
            styles: 配色方案字典
        """
        return {
            'professional': {
                'name': '专业风格（深蓝）',
                'primary': '#1E3A8A',      # 深蓝
                'secondary': '#3B82F6',    # 天蓝
                'accent': '#F59E0B',       # 琥珀
                'positive': '#10B981',     # 翠绿
                'negative': '#EF4444',     # 红
                'neutral': '#6B7280',      # 灰
                'background': '#F9FAFB',
                'text': '#111827'
            },
            'data_driven': {
                'name': '数据驱动（深灰）',
                'primary': '#1F2937',      # 深灰
                'secondary': '#4B5563',    # 灰
                'accent': '#8B5CF6',       # 紫
                'positive': '#059669',     # 绿
                'negative': '#DC2626',     # 红
                'neutral': '#9CA3AF',
                'background': '#FFFFFF',
                'text': '#000000'
            },
            'clear_actionable': {
                'name': '清晰可执行（暖色）',
                'primary': '#DC2626',      # 红
                'secondary': '#F59E0B',    # 橙
                'accent': '#3B82F6',       # 蓝
                'positive': '#10B981',     # 绿
                'negative': '#EF4444',     # 红
                'neutral': '#6B7280',
                'background': '#FFFBEB',   # 暖色背景
                'text': '#1F2937'
            },
            'decision_oriented': {
                'name': '决策导向（对比色）',
                'primary': '#7C3AED',      # 紫
                'secondary': '#2DD4BF',    # 青
                'accent': '#F59E0B',       # 橙
                'positive': '#10B981',     # 绿
                'negative': '#EF4444',     # 红
                'neutral': '#6B7280',
                'background': '#FAFAF9',
                'text': '#0C0A09'
            }
        }

    def list_templates(self) -> List[Dict]:
        """
        列出所有可用模板

        Returns:
            templates: 模板列表
        """
        templates = []
        for template_id, template in self.templates.items():
            templates.append({
                'id': template_id,
                'name': template['name'],
                'description': template['description'],
                'total_pages': sum(s['page_limit'] for s in template['structure']),
                'chart_density': template['chart_density']
            })

        return templates

    def get_template(self, template_id: str) -> Optional[Dict]:
        """
        获取模板详情

        Args:
            template_id: 模板ID

        Returns:
            template: 模板定义
        """
        return self.templates.get(template_id)

    def customize_template(self,
                          base_template_id: str,
                          custom_sections: Optional[List[Dict]] = None,
                          custom_chart_style: Optional[str] = None) -> Dict:
        """
        自定义模板

        Args:
            base_template_id: 基础模板ID
            custom_sections: 自定义章节列表（可选）
            custom_chart_style: 自定义配色方案（可选）

        Returns:
            customized: 自定义后的模板
        """
        base_template = self.templates.get(base_template_id)
        if not base_template:
            raise ValueError(f"Template {base_template_id} not found")

        customized = base_template.copy()

        # 替换章节结构
        if custom_sections:
            customized['structure'] = custom_sections

        # 替换配色方案
        if custom_chart_style and custom_chart_style in self.chart_styles:
            customized['visual_style'] = custom_chart_style

        customized['custom'] = True
        customized['base_template'] = base_template_id

        return customized

    def generate_report_outline(self,
                               template_id: str,
                               industry: str,
                               custom_params: Optional[Dict] = None) -> Dict:
        """
        生成报告大纲

        Args:
            template_id: 模板ID
            industry: 行业名称
            custom_params: 自定义参数（可选）

        Returns:
            outline: 报告大纲
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")

        outline = {
            'title': f"{industry}行业研究报告",
            'subtitle': template['name'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'template_id': template_id,
            'structure': template['structure'],
            'total_pages': sum(s['page_limit'] for s in template['structure']),
            'chart_style': self.chart_styles[template['visual_style']],
            'metadata': {
                'chart_density': template['chart_density'],
                'data_emphasis': template['data_emphasis']
            }
        }

        # 应用自定义参数
        if custom_params:
            if 'title' in custom_params:
                outline['title'] = custom_params['title']
            if 'subtitle' in custom_params:
                outline['subtitle'] = custom_params['subtitle']

        return outline

    def get_chart_style(self, style_name: str) -> Optional[Dict]:
        """
        获取图表配色方案

        Args:
            style_name: 配色方案名称

        Returns:
            style: 配色方案
        """
        return self.chart_styles.get(style_name)


def main():
    """测试专业报告模板生成器"""
    generator = ProfessionalReportTemplateGenerator()

    print("="*60)
    print("测试1: 列出所有模板")
    print("="*60)
    templates = generator.list_templates()
    for i, template in enumerate(templates, 1):
        print(f"\n{i}. {template['name']}")
        print(f"   {template['description']}")
        print(f"   页数: ~{template['total_pages']}页")
        print(f"   图表密度: {template['chart_density']}")

    print("\n" + "="*60)
    print("测试2: 生成报告大纲（咨询风格）")
    print("="*60)
    outline = generator.generate_report_outline(
        template_id='consulting_style',
        industry='医疗陪护'
    )
    print(f"\n报告标题: {outline['title']}")
    print(f"预计页数: {outline['total_pages']}页")
    print(f"\n章节结构:")
    for i, section in enumerate(outline['structure'], 1):
        print(f"  {i}. {section['section']} (~{section['page_limit']}页)")
        for subsection in section['subsections'][:2]:
            print(f"     - {subsection}")

    print("\n" + "="*60)
    print("测试3: 获取配色方案")
    print("="*60)
    style = generator.get_chart_style('professional')
    print(f"\n配色方案: {style['name']}")
    print(f"  主色: {style['primary']}")
    print(f"  辅色: {style['secondary']}")
    print(f"  强调色: {style['accent']}")


if __name__ == '__main__':
    main()
