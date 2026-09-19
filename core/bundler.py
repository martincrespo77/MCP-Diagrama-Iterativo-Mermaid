import json
from typing import List, Dict, Any

class SingleFileBundler:
    """Empaqueta nodos, zonas y conexiones en una aplicación web interactiva autónoma HTML5+SVG+Vanilla JS."""

    PALETTE = [
        {"border": "#38bdf8", "bg": "#0c4a6e", "text": "#38bdf8"},
        {"border": "#3b82f6", "bg": "#1e3a8a", "text": "#60a5fa"},
        {"border": "#8b5cf6", "bg": "#4c1d95", "text": "#a78bfa"},
        {"border": "#10b981", "bg": "#064e3b", "text": "#34d399"},
        {"border": "#f59e0b", "bg": "#78350f", "text": "#fbbf24"},
        {"border": "#ef4444", "bg": "#7f1d1d", "text": "#f87171"},
        {"border": "#ec4899", "bg": "#831843", "text": "#f472b6"},
        {"border": "#14b8a6", "bg": "#134e4a", "text": "#2dd4bf"},
    ]

    SHAPE_ICONS = {
        "rect": "📦",
        "round": "⭕",
        "pill": "💊",
        "cylinder": "🛢️",
        "diamond": "🔷",
        "hexagon": "⬡",
        "parallelogram": "▱",
        "circle": "⚪",
    }

    def bundle(self, title: str, nodes: List[Dict[str, Any]], connections: List[Dict[str, Any]], subgraphs: List[Dict[str, Any]]) -> str:
        # Colores por subgrafo o capas
        sub_colors = {}
        for idx, sub in enumerate(subgraphs):
            color = self.PALETTE[idx % len(self.PALETTE)]
            sub_colors[sub["id"]] = color

        for n in nodes:
            sub_id = n.get("subgraph", "General")
            default_color = sub_colors.get(sub_id, self.PALETTE[0])
            custom_style = n.get("custom_style", {})
            color = {
                "border": custom_style.get("border", default_color["border"]),
                "bg": custom_style.get("bg", default_color["bg"]),
                "text": custom_style.get("text", default_color["text"])
            }
            n["color"] = color

            raw_label = n.get("raw_label", n.get("title", n["id"]))
            parts = [p.strip() for p in raw_label.replace("<br/>", "<br>").split("<br>") if p.strip()]
            main_title = parts[0] if parts else n["id"]
            sub_desc = " · ".join(parts[1:]) if len(parts) > 1 else ""

            shape = n.get("shape", "rect")
            icon = self.SHAPE_ICONS.get(shape, "📦")
            meta_pattern = n.get("meta", {}).get("patron", "")

            n["html"] = f"""
            <div class="comp-card shape-{shape}" style="border-color:{color['border']};">
                <div class="comp-header" style="background:{color['bg']};">
                    <span class="comp-icon">{icon}</span>
                    <div class="comp-title-group">
                        <span class="comp-id">{n['id']}</span>
                        <span class="comp-name" title="{main_title}">{main_title}</span>
                    </div>
                </div>
                <div class="comp-body">
                    {f'<div class="comp-subtitle" title="{sub_desc}">{sub_desc}</div>' if sub_desc else ''}
                    <div class="comp-meta-row">
                        <span class="comp-sub">{sub_id}</span>
                        <span class="comp-tag">{meta_pattern or shape}</span>
                    </div>
                </div>
            </div>
            """

        nodes_json = json.dumps(nodes, ensure_ascii=False)
        connections_json = json.dumps(connections, ensure_ascii=False)
        subgraphs_json = json.dumps(subgraphs, ensure_ascii=False)

        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: #080c14;
    color: #e2e8f0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
  }}

  #topbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 54px;
    background: #0b1120;
    border-bottom: 1px solid #1e293b;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 12px;
    z-index: 1000;
    box-shadow: 0 4px 14px rgba(0,0,0,0.6);
  }}
  #topbar h1 {{
    font-size: 13.5px;
    color: #38bdf8;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  #topbar h1 .badge {{
    background: #1e293b;
    color: #94a3b8;
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid #334155;
  }}
  #searchBox {{
    width: 200px;
    padding: 6px 12px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    font-size: 11.5px;
    outline: none;
    transition: border-color 0.2s;
  }}
  #searchBox:focus {{ border-color: #38bdf8; }}

  .toolbar-group {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .toolbar-label {{
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    white-space: nowrap;
  }}

  .btn {{
    padding: 5px 10px;
    border-radius: 5px;
    border: 1px solid #334155;
    background: #1e293b;
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }}
  .btn:hover {{ background: #273549; color: #f1f5f9; }}
  .btn.active {{
    background: #0369a1;
    border-color: #38bdf8;
    color: #ffffff;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.35);
  }}
  .btn-chip {{
    padding: 4px 8px;
    font-size: 10.5px;
    border-radius: 12px;
  }}
  .btn-chip.active {{
    background: #1e3a5f;
    border-color: #38bdf8;
    color: #e0f2fe;
  }}
  .btn-danger {{ border-color: #dc2626; color: #f87171; }}
  .btn-danger:hover {{ background: #450a0a; }}

  /* Banner de Enfoque Activo */
  #focusBanner {{
    display: none;
    position: fixed;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 23, 42, 0.94);
    border: 1px solid #38bdf8;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    color: #f8fafc;
    z-index: 999;
    box-shadow: 0 6px 20px rgba(0,0,0,0.6);
    backdrop-filter: blur(8px);
    align-items: center;
    gap: 12px;
  }}
  #focusBanner.show {{ display: flex; }}
  #focusBanner .badge-in {{ color: #10b981; font-weight: 700; }}
  #focusBanner .badge-out {{ color: #f59e0b; font-weight: 700; }}
  #focusClearBtn {{
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 13px;
    padding: 2px 6px;
    border-radius: 4px;
  }}
  #focusClearBtn:hover {{ color: #f87171; background: rgba(239,68,68,0.2); }}

  #canvas {{
    position: absolute;
    top: 54px; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    cursor: grab;
    background: radial-gradient(circle at 1px 1px, #151d2f 1.2px, transparent 0);
    background-size: 32px 32px;
  }}
  #canvas.grabbing {{ cursor: grabbing; }}
  
  #world {{
    position: absolute;
    top: 0; left: 0;
    width: 6500px;
    height: 4000px;
    transform-origin: 0 0;
  }}

  #connections {{
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
  }}

  .subgraph-zone {{
    position: absolute;
    border: 1.5px dashed #334155;
    border-radius: 14px;
    pointer-events: none;
    background: rgba(15, 23, 42, 0.35);
    z-index: 2;
    transition: opacity 0.2s;
  }}
  .subgraph-label {{
    position: absolute;
    top: -12px; left: 16px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 2px 10px;
    border-radius: 4px;
    background: #0b1120;
    border: 1px solid #334155;
    color: #38bdf8;
  }}

  .node {{
    position: absolute;
    z-index: 10;
    cursor: grab;
    user-select: none;
    transition: opacity 0.25s, transform 0.1s, box-shadow 0.2s;
  }}
  .node.dragging {{ cursor: grabbing; z-index: 100 !important; }}
  .node.highlight {{
    box-shadow: 0 0 25px #38bdf8 !important;
    border-radius: 10px;
  }}
  .node.neighbor-in {{
    box-shadow: 0 0 20px #10b981 !important;
    border-radius: 10px;
  }}
  .node.neighbor-out {{
    box-shadow: 0 0 20px #f59e0b !important;
    border-radius: 10px;
  }}
  .node.dimmed {{ opacity: 0.12 !important; }}

  .comp-card {{
    background: #0f172a;
    border: 2px solid;
    border-radius: 9px;
    width: 300px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
  }}
  .comp-card:hover {{
    filter: brightness(1.1);
  }}
  .comp-header {{
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}
  .comp-icon {{ font-size: 18px; }}
  .comp-title-group {{ display: flex; flex-direction: column; overflow: hidden; }}
  .comp-id {{ font-size: 10px; font-family: monospace; color: #94a3b8; font-weight: 700; }}
  .comp-name {{ font-size: 12.5px; font-weight: 700; color: #f8fafc; line-height: 1.25; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }}
  .comp-body {{
    padding: 7px 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: rgba(15, 23, 42, 0.7);
  }}
  .comp-subtitle {{
    font-size: 10.5px;
    color: #94a3b8;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }}
  .comp-meta-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2px;
  }}
  .comp-sub {{ font-size: 9.5px; color: #64748b; font-family: monospace; }}
  .comp-tag {{
    font-size: 9px;
    background: #1e293b;
    color: #cbd5e1;
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid #334155;
  }}

  /* Shapes */
  .shape-round {{ border-radius: 18px !important; }}
  .shape-pill {{ border-radius: 25px !important; }}
  .shape-diamond {{ border-style: double !important; border-width: 3px !important; }}
  .shape-hexagon {{ border-radius: 6px !important; }}
  .shape-circle {{ border-radius: 22px !important; }}

  /* Conexiones SVG */
  .conn-group {{
    pointer-events: stroke;
    cursor: pointer;
  }}
  .conn-hit {{
    fill: none;
    stroke: transparent;
    stroke-width: 18;
    cursor: pointer;
    pointer-events: stroke;
  }}
  .conn-path {{
    fill: none;
    stroke: #38bdf8;
    stroke-width: 1.8;
    transition: stroke 0.2s, stroke-width 0.2s, opacity 0.25s;
    opacity: 0.75;
  }}
  .conn-path.dashed {{ stroke: #a78bfa; stroke-dasharray: 6, 4; }}
  .conn-path.thick {{ stroke: #10b981; stroke-width: 2.6; opacity: 0.9; }}
  .conn-path.dimmed {{ opacity: 0.04 !important; }}
  
  .conn-path.highlight-incoming {{
    stroke: #10b981 !important;
    stroke-width: 3.5 !important;
    opacity: 1 !important;
    filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));
  }}
  .conn-path.highlight-outgoing {{
    stroke: #f59e0b !important;
    stroke-width: 3.5 !important;
    opacity: 1 !important;
    filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.8));
  }}
  .conn-path.highlight-self {{
    stroke: #38bdf8 !important;
    stroke-width: 3.5 !important;
    opacity: 1 !important;
    filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));
  }}
  .conn-path.hovered {{
    stroke: #38bdf8 !important;
    stroke-width: 4 !important;
    opacity: 1 !important;
    filter: drop-shadow(0 0 8px #38bdf8);
  }}

  /* Etiquetas de Conexiones */
  .conn-label-group {{
    pointer-events: none;
    transition: opacity 0.2s;
  }}
  .conn-label-group.hidden {{ display: none !important; }}
  .conn-label-bg {{
    fill: #0b1120;
    stroke: #334155;
    stroke-width: 1;
    rx: 4;
  }}
  .conn-label-text {{
    font-size: 9px;
    font-family: monospace;
    font-weight: 600;
    fill: #94a3b8;
    text-anchor: middle;
    dominant-baseline: middle;
  }}
  .conn-label-group.active .conn-label-bg {{
    stroke: #38bdf8;
    fill: #031e38;
  }}
  .conn-label-group.active .conn-label-text {{
    fill: #e0f2fe;
    font-weight: 700;
  }}

  /* Tooltip Flotante para Aristas */
  #edgeTooltip {{
    display: none;
    position: fixed;
    background: rgba(11, 17, 32, 0.95);
    border: 1px solid #38bdf8;
    border-radius: 8px;
    padding: 10px 14px;
    color: #f8fafc;
    font-size: 12px;
    max-width: 360px;
    z-index: 2500;
    pointer-events: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    backdrop-filter: blur(6px);
  }}
  #edgeTooltip.show {{ display: block; }}
  .edge-tt-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid #1e293b;
    font-size: 11px;
    font-weight: 700;
    color: #38bdf8;
  }}
  .edge-tt-badge {{
    background: #1e293b;
    color: #94a3b8;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 10px;
  }}
  .edge-tt-desc {{
    font-size: 11.5px;
    color: #cbd5e1;
    line-height: 1.4;
  }}

  /* Modal de Detalles */
  #modalOverlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(4, 7, 13, 0.8);
    backdrop-filter: blur(4px);
    z-index: 3000;
    justify-content: center;
    align-items: center;
  }}
  #modalOverlay.show {{ display: flex; }}
  #modalCard {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    width: 90%;
    max-width: 720px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
  }}
  #modalHeader {{
    padding: 14px 20px;
    border-bottom: 1px solid #1e293b;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  #modalTitle {{ font-size: 15px; font-weight: 700; color: #38bdf8; }}
  #modalBody {{
    padding: 18px 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .modal-sec {{
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 12px 14px;
  }}
  .modal-sec-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 6px;
  }}
  .modal-list {{ list-style: none; }}
  .modal-list li {{ font-size: 12px; color: #cbd5e1; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }}

  /* Minimapa y Controles de Zoom */
  #zoomControls {{
    position: fixed;
    bottom: 16px;
    left: 16px;
    display: flex;
    gap: 6px;
    background: #0b1120;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 4px;
    z-index: 900;
  }}
  #zoomControls .btn {{
    padding: 6px 10px;
    font-size: 12px;
  }}

  #minimap {{
    position: fixed;
    bottom: 16px; right: 16px;
    width: 220px; height: 110px;
    background: #0b1120;
    border: 1px solid #1e293b;
    border-radius: 8px;
    z-index: 900;
    overflow: hidden;
  }}
  #minimapViewport {{
    position: absolute;
    border: 1.5px solid #38bdf8;
    background: rgba(56, 189, 248, 0.15);
    pointer-events: none;
  }}
