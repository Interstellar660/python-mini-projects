"""
双缝衍射模拟 — Fraunhofer 远场衍射
===================================
物理模型：
  - 干涉因子: cos²(β)，β = π·d·sin(θ) / λ
  - 衍射因子: [sin(α)/α]²，α = π·a·sin(θ) / λ
  - 总光强: I = I₀ · cos²(β) · [sin(α)/α]²

参数：
  a = 缝宽 (μm)
  d = 缝中心间距 (μm)
  λ = 波长 (nm)
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 可调参数
# ============================================================
WAVELENGTH = 632.8  # 波长 (nm)，He-Ne 激光
SLIT_WIDTH = 50.0   # 单缝宽度 (μm)
SLIT_GAP = 200.0    # 双缝中心间距 (μm)
SCREEN_DIST = 1.0   # 屏距 (m)
SCREEN_WIDTH = 0.05 # 屏幕观察范围 (m)，±2.5cm

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def double_slit_intensity(x, wavelength, slit_width, slit_gap, screen_dist):
    """
    计算双缝衍射光强分布。

    x: 屏幕上的位置数组 (m)
    返回归一化光强 (0~1)
    """
    # 将单位统一为米
    lam = wavelength * 1e-9   # nm → m
    a = slit_width * 1e-6     # μm → m
    d = slit_gap * 1e-6       # μm → m

    theta = np.arctan(x / screen_dist)  # 衍射角

    # 避免除零：当 alpha → 0 时 sin(alpha)/alpha → 1
    alpha = np.pi * a * np.sin(theta) / lam
    beta = np.pi * d * np.sin(theta) / lam

    # 使用 np.sinc (归一化 sinc: sin(πx)/(πx))
    diffraction = np.sinc(alpha / np.pi) ** 2
    interference = np.cos(beta) ** 2

    intensity = diffraction * interference
    return intensity / intensity.max()


# ============================================================
# 计算
# ============================================================
x = np.linspace(-SCREEN_WIDTH / 2, SCREEN_WIDTH / 2, 4096)
intensity = double_slit_intensity(x, WAVELENGTH, SLIT_WIDTH, SLIT_GAP, SCREEN_DIST)

# ============================================================
# 图 1: 一维光强分布
# ============================================================
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(x * 1e3, intensity, color="darkblue", lw=1.2)
ax1.fill_between(x * 1e3, 0, intensity, color="royalblue", alpha=0.25)
ax1.set_xlabel("屏幕位置 (mm)")
ax1.set_ylabel("相对光强")
ax1.set_title(
    f"双缝衍射光强分布\n"
    f"λ = {WAVELENGTH} nm, 缝宽 a = {SLIT_WIDTH:.0f} μm, 缝距 d = {SLIT_GAP:.0f} μm, 屏距 L = {SCREEN_DIST} m"
)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(x.min() * 1e3, x.max() * 1e3)
ax1.set_ylim(0, 1.05)
fig1.tight_layout()

# ============================================================
# 图 2: 二维干涉条纹
# ============================================================
fig2, ax2 = plt.subplots(figsize=(8, 6))

# 构建 2D 图案：竖直方向高斯衰减模拟实际光束分布
y = np.linspace(-SCREEN_WIDTH / 4, SCREEN_WIDTH / 4, 512)
X, Y = np.meshgrid(x, y)
I_2d = double_slit_intensity(X, WAVELENGTH, SLIT_WIDTH, SLIT_GAP, SCREEN_DIST)
# 竖直高斯衰减
I_2d *= np.exp(-Y**2 / (0.5 * SCREEN_WIDTH / 4) ** 2)

ax2.imshow(
    I_2d,
    extent=[x.min() * 1e3, x.max() * 1e3, y.min() * 1e3, y.max() * 1e3],
    origin="lower",
    cmap="inferno",
    aspect="auto",
)
ax2.set_xlabel("水平位置 (mm)")
ax2.set_ylabel("竖直位置 (mm)")
ax2.set_title("双缝衍射 — 二维干涉条纹")
fig2.tight_layout()

# ============================================================
# 图 3: 分解 — 干涉项 / 衍射项 / 合成
# ============================================================
lam = WAVELENGTH * 1e-9
a = SLIT_WIDTH * 1e-6
d = SLIT_GAP * 1e-6
theta = np.arctan(x / SCREEN_DIST)
alpha = np.pi * a * np.sin(theta) / lam
beta = np.pi * d * np.sin(theta) / lam

diffraction = np.sinc(alpha / np.pi) ** 2
interference = np.cos(beta) ** 2
combined = diffraction * interference
combined /= combined.max()
diffraction /= diffraction.max()
interference /= interference.max()

fig3, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

axes[0].plot(x * 1e3, diffraction, color="crimson", lw=1.2, label="衍射因子 [sin(α)/α]²")
axes[0].fill_between(x * 1e3, 0, diffraction, color="crimson", alpha=0.15)
axes[0].set_ylabel("相对光强")
axes[0].legend(loc="upper right")
axes[0].grid(True, alpha=0.3)

axes[1].plot(x * 1e3, interference, color="forestgreen", lw=1.2, label="干涉因子 cos²(β)")
axes[1].fill_between(x * 1e3, 0, interference, color="forestgreen", alpha=0.15)
axes[1].set_ylabel("相对光强")
axes[1].legend(loc="upper right")
axes[1].grid(True, alpha=0.3)

axes[2].plot(x * 1e3, combined, color="darkblue", lw=1.2, label="合成光强")
axes[2].fill_between(x * 1e3, 0, combined, color="royalblue", alpha=0.15)
axes[2].set_xlabel("屏幕位置 (mm)")
axes[2].set_ylabel("相对光强")
axes[2].legend(loc="upper right")
axes[2].grid(True, alpha=0.3)

fig3.suptitle("双缝衍射分解 — 衍射包络 × 干涉条纹", fontsize=13)
fig3.tight_layout()

# ============================================================
# 显示
# ============================================================
plt.show()

# 打印关键参数
m = int(SLIT_GAP / WAVELENGTH * 1e-3)  # 近似条纹数
fringe_spacing = WAVELENGTH * 1e-9 * SCREEN_DIST / (SLIT_GAP * 1e-6) * 1e3  # mm
print(f"波长: {WAVELENGTH} nm")
print(f"缝宽: {SLIT_WIDTH:.0f} μm")
print(f"缝距: {SLIT_GAP:.0f} μm")
print(f"屏距: {SCREEN_DIST} m")
print(f"条纹间距 ≈ {fringe_spacing:.4f} mm")
print(f"中心包络内可见条纹数 ≈ {int(2 * SLIT_GAP / SLIT_WIDTH)}")
