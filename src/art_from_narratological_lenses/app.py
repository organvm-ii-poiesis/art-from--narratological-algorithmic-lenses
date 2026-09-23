"""Flask web application for art-from-narratological-lenses.

Provides interactive web experience and REST API endpoints for narrative models
and visual algorithmic lenses.
"""

from __future__ import annotations

import argparse
from typing import Any

from flask import Flask, jsonify, request

from art_from_narratological_lenses.lens_renderer import LENS_CONFIGS, LensRenderer
from art_from_narratological_lenses.narrative_engine import (
    NARRATIVE_MODELS,
    NarrativeVisualizationEngine,
)

app = Flask(__name__)
engine = NarrativeVisualizationEngine()
renderer = LensRenderer(engine=engine)


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Narratological Algorithmic Lenses</title>
  <style>
    :root {
      --bg-color: #0d1117;
      --card-bg: #161b22;
      --border-color: #30363d;
      --text-main: #c9d1d9;
      --text-heading: #f0f6fc;
      --accent-color: #58a6ff;
      --accent-hover: #1f6feb;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }
    header {
      background-color: var(--card-bg);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    header h1 {
      font-size: 1.2rem;
      color: var(--text-heading);
      font-weight: 600;
    }
    header .subtitle {
      font-size: 0.85rem;
      color: #8b949e;
      margin-top: 2px;
    }
    .badge {
      background: rgba(88, 166, 255, 0.15);
      color: var(--accent-color);
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
      border: 1px solid rgba(88, 166, 255, 0.3);
    }
    main {
      display: flex;
      flex: 1;
      overflow: hidden;
    }
    sidebar {
      width: 320px;
      background-color: var(--card-bg);
      border-right: 1px solid var(--border-color);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      overflow-y: auto;
    }
    .section-title {
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #8b949e;
      margin-bottom: 8px;
    }
    .btn-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .btn {
      background: var(--bg-color);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 6px;
      cursor: pointer;
      text-align: left;
      font-size: 0.9rem;
      transition: all 0.2s ease;
    }
    .btn:hover {
      border-color: var(--accent-color);
      color: var(--text-heading);
    }
    .btn.active {
      background: rgba(88, 166, 255, 0.15);
      border-color: var(--accent-color);
      color: var(--accent-color);
      font-weight: 600;
    }
    .lens-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .lens-btn {
      text-align: center;
      padding: 8px;
      font-size: 0.85rem;
    }
    textarea {
      width: 100%;
      height: 90px;
      background: var(--bg-color);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      color: var(--text-main);
      padding: 10px;
      font-family: inherit;
      font-size: 0.85rem;
      resize: vertical;
    }
    textarea:focus {
      outline: none;
      border-color: var(--accent-color);
    }
    content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--bg-color);
      position: relative;
    }
    .canvas-container {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
      overflow: hidden;
    }
    .canvas-container svg {
      width: 100%;
      height: 100%;
      max-width: 1200px;
      max-height: 800px;
    }
    .info-bar {
      background-color: var(--card-bg);
      border-top: 1px solid var(--border-color);
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .info-details h2 {
      font-size: 1rem;
      color: var(--text-heading);
      margin-bottom: 4px;
    }
    .info-details p {
      font-size: 0.85rem;
      color: #8b949e;
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Narratological Algorithmic Lenses</h1>
      <div class="subtitle">ORGAN-II (Poiesis) — Algorithmic Narrative Visualizer</div>
    </div>
    <span class="badge">ACTIVE DEMO</span>
  </header>

  <main>
    <sidebar>
      <div>
        <div class="section-title">Narrative Structure</div>
        <div class="btn-group" id="model-selector"></div>
      </div>

      <div>
        <div class="section-title">Visual Lens</div>
        <div class="lens-grid" id="lens-selector"></div>
      </div>

      <div>
        <div class="section-title">Sample Narrative Corpus</div>
        <textarea id="sample-text" placeholder="Enter text narrative beat to sample transform..."></textarea>
      </div>
    </sidebar>

    <content-area>
      <div class="canvas-container" id="svg-canvas">
        <p>Loading visualization...</p>
      </div>
      <div class="info-bar">
        <div class="info-details">
          <h2 id="info-title">Hero's Journey</h2>
          <p id="info-desc">Campbell's monomyth — circular journey of departure, initiation, and return</p>
        </div>
      </div>
    </content-area>
  </main>

  <script>
    const models = [
      { id: 'heros_journey', name: "The Hero's Journey", desc: "Campbell's monomyth — circular journey of departure, initiation, and return" },
      { id: 'kishotenketsu', name: "Kishōtenketsu", desc: "Four-act structure without conflict — introduction, development, twist, reconciliation" },
      { id: 'ring_composition', name: "Ring Composition", desc: "Palindromic narrative where the ending mirrors the beginning" },
      { id: 'freytags_pyramid', name: "Freytag's Pyramid", desc: "Five-act dramatic structure with rising tension, climax, and resolution" },
      { id: 'three_act', name: "Three-Act Structure", desc: "Classical dramatic structure — setup, confrontation, resolution" },
      { id: 'in_medias_res', name: "In Medias Res", desc: "Beginning in the middle of the action — temporal displacement" }
    ];

    const lenses = [
      { id: 'chromatic', name: 'Chromatic' },
      { id: 'topographic', name: 'Topographic' },
      { id: 'temporal', name: 'Temporal' },
      { id: 'relational', name: 'Relational' }
    ];

    let currentModel = 'heros_journey';
    let currentLens = 'chromatic';

    function initUI() {
      const modelContainer = document.getElementById('model-selector');
      modelContainer.innerHTML = models.map(m => `
        <button class="btn ${m.id === currentModel ? 'active' : ''}" onclick="selectModel('${m.id}')">
          ${m.name}
        </button>
      `).join('');

      const lensContainer = document.getElementById('lens-selector');
      lensContainer.innerHTML = lenses.map(l => `
        <button class="btn lens-btn ${l.id === currentLens ? 'active' : ''}" onclick="selectLens('${l.id}')">
          ${l.name}
        </button>
      `).join('');

      renderCanvas();
    }

    async function renderCanvas() {
      const canvas = document.getElementById('svg-canvas');
      const modelObj = models.find(m => m.id === currentModel);
      document.getElementById('info-title').textContent = `${modelObj.name} (${currentLens} Lens)`;
      document.getElementById('info-desc').textContent = modelObj.desc;

      try {
        const res = await fetch(`/api/render/${currentModel}/${currentLens}`);
        if (res.ok) {
          const svgText = await res.text();
          canvas.innerHTML = `<svg viewBox="0 0 1400 900" width="100%" height="100%">${svgText}</svg>`;
        } else {
          canvas.innerHTML = `<p style="color: #f85149;">Error loading structure visualization</p>`;
        }
      } catch (e) {
        // Fallback for static builds without server backend
        canvas.innerHTML = `<p style="color: #8b949e;">Interactive view loaded (${currentModel} / ${currentLens})</p>`;
      }
    }

    function selectModel(id) {
      currentModel = id;
      initUI();
    }

    function selectLens(id) {
      currentLens = id;
      initUI();
    }

    window.addEventListener('DOMContentLoaded', initUI);
  </script>
</body>
</html>
"""


@app.route("/")
def index() -> Any:
    """Serve main interactive web interface."""
    return INDEX_HTML


@app.route("/health")
def health() -> Any:
    """Service health check endpoint."""
    return jsonify(
        {
            "status": "ok",
            "app": "art-from-narratological-lenses",
            "version": "0.1.0",
        }
    )


@app.route("/api/models")
def list_models() -> Any:
    """Return all available narrative models with metadata."""
    models_data = [
        {
            "name": name,
            "display_name": model.display_name,
            "layout_type": model.layout_type,
            "stages_count": len(model.stages),
            "description": model.description,
        }
        for name, model in NARRATIVE_MODELS.items()
    ]
    return jsonify({"models": models_data, "total": len(models_data)})


@app.route("/api/model/<name>")
def get_model(name: str) -> Any:
    """Return model layout data and stages as JSON."""
    try:
        data_json = engine.to_json(name)
        return app.response_class(data_json, mimetype="application/json")
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


@app.route("/api/lenses")
def list_lenses() -> Any:
    """Return all available lenses and configurations."""
    lenses_data = [
        {
            "name": name,
            "description": config.description,
            "saturation_boost": config.saturation_boost,
            "opacity_base": config.opacity_base,
            "stroke_weight": config.stroke_weight,
            "animation_duration": config.animation_duration,
        }
        for name, config in LENS_CONFIGS.items()
    ]
    return jsonify({"lenses": lenses_data, "total": len(lenses_data)})


@app.route("/api/render/<name>")
@app.route("/api/render/<name>/<lens>")
def render_model(name: str, lens: str | None = None) -> Any:
    """Render a narrative model SVG, optionally applying a lens."""
    try:
        if lens:
            svg_content = renderer.render_with_lens(name, lens)  # type: ignore[arg-type]
        else:
            svg_content = engine.render_model(name)
        return app.response_class(svg_content, mimetype="image/svg+xml")
    except (ValueError, KeyError) as err:
        return jsonify({"error": str(err)}), 404


@app.route("/api/transform", methods=["POST"])
def transform_text() -> Any:
    """Transform input text sample through specified narrative lens."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    model_name = data.get("model", "heros_journey")
    lens_type = data.get("lens", "chromatic")

    try:
        model = engine.get_model(model_name)
        positions = engine.compute_layout(model_name)
        enriched = renderer.apply_lens(lens_type, positions)  # type: ignore[arg-type]
        return jsonify(
            {
                "input_text": text,
                "model": model.display_name,
                "lens": lens_type,
                "stages_mapped": len(enriched),
                "visual_nodes": enriched,
            }
        )
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


def main() -> None:
    """Run Flask development server."""
    parser = argparse.ArgumentParser(
        description="Run Narratological Algorithmic Lenses web server"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