</style>
</head>
<body>

<div id="topbar">
  <h1><span>{title}</span> <span class="badge">Interactivo Air-Gapped</span></h1>
  <input type="text" id="searchBox" placeholder="Buscar componente o ID...">
  
  <div class="toolbar-group">
    <span class="toolbar-label">🏷️ Etiquetas:</span>
    <button class="btn btn-label active" data-label-mode="smart" title="Muestra etiquetas al enfocar nodo o sobrevolar línea">Inteligente</button>
    <button class="btn btn-label" data-label-mode="all" title="Muestra todas las etiquetas">Todas</button>
    <button class="btn btn-label" data-label-mode="primary" title="Solo muestra etiquetas de flujo principal ==&gt;">Principales</button>
    <button class="btn btn-label" data-label-mode="none" title="Oculta todas las etiquetas">Ocultas</button>
  </div>

  <div class="toolbar-group">
    <span class="toolbar-label">👁️ Enlaces:</span>
    <button class="btn btn-chip active" data-filter-type="thick" title="Alternar Flujo Principal (==&gt;)">==&gt; Principal</button>
    <button class="btn btn-chip active" data-filter-type="arrow" title="Alternar Transiciones (--&gt;)">--&gt; Métodos</button>
    <button class="btn btn-chip active" data-filter-type="dashed" title="Alternar Guardas/Roles/Eventos (-.-&gt;)">-.-&gt; Reglas</button>
  </div>

  <div class="toolbar-group" id="subgraphFilters">
    <button class="btn active" data-sub="all">Todos</button>
  </div>

  <button class="btn btn-danger" id="resetBtn" title="Restaurar posición y zoom iniciales">↺ Restaurar</button>
