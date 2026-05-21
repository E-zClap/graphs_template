"""Shared lab graph style.

This module centralizes the semantic palette, font choices, line widths, and
colormap access used by the example graph templates.
"""

from __future__ import annotations

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager


FONT_TEXT = "Libertinus Serif"
FONT_MATH = "Libertinus Math"

COLORS = {
    "ink": "#111318",
    "graphite": "#5F646A",
    "reference": "#A7A9AC",
    "mist": "#D9DEE3",
    "exp": "#0B4F71",
    "exp_light": "#8CC7D8",
    "theory": "#C48A00",
    "simulation": "#0A7A75",
    "error": "#A33A2B",
    "black": "#111318",
    "grid": "#D9DEE3",
}

COLORMAPS = {
    "sequential": "quantum_seq",
    "positive": "quantum_seq",
    "diverging": "quantum_div",
    "signed": "quantum_div",
    "cyclic": "quantum_phase",
    "phase": "quantum_phase",
}

QUANTUM_COLORMAP_COLORS = {
    "quantum_seq": [
        "#071820",
        "#0B4F71",
        "#0A7A75",
        "#E2B84A",
    ],
    "quantum_div": [
        "#A33A2B",
        "#F3EFE6",
        "#0B4F71",
    ],
    "quantum_phase": [
        "#0B4F71",
        "#0A7A75",
        "#C48A00",
        "#A33A2B",
        "#0B4F71",
    ],
}

LAB_GRAPH_IDENTITY = {
    "name": "Quantum Ink",
    "fonts": {
        "text": FONT_TEXT,
        "math": FONT_MATH,
    },
    "colors": COLORS,
    "colormaps": {
        "positive": QUANTUM_COLORMAP_COLORS["quantum_seq"],
        "signed": QUANTUM_COLORMAP_COLORS["quantum_div"],
        "phase": QUANTUM_COLORMAP_COLORS["quantum_phase"],
    },
    "rules": {
        "normal_panel_color_budget": "1-2 accent colors maximum",
        "experiment": "deep blue markers or line",
        "theory": "amber line, no markers",
        "simulation": "teal dashed line",
        "error": "oxide red only for bad/unwanted physics",
        "references": "grey, thin, visually secondary",
        "many_categories": "grey line styles, not many colors",
        "heatmaps": "use lab-native colormaps only",
    },
}

LINEWIDTH = {
    "axis": 0.6,
    "main": 1.2,
    "secondary": 0.9,
    "errorbar": 0.7,
    "reference": 0.7,
}

MARKER_SIZE = 4.0

ROOT = Path(__file__).resolve().parent
FONT_DIR = ROOT / "fonts"


def register_project_fonts() -> None:
    """Register vendored fonts without requiring a system font install."""

    static_fonts = list(FONT_DIR.glob("*.otf"))
    font_paths = static_fonts if static_fonts else list(FONT_DIR.glob("*.ttf"))
    for font_path in font_paths:
        font_manager.fontManager.addfont(str(font_path))


def cmap(role_or_name: str):
    """Return a lab-native Quantum Ink colormap by role or explicit name."""

    name = COLORMAPS.get(role_or_name, role_or_name)
    if name not in QUANTUM_COLORMAP_COLORS:
        raise ValueError(f"Unknown Quantum Ink colormap role: {role_or_name!r}")
    return LinearSegmentedColormap.from_list(name, QUANTUM_COLORMAP_COLORS[name])


def apply_style() -> None:
    """Apply the lab-wide matplotlib style."""

    register_project_fonts()
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}
    font_family = (
        FONT_TEXT
        if FONT_TEXT in available_fonts
        else "STIX Two Text"
        if "STIX Two Text" in available_fonts
        else "STIXGeneral"
        if "STIXGeneral" in available_fonts
        else "DejaVu Serif"
    )

    plt.rcParams.update(
        {
            "font.family": font_family,
            "mathtext.fontset": "custom",
            "mathtext.rm": FONT_MATH if FONT_MATH in available_fonts else font_family,
            "mathtext.it": f"{font_family}:italic",
            "mathtext.bf": f"{font_family}:bold",
            "mathtext.sf": font_family,
            "mathtext.tt": "DejaVu Sans Mono",
            "axes.edgecolor": COLORS["ink"],
            "axes.labelcolor": COLORS["ink"],
            "axes.linewidth": LINEWIDTH["axis"],
            "xtick.color": COLORS["ink"],
            "ytick.color": COLORS["ink"],
            "text.color": COLORS["ink"],
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.03,
            "axes.labelsize": 8,
            "axes.titlesize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "lines.linewidth": LINEWIDTH["main"],
            "lines.markersize": MARKER_SIZE,
            "patch.linewidth": LINEWIDTH["axis"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def clean_axes(ax) -> None:
    """Use restrained APS-friendly axes."""

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=2.5, width=LINEWIDTH["axis"], pad=2)


def panel_label(ax, label: str) -> None:
    """Place a compact panel label."""

    ax.text(
        -0.16,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        va="top",
        ha="left",
    )
