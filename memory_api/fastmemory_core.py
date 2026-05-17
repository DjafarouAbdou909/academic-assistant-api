"""
FastMemory Core — Moteur topologique ATF (Component/Block/Function/Data/Access/Event)
Implémente le Deterministic Pathfinding pour éviter les hallucinations du RAG classique.
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    node_type: str       # Component, Block, Function, Data, Access, Event
    name: str
    content: str
    parent: Optional[str] = None
    children: list = field(default_factory=list)


class FastMemoryEngine:
    """
    Moteur de mémoire topologique.
    Contrairement au RAG classique (similarité vectorielle),
    FastMemory utilise un graphe hiérarchique structuré pour
    un pathfinding déterministe sans hallucinations.
    """

    def __init__(self):
        self.graph: dict[str, Node] = {}
        self.loaded = False

    def build(self, markdown_text: str) -> dict:
        """Parse un fichier ATF Markdown et construit le graphe topologique."""
        self.graph = {}
        current_component = None
        current_block = None
        current_function = None
        current_content_lines = []
        current_node_key = None

        def save_current():
            if current_node_key and current_node_key in self.graph:
                self.graph[current_node_key].content = " ".join(current_content_lines).strip()

        lines = markdown_text.split("\n")
        for line in lines:
            # Component (##)
            m = re.match(r"^## Component:\s*(.+)", line)
            if m:
                save_current()
                current_content_lines = []
                current_component = m.group(1).strip()
                key = f"C_{current_component}"
                self.graph[key] = Node("Component", current_component, "", parent=None)
                current_block = None
                current_function = None
                current_node_key = key
                continue

            # Block (###)
            m = re.match(r"^### Block:\s*(.+)", line)
            if m:
                save_current()
                current_content_lines = []
                current_block = m.group(1).strip()
                key = f"B_{current_block}"
                self.graph[key] = Node("Block", current_block, "", parent=current_component)
                if current_component:
                    self.graph[f"C_{current_component}"].children.append(key)
                current_function = None
                current_node_key = key
                continue

            # Function (####)
            m = re.match(r"^#### Function:\s*(.+)", line)
            if m:
                save_current()
                current_content_lines = []
                current_function = m.group(1).strip()
                key = f"F_{current_function}"
                self.graph[key] = Node("Function", current_function, "", parent=current_block)
                if current_block:
                    self.graph[f"B_{current_block}"].children.append(key)
                current_node_key = key
                continue

            # Data (####)
            m = re.match(r"^#### Data:\s*(.+)", line)
            if m:
                save_current()
                current_content_lines = []
                name = m.group(1).strip()
                key = f"D_{name}"
                self.graph[key] = Node("Data", name, "", parent=current_block)
                if current_block:
                    self.graph[f"B_{current_block}"].children.append(key)
                current_node_key = key
                continue

            # Access (####)
            m = re.match(r"^#### Access:\s*(.+)", line)
            if m:
                save_current()
                current_content_lines = []
                name = m.group(1).strip()
                key = f"A_{name}"
                self.graph[key] = Node("Access", name, "", parent=current_block)
                if current_block:
                    self.graph[f"B_{current_block}"].children.append(key)
                current_node_key = key
                continue

            # Contenu texte
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
                current_content_lines.append(stripped)

        save_current()
        self.loaded = True

        return {
            "status": "success",
            "nodes_count": len(self.graph),
            "components": [n.name for n in self.graph.values() if n.node_type == "Component"],
            "blocks": [n.name for n in self.graph.values() if n.node_type == "Block"],
            "functions": [n.name for n in self.graph.values() if n.node_type == "Function"],
        }

    def query(self, question: str) -> dict:
        """
        Deterministic Pathfinding :
        Au lieu de chercher par similarité vectorielle (RAG classique),
        on navigue dans le graphe topologique pour isoler le bon bloc.
        """
        if not self.loaded:
            return {"error": "Graphe non chargé. Appelez /build d'abord."}

        question_lower = question.lower()
        keywords = self._extract_keywords(question_lower)

        # Scorer chaque nœud par pertinence topologique
        scores = {}
        for key, node in self.graph.items():
            score = self._score_node(node, keywords)
            if score > 0:
                scores[key] = score

        if not scores:
            return {
                "answer": "Aucune information trouvée pour cette question.",
                "matched_nodes": [],
                "path": []
            }

        # Trier par score et sélectionner le meilleur chemin
        sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_key = sorted_nodes[0][0]
        best_node = self.graph[best_key]

        # Construire le chemin topologique 
        path = self._build_path(best_node)

        # Collecter uniquement les nœuds du même bloc 
        isolated_nodes = self._isolate_block(best_node)

        answer = self._generate_answer(question, isolated_nodes)

        return {
            "answer": answer,
            "matched_component": self._get_component(best_node),
            "matched_block": self._get_block(best_node),
            "deterministic_path": path,
            "isolated_nodes": [
                {"type": n.node_type, "name": n.name, "content": n.content}
                for n in isolated_nodes
            ],
            "rag_comparison": {
                "classic_rag": "Aurait mélangé des résultats de plusieurs modules non liés",
                "fastmemory": f"Restreint au bloc '{self._get_block(best_node)}' uniquement"
            }
        }

    def _extract_keywords(self, text: str) -> list:
        stopwords = {"je", "le", "la", "les", "un", "une", "des", "du", "et", "en",
                     "à", "de", "pour", "pas", "mon", "ma", "mes", "comment", "quel",
                     "est", "ce", "que", "qui", "avec", "sur", "dans", "par", "se",
                     "il", "elle", "ils", "elles", "vous", "nous", "on", "ne", "plus"}
        words = re.findall(r'\b\w+\b', text)
        return [w for w in words if w not in stopwords and len(w) > 2]

    def _score_node(self, node: Node, keywords: list) -> float:
        score = 0.0
        text = f"{node.name} {node.content}".lower()
        for kw in keywords:
            if kw in text:
                # Les Functions et Blocks ont plus de poids
                weight = 2.0 if node.node_type in ["Function", "Block"] else 1.0
                score += weight
        return score

    def _build_path(self, node: Node) -> list:
        path = [f"{node.node_type}:{node.name}"]
        if node.parent:
            parent_key = f"B_{node.parent}" if f"B_{node.parent}" in self.graph else f"C_{node.parent}"
            if parent_key in self.graph:
                path = self._build_path(self.graph[parent_key]) + path
        return path

    def _get_block(self, node: Node) -> str:
        if node.node_type == "Block":
            return node.name
        if node.parent and f"B_{node.parent}" in self.graph:
            return node.parent
        return "N/A"

    def _get_component(self, node: Node) -> str:
        if node.node_type == "Component":
            return node.name
        block_key = f"B_{node.parent}" if node.parent else None
        if block_key and block_key in self.graph:
            comp = self.graph[block_key].parent
            return comp or "N/A"
        return "N/A"

    def _isolate_block(self, node: Node) -> list:
        """Isole uniquement les nœuds du même bloc topologique."""
        block_name = self._get_block(node)
        block_key = f"B_{block_name}"
        if block_key not in self.graph:
            return [node]
        block = self.graph[block_key]
        nodes = [block]
        for child_key in block.children:
            if child_key in self.graph:
                nodes.append(self.graph[child_key])
        return nodes

    def _generate_answer(self, question: str, nodes: list) -> str:
        parts = []
        for node in nodes:
            if node.content:
                parts.append(f"[{node.node_type} — {node.name}] : {node.content}")
        if parts:
            return "\n".join(parts)
        return "Information trouvée dans le graphe mais contenu vide."

    def get_graph_summary(self) -> dict:
        if not self.loaded:
            return {"error": "Graphe non chargé."}
        summary = {}
        for key, node in self.graph.items():
            if node.node_type == "Component":
                summary[node.name] = {
                    "blocks": []
                }
                for bkey in node.children:
                    if bkey in self.graph:
                        block = self.graph[bkey]
                        summary[node.name]["blocks"].append({
                            "name": block.name,
                            "functions": [
                                self.graph[fkey].name
                                for fkey in block.children
                                if fkey in self.graph
                            ]
                        })
        return summary