</div>

<!-- Banner de Enfoque Activo -->
<div id="focusBanner">
  <span>📌 Enfoque en: <strong id="focusNodeTitle" style="color:#38bdf8;"></strong></span>
  <span>🟢 Entrantes: <span id="focusInCount" class="badge-in">0</span></span>
  <span>🟠 Salientes: <span id="focusOutCount" class="badge-out">0</span></span>
  <button id="focusClearBtn" title="Liberar foco (Esc)">✕ Liberar</button>
</div>

<div id="canvas">
  <div id="world">
    <svg id="connections">
      <defs>
        <marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#38bdf8"/>
        </marker>
        <marker id="arrow-dashed" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#a78bfa"/>
        </marker>
        <marker id="arrow-thick" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#10b981"/>
        </marker>
        <marker id="arrow-incoming" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#10b981"/>
        </marker>
        <marker id="arrow-outgoing" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#f59e0b"/>
        </marker>
        <marker id="arrow-self" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 9 3.5, 0 7" fill="#38bdf8"/>
        </marker>
      </defs>
    </svg>
  </div>
</div>

<!-- Controles de Zoom -->
<div id="zoomControls">
  <button class="btn" id="zoomInBtn" title="Acercar (+)">＋</button>
  <button class="btn" id="zoomOutBtn" title="Alejar (-)">－</button>
  <button class="btn" id="zoomResetBtn" title="Restablecer zoom a 100%">100%</button>
  <button class="btn" id="zoomFitBtn" title="Ajustar a la pantalla">⛶ Ajustar</button>
