"""Core narrative visualization engine.

Models narrative structures (hero's journey, kishōtenketsu, ring composition,
Freytag's pyramid, three-act structure, in medias res) as data objects and
maps them to visual layouts for SVG rendering.
"""

from __future__ import annotations

import json
import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Palette:
    """Color palette for a narrative structure."""

    primary: str
    secondary: str
    accent: str


@dataclass(frozen=True)
class StagePosition:
    """Computed position for a narrative stage."""

    name: str
    x: float
    y: float
    radius: float = 20.0
    color: str = "#ffffff"
    label: str = ""


@dataclass(frozen=True)
class NarrativeModel:
    """Formal model of a narrative structure."""

    name: str
    display_name: str
    stages: tuple[str, ...]
    layout_type: str
    palette: Palette
    stage_connections: tuple[tuple[int, int], ...] = ()
    description: str = ""


# ------------------------------------------------------------------ #
# Canonical narrative models                                          #
# ------------------------------------------------------------------ #

NARRATIVE_MODELS: dict[str, NarrativeModel] = {
    "heros_journey": NarrativeModel(
        name="heros_journey",
        display_name="The Hero's Journey",
        stages=(
            "ordinary_world",
            "call_to_adventure",
            "refusal_of_the_call",
            "meeting_the_mentor",
            "crossing_the_threshold",
            "tests_allies_enemies",
            "approach_inmost_cave",
            "ordeal",
            "reward",
            "the_road_back",
            "resurrection",
            "return_with_elixir",
        ),
        layout_type="circular",
        palette=Palette(primary="#c9a227", secondary="#5c3d2e", accent="#2d5aa0"),
        stage_connections=tuple((i, (i + 1) % 12) for i in range(12)),
        description="Campbell's monomyth — a circular journey of departure, initiation, and return",
    ),
    "kishotenketsu": NarrativeModel(
        name="kishotenketsu",
        display_name="Kishōtenketsu",
        stages=("ki_introduction", "sho_development", "ten_twist", "ketsu_reconciliation"),
        layout_type="grid",
        palette=Palette(primary="#1a1a1a", secondary="#f5f0e8", accent="#d4453b"),
        stage_connections=((0, 1), (1, 2), (2, 3)),
        description="Four-act structure without conflict — introduction, development, twist, reconciliation",
    ),
    "ring_composition": NarrativeModel(
        name="ring_composition",
        display_name="Ring Composition",
        stages=(
            "opening_frame",
            "first_elaboration",
            "deepening",
            "central_pivot",
            "mirror_deepening",
            "mirror_elaboration",
            "closing_frame",
        ),
        layout_type="concentric",
        palette=Palette(primary="#4a1d6b", secondary="#c0c0c0", accent="#b8860b"),
        stage_connections=((0, 6), (1, 5), (2, 4)),
        description="Palindromic narrative where the ending mirrors the beginning",
    ),
    "freytags_pyramid": NarrativeModel(
        name="freytags_pyramid",
        display_name="Freytag's Pyramid",
        stages=(
            "exposition",
            "rising_action",
            "climax",
            "falling_action",
            "denouement",
        ),
        layout_type="triangular",
        palette=Palette(primary="#4a4a5a", secondary="#cc3333", accent="#3366cc"),
        stage_connections=((0, 1), (1, 2), (2, 3), (3, 4)),
        description="Five-act dramatic structure with rising tension, climax, and resolution",
    ),
    "three_act": NarrativeModel(
        name="three_act",
        display_name="Three-Act Structure",
        stages=("act_i_setup", "act_ii_confrontation", "act_iii_resolution"),
        layout_type="linear",
        palette=Palette(primary="#2d8244", secondary="#d4a017", accent="#8b1a1a"),
        stage_connections=((0, 1), (1, 2)),
        description="Classical dramatic structure — setup, confrontation, resolution",
    ),
    "in_medias_res": NarrativeModel(
        name="in_medias_res",
        display_name="In Medias Res",
        stages=(
            "mid_action_opening",
            "flashback_origin",
            "flashback_development",
            "return_to_present",
            "continuation",
            "resolution",
        ),
        layout_type="scattered",
        palette=Palette(primary="#7b4bb3", secondary="#a0845c", accent="#00a8b5"),
        stage_connections=((0, 3), (1, 2), (2, 3), (3, 4), (4, 5)),
        description="Beginning in the middle of the action — temporal displacement as narrative device",
    ),
}

MODEL_NAMES: tuple[str, ...] = tuple(NARRATIVE_MODELS.keys())


