"""Smoke tests for deployment bundle generation and reachability."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from art_from_narratological_lenses.build_site import build_site
from art_from_narratological_lenses.lens_renderer import AVAILABLE_LENSES
from art_from_narratological_lenses.narrative_engine import MODEL_NAMES


@pytest.fixture(scope="module")
def dist_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out_dir = tmp_path_factory.mktemp("dist")
    build_site(target_dir=out_dir)
    return out_dir


class TestSmokeDeploymentBundle:
    """Smoke check deployment assets."""

    def test_index_html_exists_and_valid(self, dist_dir: Path) -> None:
        index_file = dist_dir / "index.html"
        assert index_file.exists()
        content = index_file.read_text(encoding="utf-8")
        assert "Narratological Algorithmic Lenses" in content
        assert "ACTIVE DEMO" in content

    def test_404_html_exists(self, dist_dir: Path) -> None:
        file_404 = dist_dir / "404.html"
        assert file_404.exists()

    def test_models_json_api_fixture(self, dist_dir: Path) -> None:
        api_file = dist_dir / "api" / "models.json"
        assert api_file.exists()
        data = json.loads(api_file.read_text(encoding="utf-8"))
        assert "models" in data
        assert len(data["models"]) == 6

    def test_all_svg_assets_generated_and_valid_xml(self, dist_dir: Path) -> None:
        svg_dir = dist_dir / "svg"
        assert svg_dir.exists()

        expected_count = len(MODEL_NAMES) * len(AVAILABLE_LENSES)
        generated_svgs = list(svg_dir.glob("*.svg"))
        assert len(generated_svgs) == expected_count

        for model in MODEL_NAMES:
            for lens in AVAILABLE_LENSES:
                svg_path = svg_dir / f"{model}_{lens}.svg"
                assert svg_path.exists(), f"Missing SVG: {svg_path.name}"

                # Parse XML to ensure valid SVG markup
                root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
                assert root.tag.endswith("svg")