</div>

<!-- Tooltip Flotante para Conexiones -->
<div id="edgeTooltip">
  <div class="edge-tt-header">
    <span id="edgeTtEndpoints">A ➔ B</span>
    <span class="edge-tt-badge" id="edgeTtType">Tipo</span>
  </div>
  <div class="edge-tt-desc" id="edgeTtLabel">Descripción del enlace</div>
</div>

<!-- Modal de Inspección Técnica -->
<div id="modalOverlay" onclick="if(event.target===this)closeModal()">
  <div id="modalCard">
    <div id="modalHeader">
      <div id="modalTitle">Detalle</div>
      <button class="btn btn-danger" onclick="closeModal()">✕</button>
    </div>
    <div id="modalBody"></div>
  </div>
</div>

<div id="minimap"><div id="minimapViewport"></div></div>

<script>
const nodesData = {nodes_json};
const connectionsData = {connections_json};
const subgraphsData = {subgraphs_json};

const world = document.getElementById('world');
const svgEl = document.getElementById('connections');
const canvas = document.getElementById('canvas');
const modalOverlay = document.getElementById('modalOverlay');
const modalBody = document.getElementById('modalBody');
const modalTitle = document.getElementById('modalTitle');
const searchBox = document.getElementById('searchBox');
const minimapViewport = document.getElementById('minimapViewport');
const subgraphFilters = document.getElementById('subgraphFilters');
const focusBanner = document.getElementById('focusBanner');
const focusNodeTitle = document.getElementById('focusNodeTitle');
const focusInCount = document.getElementById('focusInCount');
const focusOutCount = document.getElementById('focusOutCount');
const focusClearBtn = document.getElementById('focusClearBtn');
const edgeTooltip = document.getElementById('edgeTooltip');
const edgeTtEndpoints = document.getElementById('edgeTtEndpoints');
const edgeTtType = document.getElementById('edgeTtType');
const edgeTtLabel = document.getElementById('edgeTtLabel');

const domNodes = {{}};
const initialPositions = {{}};
let currentLabelMode = 'smart'; // smart | all | primary | none
let visibleTypes = {{ 'thick': true, 'arrow': true, 'dashed': true, 'line': true }};
let lockedFocusNodeId = null;
let hoveredNodeId = null;
let hoveredEdgeId = null;

// Sistema de Coordenadas, Paneo y Zoom Transform
let panX = 40, panY = 20, zoom = 0.95;

