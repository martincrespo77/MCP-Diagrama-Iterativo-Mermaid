from pathlib import Path
from typing import Optional, Dict, Any

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP

from core.parser import MermaidParser
from core.layout import SpatialLayoutEngine
from core.bundler import SingleFileBundler
from core.scanner import CodebaseScanner


# Instancia FastMCP / MCPServer
mcp = FastMCP(
    "MCP-Diagrama-Iterativo-Mermaid",
    instructions="Servidor MCP para inspeccion de proyectos y generacion de diagramas interactivos autonomos (HTML5 + SVG + JS, 100% Air-Gapped)."
)


parser = MermaidParser()
layout_engine = SpatialLayoutEngine()
bundler = SingleFileBundler()
scanner = CodebaseScanner()

@mcp.tool()
def analizar_proyecto(project_path: str) -> dict:
    """
    Inspecciona la estructura de un proyecto en el disco local o repositorio.
    Detecta el stack tecnológico, las capas arquitectónicas (Frontend, API, Servicios, Dominio, Base de datos),
    archivos representativos y busca si ya existen diagramas (.mmd, .puml).
    
    Args:
        project_path: Ruta absoluta al proyecto o repositorio (ej: 'D:/2026/MiProyecto').
    """
    return scanner.scan(project_path)

@mcp.tool()
def generar_diagrama_desde_mermaid(mermaid_code: str, output_path: str, titulo: str = "Diagrama Interactivo") -> str:
    """
    Compila cualquier especificación textual en sintaxis Mermaid (flowchart, graph, erDiagram, classDiagram)
    en una aplicación web interactiva de un solo archivo (Single-File Bundle: HTML5 + SVG + Vanilla JS).
    
    Características:
    - 100% Air-Gapped (cero CDNs, cero npm, funciona sin conexión a internet).
    - Conectores dinámicos SVG con cálculo perimétrico trigonométrico exacto (atan2).
    - Arrastrar y soltar (drag and drop) de nodos con redibujado en tiempo real.
    - Paneo libre, zoom, minimapa y filtros por capas/subgrafos.
    - Modal de inspección de detalles de cada nodo.
    
    Args:
        mermaid_code: Código Mermaid DSL (ej: 'graph LR\n subgraph A...\n end').
        output_path: Ruta absoluta donde se guardará el archivo .html generado.
        titulo: Título visual que aparecerá en la barra superior del diagrama.
    """
    nodes, connections, subgraphs = parser.parse(mermaid_code)
    node_list, subgraph_zones = layout_engine.compute_layout(nodes, connections, subgraphs)
    html_bundle = bundler.bundle(titulo, node_list, connections, subgraph_zones)

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html_bundle, encoding="utf-8")

    return f"Diagrama interactivo generado exitosamente en: {str(out_file)} ({len(node_list)} nodos, {len(connections)} conexiones)"

@mcp.tool()
def crear_diagrama_proyecto(project_path: str, output_path: str = "", titulo: str = "") -> str:
    """
    Herramienta integral 'Todo en Uno':
    Analiza un proyecto, detecta sus capas y componentes, sintetiza su arquitectura y genera
    directamente el diagrama interactivo autónomo (.html) listo para ser abierto en cualquier navegador.
    
    Args:
        project_path: Ruta absoluta al proyecto que se desea diagramar.
        output_path: (Opcional) Ruta del archivo .html destino. Por defecto se guarda en 'docs/diagrama_interactivo.html' del proyecto.
        titulo: (Opcional) Título del diagrama. Si se omite, usa el nombre de la carpeta del proyecto.
    """
    scan_info = scanner.scan(project_path)
    proj_name = scan_info["project_name"]
    final_title = titulo or f"Arquitectura de Componentes — {proj_name}"

    # Si el proyecto ya tiene un diagrama mmd en docs, lo priorizamos
    mermaid_code = ""
    if scan_info["existing_diagrams"]:
        for d in scan_info["existing_diagrams"]:
            if "component" in d.lower() or "arquitectura" in d.lower() or "06_" in d.lower():
                full_d_path = Path(project_path) / d
                mermaid_code = full_d_path.read_text(encoding="utf-8", errors="ignore")
                break

    if not mermaid_code:
        # Generar arquitectura inferida a partir del escaneo de carpetas
        mermaid_code = scanner.generate_mermaid_from_scan(scan_info)

    # Determinar destino
    if not output_path:
        docs_dir = Path(project_path) / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        out_file = docs_dir / f"diagrama_arquitectura_{proj_name.lower()}.html"
    else:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

    return generar_diagrama_desde_mermaid(mermaid_code, str(out_file), final_title)

@mcp.tool()
def convertir_archivo_mermaid(input_file: str, output_path: str = "") -> str:
    """
    Convierte un archivo existente con extensión .mmd o .mermaid en una aplicación web interactiva HTML5.
    
    Args:
        input_file: Ruta absoluta al archivo .mmd o .mermaid.
        output_path: (Opcional) Ruta del .html resultante. Si no se especifica, se genera junto al archivo original.
    """
    inp = Path(input_file).resolve()
    if not inp.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_file}")

    content = inp.read_text(encoding="utf-8", errors="ignore")
    if not output_path:
        out = inp.with_suffix(".html")
    else:
        out = Path(output_path).resolve()

    return generar_diagrama_desde_mermaid(content, str(out), f"Diagrama — {inp.stem}")

def main():
    mcp.run()

if __name__ == "__main__":
    main()
