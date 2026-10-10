# MCP Diagrama Iterativo Mermaid (Air-Gapped)

Servidor MCP (Model Context Protocol) diseñado para que cualquier Asistente de IA (Antigravity, Claude Desktop, Cursor, VS Code, etc.) pueda **analizar cualquier repositorio de código y generar diagramas de arquitectura interactivos autónomos (HTML5 + SVG + Vanilla JS) o Suites Unificadas Multi-pestaña** en un solo paso.

---

## 🚀 Características Principales

1. **100% Air-Gapped (Cero Internet, Cero CDN, Cero NPM en el visor):**
   - El archivo `.html` resultante es un artefacto autónomo y portable que se puede abrir con doble clic en cualquier máquina o red militar/bancaria aislada.
2. **Suites Unificadas Multi-pestaña:**
   - Permite compilar en un único archivo HTML interactivo:
     - 📌 **Casos de Uso UML** (actores, casos, asociaciones, includes/extends).
     - 🔀 **Flujos de Procesos y Caminos Críticos** (decisiones, respuestas HTTP, terminales, simulador de escenarios).
     - ⏳ **Diagramas de Secuencia UML** (líneas de vida, mensajes síncronos/retorno, fragmentos alt/opt, notas).
     - 🏛️ **Arquitectura y Clases por Capas** (estereotipos, atributos, métodos, conectores dinámicos).
3. **Buscador en Tiempo Real (Ctrl+K):**
   - Búsqueda instantánea en vivo de cualquier componente, método, endpoint, tabla, caso de uso o código de prueba.
4. **Modo Enfoque y Trazabilidad Inteligente (Cero Ruido Visual):**
   - **Hover / Clic sobre Nodo:** al interactuar con cualquier componente, se atenúan todas las conexiones ajenas (reduciendo el 95% del ruido visual) y se iluminan en alta fidelidad sus conexiones **Entrantes** (verde esmeralda) y **Salientes** (ámbar/oro).
   - **Fijación de Enfoque (Focus Lock):** un clic fija el foco en el componente seleccionado.
5. **Panel Inspector Lateral:**
   - Despliega detalles técnicos, atributos, métodos, relaciones entrantes/salientes y trazabilidad a requisitos o tests.
6. **Navegación Fluida con Zoom y Paneo:**
   - Zoom con la rueda del ratón centrado en el cursor.
   - Drag & drop de nodos con recálculo en tiempo real y minimapa reactivo.

---

## 🛠️ Herramientas MCP Disponibles

| Herramienta | Descripción | Parámetros Clave |
|---|---|---|
| `analizar_proyecto` | Escanea un proyecto en disco e infiere su stack, capas arquitectónicas y diagramas existentes. | `project_path` |
| `generar_diagrama_desde_mermaid` | Compila cualquier texto Mermaid DSL en una app web interactiva HTML5/SVG individual. | `mermaid_code`, `output_path`, `titulo` |
| `generar_suite_unificada` | **Suite Completa:** Genera un HTML interactivo multi-pestaña (Casos de uso, Flujos, Secuencia, Clases/Arquitectura) con buscador y panel lateral. | `titulo`, `output_path`, `eyebrow`, `casos_de_uso`, `flujos`, `capas`, `clases`, `aristas_clases`, `secuencias` |
| `crear_diagrama_proyecto` | **Todo en uno:** Analiza el proyecto y genera el `.html` interactivo en `docs/`. | `project_path`, `output_path`, `titulo` |
| `convertir_archivo_mermaid` | Convierte un archivo `.mmd` o `.mermaid` existente a su versión interactiva. | `input_file`, `output_path` |

---

## 📂 Galería de Ejemplos
En la carpeta [examples/](examples/) se incluyen suites interactivas de demostración completa:
- `diagrama_suite_unificada.html` (Link Shortener)
- `diagrama_seccap_suite.html` (SECCAP - Ejército Argentino)

---

## 📄 Licencia
MIT — Desarrollado para ecosistemas de desarrollo asistido por IA de alta fidelidad técnica.
