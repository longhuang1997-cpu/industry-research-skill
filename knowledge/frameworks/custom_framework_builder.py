"""
用户自定义框架构建器

允许用户创建、保存、管理自己的分析框架
框架会自动集成到知识层，被Skill调用
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class CustomFrameworkBuilder:
    """
    用户自定义框架构建器

    功能:
    1. 引导用户创建分析框架
    2. 保存到本地框架库
    3. 自动集成到FrameworkSelector
    4. 提供框架模板
    """

    def __init__(self, custom_frameworks_dir: Optional[Path] = None):
        """
        初始化框架构建器

        Args:
            custom_frameworks_dir: 自定义框架存储目录
        """
        if custom_frameworks_dir is None:
            self.frameworks_dir = Path(__file__).parent / 'custom_frameworks'
        else:
            self.frameworks_dir = Path(custom_frameworks_dir)

        # 确保目录存在
        self.frameworks_dir.mkdir(parents=True, exist_ok=True)

        # 加载已有的自定义框架
        self.custom_frameworks = self._load_custom_frameworks()

    def _load_custom_frameworks(self) -> Dict:
        """加载所有自定义框架"""
        frameworks = {}

        for yaml_file in self.frameworks_dir.glob('*.yaml'):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    framework = yaml.safe_load(f)
                    frameworks[framework['framework_id']] = framework
            except Exception as e:
                print(f"[WARNING] Failed to load {yaml_file}: {e}")

        return frameworks

    def list_available_templates(self) -> List[Dict]:
        """
        列出可用的框架模板

        Returns:
            templates: 模板列表
        """
        templates = [
            {
                'id': 'pest_variant',
                'name': 'PEST变体分析',
                'description': '基于PEST，可自定义维度',
                'dimensions': ['Political', 'Economic', 'Social', 'Technological']
            },
            {
                'id': 'value_chain',
                'name': '价值链分析',
                'description': '分析产业链上中下游',
                'dimensions': ['上游供应商', '中游生产', '下游渠道', '终端客户']
            },
            {
                'id': 'business_model_canvas',
                'name': '商业模式画布',
                'description': '9要素商业模式分析',
                'dimensions': ['客户细分', '价值主张', '渠道', '客户关系', '收入来源',
                              '核心资源', '关键业务', '重要伙伴', '成本结构']
            },
            {
                'id': 'swot',
                'name': 'SWOT分析',
                'description': '优势/劣势/机会/威胁',
                'dimensions': ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
            },
            {
                'id': 'custom',
                'name': '完全自定义',
                'description': '从零创建自己的分析框架',
                'dimensions': []
            }
        ]

        return templates

    def create_framework_interactive(self):
        """
        交互式创建框架（CLI版本）

        引导用户一步步创建框架
        """
        print("\n" + "="*60)
        print("🎨 欢迎使用自定义框架构建器")
        print("="*60)

        # 1. 选择模板
        print("\n📋 步骤1: 选择框架模板")
        templates = self.list_available_templates()
        for i, template in enumerate(templates, 1):
            print(f"  {i}. {template['name']}")
            print(f"     {template['description']}")

        template_choice = input("\n请选择模板编号 (1-5): ").strip()
        try:
            template = templates[int(template_choice) - 1]
        except:
            print("❌ 无效选择，使用完全自定义模板")
            template = templates[-1]

        print(f"\n✓ 已选择: {template['name']}")

        # 2. 基本信息
        print("\n📋 步骤2: 填写基本信息")
        framework_name = input("框架名称（如：SaaS行业分析框架）: ").strip()
        framework_desc = input("框架描述: ").strip()
        framework_id = framework_name.lower().replace(' ', '_').replace('/', '_')

        # 3. 定义维度
        print("\n📋 步骤3: 定义分析维度")
        dimensions = []

        if template['dimensions']:
            print(f"模板默认维度: {', '.join(template['dimensions'])}")
            use_default = input("是否使用默认维度？(y/n): ").strip().lower()

            if use_default == 'y':
                dimensions = template['dimensions']
            else:
                print("请自定义维度（每行一个，输入空行结束）:")
                while True:
                    dim = input(f"  维度{len(dimensions)+1}: ").strip()
                    if not dim:
                        break
                    dimensions.append(dim)
        else:
            print("请输入分析维度（每行一个，输入空行结束）:")
            while True:
                dim = input(f"  维度{len(dimensions)+1}: ").strip()
                if not dim:
                    break
                dimensions.append(dim)

        # 4. 定义关键问题
        print("\n📋 步骤4: 定义每个维度的关键问题")
        dimension_questions = {}

        for dim in dimensions:
            print(f"\n维度: {dim}")
            questions = []
            print("  请输入关键问题（每行一个，输入空行结束）:")
            while True:
                q = input(f"    问题{len(questions)+1}: ").strip()
                if not q:
                    break
                questions.append(q)
            dimension_questions[dim] = questions

        # 5. 权重分配
        print("\n📋 步骤5: 分配维度权重")
        dimension_weights = {}
        remaining = 100

        for i, dim in enumerate(dimensions):
            if i == len(dimensions) - 1:
                # 最后一个维度自动分配剩余权重
                weight = remaining
            else:
                while True:
                    try:
                        weight = int(input(f"  {dim} 权重 (剩余{remaining}%): ").strip())
                        if 0 < weight <= remaining:
                            break
                        print(f"    ❌ 权重必须在1-{remaining}之间")
                    except:
                        print("    ❌ 请输入有效数字")

            dimension_weights[dim] = weight
            remaining -= weight
            print(f"    ✓ 已分配 {weight}%")

        # 6. 适用行业
        print("\n📋 步骤6: 指定适用行业（可选）")
        applicable_industries = []
        print("  输入适用的行业（每行一个，输入空行跳过）:")
        while True:
            industry = input(f"    行业{len(applicable_industries)+1}: ").strip()
            if not industry:
                break
            applicable_industries.append(industry)

        # 7. 生成框架定义
        framework_def = {
            'framework_id': framework_id,
            'framework_name': framework_name,
            'description': framework_desc,
            'template_base': template['id'],
            'created_at': datetime.now().isoformat(),
            'dimensions': [],
            'applicable_industries': applicable_industries,
            'metadata': {
                'author': 'user',
                'version': '1.0',
                'custom': True
            }
        }

        # 构建维度详情
        for dim in dimensions:
            framework_def['dimensions'].append({
                'name': dim,
                'weight': f"{dimension_weights[dim]}%",
                'key_questions': dimension_questions.get(dim, []),
                'focus': f"{dim}的深度分析"
            })

        # 8. 保存框架
        self.save_framework(framework_def)

        print("\n" + "="*60)
        print(f"✅ 框架创建成功: {framework_name}")
        print(f"📁 保存位置: {self.frameworks_dir / f'{framework_id}.yaml'}")
        print("="*60)

        return framework_def

    def create_framework_from_dict(self, framework_dict: Dict) -> Dict:
        """
        从字典创建框架（API版本）

        Args:
            framework_dict: 框架定义字典
                {
                    'framework_name': 'XX分析框架',
                    'description': '...',
                    'dimensions': [
                        {
                            'name': 'XX维度',
                            'weight': '30%',
                            'key_questions': ['问题1', '问题2'],
                            'focus': '...'
                        }
                    ],
                    'applicable_industries': ['行业1', '行业2']
                }

        Returns:
            framework_def: 完整的框架定义
        """
        framework_id = framework_dict['framework_name'].lower().replace(' ', '_')

        framework_def = {
            'framework_id': framework_id,
            'framework_name': framework_dict['framework_name'],
            'description': framework_dict.get('description', ''),
            'template_base': framework_dict.get('template_base', 'custom'),
            'created_at': datetime.now().isoformat(),
            'dimensions': framework_dict['dimensions'],
            'applicable_industries': framework_dict.get('applicable_industries', []),
            'metadata': {
                'author': framework_dict.get('author', 'user'),
                'version': framework_dict.get('version', '1.0'),
                'custom': True
            }
        }

        self.save_framework(framework_def)
        return framework_def

    def save_framework(self, framework_def: Dict):
        """
        保存框架到YAML文件

        Args:
            framework_def: 框架定义
        """
        framework_id = framework_def['framework_id']
        file_path = self.frameworks_dir / f'{framework_id}.yaml'

        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(framework_def, f, allow_unicode=True, sort_keys=False)

        # 更新内存中的框架库
        self.custom_frameworks[framework_id] = framework_def

        print(f"[CustomFrameworkBuilder] Saved framework to {file_path}")

    def get_framework(self, framework_id: str) -> Optional[Dict]:
        """
        获取框架定义

        Args:
            framework_id: 框架ID

        Returns:
            framework_def: 框架定义，如果不存在返回None
        """
        return self.custom_frameworks.get(framework_id)

    def list_custom_frameworks(self) -> List[Dict]:
        """
        列出所有自定义框架

        Returns:
            frameworks: 框架列表
        """
        frameworks = []
        for fw_id, fw_def in self.custom_frameworks.items():
            frameworks.append({
                'framework_id': fw_id,
                'framework_name': fw_def['framework_name'],
                'description': fw_def.get('description', ''),
                'dimensions_count': len(fw_def.get('dimensions', [])),
                'created_at': fw_def.get('created_at', ''),
                'applicable_industries': fw_def.get('applicable_industries', [])
            })

        return frameworks

    def delete_framework(self, framework_id: str) -> bool:
        """
        删除自定义框架

        Args:
            framework_id: 框架ID

        Returns:
            success: 是否删除成功
        """
        file_path = self.frameworks_dir / f'{framework_id}.yaml'

        if file_path.exists():
            file_path.unlink()
            if framework_id in self.custom_frameworks:
                del self.custom_frameworks[framework_id]
            print(f"[CustomFrameworkBuilder] Deleted framework {framework_id}")
            return True
        else:
            print(f"[CustomFrameworkBuilder] Framework {framework_id} not found")
            return False

    def export_framework(self, framework_id: str, export_path: Path) -> bool:
        """
        导出框架（用于分享）

        Args:
            framework_id: 框架ID
            export_path: 导出路径

        Returns:
            success: 是否导出成功
        """
        framework_def = self.get_framework(framework_id)
        if not framework_def:
            return False

        with open(export_path, 'w', encoding='utf-8') as f:
            yaml.dump(framework_def, f, allow_unicode=True, sort_keys=False)

        print(f"[CustomFrameworkBuilder] Exported framework to {export_path}")
        return True

    def import_framework(self, import_path: Path) -> bool:
        """
        导入框架（从其他用户）

        Args:
            import_path: 导入路径

        Returns:
            success: 是否导入成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                framework_def = yaml.safe_load(f)

            self.save_framework(framework_def)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to import framework: {e}")
            return False


