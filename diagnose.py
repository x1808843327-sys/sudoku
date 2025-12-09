# -*- coding: utf-8 -*-
"""
诊断脚本 - 检查项目结构和导入
"""
import sys
import os

print("=" * 60)
print("数独项目诊断工具")
print("=" * 60)

# 1. 检查当前目录
current_dir = os.getcwd()
print(f"\n1. 当前工作目录: {current_dir}")

# 2. 检查项目结构
print("\n2. 检查项目结构:")
required_paths = [
    "src",
    "src/algorithms",
    "src/generator",
    "UI",
    "src/algorithms/solver_basic_v1.py",
    "src/algorithms/solver_ac3_mrv_lcv.py",
    "src/generator/sudoku_generator.py",
    "UI/ui_v5.py"
]

all_exist = True
for path in required_paths:
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"  {status} {path}")
    if not exists:
        all_exist = False

# 3. 测试导入
print("\n3. 测试导入:")
if all_exist:
    try:
        from src.algorithms.solver_basic_v1 import SudokuSolver
        print("  ✓ BasicSolver 导入成功")
    except ImportError as e:
        print(f"  ✗ BasicSolver 导入失败: {e}")
    
    try:
        from src.algorithms.solver_ac3_mrv_lcv import AC3_MRV_LCV_Solver
        print("  ✓ AC3_MRV_LCV_Solver 导入成功")
    except ImportError as e:
        print(f"  ✗ AC3_MRV_LCV_Solver 导入失败: {e}")
    
    try:
        from src.generator.sudoku_generator import SudokuGenerator
        print("  ✓ SudokuGenerator 导入成功")
    except ImportError as e:
        print(f"  ✗ SudokuGenerator 导入失败: {e}")
else:
    print("  ⚠ 项目结构不完整，跳过导入测试")

# 4. 建议
print("\n4. 运行建议:")
if all_exist:
    print("  ✓ 项目结构完整")
    print("  → 运行命令: python UI/ui_v5.py")
    print("  → 或运行: python run_ui.py")
else:
    print("  ✗ 项目结构不完整")
    print("  → 请确保在项目根目录运行此脚本")
    print("  → 项目根目录应包含 src 和 UI 文件夹")

print("\n" + "=" * 60)
