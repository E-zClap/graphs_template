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

BRAND = {
    "midnight": "#0A0F1C",
    "navy": "#11233F",
    "ice": "#A9B8D0",
    "white": "#F4F6F8",
    "orange": "#F47A20",
    "amber": "#FFB347",
    "rust": "#B85724",
    "slate": "#6E7785",
    "light_slate": "#D7DCE3",
}

COLORS = {
    "exp": "#F47A20",
    "exp_light": "#FFB347",
    "theory": "#244C84",
    "simulation": "#5E8FCB",
    "error": "#B85724",
    "reference": "#8A9099",
    "text": "#111318",
    "grid": "#DCE1E8",
    "ice": "#A9B8D0",
    "amber": "#FFB347",
    "black": "#111318",
    "ink": "#111318",
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
        "#08111F",
        "#15325B",
        "#244C84",
        "#F47A20",
        "#FFD08A",
    ],
    "quantum_div": [
        "#B85724",
        "#F5EFE8",
        "#244C84",
    ],
    "quantum_phase": [
        "#244C84",
        "#5E8FCB",
        "#F47A20",
        "#FFD08A",
        "#244C84",
    ],
}

LAB_GRAPH_IDENTITY = {
    "name": "Midnight Quantum",
    "fonts": {
        "text": FONT_TEXT,
        "math": FONT_MATH,
    },
    "brand": BRAND,
    "colors": COLORS,
    "colormaps": {
        "positive": QUANTUM_COLORMAP_COLORS["quantum_seq"],
        "signed": QUANTUM_COLORMAP_COLORS["quantum_div"],
        "phase": QUANTUM_COLORMAP_COLORS["quantum_phase"],
    },
    "rules": {
        "normal_panel_color_budget": "1-2 accent colors maximum",
        "experiment": "orange open markers or orange line",
        "theory": "deep cool blue line, no markers",
        "simulation": "light blue dashed line",
        "error": "rust only for bad/unwanted physics",
        "references": "slate grey, thin, visually secondary",
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
    """Return a lab-native Midnight Quantum colormap by role or explicit name."""

    name = COLORMAPS.get(role_or_name, role_or_name)
    if name not in QUANTUM_COLORMAP_COLORS:
        raise ValueError(f"Unknown Midnight Quantum colormap role: {role_or_name!r}")
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
            "axes.edgecolor": COLORS["text"],
            "axes.labelcolor": COLORS["text"],
            "axes.linewidth": LINEWIDTH["axis"],
            "xtick.color": COLORS["text"],
            "ytick.color": COLORS["text"],
            "text.color": COLORS["text"],
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
