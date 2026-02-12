# art-from--narratological-algorithmic-lenses

**Interactive web experience exploring narrative structures via visual algorithmic lenses**

[![CI](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ORGAN-II](https://img.shields.io/badge/ORGAN-II-poiesis-purple)](https://github.com/organvm-ii-poiesis)

> *Every story has a shape. The hero's journey curves like a parabola. The kishōtenketsu unfolds in four discrete panels. Ring composition folds narrative back upon itself like a palindrome. What if you could see these shapes — not as diagrams in a textbook, but as living visual structures that breathe, transform, and invite exploration?*

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
│       └── lens_renderer.py         # LensRenderer for visual transformations
├── tests/
│   └── test_narrative_engine.py     # Test suite (10+ tests)
├── pyproject.toml                   # Package configuration
├── LICENSE                          # MIT License
├── README.md                        # This document
└── .github/
    └── workflows/
        └── ci.yml                   # Continuous integration
```

### Component Responsibilities

- **`NarrativeVisualizationEngine`**: The core engine that models narrative structures as data objects and maps them to visual layouts. Each narrative structure (hero's journey, kishōtenketsu, ring composition, Freytag's pyramid, three-act, in medias res) is represented as a `NarrativeModel` with named stages, spatial coordinates, and visual properties. The engine provides methods to instantiate models, compute layouts, and prepare data for rendering.

- **`LensRenderer`**: Takes the output of the engine and applies visual transformations — color mapping, opacity gradients, animation parameters, geometric distortions. The lens metaphor is implemented here: the same narrative data looks different when passed through different rendering lenses (chromatic, topographic, temporal, relational).

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Core modeling | Python dataclasses | Clean, typed representations of narrative structures |
| Visual rendering | SVG generation | Programmatic control, scalable vector output |
| Client-side interaction | D3.js (via CDN) | Standard for interactive data visualization |
| Server | Flask | Lightweight Python web framework |
| Static export | matplotlib | Publication-quality still images |

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

### Interactive Web Experience

```bash
# Start the development server
python -m art_from_narratological_lenses.lens_renderer

# Open http://localhost:5000 in your browser
```

The web interface presents a split view: narrative structures on the left (selectable), the visualization canvas on the right. Apply different lenses using the toolbar. Load sample texts or paste your own to see how the chosen narrative structure and lens transform the content into a visual composition.

### Programmatic Use

```python
from art_from_narratological_lenses.narrative_engine import NarrativeVisualizationEngine

engine = NarrativeVisualizationEngine(width=1400, height=900)

# Get a specific narrative model
heros_journey = engine.get_model("heros_journey")
print(heros_journey.stages)  # ['ordinary_world', 'call_to_adventure', ...]

# Compute the visual layout for a narrative structure
layout = engine.compute_layout("heros_journey")

# Render as SVG
svg = engine.render_model("heros_journey")

# Render all models side by side
comparison_svg = engine.render_comparison(["heros_journey", "kishotenketsu", "ring_composition"])

# Export data for D3.js consumption
json_data = engine.to_json("heros_journey")
```

### Applying Lenses

```python
from art_from_narratological_lenses.lens_renderer import LensRenderer

renderer = LensRenderer()

# Apply different visual lenses to the same structure
chromatic = renderer.apply_lens("chromatic", layout)    # Color-dominated
topographic = renderer.apply_lens("topographic", layout)  # Elevation-based
temporal = renderer.apply_lens("temporal", layout)      # Time-focused animation
relational = renderer.apply_lens("relational", layout)  # Connection-emphasis
```

## Visual Design

### Color Palettes by Narrative Structure

Each narrative structure has a dedicated color palette derived from its cultural and theoretical context:

| Structure | Primary | Secondary | Accent | Cultural Reference |
|-----------|---------|-----------|--------|-------------------|
| Hero's Journey | Warm gold (#c9a227) | Deep earth (#5c3d2e) | Celestial blue (#2d5aa0) | Campbell's solar mythology |
| Kishōtenketsu | Ink black (#1a1a1a) | Rice white (#f5f0e8) | Vermillion (#d4453b) | Japanese woodblock prints |
| Ring Composition | Royal purple (#4a1d6b) | Mirror silver (#c0c0c0) | Fold gold (#b8860b) | Byzantine manuscript illumination |
| Freytag's Pyramid | Storm grey (#4a4a5a) | Rising red (#cc3333) | Falling blue (#3366cc) | German dramatic theory |
| Three-Act Structure | Act I green (#2d8244) | Act II amber (#d4a017) | Act III crimson (#8b1a1a) | Hollywood screenplay convention |
| In Medias Res | Disorientation violet (#7b4bb3) | Flashback sepia (#a0845c) | Present cyan (#00a8b5) | Epic oral tradition |

### Animation Philosophy

Animations in this project are not decorative — they are **semantic**. Every motion communicates something about the narrative structure it represents:

- The hero's journey rotates because it is a cycle
- Kishōtenketsu's twist panel vibrates because it disrupts
- Ring composition pulses symmetrically because it mirrors
- Freytag's pyramid breathes (rises and falls) because it has a climax
- Three-act structure slides horizontally because it progresses linearly
- In medias res stutters because it begins in confusion

### Lens Visual Effects

Each lens transforms the same data differently:

- **Chromatic lens**: Maximizes color variation; structures are distinguished primarily by hue and saturation
- **Topographic lens**: Maps narrative tension to visual elevation; uses contour lines and relief shading
- **Temporal lens**: Animates the structure through time; duration and pacing become visible
- **Relational lens**: Emphasizes connections between narrative stages; uses network-like layouts with weighted edges

## How It Works

### Narrative Models

The `NarrativeVisualizationEngine` internally represents each narrative structure as a `NarrativeModel` dataclass:

```python
NarrativeModel(
    name="heros_journey",
    display_name="The Hero's Journey",
    stages=["ordinary_world", "call_to_adventure", "refusal", "meeting_mentor",
            "crossing_threshold", "tests_allies_enemies", "approach_inmost_cave",
            "ordeal", "reward", "road_back", "resurrection", "return_with_elixir"],
    layout_type="circular",
    palette=Palette(primary="#c9a227", secondary="#5c3d2e", accent="#2d5aa0"),
    stage_connections=[(0, 11), (1, 2), ...],  # Adjacency for visual connections
)
```

### Layout Computation

The `compute_layout()` method converts a narrative model's stages into positioned visual elements:

- **Circular** (hero's journey): Stages distributed evenly around a circle; departure stages in the upper hemisphere, return stages in the lower
- **Grid** (kishōtenketsu): 2x2 grid with each cell proportioned to reflect the stage's narrative weight
- **Concentric** (ring composition): Stages arranged as concentric rings; outermost and innermost rings mirror each other
- **Triangular** (Freytag's pyramid): Stages positioned along a rising-then-falling path
- **Linear** (three-act structure): Stages arranged left-to-right with proportional spacing
- **Scattered** (in medias res): Initial positions are deliberately scrambled; animation reveals the chronological reordering

### Lens Application

The `LensRenderer.apply_lens()` method takes a computed layout and applies a visual transformation without modifying the underlying data. This separation of data and presentation is architecturally important — it means the same narrative model can be rendered through multiple lenses simultaneously for comparison.

## Contributing

Contributions are welcome in the following areas:

- **New narrative structures**: Rasa theory, Propp's 31 functions, Todorov's equilibrium model, Barthes' five codes
- **New lenses**: Spatial-audio lens (sonification), haptic lens (vibration patterns for accessibility), semantic-zoom lens
- **Accessibility**: Screen reader descriptions of visual narrative structures; keyboard navigation
- **Corpus integration**: Connecting to real texts (Project Gutenberg, etc.) for live narrative analysis

### Development Setup

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Code Style

PEP 8 with type hints. Use `ruff` for linting:

```bash
ruff check src/ tests/
```

## Related Projects

- [`narratological-algorithmic-lenses`](https://github.com/organvm-i-theoria/narratological-algorithmic-lenses) — The ORGAN-I theoretical source that this project visualizes
- [`metasystem-master`](https://github.com/organvm-ii-poiesis/metasystem-master) — The ORGAN-II flagship generative art system
- [`art-from--auto-revision-epistemic-engine`](https://github.com/organvm-ii-poiesis/art-from--auto-revision-epistemic-engine) — Sibling ORGAN-II project visualizing governance structures

## License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2026 organvm-ii-poiesis

---

*Part of the [organvm](https://github.com/meta-organvm) eight-organ creative-institutional system. ORGAN-II transforms theory into art.*