function applyTransform() {{
  world.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{zoom}})`;
  updateMinimap();
}}

function zoomAt(clientX, clientY, factor) {{
  const newZoom = Math.min(Math.max(zoom * factor, 0.25), 2.5);
  const canvasRect = canvas.getBoundingClientRect();
  const mouseCanvasX = clientX - canvasRect.left;
  const mouseCanvasY = clientY - canvasRect.top;
  
  const worldX = (mouseCanvasX - panX) / zoom;
  const worldY = (mouseCanvasY - panY) / zoom;
  
  panX = mouseCanvasX - worldX * newZoom;
  panY = mouseCanvasY - worldY * newZoom;
  zoom = newZoom;
  applyTransform();
}}

// Renderizar zonas de subgrafos
subgraphsData.forEach(s => {{
  const z = document.createElement('div');
  z.className = 'subgraph-zone';
  z.id = `subzone_${{s.id}}`;
  z.style.left = `${{s.x}}px`;
  z.style.top = `${{s.y}}px`;
  z.style.width = `${{s.width}}px`;
  z.style.height = `${{s.height}}px`;

  const lbl = document.createElement('span');
  lbl.className = 'subgraph-label';
  lbl.textContent = s.title;
  z.appendChild(lbl);
  world.appendChild(z);

  // Botón de filtro de subgrafo
  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.setAttribute('data-sub', s.id);
  btn.textContent = s.title;
  subgraphFilters.appendChild(btn);
}});

// Renderizar Nodos
nodesData.forEach(n => {{
  const el = document.createElement('div');
  el.id = n.id;
  el.className = 'node';
  el.style.left = `${{n.x}}px`;
  el.style.top = `${{n.y}}px`;
  el.dataset.x = n.x;
  el.dataset.y = n.y;
  el.innerHTML = n.html;
  initialPositions[n.id] = {{ x: n.x, y: n.y }};

  // Hover para trazabilidad inteligente
  el.addEventListener('mouseenter', () => {{
    if (!lockedFocusNodeId) {{
      hoveredNodeId = n.id;
      updateVisualFocus();
    }}
  }});
  el.addEventListener('mouseleave', () => {{
    if (!lockedFocusNodeId) {{
      hoveredNodeId = null;
      updateVisualFocus();
    }}
  }});

  // Clic para fijar foco
  el.addEventListener('click', (e) => {{
    if (el.dataset.wasDragged) {{
      delete el.dataset.wasDragged;
      return;
    }}
    if (lockedFocusNodeId === n.id) {{
      openModal(n);
    }} else {{
      setFocusNode(n.id);
    }}
  }});

  // Doble clic abre siempre modal
  el.addEventListener('dblclick', () => {{
    openModal(n);
  }});

  world.appendChild(el);
  domNodes[n.id] = el;
}});

// Matemática Perimétrica para Conexiones
function getNodeEdgeRect(fromCenter, toCenter, el) {{
  const w = el.offsetWidth / 2;
  const h = el.offsetHeight / 2;
  const cx = parseFloat(el.dataset.x) + w;
  const cy = parseFloat(el.dataset.y) + h;
  const angle = Math.atan2(toCenter.y - fromCenter.y, toCenter.x - fromCenter.x);
  const absCos = Math.abs(Math.cos(angle)), absSin = Math.abs(Math.sin(angle));
  const dist = (absCos * h > absSin * w) ? (w / absCos) : (h / absSin);
  return {{ x: cx + Math.cos(angle) * dist, y: cy + Math.sin(angle) * dist }};
}}

function getCenter(el) {{
  return {{
    x: parseFloat(el.dataset.x) + el.offsetWidth / 2,
    y: parseFloat(el.dataset.y) + el.offsetHeight / 2
  }};
}}

// Dibujado Integral de Conexiones
function drawConnections() {{
  const defs = svgEl.querySelector('defs');
  svgEl.innerHTML = '';
  svgEl.appendChild(defs);

  connectionsData.forEach(c => {{
    const fromEl = domNodes[c.from];
    const toEl = domNodes[c.to];
    if (!fromEl || !toEl) return;
    if (fromEl.style.display === 'none' || toEl.style.display === 'none') return;
    if (!visibleTypes[c.type]) return;

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'conn-group');
    g.setAttribute('data-id', c.id);
    g.setAttribute('data-from', c.from);
    g.setAttribute('data-to', c.to);
    g.setAttribute('data-type', c.type);

    let pathD = '';
    let labelX = 0, labelY = 0;

    // Manejo especial de Auto-bucles (Self-Loops)
    if (c.from === c.to) {{
      const x = parseFloat(fromEl.dataset.x);
      const y = parseFloat(fromEl.dataset.y);
      const w = fromEl.offsetWidth;
      const h = fromEl.offsetHeight;
      const loopW = 55 + (c.pair_index || 0) * 22;
      const y1 = y + h * 0.28;
      const y2 = y + h * 0.72;
      pathD = `M ${{x + w}} ${{y1}} C ${{x + w + loopW}} ${{y1 - 25}}, ${{x + w + loopW}} ${{y2 + 25}}, ${{x + w}} ${{y2}}`;
      labelX = x + w + loopW + 12;
      labelY = y + h * 0.5;
    }} else {{
      const start = getNodeEdgeRect(getCenter(fromEl), getCenter(toEl), fromEl);
      const end = getNodeEdgeRect(getCenter(toEl), getCenter(fromEl), toEl);

      // Desplazamiento para conexiones paralelas
      let offset = 0;
      if (c.pair_total > 1) {{
        offset = (c.pair_index - (c.pair_total - 1) / 2) * 26;
      }}

      if (end.x >= start.x) {{
        // Hacia adelante (Left to Right o misma columna)
        const dx = Math.abs(end.x - start.x);
        const curvature = Math.min(Math.max(dx * 0.45, 45), 180);
        const cp1x = start.x + curvature;
        const cp1y = start.y + offset;
        const cp2x = end.x - curvature;
        const cp2y = end.y + offset;
        pathD = `M ${{start.x}} ${{start.y}} C ${{cp1x}} ${{cp1y}}, ${{cp2x}} ${{cp2y}}, ${{end.x}} ${{end.y}}`;
        labelX = 0.125 * start.x + 0.375 * cp1x + 0.375 * cp2x + 0.125 * end.x;
        labelY = 0.125 * start.y + 0.375 * cp1y + 0.375 * cp2y + 0.125 * end.y;
      }} else {{
        // Hacia atrás (Right to Left): Arqueo superior/inferior para evitar atravesar nodos
        const dx = Math.abs(end.x - start.x);
        const arcHeight = Math.min(Math.max(dx * 0.22, 60), 180);
        const dir = (start.y > 650) ? 1 : -1;
        const cp1x = start.x - 30;
        const cp1y = start.y + (dir * arcHeight) + offset;
        const cp2x = end.x + 30;
        const cp2y = end.y + (dir * arcHeight) + offset;
        pathD = `M ${{start.x}} ${{start.y}} C ${{cp1x}} ${{cp1y}}, ${{cp2x}} ${{cp2y}}, ${{end.x}} ${{end.y}}`;
        labelX = 0.5 * (start.x + end.x);
        labelY = 0.5 * (cp1y + cp2y);
      }}
    }}

    // Path transparente ancho para interacción fácil
    const hitPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    hitPath.setAttribute('d', pathD);
    hitPath.setAttribute('class', 'conn-hit');
    g.appendChild(hitPath);

    // Path visual
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', pathD);
    let marker = 'arrow';
    if (c.type === 'dashed') marker = 'arrow-dashed';
    if (c.type === 'thick') marker = 'arrow-thick';
    if (c.from === c.to) marker = 'arrow-self';
    path.setAttribute('class', `conn-path ${{c.type}}`);
    path.setAttribute('marker-end', `url(#${{marker}})`);
    g.appendChild(path);

    // Etiqueta visual
    if (c.label) {{
      const lblG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      lblG.setAttribute('class', 'conn-label-group');

      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', labelX);
      text.setAttribute('y', labelY);
      text.setAttribute('class', 'conn-label-text');
      
      const displayLabel = c.label.length > 36 ? c.label.substring(0, 34) + '…' : c.label;
      text.textContent = displayLabel;

      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      const w = displayLabel.length * 6.2 + 12;
      rect.setAttribute('x', labelX - w/2);
      rect.setAttribute('y', labelY - 8.5);
      rect.setAttribute('width', w);
      rect.setAttribute('height', 17);
      rect.setAttribute('class', 'conn-label-bg');

      lblG.appendChild(rect);
      lblG.appendChild(text);
      g.appendChild(lblG);
    }}

    // Eventos de arista (Tooltip y Hover)
    g.addEventListener('mouseenter', (e) => {{
      hoveredEdgeId = c.id;
      path.classList.add('hovered');
      showEdgeTooltip(e, c);
    }});
    g.addEventListener('mousemove', (e) => {{
      moveEdgeTooltip(e);
    }});
    g.addEventListener('mouseleave', () => {{
      hoveredEdgeId = null;
      path.classList.remove('hovered');
      hideEdgeTooltip();
    }});

    svgEl.appendChild(g);
  }});

  updateVisualFocus();
}}

