import json
from typing import List, Dict, Any

class SingleFileBundler:
    """Empaqueta nodos, zonas y conexiones en una aplicación web autónoma HTML5+SVG+Vanilla JS."""

    PALETTE = [
        {"border": "#38bdf8", "bg": "#0c4a6e", "text": "#38bdf8"},
        {"border": "#3b82f6", "bg": "#1e3a8a", "text": "#60a5fa"},
        {"border": "#8b5cf6", "bg": "#4c1d95", "text": "#a78bfa"},
        {"border": "#10b981", "bg": "#064e3b", "text": "#34d399"},
        {"border": "#f59e0b", "bg": "#78350f", "text": "#fbbf24"},
        {"border": "#ef4444", "bg": "#7f1d1d", "text": "#f87171"},
        {"border": "#ec4899", "bg": "#831843", "text": "#f472b6"},
    ]

    def bundle(self, title: str, nodes: List[Dict[str, Any]], connections: List[Dict[str, Any]], subgraphs: List[Dict[str, Any]]) -> str:
        # Asignar colores por subgrafo
        sub_colors = {}
        for idx, sub in enumerate(subgraphs):
            color = self.PALETTE[idx % len(self.PALETTE)]
            sub_colors[sub["id"]] = color

        # Construir HTML de tarjetas para cada nodo
        for n in nodes:
            sub_id = n.get("subgraph", "General")
            color = sub_colors.get(sub_id, self.PALETTE[0])
            n["color"] = color

            icon = n.get("meta", {}).get("icon", "📦")
            meta_desc = n.get("meta", {}).get("desc", "")
            meta_file = n.get("meta", {}).get("archivo", "")
            meta_pattern = n.get("meta", {}).get("patron", "")

            n["html"] = f"""
            <div class="comp-card" style="border-color:{color['border']};">
                <div class="comp-header" style="background:{color['bg']};">
                    <span class="comp-icon">{icon}</span>
                    <div class="comp-title-group">
                        <span class="comp-id">{n['id']}</span>
                        <span class="comp-name">{n['title']}</span>
                    </div>
                </div>
                <div class="comp-body">
                    <span class="comp-sub">{sub_id}</span>
                    <span class="comp-tag">{meta_pattern or n.get('shape', 'node')}</span>
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
    height: 52px;
    background: #0f172a;
    border-bottom: 1px solid #1e293b;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 12px;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  #topbar h1 {{
    font-size: 14px;
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
    width: 250px;
    padding: 6px 12px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    font-size: 12px;
    outline: none;
    transition: border-color 0.2s;
  }}
  #searchBox:focus {{ border-color: #38bdf8; }}
  
  .filter-group {{
    display: flex;
    gap: 6px;
    overflow-x: auto;
  }}
  .btn {{
    padding: 5px 11px;
    border-radius: 5px;
    border: 1px solid #334155;
    background: #1e293b;
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
  }}
  .btn:hover {{ background: #273549; color: #f1f5f9; }}
  .btn.active {{
    background: #0369a1;
    border-color: #38bdf8;
    color: #ffffff;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
  }}
  .btn-danger {{ border-color: #dc2626; color: #f87171; }}
  .btn-danger:hover {{ background: #450a0a; }}

  #canvas {{
    position: absolute;
    top: 52px; left: 0; right: 0; bottom: 0;
    overflow: auto;
    cursor: grab;
    background: radial-gradient(circle at 1px 1px, #172033 1px, transparent 0);
    background-size: 32px 32px;
  }}
  #canvas.grabbing {{ cursor: grabbing; }}
  
  #world {{
    position: relative;
    width: 4500px;
    height: 2500px;
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
    border: 1.5px dashed;
    border-radius: 12px;
    pointer-events: none;
    z-index: 2;
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
    background: #0f172a;
    border: 1px solid;
  }}

  .node {{
    position: absolute;
    z-index: 10;
    cursor: move;
    user-select: none;
    transition: transform 0.1s, box-shadow 0.2s, opacity 0.2s;
  }}
  .node.highlight {{
    box-shadow: 0 0 25px #f59e0b !important;
    border-radius: 8px;
  }}
  .node.dimmed {{ opacity: 0.18; }}

  .comp-card {{
    background: #0f172a;
    border: 2px solid;
    border-radius: 8px;
    width: 280px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    overflow: hidden;
    cursor: pointer;
  }}
  .comp-header {{
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}
  .comp-icon {{ font-size: 20px; }}
  .comp-title-group {{ display: flex; flex-direction: column; overflow: hidden; }}
  .comp-id {{ font-size: 10px; font-family: monospace; color: #94a3b8; font-weight: 700; }}
  .comp-name {{ font-size: 13px; font-weight: 700; color: #f8fafc; line-height: 1.2; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }}
  .comp-body {{
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.6);
  }}
  .comp-sub {{ font-size: 10px; color: #94a3b8; }}
  .comp-tag {{
    font-size: 9px;
    background: #1e293b;
    color: #cbd5e1;
    padding: 2px 6px;
    border-radius: 3px;
    border: 1px solid #334155;
  }}

  .conn-path {{
    fill: none;
    stroke: #38bdf8;
    stroke-width: 1.8;
  }}
  .conn-path.dashed {{ stroke: #a78bfa; stroke-dasharray: 6, 4; }}
  .conn-path.thick {{ stroke: #10b981; stroke-width: 2.4; }}
  .conn-label-bg {{
    fill: #0f172a;
    stroke: #334155;
    stroke-width: 1;
    rx: 4;
  }}
  .conn-label-text {{
    font-size: 9.5px;
    font-family: monospace;
    font-weight: 600;
    fill: #94a3b8;
    text-anchor: middle;
    dominant-baseline: middle;
  }}

  #modalOverlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(4, 7, 13, 0.8);
    backdrop-filter: blur(4px);
    z-index: 2000;
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
  #modalTitle {{ font-size: 16px; font-weight: 700; color: #38bdf8; }}
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
  .modal-list li {{ font-size: 12px; color: #cbd5e1; padding: 3px 0; }}

  #minimap {{
    position: fixed;
    bottom: 16px; right: 16px;
    width: 220px; height: 110px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    z-index: 900;
    overflow: hidden;
  }}
  #minimapViewport {{
    position: absolute;
    border: 1px solid #38bdf8;
    background: rgba(56, 189, 248, 0.2);
    pointer-events: none;
  }}
</style>
</head>
<body>

<div id="topbar">
  <h1><span>{title}</span> <span class="badge">Interactivo Air-Gapped</span></h1>
  <input type="text" id="searchBox" placeholder="Buscar componente o módulo...">
  <div class="filter-group" id="filterGroup">
    <button class="btn active" data-sub="all">Todos</button>
  </div>
  <button class="btn btn-danger" id="resetBtn">Restaurar Vista</button>
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
      </defs>
    </svg>
  </div>
</div>

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
const filterGroup = document.getElementById('filterGroup');

const domNodes = {{}};
const initialPositions = {{}};

// Renderizar zonas de subgrafos
subgraphsData.forEach((s, idx) => {{
  const z = document.createElement('div');
  z.className = 'subgraph-zone';
  z.style.left = `${{s.x}}px`;
  z.style.top = `${{s.y}}px`;
  z.style.width = `${{s.width}}px`;
  z.style.height = `${{s.height}}px`;
  z.style.borderColor = '#334155';
  z.style.background = 'rgba(255,255,255,0.015)';

  const lbl = document.createElement('span');
  lbl.className = 'subgraph-label';
  lbl.textContent = s.title;
  lbl.style.color = '#38bdf8';
  lbl.style.borderColor = '#334155';
  z.appendChild(lbl);
  world.appendChild(z);

  // Crear boton de filtro
  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.setAttribute('data-sub', s.id);
  btn.textContent = s.title;
  filterGroup.appendChild(btn);
}});

// Renderizar Nodos
nodesData.forEach(n => {{
  const el = document.createElement('div');
  el.id = n.id;
  el.className = 'node';
  el.style.left = `${{n.x}}px`;
  el.style.top = `${{n.y}}px`;
  el.innerHTML = n.html;
  initialPositions[n.id] = {{ x: n.x, y: n.y }};

  el.addEventListener('click', () => {{
    if (!el.dataset.wasDragged) openModal(n);
    delete el.dataset.wasDragged;
  }});

  world.appendChild(el);
  domNodes[n.id] = el;
}});

// Matematica perimetrica
function getNodeEdgeRect(fromCenter, toCenter, el) {{
  const w = el.offsetWidth / 2;
  const h = el.offsetHeight / 2;
  const cx = parseInt(el.style.left) + w;
  const cy = parseInt(el.style.top) + h;
  const angle = Math.atan2(toCenter.y - fromCenter.y, toCenter.x - fromCenter.x);
  const absCos = Math.abs(Math.cos(angle)), absSin = Math.abs(Math.sin(angle));
  const dist = (absCos * h > absSin * w) ? (w / absCos) : (h / absSin);
  return {{ x: cx + Math.cos(angle) * dist, y: cy + Math.sin(angle) * dist }};
}}

function getCenter(el) {{
  return {{ x: parseInt(el.style.left) + el.offsetWidth / 2, y: parseInt(el.style.top) + el.offsetHeight / 2 }};
}}

function drawConnections() {{
  const defs = svgEl.querySelector('defs');
  svgEl.innerHTML = '';
  svgEl.appendChild(defs);

  connectionsData.forEach(c => {{
    const fromEl = domNodes[c.from];
    const toEl = domNodes[c.to];
    if (!fromEl || !toEl) return;
    if (fromEl.style.display === 'none' || toEl.style.display === 'none') return;

    const start = getNodeEdgeRect(getCenter(fromEl), getCenter(toEl), fromEl);
    const end = getNodeEdgeRect(getCenter(toEl), getCenter(fromEl), toEl);

    const dx = Math.abs(end.x - start.x);
    const curvature = Math.min(Math.max(dx * 0.45, 40), 160);
    const cp1x = start.x + (end.x > start.x ? curvature : -curvature);
    const cp2x = end.x - (end.x > start.x ? curvature : -curvature);

    const d = `M ${{start.x}} ${{start.y}} C ${{cp1x}} ${{start.y}}, ${{cp2x}} ${{end.y}}, ${{end.x}} ${{end.y}}`;

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    let marker = 'arrow';
    if (c.type === 'dashed') marker = 'arrow-dashed';
    if (c.type === 'thick') marker = 'arrow-thick';
    path.setAttribute('class', `conn-path ${{c.type}}`);
    path.setAttribute('marker-end', `url(#${{marker}})`);
    svgEl.appendChild(path);

    if (c.label) {{
      const midX = 0.125 * start.x + 0.375 * cp1x + 0.375 * cp2x + 0.125 * end.x;
      const midY = 0.125 * start.y + 0.375 * start.y + 0.375 * end.y + 0.125 * end.y;
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', midX); text.setAttribute('y', midY);
      text.setAttribute('class', 'conn-label-text');
      text.textContent = c.label;

      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      const w = c.label.length * 6.5 + 10;
      rect.setAttribute('x', midX - w/2); rect.setAttribute('y', midY - 9);
      rect.setAttribute('width', w); rect.setAttribute('height', 18);
      rect.setAttribute('class', 'conn-label-bg');
      g.appendChild(rect); g.appendChild(text);
      svgEl.appendChild(g);
    }}
  }});
  updateMinimap();
}}

// Drag & Drop
let dragTarget = null, offX = 0, offY = 0;
world.addEventListener('mousedown', e => {{
  const el = e.target.closest('.node');
  if (!el) return;
  dragTarget = el;
  offX = e.clientX - el.getBoundingClientRect().left;
  offY = e.clientY - el.getBoundingClientRect().top;
  el.style.zIndex = 100;
  e.preventDefault();
}});

document.addEventListener('mousemove', e => {{
  if (!dragTarget) return;
  dragTarget.dataset.wasDragged = '1';
  const worldRect = world.getBoundingClientRect();
  dragTarget.style.left = `${{Math.max(10, e.clientX - worldRect.left - offX + canvas.scrollLeft)}}px`;
  dragTarget.style.top = `${{Math.max(10, e.clientY - worldRect.top - offY + canvas.scrollTop)}}px`;
  drawConnections();
}});

document.addEventListener('mouseup', () => {{ if (dragTarget) {{ dragTarget.style.zIndex = 10; dragTarget = null; }} }});

// Paneo
let isPanning = false, panX = 0, panY = 0;
canvas.addEventListener('mousedown', e => {{
  if (e.target.closest('.node') || e.target.closest('#modalCard')) return;
  isPanning = true; panX = e.clientX + canvas.scrollLeft; panY = e.clientY + canvas.scrollTop;
  canvas.classList.add('grabbing');
}});
document.addEventListener('mousemove', e => {{
  if (!isPanning) return;
  canvas.scrollLeft = panX - e.clientX; canvas.scrollTop = panY - e.clientY;
  updateMinimap();
}});
document.addEventListener('mouseup', () => {{ isPanning = false; canvas.classList.remove('grabbing'); }});

// Filtros
document.addEventListener('click', e => {{
  const btn = e.target.closest('.filter-group .btn');
  if (!btn) return;
  document.querySelectorAll('.filter-group .btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const sub = btn.getAttribute('data-sub');
  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    el.style.display = (sub === 'all' || n.subgraph === sub) ? 'block' : 'none';
  }});
  drawConnections();
}});

// Busqueda
searchBox.addEventListener('input', e => {{
  const t = e.target.value.toLowerCase().trim();
  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    const match = !t || n.id.toLowerCase().includes(t) || n.title.toLowerCase().includes(t);
    el.classList.toggle('highlight', !!t && match);
    el.classList.toggle('dimmed', !!t && !match);
  }});
}});

// Reset
document.getElementById('resetBtn').addEventListener('click', () => {{
  nodesData.forEach(n => {{
    const el = domNodes[n.id];
    el.style.left = `${{initialPositions[n.id].x}}px`;
    el.style.top = `${{initialPositions[n.id].y}}px`;
    el.classList.remove('highlight', 'dimmed');
  }});
  searchBox.value = '';
  document.querySelector('.filter-group .btn[data-sub="all"]').click();
  canvas.scrollLeft = 0; canvas.scrollTop = 0;
  drawConnections();
}});

function updateMinimap() {{
  const scaleX = 220 / 4500, scaleY = 110 / 2500;
  minimapViewport.style.width = `${{Math.min(canvas.clientWidth * scaleX, 220)}}px`;
  minimapViewport.style.height = `${{Math.min(canvas.clientHeight * scaleY, 110)}}px`;
  minimapViewport.style.left = `${{canvas.scrollLeft * scaleX}}px`;
  minimapViewport.style.top = `${{canvas.scrollTop * scaleY}}px`;
}}

function openModal(n) {{
  modalTitle.textContent = `${{n.title}} (${{n.id}})`;
  const inc = connectionsData.filter(c => c.to === n.id);
  const out = connectionsData.filter(c => c.from === n.id);

  modalBody.innerHTML = `
    <div class="modal-sec">
      <div class="modal-sec-title">📍 Subgrafo / Capa</div>
      <p style="font-size:13px;color:#f8fafc;">${{n.subgraph}}</p>
    </div>
    ${{n.meta && n.meta.desc ? `
    <div class="modal-sec">
      <div class="modal-sec-title">📝 Descripción</div>
      <p style="font-size:13px;color:#cbd5e1;line-height:1.5;">${{n.meta.desc}}</p>
    </div>` : ''}}
    ${{n.meta && n.meta.archivo ? `
    <div class="modal-sec">
      <div class="modal-sec-title">📁 Archivo / Paquete</div>
      <code style="font-size:12px;background:#0b1120;padding:4px 8px;border-radius:4px;color:#38bdf8;">${{n.meta.archivo}}</code>
    </div>` : ''}}
    <div class="modal-sec">
      <div class="modal-sec-title">🔗 Conexiones Entrantes</div>
      <ul class="modal-list">${{inc.length ? inc.map(c => `<li><strong>${{c.from}}</strong> ➔ ${{c.label || 'invoca'}}</li>`).join('') : '<li style="color:#64748b">Ninguna</li>'}}</ul>
    </div>
    <div class="modal-sec">
      <div class="modal-sec-title">➡️ Conexiones Salientes</div>
      <ul class="modal-list">${{out.length ? out.map(c => `<li>➔ <strong>${{c.to}}</strong> (${{c.label || 'invoca'}})</li>`).join('') : '<li style="color:#64748b">Ninguna</li>'}}</ul>
    </div>
  `;
  modalOverlay.classList.add('show');
}}

function closeModal() {{ modalOverlay.classList.remove('show'); }}

window.addEventListener('DOMContentLoaded', () => {{
  drawConnections();
}});
window.addEventListener('resize', drawConnections);
</script>
</body>
</html>
"""
        return html_template