def main():
    """测试自定义框架构建器"""
    builder = CustomFrameworkBuilder()

    print("="*60)
    print("测试1: 列出框架模板")
    print("="*60)
    templates = builder.list_available_templates()
    for template in templates:
        print(f"  - {template['name']}: {template['description']}")

    print("\n" + "="*60)
    print("测试2: 从字典创建框架")
    print("="*60)

    test_framework = {
        'framework_name': 'SaaS产品分析框架',
        'description': '专门用于分析SaaS产品的框架',
        'template_base': 'custom',
        'dimensions': [
            {
                'name': '产品功能',
                'weight': '30%',
                'key_questions': [
                    '核心功能是什么？',
                    '有哪些独特功能？',
                    '功能完整性如何？'
                ],
                'focus': '产品功能的深度和广度'
            },
            {
                'name': '定价策略',
                'weight': '25%',
                'key_questions': [
                    '定价模式是什么？',
                    '价格区间如何？',
                    '是否有免费版？'
                ],
                'focus': '定价策略的合理性和竞争力'
            },
            {
                'name': '客户获取',
                'weight': '25%',
                'key_questions': [
                    'CAC是多少？',
                    '主要获客渠道？',
                    '转化率如何？'
                ],
                'focus': '客户获取的效率和成本'
            },
            {
                'name': '留存与扩张',
                'weight': '20%',
                'key_questions': [
                    '流失率是多少？',
                    'NDR是多少？',
                    '扩张路径是什么？'
                ],
                'focus': '客户留存和收入扩张能力'
            }
        ],
        'applicable_industries': ['SaaS', '企业软件', 'B2B软件']
    }

    framework_def = builder.create_framework_from_dict(test_framework)
    print(f"✓ 创建框架: {framework_def['framework_name']}")

    print("\n" + "="*60)
    print("测试3: 列出所有自定义框架")
    print("="*60)
    frameworks = builder.list_custom_frameworks()
    for fw in frameworks:
        print(f"  - {fw['framework_name']} ({fw['dimensions_count']}个维度)")
        print(f"    适用: {', '.join(fw['applicable_industries'])}")


if __name__ == '__main__':
    main()
