import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1. 黑体辐射光谱 (普朗克定律)
# ============================================================
h = 6.626e-34      # 普朗克常数
c = 3e8            # 光速
k = 1.381e-23      # 玻尔兹曼常数


def planck(wavelength, T):
    return (2 * h * c ** 2 / wavelength ** 5) / (
        np.exp(h * c / (wavelength * k * T)) - 1
    )


# ============================================================
# 2. 高斯光束传播模拟
# ============================================================
def gaussian_beam(r, z, w0, wavelength=632.8e-9):
    zr = np.pi * w0 ** 2 / wavelength
    z = np.asarray(z, dtype=float)
    wz = w0 * np.sqrt(1 + (z / zr) ** 2)
    wz = np.where(z == 0, w0, wz)
    amplitude = (w0 / wz) * np.exp(-(np.asarray(r) ** 2) / wz ** 2)
    return amplitude, wz, zr


# ============================================================
# 3. 杨氏双缝干涉
# ============================================================
def young_interference(x, d, wavelength, L, a=None):
    k = 2 * np.pi / wavelength
    intensity = (np.cos(k * d * x / (2 * L))) ** 2
    if a is not None:
        sinc_arg = np.pi * a * x / (wavelength * L)
        sinc_arg = np.where(sinc_arg == 0, 1e-30, sinc_arg)
        intensity *= (np.sin(sinc_arg) / sinc_arg) ** 2
    return intensity


# ============================================================
# 绘图
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("光电基础仿真", fontsize=16)

# --- 黑体辐射 ---
wl = np.linspace(100e-9, 3000e-9, 500)
for T_C, ls in [(3000, "-"), (4000, "--"), (5000, "-."), (6000, ":")]:
    T = T_C
    axes[0, 0].plot(wl * 1e9, planck(wl, T) * 1e-9, ls=ls, label=f"{T_C} K")
axes[0, 0].set_xlabel("波长 (nm)")
axes[0, 0].set_ylabel("光谱辐射出射度 (W/m^3)")
axes[0, 0].set_title("黑体辐射光谱 (普朗克定律)")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(alpha=0.3)

# --- 高斯光束 ---
w0 = 1e-3
r = np.linspace(-5e-3, 5e-3, 200)
depths = [0, 0.5, 1, 2]
for z_ in depths:
    amp, wz, zr = gaussian_beam(np.abs(r), z_, w0)
    axes[0, 1].plot(r * 1e3, amp, label=f"z={z_:.1f} m")
axes[0, 1].set_xlabel("径向距离 (mm)")
axes[0, 1].set_ylabel("振幅 (归一化)")
axes[0, 1].set_title("高斯光束传输 (632.8nm He-Ne)")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(alpha=0.3)

# --- 光束展宽 ---
z_vals = np.linspace(0, 5, 300)
_, wz_vals, zr = gaussian_beam(0, z_vals, w0)
axes[1, 0].plot(z_vals, wz_vals * 1e3, "b-")
axes[1, 0].axvline(zr, color="r", linestyle="--", label=f"瑞利长度 zr={zr:.3f} m")
axes[1, 0].set_xlabel("传播距离 (m)")
axes[1, 0].set_ylabel("束腰半径 w(z) (mm)")
axes[1, 0].set_title("高斯光束束腰展宽")
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(alpha=0.3)

# --- 双缝干涉 ---
x_screen = np.linspace(-0.02, 0.02, 800)
I = young_interference(x_screen, d=0.5e-3, wavelength=632.8e-9, L=1.0, a=0.1e-3)
axes[1, 1].plot(x_screen * 1e3, I, "r-")
axes[1, 1].set_xlabel("屏幕位置 (mm)")
axes[1, 1].set_ylabel("相对光强")
axes[1, 1].set_title("杨氏双缝干涉 (d=0.5mm, a=0.1mm)")
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("optoelectronics_sim.png", dpi=150)
plt.show()
print("仿真完成，图表已保存为 optoelectronics_sim.png")