// Tooltip flotante de enlaces
function showEdgeTooltip(e, c) {{
  const typeMap = {{
    'thick': 'Flujo Principal (==>)',
    'arrow': 'Transición / Método (-->)',
    'dashed': 'Guarda / Regla / Auditoría (-.->)',
    'line': 'Asociación (---)'
  }};
  edgeTtEndpoints.textContent = `${{c.from}} ➔ ${{c.to}}`;
  edgeTtType.textContent = typeMap[c.type] || c.type;
  edgeTtLabel.textContent = c.label || '(Sin etiqueta de acción)';
  edgeTooltip.classList.add('show');
  moveEdgeTooltip(e);
}}

function moveEdgeTooltip(e) {{
  edgeTooltip.style.left = `${{e.clientX + 16}}px`;
  edgeTooltip.style.top = `${{e.clientY + 12}}px`;
}}

function hideEdgeTooltip() {{
  edgeTooltip.classList.remove('show');
}}

// Lógica de Enfoque y Trazabilidad Visual
function setFocusNode(nodeId) {{
  lockedFocusNodeId = nodeId;
  if (nodeId) {{
    const n = nodesData.find(x => x.id === nodeId);
    focusNodeTitle.textContent = `${{n.title}} (${{n.id}})`;
    const inc = connectionsData.filter(c => c.to === nodeId && visibleTypes[c.type]);
    const out = connectionsData.filter(c => c.from === nodeId && visibleTypes[c.type]);
    focusInCount.textContent = inc.length;
    focusOutCount.textContent = out.length;
    focusBanner.classList.add('show');
  }} else {{
    focusBanner.classList.remove('show');
  }}
  updateVisualFocus();
}}

focusClearBtn.addEventListener('click', () => setFocusNode(null));

