from pathlib import Path
import json
from typing import Dict, List, Any, Optional

class UnifiedSuiteBundler:
    """
    Empaqueta múltiples modelos de arquitectura (Casos de uso, Flujos de procesos,
    Clases/Arquitectura por capas y Secuencias UML) en una Suite Unificada interactiva
    con pestañas, buscador en tiempo real (Ctrl+K), minimapa, modo enfoque (tracing)
    y panel inspector lateral (100% Air-Gapped).
    """

    def __init__(self, template_path: Optional[Path] = None):
        if template_path is None:
            self.template_path = Path(__file__).parent / "template_suite.html"
        else:
            self.template_path = template_path

    def bundle(
        self,
        titulo: str,
        eyebrow: str,
        casos_de_uso: Dict[str, Any],
        flujos: Dict[str, Any],
        capas: Dict[str, Any],
        clases: List[Dict[str, Any]],
        aristas_clases: List[List[Any]],
        secuencias: Dict[str, Any]
    ) -> str:
        if not self.template_path.exists():
            raise FileNotFoundError(f"No se encontró el template en: {self.template_path}")

        tpl = self.template_path.read_text(encoding="utf-8")

        data_use = json.dumps(casos_de_uso, ensure_ascii=False, indent=2)
        data_flows = json.dumps(flujos, ensure_ascii=False, indent=2)
        data_layers = json.dumps(capas, ensure_ascii=False, indent=2)
        data_classes = json.dumps(clases, ensure_ascii=False, indent=2)
        data_cedges = json.dumps(aristas_clases, ensure_ascii=False, indent=2)
        data_seqs = json.dumps(secuencias, ensure_ascii=False, indent=2)

        html = tpl.replace("{{PAGE_TITLE}}", titulo)
        html = html.replace("{{EYEBROW_TEXT}}", eyebrow)
        html = html.replace("{{MAIN_HEADING}}", titulo)
        html = html.replace("{{DATA_USE}}", data_use)
        html = html.replace("{{DATA_FLOWS}}", data_flows)
        html = html.replace("{{DATA_LAYERS}}", data_layers)
        html = html.replace("{{DATA_CLASSES}}", data_classes)
        html = html.replace("{{DATA_CEDGES}}", data_cedges)
        html = html.replace("{{DATA_SEQS}}", data_seqs)

        return html
