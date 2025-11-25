import tkinter as tk
from tkinter import ttk
import time
import random

# ---------------------- 1. 初始化主窗口（整合V1尺寸+V2标题）----------------------
root = tk.Tk()
root.title("数独求解可视化工具 - V3.0（动画+编辑+性能统计）")
root.geometry("500x780")  # 适配性能统计+测试按钮，高度微调
root.resizable(False, False)

# ---------------------- 2. 创建9×9网格容器（整合V2布局+V1可编辑）----------------------
grid_frame = ttk.Frame(root, padding="20")
grid_frame.pack(expand=True, fill=tk.BOTH)

# 存储9×9输入框的二维列表
sudoku_entries = [[None for _ in range(9)] for _ in range(9)]

# 宫格颜色配置（沿用V2，3×3宫交替区分）
cell_colors = []
for row in range(9):
    row_colors = []
    for col in range(9):
        if (row // 3 + col // 3) % 2 == 0:
            row_colors.append("#f0f0f0")  # 浅色
        else:
            row_colors.append("#ffffff")  # 白色
    cell_colors.append(row_colors)

# 循环创建9×9输入框（用tk.Entry保证兼容性，默认可编辑）
for row in range(9):
    for col in range(9):
        entry = tk.Entry(
            grid_frame,
            width=3,
            font=("Arial", 16, "bold"),
            justify=tk.CENTER,
            state="normal",  # 允许用户编辑初始数独
            bg=cell_colors[row][col],
            relief=tk.SOLID,
            borderwidth=1
        )
        entry.grid(
            row=row, column=col,
            padx=1 if (col + 1) % 3 != 0 else 3,
            pady=1 if (row + 1) % 3 != 0 else 3,
            sticky="nsew"
        )
        sudoku_entries[row][col] = entry

# 网格自适应配置（沿用V2）
for row in range(9):
    grid_frame.grid_rowconfigure(row, weight=1)
for col in range(9):
    grid_frame.grid_columnconfigure(col, weight=1)

# ---------------------- 3. 核心数据处理函数（整合V2状态控制+V1数据读取）----------------------
def fill_sudoku(sudoku_data):
    """填充数独数据（动画/示例填充通用）"""
    disable_buttons()
    for row in range(9):
        for col in range(9):
            value = sudoku_data[row][col]
            entry = sudoku_entries[row][col]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            if value != 0:
                entry.insert(0, str(value))
            entry.config(state="readonly" if is_animating else "normal")  # 动画时锁定
    enable_buttons()

def clear_sudoku():
    """清空网格+重置性能数据（整合V1+V2）"""
    disable_buttons()
    empty_data = [[0 for _ in range(9)] for _ in range(9)]
    fill_sudoku(empty_data)
    update_performance(None)  # 重置性能统计
    enable_buttons()

def read_sudoku():
    """读取用户编辑的数独数据（V1新增，供算法调用）"""
    sudoku_data = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            value = sudoku_entries[row][col].get().strip()
            if value.isdigit() and 1 <= int(value) <= 9:
                sudoku_data[row][col] = int(value)
            else:
                sudoku_data[row][col] = 0
    return sudoku_data

# 示例数独数据（沿用V1/V2）
sample_sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# ---------------------- 4. 动画模块（完整保留你的优化版，无改动）----------------------
def animate_cell_color(entry, start_color, end_color, duration=200):
    steps = 20  # 你的优化：颜色过渡更细腻
    step_duration = duration // steps

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    start_r, start_g, start_b = hex_to_rgb(start_color)
    end_r, end_g, end_b = hex_to_rgb(end_color)
    
    delta_r = (end_r - start_r) / steps
    delta_g = (end_g - start_g) / steps
    delta_b = (end_b - start_b) / steps
    
    def update_step(step):
        if step > steps:
            entry.config(bg=end_color)
            return
        current_r = int(start_r + delta_r * step)
        current_g = int(start_g + delta_g * step)
        current_b = int(start_b + delta_b * step)
        current_color = f"#{current_r:02x}{current_g:02x}{current_b:02x}"
        entry.config(bg=current_color)
        entry.after(step_duration, update_step, step + 1)
    
    update_step(1)

def animate_number_fill(entry, value, duration=300):
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, value)
    entry.config(fg=entry["bg"])  # 初始透明
    
    steps = 15  # 你的优化：数字过渡更平滑
    step_duration = duration // steps
    start_r, start_g, start_b = 240, 240, 240
    end_r, end_g, end_b = 0, 0, 0
    
    def update_step(step):
        if step > steps:
            entry.config(fg="#000000")
            entry.config(state="readonly" if is_animating else "normal")
            return
        current_r = int(start_r - (start_r - end_r) * (step / steps))
        current_g = int(start_g - (start_g - end_g) * (step / steps))
        current_b = int(start_b - (start_b - end_b) * (step / steps))
        current_color = f"#{current_r:02x}{current_g:02x}{current_b:02x}"
        entry.config(fg=current_color)
        entry.after(step_duration, update_step, step + 1)
    
    update_step(1)