function updateVisualFocus() {{
  const activeId = lockedFocusNodeId || hoveredNodeId;

  const connGroups = svgEl.querySelectorAll('.conn-group');
  const allNodes = Object.values(domNodes);

  if (!activeId) {{
    // Vista Normal: Sin foco
    allNodes.forEach(el => {{
      el.classList.remove('dimmed', 'highlight', 'neighbor-in', 'neighbor-out');
    }});
    connGroups.forEach(g => {{
      const path = g.querySelector('.conn-path');
      path.classList.remove('dimmed', 'highlight-incoming', 'highlight-outgoing', 'highlight-self');
      
      let defaultMarker = 'arrow';
      const type = g.getAttribute('data-type');
      if (type === 'dashed') defaultMarker = 'arrow-dashed';
      if (type === 'thick') defaultMarker = 'arrow-thick';
      if (g.getAttribute('data-from') === g.getAttribute('data-to')) defaultMarker = 'arrow-self';
      path.setAttribute('marker-end', `url(#${{defaultMarker}})`);

      const lbl = g.querySelector('.conn-label-group');
      if (lbl) {{
        if (currentLabelMode === 'all') lbl.classList.remove('hidden', 'active');
        else if (currentLabelMode === 'primary') {{
          const isPrimary = g.getAttribute('data-type') === 'thick';
          lbl.classList.toggle('hidden', !isPrimary);
        }} else {{
          lbl.classList.add('hidden'); // 'smart' y 'none' ocultan por defecto
        }}
      }}
    }});
    return;
  }}

  // Vista Focalizada: Aislar el nodo activo
  const incoming = new Set();
  const outgoing = new Set();

  connectionsData.forEach(c => {{
    if (!visibleTypes[c.type]) return;
    if (c.to === activeId && c.from !== activeId) incoming.add(c.from);
    if (c.from === activeId && c.to !== activeId) outgoing.add(c.to);
  }});

  // Nodos
  allNodes.forEach(el => {{
    const id = el.id;
    if (id === activeId) {{
      el.classList.add('highlight');
      el.classList.remove('dimmed', 'neighbor-in', 'neighbor-out');
    }} else if (incoming.has(id)) {{
      el.classList.add('neighbor-in');
      el.classList.remove('dimmed', 'highlight', 'neighbor-out');
    }} else if (outgoing.has(id)) {{
      el.classList.add('neighbor-out');
      el.classList.remove('dimmed', 'highlight', 'neighbor-in');
    }} else {{
      el.classList.add('dimmed');
      el.classList.remove('highlight', 'neighbor-in', 'neighbor-out');
    }}
  }});

  // Conexiones
  connGroups.forEach(g => {{
    const from = g.getAttribute('data-from');
    const to = g.getAttribute('data-to');
    const path = g.querySelector('.conn-path');
    const lbl = g.querySelector('.conn-label-group');

    path.classList.remove('dimmed', 'highlight-incoming', 'highlight-outgoing', 'highlight-self');
    if (lbl) lbl.classList.remove('active');

    if (from === activeId && to === activeId) {{
      path.classList.add('highlight-self');
      path.setAttribute('marker-end', 'url(#arrow-self)');
      svgEl.appendChild(g); // Traer al frente
      if (lbl && currentLabelMode !== 'none') lbl.classList.remove('hidden'), lbl.classList.add('active');
    }} else if (to === activeId) {{
      path.classList.add('highlight-incoming');
      path.setAttribute('marker-end', 'url(#arrow-incoming)');
      svgEl.appendChild(g);
      if (lbl && currentLabelMode !== 'none') lbl.classList.remove('hidden'), lbl.classList.add('active');
    }} else if (from === activeId) {{
      path.classList.add('highlight-outgoing');
      path.setAttribute('marker-end', 'url(#arrow-outgoing)');
      svgEl.appendChild(g);
      if (lbl && currentLabelMode !== 'none') lbl.classList.remove('hidden'), lbl.classList.add('active');
    }} else {{
      path.classList.add('dimmed');
      if (lbl) lbl.classList.add('hidden');
    }}
  }});
}}

// Drag & Drop de Nodos
let dragTarget = null, startDragX = 0, startDragY = 0, initialNodeX = 0, initialNodeY = 0;
world.addEventListener('mousedown', e => {{
  const el = e.target.closest('.node');
  if (!el) return;
  dragTarget = el;
  startDragX = e.clientX;
  startDragY = e.clientY;
  initialNodeX = parseFloat(el.dataset.x);
  initialNodeY = parseFloat(el.dataset.y);
  el.classList.add('dragging');
  e.stopPropagation();
}});

document.addEventListener('mousemove', e => {{
  if (!dragTarget) return;
  const dx = (e.clientX - startDragX) / zoom;
  const dy = (e.clientY - startDragY) / zoom;
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {{
    dragTarget.dataset.wasDragged = '1';
  }}
  const newX = Math.max(10, initialNodeX + dx);
  const newY = Math.max(10, initialNodeY + dy);
  dragTarget.dataset.x = newX;
  dragTarget.dataset.y = newY;
  dragTarget.style.left = `${{newX}}px`;
  dragTarget.style.top = `${{newY}}px`;
  drawConnections();
}});

document.addEventListener('mouseup', () => {{
  if (dragTarget) {{
    dragTarget.classList.remove('dragging');
    dragTarget = null;
  }}
}});

// Paneo del Canvas
let isPanning = false, startPanX = 0, startPanY = 0;
canvas.addEventListener('mousedown', e => {{
  if (e.target.closest('.node') || e.target.closest('#modalCard') || e.target.closest('#zoomControls')) return;
  isPanning = true;
  startPanX = e.clientX - panX;
  startPanY = e.clientY - panY;
  canvas.classList.add('grabbing');
}});
document.addEventListener('mousemove', e => {{
  if (!isPanning) return;
  panX = e.clientX - startPanX;
  panY = e.clientY - startPanY;
  applyTransform();
}});
document.addEventListener('mouseup', () => {{
  isPanning = false;
  canvas.classList.remove('grabbing');
}});

// Zoom con Rueda Centrado en Cursor
canvas.addEventListener('wheel', e => {{
  e.preventDefault();
  const factor = e.deltaY < 0 ? 1.12 : 0.89;
  zoomAt(e.clientX, e.clientY, factor);
}}, {{ passive: false }});

// Botones de Zoom
document.getElementById('zoomInBtn').addEventListener('click', () => {{
  const rect = canvas.getBoundingClientRect();
  zoomAt(rect.left + rect.width/2, rect.top + rect.height/2, 1.2);
}});
document.getElementById('zoomOutBtn').addEventListener('click', () => {{
  const rect = canvas.getBoundingClientRect();
  zoomAt(rect.left + rect.width/2, rect.top + rect.height/2, 0.83);
}});
document.getElementById('zoomResetBtn').addEventListener('click', () => {{
  zoom = 1.0;
  panX = 40; panY = 20;
  applyTransform();
}});
document.getElementById('zoomFitBtn').addEventListener('click', () => {{
  zoom = 0.65;
  panX = 20; panY = 20;
  applyTransform();
}});

