# Quantum Ink v1

This is the lab graph identity, not just a safe plotting palette. The goal is a
recognizable visual language: precise, minimal, Journal-compatible, and clearly
connected across papers.

The graph taxonomy remains useful, but the house style is **Quantum Ink v1**:
deep ink-blue experimental data, warm amber theory, graphite references, dark
teal simulation only when needed, and oxide red only for unwanted physics.

## How to Run

```bash
python scripts/generate_data.py
python generate_graphs.py
```

Outputs:

- `data/lab_graph_examples.npz`: deterministic synthetic data.
- `data/metadata.json`: data-generation metadata.
- `figures/png/*.png`: one PNG per graph class.
- `figures/quantum_ink_taxonomy_one_page.pdf`: compact 30-panel taxonomy sheet.
- `figures/quantum_ink_templates_full_size.pdf`: one full-size template per page.

## Identity Object

```python
LAB_GRAPH_IDENTITY = {
    "name": "Quantum Ink",

    "fonts": {
        "text": "Libertinus Serif",
        "math": "Libertinus Math",
    },

    "colors": {
        "ink":        "#111318",
        "graphite":   "#5F646A",
        "reference":  "#A7A9AC",
        "mist":       "#D9DEE3",
        "exp":        "#0B4F71",
        "exp_light":  "#8CC7D8",
        "theory":     "#C48A00",
        "simulation": "#0A7A75",
        "error":      "#A33A2B",
    },

    "colormaps": {
        "positive": [
            "#071820",
            "#0B4F71",
            "#0A7A75",
            "#E2B84A",
        ],
        "signed": [
            "#A33A2B",
            "#F3EFE6",
            "#0B4F71",
        ],
        "phase": [
            "#0B4F71",
            "#0A7A75",
            "#C48A00",
            "#A33A2B",
            "#0B4F71",
        ],
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
```

## Visual Personality

Quantum Ink figures should feel:

- precise
- high-end
- quantum
- minimal
- slightly dark-toned
- not rainbow
- not generic Matplotlib
- not generic APS

Most panels should visually reduce to:

```text
ink axes
graphite references
deep blue experiment
warm amber theory
```

Teal and oxide red are special-use colors. A normal figure should not use the
whole palette.

## Semantic Colors

| Role | Color | Rule |
| --- | --- | --- |
| Experimental data | `#0B4F71` | Main measured data. |
| Secondary/control data | `#8CC7D8` | Only when needed. |
| Theory / fit | `#C48A00` | Analytical prediction or fitted model. |
| Simulation | `#0A7A75` | Only when simulation is explicitly present. |
| Error / loss / leakage | `#A33A2B` | Reserved for bad or unwanted physics. |
| Reference / inactive / guide | `#A7A9AC` | Never a main result. |
| Text / axes | `#111318` | Always consistent. |
| Light guides | `#D9DEE3` | Timing windows, grids, uncertainty edges. |

Do not add purple, magenta, bright cyan, bright yellow, rainbow maps, or random
categorical colors in ordinary figures.

## Experimental Data Grammar

Experimental data should normally use open ink-blue circles:

```python
marker = "o"
markersize = 3.8
markerfacecolor = "white"
markeredgecolor = LAB_COLORS["exp"]
color = LAB_COLORS["exp"]
```

Dense measured traces may use an ink-blue line. Error bars use the same ink-blue
stroke, thin lines, and small caps.

## Theory and Simulation Grammar

Theory or fit:

```python
color = LAB_COLORS["theory"]
linewidth = 1.25
linestyle = "-"
```

Simulation:

```python
color = LAB_COLORS["simulation"]
linewidth = 1.1
linestyle = "--"
```

References and extra curves should be graphite/reference grey, thin, and
visually secondary. Extra curves do not get new colors.

## Oxide Red Rule

Oxide red is sacred. Use it only for:

- loss
- heating
- leakage
- infidelity
- decay channel
- failure mode
- unwanted transition

Never use oxide red for an ordinary dataset.

## Lab-Native Colormaps

Use only the Quantum Ink colormap family.

Positive scalar data:

```python
QUANTUM_SEQ = ["#071820", "#0B4F71", "#0A7A75", "#E2B84A"]
```

Signed data:

```python
QUANTUM_DIV = ["#A33A2B", "#F3EFE6", "#0B4F71"]
```

Phase/cyclic data:

```python
QUANTUM_PHASE = ["#0B4F71", "#0A7A75", "#C48A00", "#A33A2B", "#0B4F71"]
```

Every continuous color encoding needs a colorbar with a label and units where
applicable.

## Allowed Color Uses

Color may mean only one of three things:

1. Physical role: experiment, theory, simulation, error, reference.
2. Continuous parameter: Quantum Ink colormap plus colorbar.
3. Scalar field value: Quantum Ink heatmap colormap plus colorbar.

Anything else is decorative and should be removed.

## Graph Taxonomy

The 30 supported classes are:

1. Single measured trace
2. Scatter / point plot
3. Data with error bars
4. Data plus fit / theory curve
5. Residual plot
6. Semi-log decay plot
7. Log-log scaling plot
8. Experiment / theory / simulation comparison
9. Multi-curve categorical plot
10. Gradient curve family
11. Diverging gradient curve family
12. Offset / waterfall plot
13. Envelope / uncertainty band plot
14. Small multiples / faceted panels
15. Time trace
16. Pulse sequence / control waveform plot
17. Spectrum line plot
18. Standard heatmap
19. Spectroscopy map
20. Phase diagram
21. Diverging heatmap
22. Phase / cyclic heatmap
23. Contour plot
24. Matrix heatmap
25. Wigner function / quasiprobability map
26. Histogram
27. Probability mass / state population bar chart
28. Grouped bar chart
29. Box / violin / swarm plot
30. Bloch-sphere / state-space plot

The taxonomy sheet is an index. The full-size PDF and PNG outputs are the usable
templates.

## Use It For Your Own Graph

For a new figure, start from the shared style module instead of redefining
colors inside the plotting script.

```python
import matplotlib.pyplot as plt

from lab_graph_style import COLORS, LINEWIDTH, MARKER_SIZE, apply_style, cmap

apply_style()
```

### Data Plus Fit

Use open ink-blue circles for measured data and an amber line for the fit or
theory curve.

```python
fig, ax = plt.subplots(figsize=(3.35, 2.45), constrained_layout=True)

ax.errorbar(
    x_data,
    y_data,
    yerr=y_err,
    fmt="o",
    color=COLORS["exp"],
    ecolor=COLORS["exp"],
    markerfacecolor="white",
    markeredgecolor=COLORS["exp"],
    markeredgewidth=0.8,
    markersize=MARKER_SIZE,
    elinewidth=LINEWIDTH["errorbar"],
    capsize=2,
    label="exp.",
)

ax.plot(x_fit, y_fit, color=COLORS["theory"], linewidth=1.25, label="fit")

ax.set_xlabel(r"Time ($\mu$s)")
ax.set_ylabel("Population")
ax.legend(frameon=False)
fig.savefig("my_figure.png", dpi=300, bbox_inches="tight")
```

### Experiment, Theory, Simulation

Use this grammar whenever all three are present:

```python
ax.plot(
    x_exp,
    y_exp,
    "o",
    color=COLORS["exp"],
    markerfacecolor="white",
    markeredgecolor=COLORS["exp"],
    label="exp.",
)
ax.plot(x_theory, y_theory, color=COLORS["theory"], label="theory")
ax.plot(x_sim, y_sim, color=COLORS["simulation"], linestyle="--", label="simulation")
```

Do not introduce a new color for a fourth ordinary curve. Use grey line styles
unless the new curve has a fixed semantic role.

### Many Curves With A Continuous Parameter

If color encodes a swept scalar parameter, use a Quantum Ink colormap and a
colorbar.

```python
import matplotlib as mpl

norm = mpl.colors.Normalize(vmin=drive.min(), vmax=drive.max())
cm = cmap("positive")

for value, y in zip(drive, curves):
    ax.plot(t, y, color=cm(norm(value)), linewidth=1.0)

sm = mpl.cm.ScalarMappable(norm=norm, cmap=cm)
cb = fig.colorbar(sm, ax=ax)
cb.set_label("Drive amplitude (a.u.)")
```

For signed sweeps, use `cmap("signed")` with `TwoSlopeNorm(vcenter=0)`. For
phase sweeps, use `cmap("phase")`.

### Heatmaps

Use a lab-native colormap based on the data type:

```python
im = ax.imshow(
    z,
    origin="lower",
    aspect="auto",
    extent=[x.min(), x.max(), y.min(), y.max()],
    cmap=cmap("positive"),
)
cb = fig.colorbar(im, ax=ax)
cb.set_label("Population")
```

For signed data:

```python
lim = abs(z).max()
im = ax.imshow(
    z,
    origin="lower",
    cmap=cmap("signed"),
    vmin=-lim,
    vmax=lim,
)
cb = fig.colorbar(im, ax=ax)
cb.set_label("Residual")
```

For phase:

```python
im = ax.imshow(phase, origin="lower", cmap=cmap("phase"), vmin=-3.14159, vmax=3.14159)
cb = fig.colorbar(im, ax=ax)
cb.set_label("Phase")
```

### Bars And Distributions

State populations and measured discrete outcomes use blue bars. Theory should
be an amber marker or outline, not a second decorative fill.

```python
ax.bar(states, population, color=COLORS["exp"], label="exp.")
ax.plot(states, theory_population, "o", color=COLORS["theory"], label="theory")
```

Distribution plots should stay restrained:

```python
parts = ax.violinplot(groups, showmedians=True)
for body in parts["bodies"]:
    body.set_facecolor(COLORS["exp_light"])
    body.set_edgecolor(COLORS["exp"])
    body.set_alpha(0.35)
```

### Figure Size

Use journal-like sizes by default:

```python
single_column = (3.35, 2.45)
double_column = (6.8, 3.0)
fig, ax = plt.subplots(figsize=single_column, constrained_layout=True)
```

Before exporting, check that tick labels, axis labels, legends, and colorbars are
still readable at the final printed size.

## Hard Rules

1. Most panels use only one or two accent colors.
2. Deep blue always means experimental data.
3. Amber always means theory or fit.
4. Dark teal means simulation only.
5. Oxide red is reserved for loss, leakage, heating, error, or failure.
6. Graphite/reference grey is for background, inactive curves, and guides.
7. Continuous gradients always need a colorbar.
8. Heatmaps always use the lab-native colormaps.
9. Categorical rainbow plots are forbidden.
10. Color is never decorative.
