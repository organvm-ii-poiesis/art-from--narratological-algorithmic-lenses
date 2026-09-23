# art-from--narratological-algorithmic-lenses

**Interactive web experience exploring narrative structures via visual algorithmic lenses**

[![Live Demo](https://img.shields.io/badge/Live_Demo-GitHub_Pages-blue.svg)](https://organvm-ii-poiesis.github.io/art-from--narratological-algorithmic-lenses/)
[![CI](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/ci.yml)
[![Deploy](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/deploy.yml/badge.svg)](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ORGAN-II](https://img.shields.io/badge/ORGAN-II-poiesis-purple)](https://github.com/organvm-ii-poiesis)

> *Every story has a shape. The hero's journey curves like a parabola. The kishōtenketsu unfolds in four discrete panels. Ring composition folds narrative back upon itself like a palindrome. What if you could see these shapes — not as diagrams in a textbook, but as living visual structures that breathe, transform, and invite exploration?*

**Hosted Live Experience**: [https://organvm-ii-poiesis.github.io/art-from--narratological-algorithmic-lenses/](https://organvm-ii-poiesis.github.io/art-from--narratological-algorithmic-lenses/)

---

## Overview

`art-from--narratological-algorithmic-lenses` is an interactive web experience that transforms narrative structures from literary theory into visual algorithmic compositions. It takes the theoretical frameworks catalogued in [narratological-algorithmic-lenses](https://github.com/organvm-i-theoria/narratological-algorithmic-lenses) (ORGAN-I) and renders them as explorable, animated visual artworks.

Where the ORGAN-I source repository treats narrative structures as objects of formal analysis — classifying them, comparing them, extracting algorithmic patterns — this ORGAN-II project treats those same structures as raw material for art. The classification becomes a color palette. The comparison becomes a composition. The algorithm becomes an animation.

This project demonstrates a core principle of the organvm system: that the same intellectual structure can be simultaneously a theoretical object (in ORGAN-I) and an aesthetic object (in ORGAN-II), and that the translation between these modes is itself a creative act worthy of study and exhibition.

### Position Within the ORGAN System

| Layer | Role |
|-------|------|
| **ORGAN-I** (Theoria) | Provides formal models of narrative structures — the hero's journey, kishōtenketsu, ring composition, and others — as algorithmic specifications |
| **ORGAN-II** (Poiesis) | **This repository** — transforms those formal models into interactive visual experiences |
| **ORGAN-V** (Logos) | Documents the artistic process through public-process essays |

The dependency is strictly unidirectional: this project reads from ORGAN-I's narrative models and produces visual output. It never modifies the models it visualizes.

## Concept

### Narrative as Visual Architecture

Literary theorists have long understood that narratives possess spatial qualities. Aristotle's three-act structure implies a rising and falling topology. Joseph Campbell's monomyth traces a circular path through departure, initiation, and return. The Japanese kishōtenketsu — introduction, development, twist, reconciliation — arranges four discrete moments in a grid-like pattern.

These spatial metaphors are usually confined to textbook diagrams: arrows, boxes, dotted lines. This project takes the metaphors literally and renders them as full visual environments:

| Narrative Structure | Visual Mapping | Interaction Mode |
|---|---|---|
| **Hero's Journey** (Campbell) | Circular orbit with 12 waypoints; departures diverge outward, returns converge inward | Click waypoints to expand story beats; drag to reorient the circle |
| **Kishōtenketsu** | Four-panel grid with distinct color temperatures; the twist panel vibrates at a different frequency | Hover panels to see how the twist disrupts the visual harmony |
| **Ring Composition** (Douglas) | Concentric rings where outer narrative frames mirror inner content; palindromic symmetry is literal visual symmetry | Collapse/expand rings to see the mirroring structure |
| **Freytag's Pyramid** | Rising/falling topographic surface with dramatic tension mapped to elevation | Scrub a timeline to watch the surface deform in real time |
| **Three-Act Structure** | Triptych — three vertical columns with proportional width (25%-50%-25%) reflecting act duration | Resize columns to explore how pacing affects visual balance |
| **In Medias Res** | The visualization starts mid-animation; scrubbing backward reveals the temporal inversion | The initial state is deliberately disorienting — the user must discover chronological order |

### The Lens Metaphor

The project title uses the word *lenses* deliberately. Each narrative structure is not merely displayed — it is applied as a transformational lens to sample texts. A lens is something you look *through*, not *at*. The same sample text (configurable by the user or drawn from a built-in corpus) looks radically different when viewed through the hero's journey lens versus the kishōtenketsu lens versus the ring composition lens.

This is the core interactive conceit: the user does not passively observe narrative structures. The user applies them as perceptual filters and experiences how the choice of narrative framework changes what is visible, what is emphasized, and what disappears. The artistic claim embedded in this interaction is that **narrative structure is not discovered in texts — it is projected onto them**. The lens metaphor makes this epistemological claim visceral.

### Art-Theoretical Grounding

The project engages with several traditions in computational and conceptual art:

1. **Oulipo and constrained writing** (Queneau, Perec): Literature generated by formal constraints. Here, the constraints are narrative structures, and the generation is visual rather than textual.
2. **Data visualization as narrative** (Segel & Heer): Research on how visual representations tell stories. This project inverts the question — how do stories become visual representations?
3. **Interactive fiction and ergodic literature** (Aarseth): Texts that require nontrivial effort to traverse. The interactive visualizations in this project are ergodic artworks — the viewer must navigate, click, scrub, and explore to experience them fully.
4. **Computational narratology** (Mani, Meister): The algorithmic formalization of narrative theory. This project takes computational narratology's formalisms and renders them as aesthetic objects.

## Architecture

```
art-from--narratological-algorithmic-lenses/
├── src/
│   └── art_from_narratological_lenses/
│       ├── __init__.py              # Package metadata and version
│       ├── narrative_engine.py      # Core NarrativeVisualizationEngine
│       ├── lens_renderer.py         # LensRenderer for visual transformations
│       ├── app.py                   # Flask interactive server & REST API
│       └── build_site.py            # Static site generator for GitHub Pages
├── tests/
│   ├── test_narrative_engine.py     # Core engine and lens test suite
│   ├── test_app.py                  # Flask web route and API test suite
│   └── test_smoke.py                # Deployment bundle smoke tests
├── dist/                            # Generated web deployment bundle
├── pyproject.toml                   # Package configuration & CLI entrypoints
├── LICENSE                          # MIT License
├── README.md                        # This document
└── .github/
    └── workflows/
        ├── ci.yml                   # CI pipeline
        └── deploy.yml               # GitHub Pages deployment pipeline
```

### Component Responsibilities

- **`NarrativeVisualizationEngine`**: The core engine that models narrative structures as data objects and maps them to visual layouts. Each narrative structure (hero's journey, kishōtenketsu, ring composition, Freytag's pyramid, three-act, in medias res) is represented as a `NarrativeModel` with named stages, spatial coordinates, and visual properties.

- **`LensRenderer`**: Takes the output of the engine and applies visual transformations — color mapping, opacity gradients, animation parameters, geometric distortions.

- **`app.py`**: Flask web application server providing interactive web UI and API endpoints (`/api/models`, `/api/model/<name>`, `/api/render/<name>/<lens>`, `/api/transform`, `/health`).

- **`build_site.py`**: Static website bundler generating `dist/` web deployment assets for GitHub Pages deployment.

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Core modeling | Python dataclasses | Clean, typed representations of narrative structures |
| Visual rendering | SVG generation | Programmatic control, scalable vector output |
| Web Application | Flask & Single Page UI | Lightweight Python web framework and responsive UI |
| Static Deployment | GitHub Pages | Zero-maintenance hosted public reachability |

## Installation

### Prerequisites

- Python 3.10 or later
- pip (bundled with Python)

### Setup

```bash
# Clone the repository
git clone https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses.git
cd art-from--narratological-algorithmic-lenses

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "from art_from_narratological_lenses.narrative_engine import NarrativeVisualizationEngine; print('OK')"
```

## Usage

### Interactive Web Experience (Local Server)

```bash
# Start the interactive web server
python -m art_from_narratological_lenses.app

# Or use the installed CLI command
art-lenses

# Open http://localhost:5000 in your browser
```

Check server health at `http://localhost:5000/health`.

### Building Static Deployment Bundle

```bash
# Generate static web bundle in dist/
python -m art_from_narratological_lenses.build_site
```

The output in `dist/` is automatically deployed to [GitHub Pages](https://organvm-ii-poiesis.github.io/art-from--narratological-algorithmic-lenses/) via `.github/workflows/deploy.yml`.

### Programmatic Use

```python
from art_from_narratological_lenses.narrative_engine import NarrativeVisualizationEngine

engine = NarrativeVisualizationEngine(width=1400, height=900)

# Get a specific narrative model
heros_journey = engine.get_model("heros_journey")
print(heros_journey.stages)

# Compute layout and render SVG
layout = engine.compute_layout("heros_journey")
svg = engine.render_model("heros_journey")
```

### Applying Lenses Programmatically

```python
from art_from_narratological_lenses.lens_renderer import LensRenderer

renderer = LensRenderer()

# Apply different visual lenses to the layout
chromatic = renderer.apply_lens("chromatic", layout)
topographic = renderer.apply_lens("topographic", layout)
```

## Verification & Smoke Checks

Run the automated test suite and deployment smoke checks:

```bash
python -m pytest -v
```

This validates all core narrative engine models, lens rendering transformations, Flask API routes, static site builder bundle integrity, and SVG XML schema validity.

## Visual Design

### Color Palettes by Narrative Structure

| Structure | Primary | Secondary | Accent | Cultural Reference |
|-----------|---------|-----------|--------|-------------------|
| Hero's Journey | Warm gold (#c9a227) | Deep earth (#5c3d2e) | Celestial blue (#2d5aa0) | Campbell's solar mythology |
| Kishōtenketsu | Ink black (#1a1a1a) | Rice white (#f5f0e8) | Vermillion (#d4453b) | Japanese woodblock prints |
| Ring Composition | Royal purple (#4a1d6b) | Mirror silver (#c0c0c0) | Fold gold (#b8860b) | Byzantine manuscript illumination |
| Freytag's Pyramid | Storm grey (#4a4a5a) | Rising red (#cc3333) | Falling blue (#3366cc) | German dramatic theory |
| Three-Act Structure | Act I green (#2d8244) | Act II amber (#d4a017) | Act III crimson (#8b1a1a) | Hollywood screenplay convention |
| In Medias Res | Disorientation violet (#7b4bb3) | Flashback sepia (#a0845c) | Present cyan (#00a8b5) | Epic oral tradition |

## License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2026 organvm-ii-poiesis

---

*Part of the [organvm](https://github.com/meta-organvm) eight-organ creative-institutional system. ORGAN-II transforms theory into art.*
