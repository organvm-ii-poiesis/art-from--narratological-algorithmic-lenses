"""Lens renderer — applies visual transformations to narrative layouts.

A lens does not modify the underlying narrative model; it transforms
how the model's layout is rendered. The same model viewed through
different lenses produces different visual experiences.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Literal

from art_from_narratological_lenses.narrative_engine import (
    NarrativeVisualizationEngine,
    StagePosition,
)

LensType = Literal["chromatic", "topographic", "temporal", "relational"]

AVAILABLE_LENSES: tuple[LensType, ...] = ("chromatic", "topographic", "temporal", "relational")


@dataclass(frozen=True)
class LensParameters:
    """Configuration for a visual lens."""

    name: LensType
    description: str
    saturation_boost: float = 1.0
    opacity_base: float = 0.85
    stroke_weight: float = 1.5
    animation_duration: float = 3.0


LENS_CONFIGS: dict[LensType, LensParameters] = {
    "chromatic": LensParameters(
        name="chromatic",
        description="Maximizes color variation; structures distinguished by hue and saturation",
        saturation_boost=1.4,
        opacity_base=0.9,
    ),
    "topographic": LensParameters(
        name="topographic",
        description="Maps narrative tension to visual elevation with contour lines",
        saturation_boost=0.8,
        opacity_base=0.75,
        stroke_weight=2.0,
    ),
    "temporal": LensParameters(
        name="temporal",
        description="Animates the structure through time; duration and pacing become visible",
        animation_duration=5.0,
        opacity_base=0.6,
    ),
    "relational": LensParameters(
        name="relational",
        description="Emphasizes connections between stages with weighted edges",
        stroke_weight=3.0,
        opacity_base=0.7,
    ),
}


@dataclass
class LensRenderer:
    """Applies visual lenses to narrative structure layouts.

    A lens transforms the visual presentation of a narrative model
    without altering the model's data or layout positions.
    """

    engine: NarrativeVisualizationEngine | None = None

    def __post_init__(self) -> None:
        if self.engine is None:
            self.engine = NarrativeVisualizationEngine()

    def get_available_lenses(self) -> list[str]:
        """Return all available lens names."""
        return list(AVAILABLE_LENSES)

    def get_lens_config(self, lens_type: LensType) -> LensParameters:
        """Return configuration for a specific lens.

        Raises
        ------
        ValueError
            If *lens_type* is not a recognized lens.
        """
        if lens_type not in LENS_CONFIGS:
            raise ValueError(
                f"Unknown lens '{lens_type}'. Available: {', '.join(AVAILABLE_LENSES)}"
            )
        return LENS_CONFIGS[lens_type]

    def apply_lens(
        self, lens_type: LensType, positions: list[StagePosition]
    ) -> list[dict]:
        """Apply a visual lens to a set of stage positions.

        Returns a list of dictionaries enriched with lens-specific
        visual properties (adjusted opacity, stroke, animation, etc.).
        """
        config = self.get_lens_config(lens_type)
        transform_fn = {
            "chromatic": self._apply_chromatic,
            "topographic": self._apply_topographic,
            "temporal": self._apply_temporal,
            "relational": self._apply_relational,
        }
        fn = transform_fn[lens_type]
        return fn(positions, config)

    def render_with_lens(self, model_name: str, lens_type: LensType) -> str:
        """Render a narrative model through a specific lens as SVG."""
        assert self.engine is not None
        positions = self.engine.compute_layout(model_name)
        enriched = self.apply_lens(lens_type, positions)
        model = self.engine.get_model(model_name)

        g = ET.Element(
            "g",
            {
                "id": f"lens-{lens_type}-{model_name}",
                "class": f"lens-{lens_type}",
            },
        )

        # Draw connections
        config = self.get_lens_config(lens_type)
        for a, b in model.stage_connections:
            if a < len(enriched) and b < len(enriched):
                pa, pb = enriched[a], enriched[b]
                ET.SubElement(
                    g,
                    "line",
                    {
                        "x1": str(pa["x"]),
                        "y1": str(pa["y"]),
                        "x2": str(pb["x"]),
                        "y2": str(pb["y"]),
                        "stroke": pa.get("stroke_color", "#666"),
                        "stroke-width": str(config.stroke_weight),
                        "opacity": str(pa.get("connection_opacity", 0.4)),
                    },
                )

        # Draw stages
        for item in enriched:
            ET.SubElement(
                g,
                "circle",
                {
                    "cx": str(item["x"]),
                    "cy": str(item["y"]),
                    "r": str(item.get("radius", 20)),
                    "fill": item["color"],
                    "opacity": str(item.get("opacity", 0.85)),
                },
            )

        return ET.tostring(g, encoding="unicode")

    # ------------------------------------------------------------------ #
    # Lens implementations                                                #
    # ------------------------------------------------------------------ #

    def _apply_chromatic(
        self, positions: list[StagePosition], config: LensParameters
    ) -> list[dict]:
        """Chromatic lens: boost saturation and spread hues."""
        result = []
        n = len(positions)
        for i, pos in enumerate(positions):
            hue_shift = (360 * i / n) % 360
            result.append(
                {
                    "name": pos.name,
                    "x": pos.x,
                    "y": pos.y,
                    "radius": pos.radius * 1.1,
                    "color": pos.color,
                    "opacity": config.opacity_base,
                    "hue_shift": hue_shift,
                    "saturation_boost": config.saturation_boost,
                    "stroke_color": pos.color,
                    "connection_opacity": 0.3,
                    "lens": "chromatic",
                }
            )
        return result

    def _apply_topographic(
        self, positions: list[StagePosition], config: LensParameters
    ) -> list[dict]:
        """Topographic lens: map vertical position to elevation contours."""
        if not positions:
            return []
        min_y = min(p.y for p in positions)
        max_y = max(p.y for p in positions)
        y_range = max_y - min_y if max_y != min_y else 1.0
        result = []
        for pos in positions:
            elevation = 1.0 - (pos.y - min_y) / y_range  # Higher y = lower elevation
            result.append(
                {
                    "name": pos.name,
                    "x": pos.x,
                    "y": pos.y,
                    "radius": pos.radius * (0.8 + 0.4 * elevation),
                    "color": pos.color,
                    "opacity": config.opacity_base + 0.15 * elevation,
                    "elevation": round(elevation, 3),
                    "stroke_color": "#888",
                    "connection_opacity": 0.5,
                    "lens": "topographic",
                }
            )
        return result

    def _apply_temporal(
        self, positions: list[StagePosition], config: LensParameters
    ) -> list[dict]:
        """Temporal lens: assign animation delays based on sequence order."""
        n = len(positions)
        result = []
        for i, pos in enumerate(positions):
            delay = (config.animation_duration * i / n) if n > 0 else 0
            result.append(
                {
                    "name": pos.name,
                    "x": pos.x,
                    "y": pos.y,
                    "radius": pos.radius,
                    "color": pos.color,
                    "opacity": config.opacity_base + 0.3 * (i / n if n > 0 else 0),
                    "animation_delay": round(delay, 2),
                    "animation_duration": config.animation_duration,
                    "stroke_color": pos.color,
                    "connection_opacity": 0.2 + 0.3 * (i / n if n > 0 else 0),
                    "lens": "temporal",
                }
            )
        return result

    def _apply_relational(
        self, positions: list[StagePosition], config: LensParameters
    ) -> list[dict]:
        """Relational lens: shrink nodes, thicken connections."""
        result = []
        for pos in positions:
            result.append(
                {
                    "name": pos.name,
                    "x": pos.x,
                    "y": pos.y,
                    "radius": pos.radius * 0.7,  # Smaller nodes
                    "color": pos.color,
                    "opacity": config.opacity_base,
                    "stroke_color": pos.color,
                    "connection_opacity": 0.7,  # Thicker, more visible connections
                    "lens": "relational",
                }
            )
        return result
