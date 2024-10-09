import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# リンク機構のパラメータ
L1 = 13.4
L2 = 16.4
L3 = 4.8

# 時間の設定
time = np.linspace(0, 2 * np.pi, 100)

def calculate_radian(x, y, is_right):
    alpha = -(x + (-L3 if is_right else L3)) / y
    beta = (x**2 + y**2 - L3**2 + L1**2 - L2**2) / (2 * y)
    
    A = 1 + alpha**2
    B = L3 + alpha * beta * (-1 if is_right else 1)
    C = L3**2 - L1**2 + beta**2
    
    X = (1 if is_right else -1) * (B + np.sqrt(B**2 - A * C)) / A
    Y = alpha * X + beta

    print(f"{Y}")
    
    return np.arcsin(Y / L1)

def final_radian(x, y):
    angle1 = np.pi - calculate_radian(x, y, False)
    angle2 = calculate_radian(x, y, True)
    return angle1, angle2

def draw_circle(theta):
    x = L3 + 5 * np.cos(theta)
    y = L2 + 5 * np.sin(theta)
    return x, y

def calculate_drawpoint(p1, p2, d):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = np.sqrt(dx**2 + dy**2)

    if dist == 0:
        raise ValueError("p1 and p2 are the same point, an infinite number of solutions exist.")

    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2
    half_dist = dist / 2
    a = np.sqrt(d**2 - half_dist**2)

    x_diff = (dy / dist) * a
    y_diff = (dx / dist) * a

    point = [mid_x - x_diff, mid_y + y_diff]

    return point

def calculate_positions(theta):
    x, y = draw_circle(theta)
    target_angle1, target_angle2 = final_radian(x, y)

    x1 = L1 * np.cos(target_angle1)
    y1 = L1 * np.sin(target_angle1)

    x2 = 2 * L3 + L1 * np.cos(target_angle2)
    y2 = L1 * np.sin(target_angle2)

    x3, y3 = calculate_drawpoint([x1, y1], [x2, y2], L2)

    return x1, y1, x2, y2, x3, y3

# プロットの設定
fig, ax = plt.subplots()
ax.set_xlim(-30, 30)
ax.set_ylim(-10, 30)
line, = ax.plot([], [], 'o-', lw=2)
trail, = ax.plot([], [], 'r-', lw=1)
ax.set_aspect('equal')

x3_trail = []
y3_trail = []

def init():
    line.set_data([], [])
    trail.set_data([], [])
    return line, trail

def update(frame):
    x1, y1, x2, y2, x3, y3 = calculate_positions(frame)
    x3_trail.append(x3)
    y3_trail.append(y3)
    line.set_data([0, x1, x3, x2, 2 * L3], [0, y1, y3, y2, 0])
    trail.set_data(x3_trail, y3_trail)
    return line, trail

ani = FuncAnimation(fig, update, frames=time, init_func=init, blit=True)
plt.show()
