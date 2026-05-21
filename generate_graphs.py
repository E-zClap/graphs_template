"""Generate Quantum Ink graph taxonomy examples.

Run:
    python scripts/generate_data.py
    python generate_graphs.py

Outputs:
    figures/png/*.png
    figures/quantum_ink_taxonomy_one_page.pdf
"""

from __future__ import annotations

import runpy
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages

from lab_graph_style import COLORS, LINEWIDTH, MARKER_SIZE, apply_style, clean_axes, cmap


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "lab_graph_examples.npz"
PNG_DIR = ROOT / "figures" / "png"
PDF_FILE = ROOT / "figures" / "quantum_ink_taxonomy_one_page.pdf"
FULL_SIZE_PDF_FILE = ROOT / "figures" / "quantum_ink_templates_full_size.pdf"


@dataclass(frozen=True)
class Template:
    title: str
    slug: str
    drawer: callable
    projection: str | None = None


def _colorbar(ax, artist, label: str, compact: bool) -> None:
    cb = ax.figure.colorbar(artist, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label(label, fontsize=6 if compact else 7)
    cb.ax.tick_params(labelsize=5 if compact else 6, length=2, width=0.5)
    cb.outline.set_linewidth(0.5)


def _finish(ax, xlabel: str, ylabel: str, compact: bool = False) -> None:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    clean_axes(ax)
    if compact:
        ax.tick_params(labelsize=5)
        ax.xaxis.label.set_size(6)
        ax.yaxis.label.set_size(6)


def _label_legend(ax, compact: bool = False) -> None:
    ax.legend(frameon=False, handlelength=1.6, borderpad=0.1, labelspacing=0.25, fontsize=5 if compact else 7)


def _exp_plot(ax, x, y, label=None, compact=False, markevery=None):
    return ax.plot(
        x,
        y,
        "o",
        color=COLORS["exp"],
        markerfacecolor="white",
        markeredgecolor=COLORS["exp"],
        markeredgewidth=0.8 if compact else 0.9,
        markersize=3.2 if compact else MARKER_SIZE,
        linestyle="",
        markevery=markevery,
        label=label,
    )


def draw_single_trace(ax, d, compact=False):
    ax.plot(d["x"], d["single_trace"], color=COLORS["exp"])
    _finish(ax, r"Time ($\mu$s)", "Population", compact)


def draw_scatter(ax, d, compact=False):
    ax.scatter(
        d["scatter_x"],
        d["scatter_y"],
        s=9 if compact else 16,
        facecolors="white",
        edgecolors=COLORS["exp"],
        linewidths=0.55 if compact else 0.7,
        alpha=0.75,
    )
    _finish(ax, "Quadrature I (a.u.)", "Quadrature Q (a.u.)", compact)


def draw_error_bars(ax, d, compact=False):
    ax.errorbar(
        d["err_x"],
        d["err_y"],
        yerr=d["err"],
        fmt="o",
        color=COLORS["exp"],
        ecolor=COLORS["exp"],
        markerfacecolor="white",
        markeredgecolor=COLORS["exp"],
        markeredgewidth=0.8,
        elinewidth=LINEWIDTH["errorbar"],
        capsize=2,
        markersize=MARKER_SIZE,
    )
    _finish(ax, "Drive amplitude (a.u.)", "Signal", compact)


def draw_data_fit(ax, d, compact=False):
    ax.fill_between(d["fit_x"], d["fit_y"] - d["fit_band"], d["fit_y"] + d["fit_band"], color=COLORS["theory"], alpha=0.18, linewidth=0)
    ax.plot(d["fit_x"], d["fit_y"], color=COLORS["theory"], label="fit")
    _exp_plot(ax, d["sparse_x"], d["data_fit_y"], label="exp.", compact=compact)
    _finish(ax, r"Pulse duration ($\mu$s)", "Population", compact)
    _label_legend(ax, compact)


def draw_residual(ax, d, compact=False):
    ax.plot(d["fit_x"], d["fit_y"], color=COLORS["theory"], label="fit")
    _exp_plot(ax, d["sparse_x"], d["data_fit_y"], label="exp.", compact=compact)
    _finish(ax, r"Pulse duration ($\mu$s)", "Population", compact)
    inset = ax.inset_axes([0.16, 0.10, 0.78, 0.28])
    inset.axhline(0.0, color=COLORS["reference"], linewidth=LINEWIDTH["reference"])
    inset.plot(
        d["sparse_x"],
        d["residual"],
        "o",
        color=COLORS["exp"],
        markerfacecolor="white",
        markeredgecolor=COLORS["exp"],
        markeredgewidth=0.7,
        markersize=2.2 if compact else 3.0,
    )
    inset.set_ylabel("res.", fontsize=5 if compact else 6)
    inset.set_xlabel(r"Time ($\mu$s)", fontsize=5 if compact else 6)
    clean_axes(inset)
    inset.tick_params(labelsize=5 if compact else 6, length=2, pad=1)


def draw_semilog_decay(ax, d, compact=False):
    ax.semilogy(
        d["decay_x"],
        d["decay_y"],
        "o",
        color=COLORS["exp"],
        markerfacecolor="white",
        markeredgecolor=COLORS["exp"],
        markeredgewidth=0.8,
        markersize=MARKER_SIZE,
        label="exp.",
    )
    ax.semilogy(d["decay_fit_x"], d["decay_fit_y"], color=COLORS["theory"], label="fit")
    _finish(ax, r"Delay ($\mu$s)", "Survival probability", compact)
    _label_legend(ax, compact)


def draw_loglog_scaling(ax, d, compact=False):
    ax.loglog(
        d["log_x"],
        d["log_y"],
        "o",
        color=COLORS["exp"],
        markerfacecolor="white",
        markeredgecolor=COLORS["exp"],
        markeredgewidth=0.8,
        markersize=MARKER_SIZE,
        label="data",
    )
    ax.loglog(d["log_x"], d["log_ref"], color=COLORS["theory"], label=r"$N^{-0.55}$")
    ax.loglog(d["log_x"], d["log_ref"][0] * (d["log_x"] / d["log_x"][0]) ** -0.5, "--", color=COLORS["reference"], linewidth=LINEWIDTH["reference"], label=r"$N^{-1/2}$")
    _finish(ax, "Samples N", "Error", compact)
    _label_legend(ax, compact)


def draw_compare_three(ax, d, compact=False):
    _exp_plot(ax, d["compare_x"], d["compare_exp"], label="exp.", compact=compact, markevery=8)
    ax.plot(d["compare_x"], d["compare_theory"], color=COLORS["theory"], label="theory")
    ax.plot(d["compare_x"], d["compare_sim"], color=COLORS["simulation"], linestyle="--", label="simulation")
    _finish(ax, "Phase (rad)", "Response", compact)
    _label_legend(ax, compact)


def draw_multicurve_categorical(ax, d, compact=False):
    styles = ["-", "--", "-.", ":", (0, (5, 1, 1, 1)), "--"]
    labels = ["main", "protocol B", "protocol C", "protocol D", "protocol E", "loss"]
    colors = [COLORS["exp"], COLORS["reference"], COLORS["reference"], COLORS["reference"], COLORS["reference"], COLORS["error"]]
    widths = [1.25, 0.85, 0.85, 0.85, 0.85, 1.1]
    alphas = [1.0, 0.85, 0.75, 0.65, 0.55, 1.0]
    for y, color, ls, label, lw, alpha in zip(d["categorical"], colors, styles, labels, widths, alphas):
        ax.plot(d["categorical_x"], y, color=color, linestyle=ls, label=label, linewidth=lw, alpha=alpha)
    _finish(ax, r"Time ($\mu$s)", "Normalized signal", compact)
    _label_legend(ax, compact)


def draw_gradient_family(ax, d, compact=False):
    norm = Normalize(float(d["grad_params"].min()), float(d["grad_params"].max()))
    cm = cmap("sequential")
    for p, y in zip(d["grad_params"], d["grad_curves"]):
        ax.plot(d["grad_x"], y, color=cm(norm(p)), linewidth=0.9 if compact else 1.1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cm)
    _colorbar(ax, sm, "Drive (a.u.)", compact)
    _finish(ax, r"Time ($\mu$s)", "Signal", compact)


def draw_diverging_family(ax, d, compact=False):
    norm = TwoSlopeNorm(vmin=float(d["signed_params"].min()), vcenter=0.0, vmax=float(d["signed_params"].max()))
    cm = cmap("diverging")
    for p, y in zip(d["signed_params"], d["signed_curves"]):
        ax.plot(d["grad_x"], y, color=cm(norm(p)), linewidth=0.9 if compact else 1.1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cm)
    _colorbar(ax, sm, "Detuning (MHz)", compact)
    _finish(ax, r"Time ($\mu$s)", "Response", compact)


def draw_waterfall(ax, d, compact=False):
    offset = 0.28
    cm = cmap("diverging")
    norm = TwoSlopeNorm(vmin=float(d["waterfall_params"].min()), vcenter=0.0, vmax=float(d["waterfall_params"].max()))
    for i, (p, y) in enumerate(zip(d["waterfall_params"], d["waterfall"])):
        ax.plot(d["spec_x"], y + i * offset, color=cm(norm(p)), linewidth=0.65 if compact else 0.85)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cm)
    _colorbar(ax, sm, "Flux bias (a.u.)", compact)
    ax.set_yticks([])
    _finish(ax, "Frequency offset (MHz)", "Offset spectra", compact)


