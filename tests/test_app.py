"""Tests for Flask web application and API endpoints."""

from __future__ import annotations

import json
from typing import Generator

import pytest
from flask.testing import FlaskClient

from art_from_narratological_lenses.app import app


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestAppRoutes:
    """Validate web application endpoints."""

    def test_index_route(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Narratological Algorithmic Lenses" in response.data

    def test_health_check(self, client: FlaskClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["app"] == "art-from-narratological-lenses"

    def test_list_models_api(self, client: FlaskClient) -> None:
        response = client.get("/api/models")
        assert response.status_code == 200
        data = response.get_json()
        assert "models" in data
        assert data["total"] == 6

    def test_get_single_model_api(self, client: FlaskClient) -> None:
        response = client.get("/api/model/heros_journey")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "heros_journey"
        assert len(data["stages"]) == 12

    def test_get_invalid_model_api(self, client: FlaskClient) -> None:
        response = client.get("/api/model/nonexistent_model")
        assert response.status_code == 404

    def test_list_lenses_api(self, client: FlaskClient) -> None:
        response = client.get("/api/lenses")
        assert response.status_code == 200
        data = response.get_json()
        assert "lenses" in data
        assert data["total"] == 4

    def test_render_model_svg(self, client: FlaskClient) -> None:
        response = client.get("/api/render/kishotenketsu")
        assert response.status_code == 200
        assert response.mimetype == "image/svg+xml"
        assert b"<g id=\"narrative-kishotenketsu\"" in response.data

    def test_render_model_with_lens_svg(self, client: FlaskClient) -> None:
        response = client.get("/api/render/kishotenketsu/topographic")
        assert response.status_code == 200
        assert response.mimetype == "image/svg+xml"
        assert b"lens-topographic-kishotenketsu" in response.data

    def test_render_invalid_model_or_lens(self, client: FlaskClient) -> None:
        response = client.get("/api/render/invalid_model/chromatic")
        assert response.status_code == 404

    def test_transform_text_api(self, client: FlaskClient) -> None:
        payload = {
            "text": "The protagonist receives a mysterious letter.",
            "model": "heros_journey",
            "lens": "temporal",
        }
        response = client.post(
            "/api/transform",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["model"] == "The Hero's Journey"
        assert data["lens"] == "temporal"
        assert data["stages_mapped"] == 12