// Selector de Modos de Etiqueta
document.querySelectorAll('.btn-label').forEach(b => {{
  b.addEventListener('click', () => {{
    document.querySelectorAll('.btn-label').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    currentLabelMode = b.getAttribute('data-label-mode');
    updateVisualFocus();
  }});
}});

// Filtro de Tipos de Conexión (Chips)
document.querySelectorAll('.btn-chip').forEach(b => {{
  b.addEventListener('click', () => {{
    const type = b.getAttribute('data-filter-type');
    visibleTypes[type] = !visibleTypes[type];
    b.classList.toggle('active', visibleTypes[type]);
    drawConnections();
  }});
}});

// Filtro por Subgrafo
document.addEventListener('click', e => {{
  const btn = e.target.closest('#subgraphFilters .btn');
  if (!btn) return;
  document.querySelectorAll('#subgraphFilters .btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const sub = btn.getAttribute('data-sub');

  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    el.style.display = (sub === 'all' || n.subgraph === sub) ? 'block' : 'none';
  }});

  subgraphsData.forEach(s => {{
    const z = document.getElementById(`subzone_${{s.id}}`);
    if (z) z.style.display = (sub === 'all' || s.id === sub) ? 'block' : 'none';
  }});

  setFocusNode(null);
  drawConnections();
}});

// Búsqueda en vivo
searchBox.addEventListener('input', e => {{
  const t = e.target.value.toLowerCase().trim();
  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    const match = !t || n.id.toLowerCase().includes(t) || n.title.toLowerCase().includes(t);
    el.classList.toggle('highlight', !!t && match);
    el.classList.toggle('dimmed', !!t && !match);
  }});
}});

// Restaurar Vista
document.getElementById('resetBtn').addEventListener('click', () => {{
  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    el.dataset.x = initialPositions[n.id].x;
    el.dataset.y = initialPositions[n.id].y;
    el.style.left = `${{initialPositions[n.id].x}}px`;
    el.style.top = `${{initialPositions[n.id].y}}px`;
    el.classList.remove('highlight', 'dimmed', 'neighbor-in', 'neighbor-out');
  }});
  searchBox.value = '';
  document.querySelector('#subgraphFilters .btn[data-sub="all"]').click();
  setFocusNode(null);
  panX = 40; panY = 20; zoom = 0.95;
  applyTransform();
  drawConnections();
}});

// Tecla ESC para liberar foco o cerrar modal
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{
    if (modalOverlay.classList.contains('show')) closeModal();
    else if (lockedFocusNodeId) setFocusNode(null);
  }}
}});

// Minimapa
function updateMinimap() {{
  const worldW = 5000, worldH = 3000;
  const mmW = 220, mmH = 110;
  const scaleX = mmW / worldW, scaleY = mmH / worldH;
  const vpW = Math.min((canvas.clientWidth / zoom) * scaleX, mmW);
  const vpH = Math.min((canvas.clientHeight / zoom) * scaleY, mmH);
  const vpX = Math.max(0, (-panX / zoom) * scaleX);
  const vpY = Math.max(0, (-panY / zoom) * scaleY);
  minimapViewport.style.width = `${{vpW}}px`;
  minimapViewport.style.height = `${{vpH}}px`;
  minimapViewport.style.left = `${{vpX}}px`;
  minimapViewport.style.top = `${{vpY}}px`;
}}

// Modal Técnico
function openModal(n) {{
  modalTitle.textContent = `${{n.title}} (${{n.id}})`;
  const inc = connectionsData.filter(c => c.to === n.id);
  const out = connectionsData.filter(c => c.from === n.id);

  modalBody.innerHTML = `
    <div class="modal-sec">
      <div class="modal-sec-title">📍 Subgrafo / Capa</div>
      <p style="font-size:13px;color:#f8fafc;">${{n.subgraph}}</p>
    </div>
    ${{n.raw_label ? `
    <div class="modal-sec">
      <div class="modal-sec-title">📝 Descripción / Semántica</div>
      <p style="font-size:13px;color:#cbd5e1;line-height:1.5;">${{n.raw_label.split('<br/>').join(' · ').split('<br>').join(' · ')}}</p>
    </div>` : ''}}
    <div class="modal-sec">
      <div class="modal-sec-title">🟢 Conexiones Entrantes (${{inc.length}})</div>
      <ul class="modal-list">${{inc.length ? inc.map(c => `<li><strong>${{c.from}}</strong> ➔ <span style="color:#38bdf8">${{c.label || '(invoca)'}}</span></li>`).join('') : '<li style="color:#64748b">Ninguna</li>'}}</ul>
    </div>
    <div class="modal-sec">
      <div class="modal-sec-title">🟠 Conexiones Salientes (${{out.length}})</div>
      <ul class="modal-list">${{out.length ? out.map(c => `<li>➔ <strong>${{c.to}}</strong> <span style="color:#f59e0b">(${{c.label || '(invoca)'}})</span></li>`).join('') : '<li style="color:#64748b">Ninguna</li>'}}</ul>
    </div>
  `;
  modalOverlay.classList.add('show');
}}

function closeModal() {{ modalOverlay.classList.remove('show'); }}

function initDiagram() {{
  applyTransform();
  drawConnections();
}}

if (document.readyState === 'loading') {{
  window.addEventListener('DOMContentLoaded', initDiagram);
}} else {{
  initDiagram();
}}

window.addEventListener('resize', () => {{
  applyTransform();
  drawConnections();
}});
</script>
</body>
</html>
"""
        return html_template
