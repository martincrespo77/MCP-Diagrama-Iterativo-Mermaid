from collections import defaultdict
from typing import Dict, List, Tuple, Any

class SpatialLayoutEngine:
    """Calculador de coordenadas virtuales (X, Y), espaciado holgado y delimitadores de subgrafos."""

    def __init__(self, node_width: int = 300, node_height: int = 90, col_spacing: int = 560, row_spacing: int = 140):
        self.node_width = node_width
        self.node_height = node_height
        self.col_spacing = col_spacing
        self.row_spacing = row_spacing

    def compute_layout(self, nodes: Dict[str, Any], connections: List[Dict[str, Any]], subgraphs: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        # Organizar columnas por subgrafos
        subgraph_order = list(subgraphs.keys()) if subgraphs else ["General"]
        if not subgraphs and nodes:
            subgraph_order = ["General"]

        col_x = 90
        subgraph_zones = []
        node_positions = {}

        for sub_id in subgraph_order:
            sub_info = subgraphs.get(sub_id, {"title": sub_id, "nodes": []})
            sub_nodes = [nid for nid, ndata in nodes.items() if ndata.get("subgraph") == sub_id]
            if not sub_nodes and sub_info.get("nodes"):
                sub_nodes = sub_info["nodes"]

            if not sub_nodes and sub_id != "General":
                continue

            curr_y = 80
            min_x = col_x
            min_y = curr_y - 35

            for nid in sub_nodes:
                node_positions[nid] = (col_x, curr_y)
                curr_y += self.row_spacing

            max_y = max(curr_y + 20, 320)

            subgraph_zones.append({
                "id": sub_id,
                "title": sub_info.get("title", sub_id),
                "x": min_x - 25,
                "y": min_y,
                "width": self.node_width + 50,
                "height": max_y - min_y
            })

            col_x += self.col_spacing

        # Nodos que no quedaron explícitamente en ningún subgrafo
        unplaced = [nid for nid in nodes if nid not in node_positions]
        if unplaced:
            curr_y = 80
            for nid in unplaced:
                node_positions[nid] = (col_x, curr_y)
                curr_y += self.row_spacing
            subgraph_zones.append({
                "id": "General",
                "title": "Otros Componentes",
                "x": col_x - 25,
                "y": 45,
                "width": self.node_width + 50,
                "height": max(curr_y - 10, 320)
            })

        # Construir lista de nodos final
        node_list = []
        for nid, ndata in nodes.items():
            pos = node_positions.get(nid, (100, 100))
            node_list.append({
                "id": nid,
                "title": ndata.get("title", nid),
                "raw_label": ndata.get("raw_label", nid),
                "shape": ndata.get("shape", "rect"),
                "subgraph": ndata.get("subgraph", "General"),
                "custom_style": ndata.get("custom_style", {}),
                "x": pos[0],
                "y": pos[1],
                "meta": ndata.get("meta", {})
            })

        # Indexado de conexiones múltiples y detección de auto-bucles (self-loops)
        pair_counts = defaultdict(int)
        for c in connections:
            pair_key = (c["from"], c["to"])
            pair_counts[pair_key] += 1

        pair_indices = defaultdict(int)
        for idx, c in enumerate(connections):
            c["id"] = f"conn_{idx}"
            pair_key = (c["from"], c["to"])
            c["pair_index"] = pair_indices[pair_key]
            c["pair_total"] = pair_counts[pair_key]
            c["is_self"] = (c["from"] == c["to"])
            pair_indices[pair_key] += 1

        return node_list, subgraph_zones
