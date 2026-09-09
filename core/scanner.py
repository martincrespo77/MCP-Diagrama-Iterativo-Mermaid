import os
from pathlib import Path
from typing import Dict, List, Any

class CodebaseScanner:
    """Escanea la estructura de carpetas y archivos de un proyecto para inferir su arquitectura."""

    LAYER_KEYWORDS = {
        "Frontend": ["frontend", "client", "ui", "web", "views", "components", "pages", "public"],
        "API_Gateways": ["api", "controllers", "routes", "endpoints", "handlers", "grpc", "graphql"],
        "Middlewares": ["middlewares", "filters", "interceptors", "guards", "auth", "security"],
        "Application": ["application", "services", "usecases", "use_cases", "logic", "commands", "queries"],
        "Domain": ["domain", "models", "entities", "aggregates", "core", "types", "schemas"],
        "Integration_ACL": ["infrastructure", "adapters", "gateways", "clients", "external", "integrations"],
        "Persistence": ["persistence", "repositories", "db", "database", "data", "migrations", "store"],
    }

    def scan(self, project_path: str) -> Dict[str, Any]:
        root = Path(project_path).resolve()
        if not root.exists():
            raise FileNotFoundError(f"La ruta no existe: {project_path}")

        detected_stack = []
        existing_diagrams = []
        layers_found = {k: [] for k in self.LAYER_KEYWORDS}

        # Analizar archivos clave de stack
        files_at_root = [f.name.lower() for f in root.glob("*") if f.is_file()]
        
        if "package.json" in files_at_root:
            detected_stack.append("Node.js / JavaScript")
        if any(f.endswith(".csproj") or f.endswith(".sln") for f in files_at_root) or list(root.glob("*/*.csproj")):
            detected_stack.append(".NET / C#")
        if "pyproject.toml" in files_at_root or "requirements.txt" in files_at_root:
            detected_stack.append("Python")
        if "go.mod" in files_at_root:
            detected_stack.append("Go")
        if "pom.xml" in files_at_root or "build.gradle" in files_at_root:
            detected_stack.append("Java / Spring")
        if "docker-compose.yml" in files_at_root or "docker-compose.yaml" in files_at_root:
            detected_stack.append("Docker Compose")

        # Buscar diagramas existentes
        for ext in ["*.mmd", "*.mermaid", "*.puml"]:
            for d_file in root.glob(f"**/{ext}"):
                if "node_modules" not in str(d_file) and ".venv" not in str(d_file):
                    existing_diagrams.append(str(d_file.relative_to(root)))

        # Clasificar carpetas en capas arquitectónicas
        for dirpath, dirnames, filenames in os.walk(root):
            p = Path(dirpath)
            # Ignorar carpetas pesadas
            if any(skip in p.parts for skip in ["node_modules", ".venv", ".git", "bin", "obj", "dist", "build", ".idea", ".vscode"]):
                continue

            folder_name = p.name.lower()
            rel_path = str(p.relative_to(root))

            for layer_name, keywords in self.LAYER_KEYWORDS.items():
                if any(k == folder_name for k in keywords):
                    # Contar archivos de código significativos
                    code_files = [f for f in filenames if f.endswith(('.cs', '.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.java'))]
                    if code_files or len(dirnames) > 0:
                        layers_found[layer_name].append({
                            "path": rel_path,
                            "folder": p.name,
                            "file_count": len(code_files),
                            "sample_files": code_files[:5]
                        })

        # Filtrar capas vacías
        active_layers = {k: v for k, v in layers_found.items() if len(v) > 0}

        return {
            "project_name": root.name,
            "root_path": str(root),
            "stack": detected_stack or ["Estructura General de Archivos"],
            "existing_diagrams": existing_diagrams,
            "layers": active_layers
        }

    def generate_mermaid_from_scan(self, scan_result: Dict[str, Any]) -> str:
        """Sintetiza una especificación Mermaid architecture a partir del escaneo."""
        lines = ["graph LR"]
        layers = scan_result["layers"]

        prev_subgraph_nodes = []

        for layer_name, folders in layers.items():
            sub_id = layer_name.replace(" ", "_")
            lines.append(f'    subgraph {sub_id}["{layer_name.replace("_", " ")}"]')
            current_nodes = []
            
            for idx, f in enumerate(folders[:4]):  # Limitar para legibilidad
                node_id = f"{sub_id}_{idx}"
                folder_title = f["folder"].capitalize()
                files_hint = f"<br/>({f['file_count']} archivos)" if f['file_count'] else ""
                lines.append(f'        {node_id}["📁 {folder_title}{files_hint}"]')
                current_nodes.append(node_id)

            lines.append("    end")

            # Conectar capa anterior con capa actual
            if prev_subgraph_nodes and current_nodes:
                lines.append(f"    {prev_subgraph_nodes[0]} --> {current_nodes[0]}")

            if current_nodes:
                prev_subgraph_nodes = current_nodes

        return "\n".join(lines)
