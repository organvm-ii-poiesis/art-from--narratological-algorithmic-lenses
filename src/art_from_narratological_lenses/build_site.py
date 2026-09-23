"""Build script for static site export.

Generates deployable web assets for GitHub Pages deployment in `dist/`.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from art_from_narratological_lenses.lens_renderer import AVAILABLE_LENSES, LensRenderer
from art_from_narratological_lenses.narrative_engine import MODEL_NAMES, NarrativeVisualizationEngine

DIST_DIR = Path("dist")

STATIC_INDEX_HTML = """<!DOCTYPE html>
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
        const res = await fetch(`svg/${currentModel}_${currentLens}.svg`);
        if (res.ok) {
          const svgText = await res.text();
          canvas.innerHTML = svgText;
        } else {
          canvas.innerHTML = `<p style="color: #f85149;">Error loading structure visualization</p>`;
        }
      } catch (e) {
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


def build_site(target_dir: Path = DIST_DIR) -> None:
    """Build complete static web distribution in target_dir."""
    if target_dir.exists():
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    svg_dir = target_dir / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)
    api_dir = target_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    # Write main index.html and 404.html
    (target_dir / "index.html").write_text(STATIC_INDEX_HTML, encoding="utf-8")
    (target_dir / "404.html").write_text(STATIC_INDEX_HTML, encoding="utf-8")

    engine = NarrativeVisualizationEngine()
    renderer = LensRenderer(engine=engine)

    # Generate pre-rendered SVGs for every model x lens combination
    for model_name in MODEL_NAMES:
        for lens_name in AVAILABLE_LENSES:
            svg_content = renderer.render_with_lens(model_name, lens_name)
            svg_doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" width="100%" height="100%">{svg_content}</svg>'
            out_file = svg_dir / f"{model_name}_{lens_name}.svg"
            out_file.write_text(svg_doc, encoding="utf-8")

    # Generate API fixture json files
    models_data = [
        {
            "name": m,
            "display_name": model.display_name,
            "layout_type": model.layout_type,
            "stages_count": len(model.stages),
            "description": model.description,
        }
        for m in engine.list_models()
        for model in [engine.get_model(m)]
    ]
    (api_dir / "models.json").write_text(json.dumps({"models": models_data}, indent=2), encoding="utf-8")

    print(f"Successfully built static site in '{target_dir}'")


if __name__ == "__main__":
    build_site()