def draw_envelope(ax, d, compact=False):
    ax.fill_between(d["x"], d["envelope_lo"], d["envelope_hi"], color=COLORS["simulation"], alpha=0.20, linewidth=0, label="16-84%")
    ax.plot(d["x"], d["envelope_mean"], color=COLORS["simulation"], label="mean")
    _finish(ax, r"Time ($\mu$s)", "Trajectory", compact)
    _label_legend(ax, compact)


def draw_small_multiples(ax, d, compact=False):
    ax.axis("off")
    for k in range(4):
        left = 0.07 + 0.47 * (k % 2)
        bottom = 0.57 - 0.47 * (k // 2)
        sub = ax.inset_axes([left, bottom, 0.40, 0.34])
        sub.plot(d["facet_x"], d["facet"][k], color=COLORS["exp"])
        sub.set_title(f"g={k + 1}", fontsize=5 if compact else 6, pad=1)
        clean_axes(sub)
        sub.tick_params(labelsize=4.5 if compact else 5.5, length=1.8, pad=1)


def draw_time_trace(ax, d, compact=False):
    ax.axvspan(32, 52, color=COLORS["grid"], alpha=0.45, linewidth=0)
    ax.axvspan(78, 94, color=COLORS["grid"], alpha=0.45, linewidth=0)
    ax.plot(d["time_x"], d["time_trace"], color=COLORS["exp"])
    _finish(ax, r"Time ($\mu$s)", "Voltage (a.u.)", compact)


def draw_pulse_sequence(ax, d, compact=False):
    offsets = [1.6, 0.8, 0.0]
    labels = ["I", "Q", "RO"]
    arrays = [d["pulse_i"], d["pulse_q"], d["pulse_ro"]]
    colors = [COLORS["exp_light"], COLORS["exp_light"], COLORS["reference"]]
    for off, label, arr, color in zip(offsets, labels, arrays, colors):
        ax.plot(d["pulse_t"], arr + off, color=color)
        ax.text(d["pulse_t"][0] - 3, off + 0.25, label, ha="right", va="center", fontsize=6 if compact else 7)
    ax.set_yticks([])
    _finish(ax, "Time (ns)", "Channel", compact)


def draw_spectrum(ax, d, compact=False):
    _exp_plot(ax, d["freq"], d["spectrum"], label="exp.", compact=compact, markevery=8)
    ax.plot(d["freq"], d["spectrum_fit"], color=COLORS["theory"], label="fit")
    for peak in [4.72, 4.94]:
        ax.axvline(peak, color=COLORS["reference"], linewidth=LINEWIDTH["reference"])
    _finish(ax, "Frequency (GHz)", "Counts (a.u.)", compact)
    _label_legend(ax, compact)


def draw_heatmap(ax, d, compact=False):
    im = ax.imshow(d["heat"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("sequential"))
    _colorbar(ax, im, "Population", compact)
    _finish(ax, r"Detuning $\Delta/2\pi$ (MHz)", "Drive (a.u.)", compact)


def draw_spectroscopy_map(ax, d, compact=False):
    im = ax.imshow(d["spectroscopy"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("sequential"))
    x = d["grid_x"]
    ax.plot(x, 0.55 * np.sin(1.6 * x), color=COLORS["theory"], linewidth=1.0)
    ax.plot(x, -0.6 - 0.12 * x, color=COLORS["reference"], linewidth=0.8)
    _colorbar(ax, im, "Intensity", compact)
    _finish(ax, "Flux bias (a.u.)", r"Frequency $\omega/2\pi$ (GHz)", compact)


def draw_phase_diagram(ax, d, compact=False):
    im = ax.imshow(d["phase_diagram"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("sequential"), vmin=0, vmax=1)
    x = d["grid_x"]
    boundary = 0.35 * x**2 - 0.7
    ax.plot(x, boundary, color=COLORS["black"], linewidth=0.9)
    ax.text(-2.6, 1.2, "I", fontsize=6 if compact else 7)
    ax.text(1.4, -1.1, "II", fontsize=6 if compact else 7)
    _colorbar(ax, im, "Order", compact)
    _finish(ax, r"Coupling $g/2\pi$ (MHz)", r"Detuning $\Delta/2\pi$ (MHz)", compact)


def draw_diverging_heatmap(ax, d, compact=False):
    lim = float(np.max(np.abs(d["diverging"])))
    im = ax.imshow(d["diverging"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("diverging"), vmin=-lim, vmax=lim)
    _colorbar(ax, im, "Residual", compact)
    _finish(ax, r"$x$ ($\mu$m)", r"$y$ ($\mu$m)", compact)


def draw_phase_heatmap(ax, d, compact=False):
    im = ax.imshow(d["phase"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("cyclic"), vmin=-np.pi, vmax=np.pi)
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.02, ticks=[-np.pi, 0, np.pi])
    cb.ax.set_yticklabels([r"$-\pi$", "0", r"$\pi$"])
    cb.set_label("Phase", fontsize=6 if compact else 7)
    cb.ax.tick_params(labelsize=5 if compact else 6, length=2, width=0.5)
    _finish(ax, "q", "p", compact)


def draw_contour(ax, d, compact=False):
    im = ax.imshow(d["heat"], origin="lower", aspect="auto", extent=[d["grid_x"].min(), d["grid_x"].max(), d["grid_y"].min(), d["grid_y"].max()], cmap=cmap("sequential"), alpha=0.95)
    ax.contour(d["grid_x"], d["grid_y"], d["contour_z"], levels=6, colors=COLORS["black"], linewidths=0.55)
    _colorbar(ax, im, "Signal", compact)
    _finish(ax, "x", "y", compact)


def draw_matrix(ax, d, compact=False):
    ax.axis("off")
    a1 = ax.inset_axes([0.02, 0.06, 0.36, 0.82])
    im1 = a1.imshow(d["pos_matrix"], cmap=cmap("sequential"), vmin=0)
    a1.set_title(r"$|\rho|$", fontsize=5 if compact else 6, pad=1)
    a1.set_xticks([])
    a1.set_yticks([])
    cax1 = ax.inset_axes([0.40, 0.12, 0.025, 0.68])
    cb1 = ax.figure.colorbar(im1, cax=cax1)
    cb1.ax.tick_params(labelsize=4.5 if compact else 6, length=1.8, width=0.5)
    cb1.set_label("amp.", fontsize=5 if compact else 7)
    a2 = ax.inset_axes([0.55, 0.06, 0.36, 0.82])
    lim = float(np.max(np.abs(d["signed_matrix"])))
    im2 = a2.imshow(d["signed_matrix"], cmap=cmap("diverging"), vmin=-lim, vmax=lim)
    a2.set_title(r"Re($\rho$)", fontsize=5 if compact else 6, pad=1)
    a2.set_xticks([])
    a2.set_yticks([])
    cax2 = ax.inset_axes([0.93, 0.12, 0.025, 0.68])
    cb2 = ax.figure.colorbar(im2, cax=cax2)
    cb2.ax.tick_params(labelsize=4.5 if compact else 6, length=1.8, width=0.5)
    cb2.set_label("value", fontsize=5 if compact else 7)
    for sub in [a1, a2]:
        for spine in sub.spines.values():
            spine.set_linewidth(0.5)
            spine.set_edgecolor(COLORS["black"])


def draw_wigner(ax, d, compact=False):
    lim = float(np.max(np.abs(d["wigner"])))
    im = ax.imshow(d["wigner"], origin="lower", extent=[d["q"].min(), d["q"].max(), d["p"].min(), d["p"].max()], cmap=cmap("diverging"), vmin=-lim, vmax=lim)
    ax.contour(d["q"], d["p"], d["wigner"], levels=[0], colors=COLORS["black"], linewidths=0.6)
    ax.set_aspect("equal")
    _colorbar(ax, im, "W(q,p)", compact)
    _finish(ax, "q", "p", compact)


def draw_histogram(ax, d, compact=False):
    ax.hist(d["hist_samples"], bins=28, density=True, color=COLORS["exp"], alpha=0.75, edgecolor="white", linewidth=0.3)
    ax.plot(d["hist_grid"], d["hist_pdf"], color=COLORS["theory"], label="fit")
    _finish(ax, "Photon counts (a.u.)", "Density", compact)
    _label_legend(ax, compact)


def draw_population_bars(ax, d, compact=False):
    states = np.arange(d["populations"].size)
    ax.bar(states, d["populations"], color=COLORS["exp"], width=0.72, label="exp.")
    ax.plot(states, d["theory_pop"], "o", color=COLORS["theory"], markersize=MARKER_SIZE, label="theory")
    ax.set_xticks(states)
    ax.set_xticklabels([rf"$|{i}\rangle$" for i in states])
    _finish(ax, "State", "Population", compact)
    _label_legend(ax, compact)


def draw_grouped_bars(ax, d, compact=False):
    x = np.arange(d["grouped"].shape[0])
    width = 0.23
    colors = [COLORS["exp"], COLORS["theory"], COLORS["simulation"]]
    labels = ["exp.", "theory", "sim."]
    for k in range(3):
        ax.bar(x + (k - 1) * width, d["grouped"][:, k], width=width, color=colors[k], label=labels[k])
    ax.set_xticks(x)
    ax.set_xticklabels(["A", "B", "C", "D"])
    ax.set_ylim(0.45, 1.0)
    _finish(ax, "Protocol", "Fidelity", compact)
    _label_legend(ax, compact)


def draw_violin_swarm(ax, d, compact=False):
    vals = [row for row in d["distribution_groups"]]
    parts = ax.violinplot(vals, showmedians=True, widths=0.72)
    for body in parts["bodies"]:
        body.set_facecolor(COLORS["exp_light"])
        body.set_alpha(0.35)
        body.set_edgecolor(COLORS["exp"])
        body.set_linewidth(0.6)
    for key in ["cmedians", "cbars", "cmins", "cmaxes"]:
        parts[key].set_color(COLORS["black"])
        parts[key].set_linewidth(0.6)
    rng = np.random.default_rng(5)
    for i, row in enumerate(vals, start=1):
        jitter = rng.normal(0.0, 0.035, size=len(row))
        ax.scatter(np.full_like(row, i, dtype=float) + jitter, row, s=5 if compact else 8, color=COLORS["reference"], alpha=0.45, linewidths=0)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["A", "B", "C", "D"])
    _finish(ax, "Device", "Fidelity", compact)


def draw_3d_surface(ax, d, compact=False):
    theta = np.linspace(0.0, np.pi, 36)
    phi = np.linspace(0.0, 2.0 * np.pi, 72)
    sphere_x = np.outer(np.sin(theta), np.cos(phi))
    sphere_y = np.outer(np.sin(theta), np.sin(phi))
    sphere_z = np.outer(np.cos(theta), np.ones_like(phi))
    ax.plot_wireframe(
        sphere_x,
        sphere_y,
        sphere_z,
        color=COLORS["reference"],
        linewidth=0.35 if compact else 0.45,
        alpha=0.55,
        rstride=4,
        cstride=8,
    )

    equator = np.linspace(0.0, 2.0 * np.pi, 240)
    ax.plot(np.cos(equator), np.sin(equator), 0.0, color=COLORS["reference"], linewidth=0.7)
    for start, end, label in [
        ((-1.05, 0, 0), (1.05, 0, 0), r"$x$"),
        ((0, -1.05, 0), (0, 1.05, 0), r"$y$"),
        ((0, 0, -1.05), (0, 0, 1.05), r"$z$"),
    ]:
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color=COLORS["grid"],
            linewidth=0.6,
        )
        ax.text(end[0] * 1.08, end[1] * 1.08, end[2] * 1.08, label, fontsize=6 if compact else 7)

    t = np.linspace(0.12 * np.pi, 0.86 * np.pi, 180)
    phase = np.linspace(0.0, 1.65 * np.pi, t.size)
    path_x = np.sin(t) * np.cos(phase)
    path_y = np.sin(t) * np.sin(phase)
    path_z = np.cos(t)
    ax.plot(path_x, path_y, path_z, color=COLORS["exp"], linewidth=1.3, label="state")
    ax.scatter(path_x[0], path_y[0], path_z[0], color=COLORS["exp_light"], s=14 if compact else 20, depthshade=False)
    ax.scatter(path_x[-1], path_y[-1], path_z[-1], color=COLORS["error"], s=14 if compact else 20, depthshade=False)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_zlim(-1.15, 1.15)
    ax.set_xlabel(r"$x$", labelpad=-5)
    ax.set_ylabel(r"$y$", labelpad=-5)
    ax.set_zlabel(r"$z$", labelpad=-7)
    ax.tick_params(labelsize=5 if compact else 6, pad=-2)
    ax.view_init(elev=22, azim=-45)
    ax.xaxis.pane.set_alpha(0.0)
    ax.yaxis.pane.set_alpha(0.0)
    ax.zaxis.pane.set_alpha(0.0)


TEMPLATES = [
    Template("Single measured trace", "01_single_measured_trace", draw_single_trace),
    Template("Scatter / point plot", "02_scatter_point_plot", draw_scatter),
    Template("Data with error bars", "03_data_with_error_bars", draw_error_bars),
    Template("Data + fit / theory", "04_data_plus_fit_theory", draw_data_fit),
    Template("Residual plot", "05_residual_plot", draw_residual),
    Template("Semi-log decay", "06_semilog_decay", draw_semilog_decay),
    Template("Log-log scaling", "07_loglog_scaling", draw_loglog_scaling),
    Template("Experiment / theory / simulation", "08_exp_theory_simulation", draw_compare_three),
    Template("Multi-curve categorical", "09_multicurve_categorical", draw_multicurve_categorical),
    Template("Gradient curve family", "10_gradient_curve_family", draw_gradient_family),
    Template("Diverging curve family", "11_diverging_curve_family", draw_diverging_family),
    Template("Offset / waterfall", "12_offset_waterfall", draw_waterfall),
    Template("Envelope / uncertainty band", "13_envelope_uncertainty_band", draw_envelope),
    Template("Small multiples", "14_small_multiples", draw_small_multiples),
    Template("Time trace", "15_time_trace", draw_time_trace),
    Template("Pulse sequence", "16_pulse_sequence", draw_pulse_sequence),
    Template("Spectrum line plot", "17_spectrum_line_plot", draw_spectrum),
    Template("Standard heatmap", "18_standard_heatmap", draw_heatmap),
    Template("Spectroscopy map", "19_spectroscopy_map", draw_spectroscopy_map),
    Template("Phase diagram", "20_phase_diagram", draw_phase_diagram),
    Template("Diverging heatmap", "21_diverging_heatmap", draw_diverging_heatmap),
    Template("Phase / cyclic heatmap", "22_phase_cyclic_heatmap", draw_phase_heatmap),
    Template("Contour plot", "23_contour_plot", draw_contour),
    Template("Matrix heatmap", "24_matrix_heatmap", draw_matrix),
    Template("Wigner function", "25_wigner_function", draw_wigner),
    Template("Histogram", "26_histogram", draw_histogram),
    Template("State population bars", "27_state_population_bars", draw_population_bars),
    Template("Grouped bar chart", "28_grouped_bar_chart", draw_grouped_bars),
    Template("Violin / swarm plot", "29_violin_swarm_plot", draw_violin_swarm),
    Template("Bloch sphere / state path", "30_bloch_sphere_state_path", draw_3d_surface, projection="3d"),
]


def ensure_data() -> None:
    if not DATA_FILE.exists():
        runpy.run_path(str(ROOT / "scripts" / "generate_data.py"), run_name="__main__")


def load_data():
    ensure_data()
    return np.load(DATA_FILE)


def save_individual_pngs(data) -> list[Path]:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    for stale_png in PNG_DIR.glob("*.png"):
        stale_png.unlink()
    outputs = []
    for i, template in enumerate(TEMPLATES, start=1):
        fig = plt.figure(figsize=(3.35, 2.45), constrained_layout=True)
        ax = fig.add_subplot(111, projection=template.projection) if template.projection else fig.add_subplot(111)
        template.drawer(ax, data, compact=False)
        ax.set_title(f"{i}. {template.title}", loc="left", pad=3)
        out = PNG_DIR / f"{template.slug}.png"
        fig.savefig(out)
        plt.close(fig)
        outputs.append(out)
    return outputs


def save_full_size_pdf(data) -> Path:
    FULL_SIZE_PDF_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(FULL_SIZE_PDF_FILE) as pdf:
        for i, template in enumerate(TEMPLATES, start=1):
            fig = plt.figure(figsize=(3.35, 2.45), constrained_layout=True)
            ax = fig.add_subplot(111, projection=template.projection) if template.projection else fig.add_subplot(111)
            template.drawer(ax, data, compact=False)
            ax.set_title(f"{i}. {template.title}", loc="left", pad=3)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
    return FULL_SIZE_PDF_FILE


def save_one_page_pdf(data) -> Path:
    PDF_FILE.parent.mkdir(parents=True, exist_ok=True)
    for stale_pdf in [
        ROOT / "figures" / "lab_graph_templates_one_page.pdf",
        ROOT / "figures" / "lab_graph_templates_full_size.pdf",
    ]:
        if stale_pdf.exists():
            stale_pdf.unlink()
    fig = plt.figure(figsize=(21, 25), constrained_layout=True)
    gs = fig.add_gridspec(6, 5)
    for i, template in enumerate(TEMPLATES):
        row, col = divmod(i, 5)
        ax = fig.add_subplot(gs[row, col], projection=template.projection) if template.projection else fig.add_subplot(gs[row, col])
        template.drawer(ax, data, compact=True)
        ax.set_title(f"{i + 1}. {template.title}", loc="left", pad=2, fontsize=7)
    handles = [
        Line2D([0], [0], color=COLORS["exp"], marker="o", markerfacecolor="white", markeredgecolor=COLORS["exp"], linestyle="", label="experiment"),
        Line2D([0], [0], color=COLORS["exp_light"], linestyle="-", label="secondary / control"),
        Line2D([0], [0], color=COLORS["theory"], linestyle="-", label="theory / fit"),
        Line2D([0], [0], color=COLORS["simulation"], linestyle="--", label="simulation"),
        Line2D([0], [0], color=COLORS["error"], linestyle="-", label="loss / error"),
        Line2D([0], [0], color=COLORS["reference"], linestyle="-", label="reference"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(0.5, 1.012), fontsize=8)
    fig.suptitle("Quantum Ink v1: Lab Graph Taxonomy", fontsize=14, y=1.028)
    fig.savefig(PDF_FILE)
    plt.close(fig)
    return PDF_FILE


def main() -> None:
    apply_style()
    data = load_data()
    pngs = save_individual_pngs(data)
    full_pdf = save_full_size_pdf(data)
    pdf = save_one_page_pdf(data)
    print(f"Wrote {len(pngs)} PNG files to {PNG_DIR}")
    print(f"Wrote {full_pdf}")
    print(f"Wrote {pdf}")


if __name__ == "__main__":
    main()