@dataclass
class NarrativeVisualizationEngine:
    """Maps narrative structures to visual layouts and SVG output.

    Parameters
    ----------
    width : int
        Canvas width in SVG viewBox units.
    height : int
        Canvas height in SVG viewBox units.
    background : str
        Background fill color.
    """

    width: int = 1400
    height: int = 900
    background: str = "#0d1117"

    # ------------------------------------------------------------------ #
    # Public API                                                          #
    # ------------------------------------------------------------------ #

    def get_model(self, name: str) -> NarrativeModel:
        """Return a narrative model by name.

        Raises
        ------
        ValueError
            If *name* is not a recognized narrative structure.
        """
        if name not in NARRATIVE_MODELS:
            raise ValueError(
                f"Unknown narrative model '{name}'. "
                f"Valid models: {', '.join(MODEL_NAMES)}"
            )
        return NARRATIVE_MODELS[name]

    def list_models(self) -> list[str]:
        """Return the names of all available narrative models."""
        return list(MODEL_NAMES)

    def get_model_count(self) -> int:
        """Return the number of available narrative models."""
        return len(NARRATIVE_MODELS)

    def compute_layout(self, name: str) -> list[StagePosition]:
        """Compute positioned stage elements for a narrative structure."""
        model = self.get_model(name)
        layout_fn = {
            "circular": self._layout_circular,
            "grid": self._layout_grid,
            "concentric": self._layout_concentric,
            "triangular": self._layout_triangular,
            "linear": self._layout_linear,
            "scattered": self._layout_scattered,
        }
        fn = layout_fn.get(model.layout_type)
        if fn is None:
            raise ValueError(f"Unknown layout type: {model.layout_type}")
        return fn(model)

    def render_model(self, name: str) -> str:
        """Render a single narrative structure as an SVG fragment."""
        model = self.get_model(name)
        positions = self.compute_layout(name)
        g = ET.Element("g", {"id": f"narrative-{name}", "class": "narrative-model"})

        # Draw connections first (behind nodes)
        for a, b in model.stage_connections:
            if a < len(positions) and b < len(positions):
                pa, pb = positions[a], positions[b]
                ET.SubElement(
                    g,
                    "line",
                    {
                        "x1": str(pa.x),
                        "y1": str(pa.y),
                        "x2": str(pb.x),
                        "y2": str(pb.y),
                        "stroke": model.palette.secondary,
                        "stroke-width": "1.5",
                        "opacity": "0.5",
                    },
                )

        # Draw stage nodes
        for pos in positions:
            ET.SubElement(
                g,
                "circle",
                {
                    "cx": str(pos.x),
                    "cy": str(pos.y),
                    "r": str(pos.radius),
                    "fill": pos.color,
                    "opacity": "0.85",
                },
            )
            label = ET.SubElement(
                g,
                "text",
                {
                    "x": str(pos.x),
                    "y": str(pos.y + pos.radius + 14),
                    "text-anchor": "middle",
                    "fill": "#c9d1d9",
                    "font-size": "9",
                    "font-family": "Inter, sans-serif",
                },
            )
            label.text = pos.label or pos.name.replace("_", " ")

        return ET.tostring(g, encoding="unicode")

    def render_comparison(self, names: list[str]) -> str:
        """Render multiple narrative structures side by side."""
        n = len(names)
        if n == 0:
            raise ValueError("At least one model name is required")

        col_width = self.width / n
        root = ET.Element("g", {"id": "comparison"})

        for i, name in enumerate(names):
            model = self.get_model(name)
            sub_engine = NarrativeVisualizationEngine(
                width=int(col_width),
                height=self.height,
                background=self.background,
            )
            svg_fragment = sub_engine.render_model(name)
            group = ET.fromstring(svg_fragment)
            group.set("transform", f"translate({int(i * col_width)}, 0)")
            root.append(group)

        return ET.tostring(root, encoding="unicode")

    def to_json(self, name: str) -> str:
        """Export a narrative model and its layout as JSON for D3.js."""
        model = self.get_model(name)
        positions = self.compute_layout(name)
        data = {
            "name": model.name,
            "display_name": model.display_name,
            "layout_type": model.layout_type,
            "palette": {
                "primary": model.palette.primary,
                "secondary": model.palette.secondary,
                "accent": model.palette.accent,
            },
            "stages": [
                {"name": p.name, "x": round(p.x, 1), "y": round(p.y, 1), "color": p.color}
                for p in positions
            ],
            "connections": [{"source": a, "target": b} for a, b in model.stage_connections],
        }
        return json.dumps(data, indent=2)

    def generate_svg(self, name: str) -> str:
        """Generate a complete standalone SVG document for one narrative model."""
        svg = ET.Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": f"0 0 {self.width} {self.height}",
                "width": str(self.width),
                "height": str(self.height),
            },
        )
        ET.SubElement(
            svg,
            "rect",
            {
                "width": str(self.width),
                "height": str(self.height),
                "fill": self.background,
            },
        )
        title = ET.SubElement(svg, "title")
        model = self.get_model(name)
        title.text = f"Narrative Visualization — {model.display_name}"

        fragment = ET.fromstring(self.render_model(name))
        svg.append(fragment)

        return ET.tostring(svg, encoding="unicode", xml_declaration=True)

    # ------------------------------------------------------------------ #
    # Layout algorithms                                                   #
    # ------------------------------------------------------------------ #

    def _layout_circular(self, model: NarrativeModel) -> list[StagePosition]:
        """Distribute stages evenly around a circle."""
        cx, cy = self.width / 2, self.height / 2
        radius = min(self.width, self.height) * 0.35
        n = len(model.stages)
        positions = []
        for i, stage in enumerate(model.stages):
            angle = (2 * math.pi * i / n) - math.pi / 2  # Start at top
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            color = model.palette.primary if i < n // 2 else model.palette.accent
            positions.append(StagePosition(name=stage, x=x, y=y, color=color))
        return positions

    def _layout_grid(self, model: NarrativeModel) -> list[StagePosition]:
        """Arrange stages in a 2x2 grid."""
        positions = []
        grid_coords = [(0, 0), (1, 0), (0, 1), (1, 1)]
        cell_w = self.width / 3
        cell_h = self.height / 3
        for i, stage in enumerate(model.stages):
            col, row = grid_coords[i] if i < 4 else (i % 2, i // 2)
            x = cell_w + col * cell_w
            y = cell_h + row * cell_h
            # The twist (ten) gets the accent color
            color = model.palette.accent if i == 2 else model.palette.primary
            positions.append(StagePosition(name=stage, x=x, y=y, radius=30, color=color))
        return positions

    def _layout_concentric(self, model: NarrativeModel) -> list[StagePosition]:
        """Arrange stages as concentric rings."""
        cx, cy = self.width / 2, self.height / 2
        n = len(model.stages)
        max_radius = min(self.width, self.height) * 0.4
        positions = []
        for i, stage in enumerate(model.stages):
            # Distance from center: outermost for first/last, innermost for middle
            distance_from_center = abs(i - n // 2)
            r = max_radius * (distance_from_center + 1) / (n // 2 + 1)
            angle = math.pi / 2 if i <= n // 2 else -math.pi / 2
            x = cx + r * math.cos(angle + i * 0.3)
            y = cy + r * math.sin(angle + i * 0.3)
            color = model.palette.accent if i == n // 2 else model.palette.primary
            positions.append(StagePosition(name=stage, x=x, y=y, color=color))
        return positions

    def _layout_triangular(self, model: NarrativeModel) -> list[StagePosition]:
        """Position stages along a rising-then-falling path (pyramid)."""
        n = len(model.stages)
        positions = []
        margin = self.width * 0.1
        usable_w = self.width - 2 * margin
        peak_y = self.height * 0.2
        base_y = self.height * 0.75
        climax_idx = n // 2
        for i, stage in enumerate(model.stages):
            x = margin + (usable_w * i / (n - 1)) if n > 1 else self.width / 2
            # Compute y: rises to climax, then falls
            if i <= climax_idx:
                progress = i / climax_idx if climax_idx > 0 else 0
                y = base_y - (base_y - peak_y) * progress
            else:
                progress = (i - climax_idx) / (n - 1 - climax_idx) if (n - 1 - climax_idx) > 0 else 0
                y = peak_y + (base_y - peak_y) * progress
            color = model.palette.secondary if i == climax_idx else model.palette.primary
            positions.append(StagePosition(name=stage, x=x, y=y, color=color))
        return positions

    def _layout_linear(self, model: NarrativeModel) -> list[StagePosition]:
        """Arrange stages left to right with proportional spacing."""
        n = len(model.stages)
        margin = self.width * 0.1
        usable_w = self.width - 2 * margin
        cy = self.height / 2
        colors = [model.palette.primary, model.palette.secondary, model.palette.accent]
        positions = []
        for i, stage in enumerate(model.stages):
            x = margin + (usable_w * i / (n - 1)) if n > 1 else self.width / 2
            color = colors[i % len(colors)]
            positions.append(StagePosition(name=stage, x=x, y=cy, radius=35, color=color))
        return positions

    def _layout_scattered(self, model: NarrativeModel) -> list[StagePosition]:
        """Deliberately scatter stages to represent temporal displacement."""
        n = len(model.stages)
        positions = []
        # Use a deterministic but non-sequential scatter pattern
        scatter_offsets = [
            (0.6, 0.3),   # mid_action_opening — center-right
            (0.15, 0.7),  # flashback_origin — bottom-left
            (0.35, 0.55), # flashback_development — center-left-low
            (0.65, 0.5),  # return_to_present — center-right
            (0.8, 0.4),   # continuation — right
            (0.5, 0.2),   # resolution — top-center
        ]
        for i, stage in enumerate(model.stages):
            ox, oy = scatter_offsets[i] if i < len(scatter_offsets) else (0.5, 0.5)
            x = self.width * ox
            y = self.height * oy
            color = model.palette.accent if i == 0 else model.palette.primary
            positions.append(StagePosition(name=stage, x=x, y=y, color=color))
        return positions
