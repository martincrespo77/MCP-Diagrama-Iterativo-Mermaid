import re
from typing import Dict, List, Tuple, Any

class MermaidParser:
    """Parser robusto para extraer nodos, aristas y subgrafos de texto Mermaid."""

    def __init__(self):
        # Regex para nodos con diferentes formas: [rect], (round), ([pill]), [(cylinder)], ((circle))
        self.re_node_shapes = [
            (re.compile(r'([A-Za-z0-9_.-]+)\(\["(.*?)"\]\)'), "pill"),
            (re.compile(r'([A-Za-z0-9_.-]+)\(\[(.*?)\]\)'), "pill"),
            (re.compile(r'([A-Za-z0-9_.-]+)\[\("(.*?)"\)\]'), "cylinder"),
            (re.compile(r'([A-Za-z0-9_.-]+)\[\((.*?)\)\]'), "cylinder"),
            (re.compile(r'([A-Za-z0-9_.-]+)\[/"(.*?)"/\]'), "parallelogram"),
            (re.compile(r'([A-Za-z0-9_.-]+)\[/(.*?)/\]'), "parallelogram"),
            (re.compile(r'([A-Za-z0-9_.-]+)\["(.*?)"\]'), "rect"),
            (re.compile(r'([A-Za-z0-9_.-]+)\[(.*?)\]'), "rect"),
            (re.compile(r'([A-Za-z0-9_.-]+)\("(.*?)"\)'), "round"),
            (re.compile(r'([A-Za-z0-9_.-]+)\((.*?)\)'), "round"),
        ]

        # Regex para aristas / conectores con labels
        self.re_arrow_labeled = re.compile(
            r'([A-Za-z0-9_.-]+)\s*(?:-->|---\s*\||-.->\||==>\||-->\|)(.*?)\|\s*([A-Za-z0-9_.-]+)'
        )
        self.re_arrow_inline = re.compile(
            r'([A-Za-z0-9_.-]+)\s*--\s*(.*?)\s*-->\s*([A-Za-z0-9_.-]+)'
        )
        self.re_arrow_simple = re.compile(
            r'([A-Za-z0-9_.-]+)\s*(-->|-.->|==>|---)\s*([A-Za-z0-9_.-]+)'
        )

        # Regex para subgrafos
        self.re_subgraph_start = re.compile(r'^\s*subgraph\s+([A-Za-z0-9_.-]+)(?:\["?(.*?)"?\])?\s*$', re.I)
        self.re_subgraph_end = re.compile(r'^\s*end\s*$', re.I)

    def parse(self, text: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
        nodes: Dict[str, Any] = {}
        connections: List[Dict[str, Any]] = []
        subgraphs: Dict[str, Any] = {}

        current_subgraph = None
        lines = text.splitlines()

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("%%") or line.startswith("graph ") or line.startswith("flowchart "):
                continue

            # Subgrafos
            match_sub_start = self.re_subgraph_start.match(line)
            if match_sub_start:
                sub_id = match_sub_start.group(1)
                sub_title = match_sub_start.group(2) or sub_id
                current_subgraph = sub_id
                subgraphs[sub_id] = {
                    "id": sub_id,
                    "title": sub_title.strip(),
                    "nodes": []
                }
                continue

            if self.re_subgraph_end.match(line):
                current_subgraph = None
                continue

            # Buscar declaraciones de nodos
            found_node = False
            for regex, shape in self.re_node_shapes:
                m = regex.search(line)
                if m and "-->" not in line and "-.->" not in line:
                    n_id = m.group(1)
                    raw_label = m.group(2)
                    clean_title = raw_label.replace("<br/>", " - ").replace("<br>", " - ").strip()
                    nodes[n_id] = {
                        "id": n_id,
                        "title": clean_title,
                        "raw_label": raw_label,
                        "shape": shape,
                        "subgraph": current_subgraph or "General"
                    }
                    if current_subgraph and current_subgraph in subgraphs:
                        subgraphs[current_subgraph]["nodes"].append(n_id)
                    found_node = True
                    break

            # Buscar conexiones múltiples con & (ej. A --> B & C & D)
            if "-->" in line or "-.->" in line or "==>" in line or "---" in line:
                self._parse_connection_line(line, nodes, connections, current_subgraph)

        # Garantizar que todos los nodos mencionados en conexiones existan
        for conn in connections:
            for endpoint in [conn["from"], conn["to"]]:
                if endpoint not in nodes:
                    nodes[endpoint] = {
                        "id": endpoint,
                        "title": endpoint,
                        "raw_label": endpoint,
                        "shape": "rect",
                        "subgraph": "General"
                    }

        return nodes, connections, subgraphs

    def _parse_connection_line(self, line: str, nodes: dict, connections: list, current_subgraph: str):
        # Manejo de labels con pipes |label|
        label = ""
        arrow_type = "call"

        if "-.->" in line:
            arrow_type = "dashed"
        elif "==>" in line:
            arrow_type = "thick"
        elif "-->" in line:
            arrow_type = "arrow"
        else:
            arrow_type = "line"

        m_labeled = self.re_arrow_labeled.search(line)
        if m_labeled:
            from_part = m_labeled.group(1)
            label = m_labeled.group(2).strip().strip('"')
            to_part = m_labeled.group(3)
            self._add_connections_multi(from_part, to_part, arrow_type, label, connections)
            return

        m_inline = self.re_arrow_inline.search(line)
        if m_inline:
            from_part = m_inline.group(1)
            label = m_inline.group(2).strip().strip('"')
            to_part = m_inline.group(3)
            self._add_connections_multi(from_part, to_part, arrow_type, label, connections)
            return

        # Separador básico
        parts = re.split(r'\s*(?:-->|-.->|==>|---)\s*', line)
        if len(parts) == 2:
            from_part, to_part = parts[0].strip(), parts[1].strip()
            self._add_connections_multi(from_part, to_part, arrow_type, "", connections)

    def _add_connections_multi(self, from_str: str, to_str: str, arrow_type: str, label: str, connections: list):
        # Permite syntax como A & B --> C & D
        from_nodes = [x.strip() for x in from_str.split("&") if x.strip()]
        to_nodes = [x.strip() for x in to_str.split("&") if x.strip()]

        for f in from_nodes:
            # Limpiar posible label inline o brackets
            f_clean = re.sub(r'[\(\[\{].*?[\)\]\}]', '', f).strip()
            for t in to_nodes:
                t_clean = re.sub(r'[\(\[\{].*?[\)\]\}]', '', t).strip()
                if f_clean and t_clean:
                    connections.append({
                        "from": f_clean,
                        "to": t_clean,
                        "type": arrow_type,
                        "label": label
                    })
