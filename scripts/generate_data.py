"""Generate deterministic synthetic data for the lab graph templates."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTFILE = DATA_DIR / "lab_graph_examples.npz"
META_FILE = DATA_DIR / "metadata.json"


def lorentzian(x, x0, gamma, amp=1.0, offset=0.0):
    return offset + amp * gamma**2 / ((x - x0) ** 2 + gamma**2)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20260521)

    x = np.linspace(0.0, 10.0, 240)
    sparse_x = np.linspace(0.0, 10.0, 28)
    true_signal = 0.55 + 0.32 * np.exp(-x / 5.0) * np.cos(2.5 * x)
    single_trace = true_signal + rng.normal(0.0, 0.025, x.size)

    fit_x = np.linspace(0.0, 10.0, 500)
    fit_y = 0.55 + 0.32 * np.exp(-fit_x / 5.0) * np.cos(2.5 * fit_x)
    data_fit_y = 0.55 + 0.32 * np.exp(-sparse_x / 5.0) * np.cos(2.5 * sparse_x)
    data_fit_y += rng.normal(0.0, 0.03, sparse_x.size)
    fit_band = 0.035 + 0.01 * np.exp(-fit_x / 4.0)

    scatter_x = rng.normal(0.0, 1.0, 260)
    scatter_y = 0.65 * scatter_x + rng.normal(0.0, 0.55, scatter_x.size)

    err_x = np.linspace(0.0, 6.0, 16)
    err_mean = 0.5 + 0.35 * np.sin(1.3 * err_x) * np.exp(-err_x / 8.0)
    err_y = err_mean + rng.normal(0.0, 0.035, err_x.size)
    err = 0.045 + 0.015 * rng.random(err_x.size)

    residual = data_fit_y - (0.55 + 0.32 * np.exp(-sparse_x / 5.0) * np.cos(2.5 * sparse_x))

    decay_x = np.linspace(0.0, 8.0, 28)
    decay_y = 0.95 * np.exp(-decay_x / 2.2) + 0.02 + rng.normal(0.0, 0.015, decay_x.size)
    decay_fit_x = np.linspace(0.0, 8.0, 300)
    decay_fit_y = 0.95 * np.exp(-decay_fit_x / 2.2) + 0.02

    log_x = np.geomspace(8, 1000, 35)
    log_y = 1.6 * log_x ** -0.55 * np.exp(rng.normal(0.0, 0.08, log_x.size))
    log_ref = 1.6 * log_x ** -0.55

    compare_x = np.linspace(0.0, 2.0 * np.pi, 180)
    compare_exp = np.sin(compare_x) + rng.normal(0.0, 0.06, compare_x.size)
    compare_theory = np.sin(compare_x)
    compare_sim = 0.97 * np.sin(compare_x + 0.08)

    categorical_x = np.linspace(0.0, 5.0, 120)
    categorical = np.vstack(
        [
            np.exp(-categorical_x / (2.0 + k * 0.35)) * np.cos(1.1 * categorical_x + 0.22 * k)
            for k in range(6)
        ]
    )

    grad_params = np.linspace(0.1, 1.0, 9)
    grad_x = np.linspace(0.0, 6.0, 220)
    grad_curves = np.vstack(
        [np.exp(-grad_x / (2.0 + 2.5 * p)) * np.cos((1.1 + p) * grad_x) for p in grad_params]
    )

    signed_params = np.linspace(-2.0, 2.0, 9)
    signed_curves = np.vstack(
        [np.sin(grad_x + 0.5 * p) * np.exp(-grad_x / 5.5) + 0.12 * p for p in signed_params]
    )

    spec_x = np.linspace(-5.0, 5.0, 260)
    waterfall_params = np.linspace(-1.8, 1.8, 16)
    waterfall = np.vstack(
        [
            lorentzian(spec_x, 1.2 * p, 0.35 + 0.04 * abs(p), amp=1.0, offset=0.03)
            + rng.normal(0.0, 0.015, spec_x.size)
            for p in waterfall_params
        ]
    )

    trajectories = []
    for _ in range(300):
        trajectories.append(
            np.exp(-x / 6.0) * np.cos(1.7 * x + rng.normal(0.0, 0.15))
            + rng.normal(0.0, 0.18, x.size)
        )
    trajectories = np.vstack(trajectories)
    envelope_mean = trajectories.mean(axis=0)
    envelope_lo = np.quantile(trajectories, 0.16, axis=0)
    envelope_hi = np.quantile(trajectories, 0.84, axis=0)

    facet_x = np.linspace(0.0, 4.0, 80)
    facet = np.vstack([np.exp(-facet_x / (1.2 + 0.35 * k)) * np.cos((1 + 0.18 * k) * facet_x) for k in range(4)])

    time_x = np.linspace(0.0, 120.0, 500)
    time_trace = 0.12 * rng.normal(size=time_x.size)
    time_trace += 0.45 * np.exp(-((time_x - 42.0) / 8.0) ** 2)
    time_trace += 0.25 * np.exp(-((time_x - 85.0) / 11.0) ** 2)

    pulse_t = np.linspace(0.0, 100.0, 400)
    pulse_i = np.where((pulse_t > 10) & (pulse_t < 42), np.sin(np.pi * (pulse_t - 10) / 32) ** 2, 0.0)
    pulse_q = np.where((pulse_t > 55) & (pulse_t < 86), 0.75 * np.sin(np.pi * (pulse_t - 55) / 31) ** 2, 0.0)
    pulse_ro = np.where((pulse_t > 88) & (pulse_t < 98), 0.65, 0.0)

    freq = np.linspace(4.2, 5.2, 240)
    spectrum = lorentzian(freq, 4.72, 0.035, amp=1.0, offset=0.05)
    spectrum += lorentzian(freq, 4.94, 0.06, amp=0.45, offset=0.0)
    spectrum += rng.normal(0.0, 0.018, freq.size)
    spectrum_fit = lorentzian(freq, 4.72, 0.035, amp=1.0, offset=0.05) + lorentzian(freq, 4.94, 0.06, amp=0.45)

    grid_x = np.linspace(-3.0, 3.0, 140)
    grid_y = np.linspace(-2.0, 2.0, 110)
    X, Y = np.meshgrid(grid_x, grid_y)
    heat = np.exp(-((X - 0.8) ** 2 + (Y + 0.2) ** 2)) + 0.45 * np.exp(-((X + 1.2) ** 2 / 1.8 + (Y - 0.8) ** 2 / 0.6))
    spectroscopy = np.exp(-((Y - 0.55 * np.sin(1.6 * X)) ** 2) / 0.09) + 0.45 * np.exp(-((Y + 0.6 + 0.12 * X) ** 2) / 0.12)
    phase_diagram = 0.5 * (1 + np.tanh(2.2 * (Y - 0.35 * X**2 + 0.7)))
    diverging = 0.9 * np.sin(1.7 * X) * np.cos(2.2 * Y) * np.exp(-(X**2 + Y**2) / 8.5)
    phase = np.angle((X + 0.1) + 1j * (Y - 0.2))
    contour_z = np.sin(X) + np.cos(1.4 * Y)

    pos_matrix = rng.random((9, 9))
    pos_matrix = pos_matrix @ pos_matrix.T
    pos_matrix /= pos_matrix.max()
    signed_matrix = rng.normal(0.0, 0.18, (9, 9))
    signed_matrix = 0.5 * (signed_matrix + signed_matrix.T)

    q = np.linspace(-3.0, 3.0, 140)
    p = np.linspace(-3.0, 3.0, 140)
    Q, P = np.meshgrid(q, p)
    wigner = (2 * (Q**2 + P**2) - 1.0) * np.exp(-(Q**2 + P**2)) / np.pi

    hist_samples = rng.gamma(shape=5.0, scale=0.45, size=700)
    hist_grid = np.linspace(0.0, 6.0, 300)
    hist_pdf = hist_grid ** 4 * np.exp(-hist_grid / 0.45)
    hist_pdf /= np.trapz(hist_pdf, hist_grid)

    populations = np.array([0.49, 0.24, 0.13, 0.08, 0.04, 0.02])
    populations += rng.normal(0.0, 0.006, populations.size)
    populations = np.clip(populations, 0.0, None)
    populations /= populations.sum()
    theory_pop = np.array([0.50, 0.23, 0.14, 0.075, 0.038, 0.017])

    grouped = np.array(
        [
            [0.91, 0.86, 0.79],
            [0.84, 0.82, 0.75],
            [0.76, 0.74, 0.69],
            [0.65, 0.63, 0.58],
        ]
    )

    distribution_groups = np.vstack(
        [
            rng.normal(0.82, 0.05, 90),
            rng.normal(0.74, 0.07, 90),
            rng.normal(0.68, 0.10, 90),
            rng.normal(0.58, 0.08, 90),
        ]
    )

    surface_x = np.linspace(-2.0, 2.0, 65)
    surface_y = np.linspace(-2.0, 2.0, 65)
    SX, SY = np.meshgrid(surface_x, surface_y)
    surface_z = np.exp(-(SX**2 + 0.7 * SY**2)) * np.cos(2.2 * SX)
    bloch_t = np.linspace(0.0, 2.8 * np.pi, 160)
    bloch_x = 0.78 * np.sin(bloch_t) * np.exp(-bloch_t / 14.0)
    bloch_y = 0.78 * np.cos(bloch_t) * np.exp(-bloch_t / 14.0)
    bloch_z = np.linspace(0.75, -0.35, bloch_t.size)

    np.savez_compressed(
        OUTFILE,
        x=x,
        sparse_x=sparse_x,
        single_trace=single_trace,
        fit_x=fit_x,
        fit_y=fit_y,
        data_fit_y=data_fit_y,
        fit_band=fit_band,
        scatter_x=scatter_x,
        scatter_y=scatter_y,
        err_x=err_x,
        err_y=err_y,
        err=err,
        residual=residual,
        decay_x=decay_x,
        decay_y=decay_y,
        decay_fit_x=decay_fit_x,
        decay_fit_y=decay_fit_y,
        log_x=log_x,
        log_y=log_y,
        log_ref=log_ref,
        compare_x=compare_x,
        compare_exp=compare_exp,
        compare_theory=compare_theory,
        compare_sim=compare_sim,
        categorical_x=categorical_x,
        categorical=categorical,
        grad_params=grad_params,
        grad_x=grad_x,
        grad_curves=grad_curves,
        signed_params=signed_params,
        signed_curves=signed_curves,
        spec_x=spec_x,
        waterfall_params=waterfall_params,
        waterfall=waterfall,
        envelope_mean=envelope_mean,
        envelope_lo=envelope_lo,
        envelope_hi=envelope_hi,
        facet_x=facet_x,
        facet=facet,
        time_x=time_x,
        time_trace=time_trace,
        pulse_t=pulse_t,
        pulse_i=pulse_i,
        pulse_q=pulse_q,
        pulse_ro=pulse_ro,
        freq=freq,
        spectrum=spectrum,
        spectrum_fit=spectrum_fit,
        grid_x=grid_x,
        grid_y=grid_y,
        heat=heat,
        spectroscopy=spectroscopy,
        phase_diagram=phase_diagram,
        diverging=diverging,
        phase=phase,
        contour_z=contour_z,
        pos_matrix=pos_matrix,
        signed_matrix=signed_matrix,
        q=q,
        p=p,
        wigner=wigner,
        hist_samples=hist_samples,
        hist_grid=hist_grid,
        hist_pdf=hist_pdf,
        populations=populations,
        theory_pop=theory_pop,
        grouped=grouped,
        distribution_groups=distribution_groups,
        surface_x=surface_x,
        surface_y=surface_y,
        surface_z=surface_z,
        bloch_x=bloch_x,
        bloch_y=bloch_y,
        bloch_z=bloch_z,
    )

    metadata = {
        "seed": 20260521,
        "description": "Synthetic quantum-physics-style datasets for the 30 lab graph templates.",
        "output": str(OUTFILE.relative_to(ROOT)),
    }
    META_FILE.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTFILE}")
    print(f"Wrote {META_FILE}")


if __name__ == "__main__":
    main()
