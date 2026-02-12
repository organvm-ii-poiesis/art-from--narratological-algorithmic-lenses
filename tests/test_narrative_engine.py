"""Tests for the NarrativeVisualizationEngine and LensRenderer.

Covers narrative models, layout computation, SVG rendering,
lens application, JSON export, and error handling.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET

import pytest

from art_from_narratological_lenses.narrative_engine import (
    MODEL_NAMES,
    NARRATIVE_MODELS,
    NarrativeModel,
    NarrativeVisualizationEngine,
    StagePosition,
)
from art_from_narratological_lenses.lens_renderer import (
    AVAILABLE_LENSES,
    LensRenderer,
)


@pytest.fixture
def engine() -> NarrativeVisualizationEngine:
    return NarrativeVisualizationEngine(width=1400, height=900)


@pytest.fixture
def renderer() -> LensRenderer:
    return LensRenderer()


class TestNarrativeModels:
    """Validate the canonical narrative model registry."""

    def test_six_models_defined(self) -> None:
        assert len(NARRATIVE_MODELS) == 6

    def test_model_names_are_canonical(self) -> None:
        expected = {
            "heros_journey",
            "kishotenketsu",
            "ring_composition",
            "freytags_pyramid",
            "three_act",
            "in_medias_res",
        }
        assert set(MODEL_NAMES) == expected

    def test_all_models_have_stages(self) -> None:
        for name, model in NARRATIVE_MODELS.items():
            assert len(model.stages) > 0, f"{name} has no stages"

    def test_all_models_have_palettes(self) -> None:
        for name, model in NARRATIVE_MODELS.items():
            assert model.palette.primary.startswith("#"), f"{name} palette missing primary"
            assert model.palette.secondary.startswith("#"), f"{name} palette missing secondary"
            assert model.palette.accent.startswith("#"), f"{name} palette missing accent"

    def test_heros_journey_has_12_stages(self) -> None:
        model = NARRATIVE_MODELS["heros_journey"]
        assert len(model.stages) == 12

    def test_kishotenketsu_has_4_stages(self) -> None:
        model = NARRATIVE_MODELS["kishotenketsu"]
        assert len(model.stages) == 4


class TestGetModel:
    """Test model lookup."""

    def test_valid_model_returns_object(self, engine: NarrativeVisualizationEngine) -> None:
        model = engine.get_model("heros_journey")
        assert isinstance(model, NarrativeModel)
        assert model.name == "heros_journey"

    def test_invalid_model_raises(self, engine: NarrativeVisualizationEngine) -> None:
        with pytest.raises(ValueError, match="Unknown narrative model"):
            engine.get_model("nonexistent")

    def test_list_models(self, engine: NarrativeVisualizationEngine) -> None:
        names = engine.list_models()
        assert len(names) == 6
        assert "heros_journey" in names

    def test_get_model_count(self, engine: NarrativeVisualizationEngine) -> None:
        assert engine.get_model_count() == 6


class TestComputeLayout:
    """Test layout computation for each narrative structure."""

    def test_circular_layout_positions(self, engine: NarrativeVisualizationEngine) -> None:
        positions = engine.compute_layout("heros_journey")
        assert len(positions) == 12
        assert all(isinstance(p, StagePosition) for p in positions)

    def test_grid_layout_positions(self, engine: NarrativeVisualizationEngine) -> None:
        positions = engine.compute_layout("kishotenketsu")
        assert len(positions) == 4

    def test_concentric_layout_positions(self, engine: NarrativeVisualizationEngine) -> None:
        positions = engine.compute_layout("ring_composition")
        assert len(positions) == 7

    def test_triangular_layout_climax_is_highest(
        self, engine: NarrativeVisualizationEngine
    ) -> None:
        positions = engine.compute_layout("freytags_pyramid")
        # Climax (index 2) should have the smallest y (highest point)
        climax = positions[2]
        assert all(
            climax.y <= p.y for p in positions
        ), "Climax should be at the highest point"

    def test_linear_layout_left_to_right(self, engine: NarrativeVisualizationEngine) -> None:
        positions = engine.compute_layout("three_act")
        assert positions[0].x < positions[1].x < positions[2].x

    def test_scattered_layout_non_sequential(
        self, engine: NarrativeVisualizationEngine
    ) -> None:
        positions = engine.compute_layout("in_medias_res")
        assert len(positions) == 6
        # First position should not be leftmost (it's scattered)
        xs = [p.x for p in positions]
        assert positions[0].x != min(xs), "In medias res should not start at the leftmost point"


class TestRenderModel:
    """Test SVG rendering."""

    def test_render_produces_svg_group(self, engine: NarrativeVisualizationEngine) -> None:
        svg = engine.render_model("heros_journey")
        root = ET.fromstring(svg)
        assert root.tag == "g"
        assert root.get("id") == "narrative-heros_journey"

    def test_render_contains_circles(self, engine: NarrativeVisualizationEngine) -> None:
        svg = engine.render_model("kishotenketsu")
        root = ET.fromstring(svg)
        circles = root.findall("circle")
        assert len(circles) == 4


class TestRenderComparison:
    """Test side-by-side rendering."""

    def test_comparison_renders_multiple(self, engine: NarrativeVisualizationEngine) -> None:
        svg = engine.render_comparison(["heros_journey", "kishotenketsu"])
        root = ET.fromstring(svg)
        assert root.get("id") == "comparison"
        groups = root.findall("g")
        assert len(groups) == 2

    def test_empty_comparison_raises(self, engine: NarrativeVisualizationEngine) -> None:
        with pytest.raises(ValueError, match="At least one model"):
            engine.render_comparison([])


class TestToJson:
    """Test JSON export."""

    def test_json_is_valid(self, engine: NarrativeVisualizationEngine) -> None:
        raw = engine.to_json("three_act")
        data = json.loads(raw)
        assert data["name"] == "three_act"
        assert len(data["stages"]) == 3
        assert "palette" in data

    def test_json_contains_connections(self, engine: NarrativeVisualizationEngine) -> None:
        raw = engine.to_json("heros_journey")
        data = json.loads(raw)
        assert len(data["connections"]) == 12


class TestLensRenderer:
    """Test the lens system."""

    def test_available_lenses(self, renderer: LensRenderer) -> None:
        lenses = renderer.get_available_lenses()
        assert len(lenses) == 4
        assert "chromatic" in lenses

    def test_invalid_lens_raises(self, renderer: LensRenderer) -> None:
        with pytest.raises(ValueError, match="Unknown lens"):
            renderer.get_lens_config("nonexistent")  # type: ignore[arg-type]

    def test_apply_chromatic_lens(self, renderer: LensRenderer) -> None:
        assert renderer.engine is not None
        positions = renderer.engine.compute_layout("heros_journey")
        result = renderer.apply_lens("chromatic", positions)
        assert len(result) == 12
        assert all(item["lens"] == "chromatic" for item in result)

    def test_apply_topographic_lens(self, renderer: LensRenderer) -> None:
        assert renderer.engine is not None
        positions = renderer.engine.compute_layout("freytags_pyramid")
        result = renderer.apply_lens("topographic", positions)
        assert all("elevation" in item for item in result)

    def test_apply_temporal_lens(self, renderer: LensRenderer) -> None:
        assert renderer.engine is not None
        positions = renderer.engine.compute_layout("three_act")
        result = renderer.apply_lens("temporal", positions)
        delays = [item["animation_delay"] for item in result]
        assert delays == sorted(delays), "Temporal delays should increase"

    def test_apply_relational_lens_shrinks_nodes(self, renderer: LensRenderer) -> None:
        assert renderer.engine is not None
        positions = renderer.engine.compute_layout("kishotenketsu")
        result = renderer.apply_lens("relational", positions)
        for item, orig in zip(result, positions):
            assert item["radius"] < orig.radius, "Relational lens should shrink nodes"

    def test_render_with_lens_produces_svg(self, renderer: LensRenderer) -> None:
        svg = renderer.render_with_lens("heros_journey", "chromatic")
        root = ET.fromstring(svg)
        assert root.tag == "g"
        assert "lens-chromatic" in root.get("class", "")
