from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


OUTPUT_DIR = Path(__file__).resolve().parent
N = 256
FFT_SIZE = 8192


WINDOWS = {
    "boxcar": lambda n: signal.windows.boxcar(n),
    "triang": lambda n: signal.windows.triang(n),
    "bartlett": lambda n: signal.windows.bartlett(n),
    "hann": lambda n: signal.windows.hann(n),
    "hamming": lambda n: signal.windows.hamming(n),
    "blackman": lambda n: signal.windows.blackman(n),
    "blackmanharris": lambda n: signal.windows.blackmanharris(n),
    "nuttall": lambda n: signal.windows.nuttall(n),
    "flattop": lambda n: signal.windows.flattop(n),
    "parzen": lambda n: signal.windows.parzen(n),
    "bohman": lambda n: signal.windows.bohman(n),
    "cosine": lambda n: signal.windows.cosine(n),
    "tukey_alpha_0_5": lambda n: signal.windows.tukey(n, alpha=0.5),
    "kaiser_beta_14": lambda n: signal.windows.kaiser(n, beta=14),
    "gaussian_std_40": lambda n: signal.windows.gaussian(n, std=40),
    "general_gaussian_p_1_5_sig_40": lambda n: signal.windows.general_gaussian(
        n, p=1.5, sig=40
    ),
    "chebwin_at_100": lambda n: signal.windows.chebwin(n, at=100),
    "exponential_tau_40": lambda n: signal.windows.exponential(n, tau=40),
    "taylor": lambda n: signal.windows.taylor(n, nbar=4, sll=60),
    "lanczos": lambda n: signal.windows.lanczos(n),
}


def frequency_response_db(window: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    spectrum = np.fft.fftshift(np.fft.fft(window, FFT_SIZE))
    magnitude = np.abs(spectrum)
    magnitude /= np.max(magnitude)
    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-12))
    frequency = np.linspace(-0.5, 0.5, FFT_SIZE, endpoint=False)
    return frequency, magnitude_db


def save_window_plot(name: str, window: np.ndarray) -> None:
    frequency, magnitude_db = frequency_response_db(window)

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), constrained_layout=True)
    fig.suptitle(f"{name} window", fontsize=16)

    axes[0].plot(window, linewidth=1.8)
    axes[0].set_title("Time domain")
    axes[0].set_xlabel("Sample")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(frequency, magnitude_db, linewidth=1.4)
    axes[1].set_title("Frequency domain")
    axes[1].set_xlabel("Normalized frequency")
    axes[1].set_ylabel("Magnitude (dB)")
    axes[1].set_ylim(-140, 5)
    axes[1].grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"{name}.jpg"
    fig.savefig(output_path, dpi=180, format="jpg")
    plt.close(fig)


def main() -> None:
    for name, factory in WINDOWS.items():
        save_window_plot(name, factory(N))
    print(f"Saved {len(WINDOWS)} JPG files to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