def animate_backtrack(entry, duration=200):
    original_color = entry["bg"]
    animate_cell_color(entry, original_color, "#ffb6c1", duration=duration//2)
    
    def clear_after_highlight():
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.config(state="readonly" if is_animating else "normal")
        animate_cell_color(entry, "#ffb6c1", original_color, duration=duration//2)
    
    entry.after(duration//2, clear_after_highlight)

# ---------------------- 5. 核心动画接口（供成员A调用，完整保留）----------------------
def animation_fill_cell(row, col, value):
    if not (0 <= row < 9 and 0 <= col < 9):
        print("无效的单元格坐标")
        return
    disable_buttons()
    entry = sudoku_entries[row][col]
    original_color = entry["bg"]
    
    animate_cell_color(entry, original_color, "#90ee90", duration=200)
    def fill_number_after_highlight():
        animate_number_fill(entry, str(value), duration=300)
        root.after(300, enable_buttons)
    
    entry.after(200, fill_number_after_highlight)

def animation_single_fill(row, col, value):
    if not (0 <= row < 9 and 0 <= col < 9):
        print("无效的单元格坐标")
        return
    disable_buttons()
    entry = sudoku_entries[row][col]
    animate_number_fill(entry, str(value), duration=200)
    root.after(200, enable_buttons)

def animation_backtrack_cell(row, col):
    if not (0 <= row < 9 and 0 <= col < 9):
        print("无效的单元格坐标")
        return
    disable_buttons()
    entry = sudoku_entries[row][col]
    animate_backtrack(entry, duration=300)
    root.after(300, enable_buttons)

# ---------------------- 6. 动画队列（优化流畅度，完整保留）----------------------
animation_queue = []
is_animating = False

def add_animation_to_queue(anim_func, *args):
    animation_queue.append((anim_func, args))
    if not is_animating:
        run_next_animation()

def run_next_animation():
    global is_animating
    if not animation_queue:
        is_animating = False
        return
    is_animating = True
    anim_func, args = animation_queue.pop(0)
    anim_func(*args)
    root.after(350, run_next_animation)

# ---------------------- 7. 按钮状态控制（整合所有按钮，新增求解/对比按钮）----------------------
def disable_buttons():
    # 包含所有功能按钮+测试按钮+求解按钮
    fill_btn.config(state="disabled")
    clear_btn.config(state="disabled")
    test_fill_btn.config(state="disabled")
    test_backtrack_btn.config(state="disabled")
    test_single_btn.config(state="disabled")
    solve_btn.config(state="disabled")
    compare_btn.config(state="disabled")

def enable_buttons():
    fill_btn.config(state="normal")
    clear_btn.config(state="normal")
    test_fill_btn.config(state="normal")
    test_backtrack_btn.config(state="normal")
    test_single_btn.config(state="normal")
    solve_btn.config(state="normal")
    compare_btn.config(state="normal")

# ---------------------- 8. 功能按钮区（整合V1填充/清空+V2测试按钮）----------------------
# 基础功能按钮（填充/清空）
button_frame = ttk.Frame(root, padding="0 10 0 10")
button_frame.pack(fill=tk.X, padx=20)

fill_btn = ttk.Button(button_frame, text="填充示例数独", command=lambda: fill_sudoku(sample_sudoku))
fill_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(button_frame, text="清空网格", command=clear_sudoku)
clear_btn.pack(side=tk.LEFT, padx=5)

# 动画测试按钮（保留V2，用于演示）
test_frame = ttk.Frame(root, padding="0 0 0 10")
test_frame.pack(fill=tk.X, padx=20)

def test_fill_animation():
    clear_sudoku()
    root.after(500, animation_fill_cell, 0, 0, 5)

test_fill_btn = ttk.Button(test_frame, text="测试填数高亮动画", command=test_fill_animation)
test_fill_btn.pack(side=tk.LEFT, padx=5)

def test_backtrack_animation():
    animation_fill_cell(1, 1, 3)
    root.after(1000, animation_backtrack_cell, 1, 1)

test_backtrack_btn = ttk.Button(test_frame, text="测试回溯撤销动画", command=test_backtrack_animation)
test_backtrack_btn.pack(side=tk.LEFT, padx=5)

def test_single_fill_animation():
    clear_sudoku()
    add_animation_to_queue(animation_single_fill, 2, 2, 7)
    add_animation_to_queue(animation_single_fill, 3, 3, 9)
    add_animation_to_queue(animation_single_fill, 4, 4, 2)

test_single_btn = ttk.Button(test_frame, text="测试单步填数过渡", command=test_single_fill_animation)
test_single_btn.pack(side=tk.LEFT, padx=5)

# ---------------------- 9. 算法选择区（用V1的Combobox，更美观）----------------------
algorithm_frame = ttk.Frame(root, padding="0 0 0 10")
algorithm_frame.pack(fill=tk.X, padx=20)

alg_label = ttk.Label(algorithm_frame, text="选择求解算法：")
alg_label.pack(side=tk.LEFT, padx=5)

algorithm_var = tk.StringVar(value="请选择算法")
alg_options = ["基础DFS算法（成员A）", "进阶CSP算法（成员C）"]
# 改用V1的Combobox（比OptionMenu交互更友好）
alg_menu = ttk.Combobox(algorithm_frame, textvariable=algorithm_var, values=alg_options, state="readonly")
alg_menu.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

# ---------------------- 10. 性能统计板块（完整保留V1，阶段3核心功能）----------------------
performance_frame = ttk.LabelFrame(root, text="算法性能统计", padding="10")
performance_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

# 性能指标标签
perf_labels = {}
metrics = [
    ("algorithm", "算法名称：", "未运行"),
    ("time", "执行时间：", "0.000 秒"),
    ("nodes", "搜索节点数：", "0"),
    ("backtracks", "回溯次数：", "0"),
    ("status", "求解状态：", "待求解")
]

for i, (key, label_text, default_value) in enumerate(metrics):
    row_frame = ttk.Frame(performance_frame)
    row_frame.pack(fill=tk.X, pady=3)
    label = ttk.Label(row_frame, text=label_text, font=("Arial", 10))
    label.pack(side=tk.LEFT)
    value_label = ttk.Label(row_frame, text=default_value, font=("Arial", 10, "bold"), foreground="#0066cc")
    value_label.pack(side=tk.LEFT, padx=5)
    perf_labels[key] = value_label

def update_performance(perf_data):
    """更新性能显示（整合动画和求解流程）"""
    if perf_data is None:
        # 重置为默认值
        perf_labels['algorithm'].config(text="未运行")
        perf_labels['time'].config(text="0.000 秒")
        perf_labels['nodes'].config(text="0")
        perf_labels['backtracks'].config(text="0")
        perf_labels['status'].config(text="待求解", foreground="#666666")
    else:
        perf_labels['algorithm'].config(text=perf_data.get('algorithm', '未知'))
        perf_labels['time'].config(text=f"{perf_data.get('time', 0):.3f} 秒")
        perf_labels['nodes'].config(text=str(perf_data.get('nodes', 0)))
        perf_labels['backtracks'].config(text=str(perf_data.get('backtracks', 0)))
        status = perf_data.get('status', '未知')
        if status == '成功':
            perf_labels['status'].config(text=status, foreground="#00aa00")
        elif status == '失败':
            perf_labels['status'].config(text=status, foreground="#cc0000")
        else:
            perf_labels['status'].config(text=status, foreground="#666666")

# ---------------------- 11. 求解按钮区（整合V1按钮+V2动画+性能统计）----------------------
solve_frame = ttk.Frame(root, padding="0 0 0 20")
solve_frame.pack(fill=tk.X, padx=20)

def solve_sudoku():
    """模拟算法求解（关联动画+性能统计，阶段3将替换为真实算法调用）"""
    selected_alg = algorithm_var.get()
    if selected_alg == "请选择算法":
        perf_labels['status'].config(text="请先选择算法", foreground="#cc0000")
        return
    
    # 读取用户编辑的数独数据
    sudoku_data = read_sudoku()
    if all(value == 0 for row in sudoku_data for value in row):
        perf_labels['status'].config(text="请输入或填充数独", foreground="#cc0000")
        return
    
    # 清空原有动画队列，重置状态
    global animation_queue
    animation_queue = []
    clear_sudoku()
    fill_sudoku(sudoku_data)  # 重新填充用户输入的数独
    perf_labels['status'].config(text="求解中...", foreground="#ff9900")
    
    # 模拟算法求解过程（触发动画+统计性能）
    start_time = time.time()
    disable_buttons()
    
    # 模拟填数动画（随机选择几个单元格，实际将替换为A/C的算法回调）
    def simulate_solve():
        # 模拟搜索节点和回溯次数
        nodes = random.randint(200, 1500)
        backtracks = random.randint(30, 300)
        
        # 模拟填数动画队列
        fill_positions = [(0,2,4), (1,3,7), (2,5,3), (3,1,2), (4,4,5), (5,6,8), (6,7,1), (7,0,6), (8,8,9)]
        for row, col, val in fill_positions:
            add_animation_to_queue(animation_single_fill, row, col, val)
        
        # 模拟回溯动画（随机选1个位置）
        backtrack_row, backtrack_col = 2, 5
        add_animation_to_queue(animation_backtrack_cell, backtrack_row, backtrack_col)
        add_animation_to_queue(animation_single_fill, backtrack_row, backtrack_col, 6)  # 回溯后重新填数
        
        # 计算耗时，更新性能统计
        end_time = time.time()
        perf_data = {
            'algorithm': selected_alg,
            'time': end_time - start_time,
            'nodes': nodes,
            'backtracks': backtracks,
            'status': '成功'
        }
        root.after(350 * len(animation_queue), update_performance, perf_data)
        root.after(350 * len(animation_queue), enable_buttons)
    
    root.after(500, simulate_solve)

# 求解按钮（关联模拟求解流程）
solve_btn = ttk.Button(solve_frame, text="开始求解", command=solve_sudoku)
solve_btn.pack(side=tk.LEFT, padx=5)

# 对比按钮（预留阶段3功能，暂用空实现）
compare_btn = ttk.Button(solve_frame, text="对比所有算法", command=lambda: print("对比功能预留"))
compare_btn.pack(side=tk.LEFT, padx=5)

# ---------------------- 12. 启动主循环 ----------------------
root.mainloop()