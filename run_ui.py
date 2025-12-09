# -*- coding: utf-8 -*-
"""
数独求解器 UI 启动脚本
直接运行此文件即可启动界面
"""
import sys
import os

# 确保在正确的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 添加到 Python 路径
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("=" * 60)
print("数独求解可视化工具 v5.0")
print("=" * 60)
print(f"工作目录: {current_dir}")

# 导入并运行 UI
try:
    import UI.ui_v5
except Exception as e:
    print(f"\n错误: {e}")
    print("\n请确保项目结构完整：")
    print("  - src/algorithms/")
    print("  - src/generator/")
    print("  - UI/")
    input("\n按回车键退出...")
