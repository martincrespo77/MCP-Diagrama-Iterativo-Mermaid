# MCP Diagrama Iterativo Mermaid (Air-Gapped)

Servidor MCP (Model Context Protocol) diseñado para que cualquier Asistente de IA (Antigravity, Claude Desktop, Cursor, VS Code, etc.) pueda **analizar cualquier repositorio de código y generar diagramas de arquitectura interactivos autónomos (HTML5 + SVG + Vanilla JS)** en un solo paso.

---

## 🌟 Características Principales

1. **100% Air-Gapped (Cero Internet, Cero CDN, Cero NPM en el visor):**
   - El archivo `.html` resultante es un artefacto autónomo y portable que se puede abrir con doble clic en cualquier máquina o red militar/bancaria aislada.
2. **Modo Enfoque y Trazabilidad Inteligente (Cero Ruido Visual):**
   - **Hover / Clic sobre Nodo:** al interactuar con cualquier componente, se atenúan todas las conexiones ajenas (reduciendo el 95% del ruido visual) y se iluminan en alta fidelidad sus conexiones **Entrantes** (verde esmeralda) y **Salientes** (ámbar/oro).
   - **Fijación de Enfoque (Focus Lock):** un clic fija el foco en el componente seleccionado para mover el cursor, inspeccionar rutas y leer etiquetas sin perder la vista activa. Se libera con `Esc` o el botón de la barra flotante.
3. **Gestión Inteligente de Etiquetas (Sin Amontonamiento):**
   - Selector en barra superior con 4 modos: `Inteligente (Foco/Hover)`, `Todas`, `Principales (==>)` y `Ocultas`.
   - **Tooltip Flotante de Aristas:** al posar el cursor sobre cualquier enlace, se resalta en neón y se despliega un panel flotante con los extremos exactos `[Origen ➔ Destino]`, el tipo de conexión y la descripción completa (rutas HTTP, permisos, roles, etc.).
4. **Filtros Semánticos de Enlaces:**
   - Botones tipo chip en la barra superior para alternar instantáneamente la visibilidad de capas de conexión:
     - `==> Flujo Principal` (transiciones troncales del sistema)
     - `--> Métodos / Transiciones` (llamadas de operación estándar)
     - `-.- > Reglas / Guardas / Auditoría` (guardas, permisos, eventos)
5. **Enrutamiento Curvo Avanzado y Auto-bucles (Self-Loops):**
   - Soporte matemático completo para auto-bucles: proyecta arcos suaves en el lateral del nodo con etiqueta exterior.
   - Enrutamiento arqueado para conexiones de retorno (Right-to-Left) evitando colisiones con columnas intermedias.
   - Separación con *offsets* para conexiones paralelas entre los mismos nodos.
6. **Soporte Completo de Sintaxis Mermaid:**
   - Soporta rectángulos `[...]`, píldoras `([...])`, cilindros `[(...)]`, rombos de decisión `{...}`, hexágonos `{{...}}` y círculos `((...))`.
   - Soporte para definición de estilos con `classDef` y asignaciones con `class`.
7. **Navegación Fluida con Zoom y Paneo:**
   - Zoom con la rueda del ratón centrado en la posición del cursor.
   - Botones de Zoom en pantalla: `[ + ]`, `[ - ]`, `[ 100% ]`, `[ ⛶ Ajustar ]`.
   - Drag & drop de nodos con recálculo en tiempo real y minimapa reactivo.

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
