# MCP Diagrama Iterativo Mermaid (Air-Gapped)

Servidor MCP (Model Context Protocol) diseñado para que cualquier Asistente de IA (Antigravity, Claude Desktop, Cursor, VS Code, etc.) pueda **analizar cualquier repositorio de código y generar diagramas de arquitectura interactivos autónomos (HTML5 + SVG + Vanilla JS)** en un solo paso.

---

## 🌟 Características Principales

1. **100% Air-Gapped (Cero Internet, Cero CDN, Cero NPM en el visor):**
   - El archivo `.html` resultante es un artefacto autónomo y portable que se puede abrir con doble clic en cualquier máquina o red militar/bancaria aislada.
2. **Matemática Vectorial SVG Perimétrica:**
   - Calcula el ángulo de incidencia $\theta = \operatorname{atan2}(\Delta y, \Delta x)$ para proyectar las flechas sobre el perímetro exterior exacto de cada tarjeta, evitando que se superpongan sobre los nodos.
   - Curvas de Bézier cúbicas con curvatura horizontal adaptativa.
3. **Interactividad Completa:**
   - **Arrastrar y soltar (Drag & Drop)** de nodos con recálculo fluido instantáneo de conexiones.
   - **Paneo libre** en lienzo infinito y **Zoom**.
   - **Minimapa** con visor de coordenadas en tiempo real.
   - **Búsqueda en vivo** que resalta coincidencias y atenúa el resto.
   - **Filtros por capa/subgrafo**.
   - **Modal de inspección técnica** al hacer clic sobre cualquier componente (responsabilidades, archivos de código, dependencias entrantes y salientes).
4. **Inspección Automática de Proyectos:**
   - Escanea la estructura de carpetas de cualquier repositorio (.NET, React, Python, Java, Go, etc.) y sintetiza su diagrama de componentes o convierte diagramas Mermaid (`.mmd`) ya existentes.

---

## 🛠️ Herramientas MCP Disponibles

| Herramienta | Descripción | Parámetros Clave |
|---|---|---|
| `analizar_proyecto` | Escanea un proyecto en disco e infiere su stack, capas arquitectónicas y diagramas existentes. | `project_path` |
| `generar_diagrama_desde_mermaid` | Compila cualquier texto Mermaid DSL en una app web interactiva HTML5/SVG. | `mermaid_code`, `output_path`, `titulo` |
| `crear_diagrama_proyecto` | **Todo en uno:** Analiza el proyecto y genera el `.html` interactivo en `docs/`. | `project_path`, `output_path`, `titulo` |
| `convertir_archivo_mermaid` | Convierte un archivo `.mmd` o `.mermaid` existente a su versión interactiva. | `input_file`, `output_path` |

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/martincrespo77/MCP-Diagrama-Iterativo-Mermaid.git
cd MCP-Diagrama-Iterativo-Mermaid
```

### 2. Configuración en Antigravity / Claude Desktop

Agrega el servidor a tu archivo de configuración de MCP (por ejemplo `~/.gemini/config/mcp_config.json` o `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-diagrama-iterativo-mermaid": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:/2026/MCP-Diagrama-Iterativo-Mermaid",
        "server.py"
      ],
      "disabled": false
    }
  }
}
```

---

## 💬 Ejemplos de Uso en el Chat de la IA

Una vez configurado, puedes hablarle a tu IA directamente así:

- *"Analiza el proyecto en `D:/MisProyectos/SistemaVentas` y créame el diagrama interactivo de arquitectura en la carpeta docs."*
- *"Tengo este diagrama Mermaid, conviértelo a visor interactivo autónomo en `D:/reportes/visor.html`: [código mermaid]"*
- *"Convierte el archivo `docs/arquitectura.mmd` en un visor interactivo HTML."*

---

## 📄 Licencia
MIT — Desarrollado para ecosistemas de desarrollo asistido por IA de alta fidelidad técnica.
