#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试workflow生成是否正确"""

import sys
import io

# 修复Windows编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from core.research_engine import ResearchEngine

engine = ResearchEngine()

# 测试公司对标
result = engine.create_workflow(['核心能力', '壁垒迁移', '财务测算'], research_type='公司对标')

print('=' * 60)
print('测试：公司对标 - 核心能力/壁垒迁移/财务测算')
print('=' * 60)
print()

# 检查workflow是否包含这3个维度
workflow_names = [step['name'] for step in result['workflow']]
print('Workflow维度：', workflow_names)
print()

# 检查是否包含这3个核心维度
assert '核心能力' in workflow_names, '缺少：核心能力'
assert '壁垒迁移' in workflow_names, '缺少：壁垒迁移'
assert '财务测算' in workflow_names, '缺少：财务测算'
print('[PASS] 3个核心维度都在workflow中')
print()

# 检查hypothesis是否是真实模板内容（非占位符）
for step in result['workflow']:
    if step['name'] == '核心能力':
        print(f"核心能力 hypothesis: {step['hypothesis'][:80]}...")
        assert '占位符' not in step['hypothesis'], '是占位符，非真实模板'
        assert '标杆公司' in step['hypothesis'], '不是真实的公司对标模板'
        print('[PASS] hypothesis是真实模板内容')
        break
print()

# 检查data_requirements
print('data_requirements:')
for req in result['data_requirements']:
    print(f'  - {req}')
print()

# 验证包含内部数据需求
assert len(result['data_requirements']) > 0, 'data_requirements为空'
assert any('B公司' in req or '标的公司' in req or '公司内部' in req for req in result['data_requirements']), \
    'data_requirements不包含内部数据'
print('[PASS] data_requirements包含内部数据需求')
print()

print('=' * 60)
print('[SUCCESS] 所有测试通过')
print('=' * 60)
