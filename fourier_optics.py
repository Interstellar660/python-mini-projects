"""
fourier_optics.py
=================
Fourier Optics Numerical Simulation
Includes:
  1. Fraunhofer Diffraction — rectangular & circular apertures
  2. Fresnel Diffraction — Angular Spectrum Method
  3. Lens Fourier Transform — 4f optical system simulation

Run:
    .venv\\Scripts\\python.exe fourier_optics.py
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, fftshift, ifft2, ifftshift

# ============================================================
# Physical parameters
# ============================================================
LAMBDA = 632.8e-9          # Wavelength: 632.8 nm (He-Ne laser)
k = 2 * np.pi / LAMBDA     # Wavenumber

# ============================================================
# Utility functions
# ============================================================

def rect(x, D):
    """Rectangle function: 1 when |x| <= D/2, else 0"""
    return np.where(np.abs(x) <= D / 2, 1.0, 0.0)

def circ(X, Y, D):
    """Circular aperture: 1 when sqrt(X^2+Y^2) <= D/2, else 0"""
    R = np.sqrt(X**2 + Y**2)
    return np.where(R <= D / 2, 1.0, 0.0)

def angular_spectrum_prop(U_in, L, z, wavelength=LAMBDA):
    """
    Angular Spectrum Method for scalar diffraction propagation.

    Parameters:
        U_in      : Input complex amplitude field (N x N)
        L         : Side length of the sampling window (m)
        z         : Propagation distance (m)
        wavelength: Wavelength (m)
    Returns:
        U_out     : Output complex amplitude field (N x N)
    """
    N = U_in.shape[0]
    dx = L / N
    fx = np.fft.fftfreq(N, d=dx)
    fy = np.fft.fftfreq(N, d=dx)
    FX, FY = np.meshgrid(fx, fy)

    # Transfer function (exact for scalar propagation)
    H = np.exp(1j * 2 * np.pi * z * np.sqrt(np.maximum(0, (1 / wavelength**2) - FX**2 - FY**2)))

    U_spectrum = fft2(U_in)
    U_out = ifft2(U_spectrum * H)
    return U_out


def fresnel_propagation(U_in, L, z, wavelength=LAMBDA):
    """
    Fresnel approximation propagation (single-FFT version).
    Suitable for intermediate distances satisfying the Fresnel approximation.
    """
    N = U_in.shape[0]
    dx = L / N
    x = np.linspace(-L / 2, L / 2, N)
    X, Y = np.meshgrid(x, x)

    Q1 = np.exp(1j * (np.pi / (wavelength * z)) * (X**2 + Y**2))
    Q2 = np.exp(1j * (2 * np.pi / wavelength) * z) / (1j * wavelength * z)

    U_out = Q2 * fftshift(fft2(ifftshift(U_in * Q1))) * (dx**2)
    return U_out


# ============================================================
# 1. Fraunhofer Diffraction
# ============================================================

def fraunhofer_diffraction():
    """Far-field diffraction from rectangular and circular apertures."""
    print("[1] Computing Fraunhofer diffraction ...")

    N = 1024
    L = 10e-3          # 10 mm window
    dx = L / N
    x = np.linspace(-L / 2, L / 2, N)
    X, Y = np.meshgrid(x, x)

    a = 1e-3           # Rectangular aperture width 1 mm
    D = 1e-3           # Circular aperture diameter 1 mm
    z = 1.0            # Propagation distance 1 m

    # Rectangular aperture
    U_rect = rect(X, a) * rect(Y, a)
    U_far_rect = fftshift(fft2(ifftshift(U_rect))) * (dx**2) / (1j * LAMBDA * z)
    I_rect = np.abs(U_far_rect)**2
    I_rect = I_rect / np.max(I_rect)

    # Circular aperture
    U_circ = circ(X, Y, D)
    U_far_circ = fftshift(fft2(ifftshift(U_circ))) * (dx**2) / (1j * LAMBDA * z)
    I_circ = np.abs(U_far_circ)**2
    I_circ = I_circ / np.max(I_circ)

    # Plotting
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    ax = axes[0, 0]
    ax.imshow(U_rect, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='gray')
    ax.set_title('Rectangular Aperture')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')

    ax = axes[0, 1]
    extent = [-1/(2*dx)*LAMBDA*z*1e3, 1/(2*dx)*LAMBDA*z*1e3,
              -1/(2*dx)*LAMBDA*z*1e3, 1/(2*dx)*LAMBDA*z*1e3]
    ax.imshow(I_rect, extent=extent, cmap='hot', vmax=0.05)
    ax.set_title('Far-field Intensity (Fraunhofer)')
    ax.set_xlabel("x' (mm)")
    ax.set_ylabel("y' (mm)")

    ax = axes[0, 2]
    center = N // 2
    x_axis = np.linspace(extent[0], extent[1], N)
    ax.plot(x_axis, I_rect[center, :], 'r-', lw=1.5)
    ax.set_title('Central Cross-section')
    ax.set_xlabel("x' (mm)")
    ax.set_ylabel('Normalized Intensity')
    ax.set_xlim(-5, 5)
    ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    ax.imshow(U_circ, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='gray')
    ax.set_title('Circular Aperture')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')

    ax = axes[1, 1]
    ax.imshow(I_circ, extent=extent, cmap='hot', vmax=0.05)
    ax.set_title('Far-field Intensity (Airy Pattern)')
    ax.set_xlabel("x' (mm)")
    ax.set_ylabel("y' (mm)")

    ax = axes[1, 2]
    ax.plot(x_axis, I_circ[center, :], 'b-', lw=1.5)
    ax.set_title('Central Cross-section')
    ax.set_xlabel("x' (mm)")
    ax.set_ylabel('Normalized Intensity')
    ax.set_xlim(-5, 5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fraunhofer_diffraction.png', dpi=200)
    plt.show()
    print("    Saved: fraunhofer_diffraction.png")


# ============================================================
# 2. Fresnel Diffraction
# ============================================================

def fresnel_diffraction():
    """Fresnel diffraction of a rectangular aperture at various distances."""
    print("[2] Computing Fresnel diffraction (Angular Spectrum) ...")

    N = 1024
    L = 5e-3           # 5 mm window
    x = np.linspace(-L / 2, L / 2, N)
    X, Y = np.meshgrid(x, x)

    a = 0.5e-3         # Aperture 0.5 mm
    U0 = rect(X, a) * rect(Y, a)

    distances = [0.01, 0.05, 0.2, 1.0]   # meters

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, z in enumerate(distances):
        Uz = angular_spectrum_prop(U0, L, z, wavelength=LAMBDA)
        Iz = np.abs(Uz)**2
        Iz = Iz / np.max(Iz)

        ax = axes[idx]
        ax.imshow(Iz, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='hot', vmax=0.2)
        ax.set_title(f'z = {z*100:.0f} cm')
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')

    plt.suptitle('Fresnel Diffraction: Rectangular Aperture at Different Distances', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('fresnel_diffraction.png', dpi=200)
    plt.show()
    print("    Saved: fresnel_diffraction.png")


# ============================================================
# 3. Lens Fourier Transform (4f System)
# ============================================================

def lens_fourier_transform_4f():
    """
    Simulate a 4f optical imaging system:
        Object plane -> Lens L1 (focal length f) -> Fourier plane (distance f)
        -> Lens L2 (focal length f) -> Image plane (distance f)
    The Fourier plane shows the spatial spectrum of the object,
    and the image plane shows the inverted image.
    """
    print("[3] Simulating 4f optical system (Lens Fourier Transform) ...")

    N = 1024
    L = 10e-3          # 10 mm
    x = np.linspace(-L / 2, L / 2, N)
    X, Y = np.meshgrid(x, x)
    dx = L / N

    f = 0.1            # Lens focal length 100 mm
    wavelength = LAMBDA

    # Object: two small circular apertures (double pinhole)
    d = 1.5e-3         # Separation 1.5 mm
    r = 0.2e-3         # Radius 0.2 mm
    obj = circ(X - d/2, Y, 2*r) + circ(X + d/2, Y, 2*r)

    # Lens phase modulation
    lens_phase = np.exp(-1j * (k / (2 * f)) * (X**2 + Y**2))

    # Step 1: Object -> Lens L1 (placed immediately after object)
    U_after_L1 = obj * lens_phase

    # Step 2: Propagate to Fourier plane (distance f)
    U_fourier = angular_spectrum_prop(U_after_L1, L, f, wavelength)

    # Step 3: Pass through Lens L2
    U_after_L2 = U_fourier * lens_phase

    # Step 4: Propagate to image plane (distance f)
    U_image = angular_spectrum_prop(U_after_L2, L, f, wavelength)

    I_obj = np.abs(obj)**2
    I_fourier = np.abs(U_fourier)**2
    I_image = np.abs(U_image)**2

    I_obj = I_obj / np.max(I_obj)
    I_fourier = I_fourier / np.max(I_fourier)
    I_image = I_image / np.max(I_image)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    ax = axes[0]
    ax.imshow(I_obj, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='gray')
    ax.set_title('Object Plane')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')

    ax = axes[1]
    ax.imshow(I_fourier, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='hot', vmax=0.3)
    ax.set_title('Fourier Plane')
    ax.set_xlabel("x' (mm)")
    ax.set_ylabel("y' (mm)")

    ax = axes[2]
    ax.imshow(I_image, extent=[-L/2*1e3, L/2*1e3, -L/2*1e3, L/2*1e3], cmap='gray')
    ax.set_title('Image Plane')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')

    plt.suptitle('4f Optical System Simulation', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('lens_fourier_4f.png', dpi=200)
    plt.show()
    print("    Saved: lens_fourier_4f.png")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Fourier Optics Numerical Simulation")
    print(f"Wavelength lambda = {LAMBDA*1e9:.1f} nm")
    print("=" * 60)

    fraunhofer_diffraction()
    fresnel_diffraction()
    lens_fourier_transform_4f()

    print("\nAll computations completed!")
