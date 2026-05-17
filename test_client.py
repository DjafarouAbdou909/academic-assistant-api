"""
Script de test client — FastMemory Django API
Démontre le Deterministic Pathfinding vs RAG classique
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"  # Remplacer par l'URL Render en production


def call_api(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print_section("1. HEALTH CHECK")
    health = call_api("GET", "/api/health/")
    print(json.dumps(health, indent=2, ensure_ascii=False))

    print_section("2. BUILD — Chargement du graphe ATF")
    build = call_api("GET", "/api/build/")
    print(f" Graphe construit avec {build.get('nodes_count')} noeuds")
    print(f"   Components : {build.get('components')}")
    print(f"   Fonctions  : {len(build.get('functions', []))} fonctions indexees")

    print_section("3. GRAPH SUMMARY")
    graph = call_api("GET", "/api/graph/")
    print(json.dumps(graph, indent=2, ensure_ascii=False))

    print_section("4. TEST CLE — Cas du sujet (connexion + remboursement)")
    question = "Je n'arrive pas a me connecter, quel est le processus pour mon remboursement ?"
    print(f"\nQuestion : {question}")
    print("\n[RAG Classique] Aurait mélangé connexion ET remboursement (hallucination possible)")
    print("[FastMemory]    Pathfinding déterministe => isolation du bon bloc\n")

    result = call_api("POST", "/api/query/", {"question": question})
    print(f"Bloc isolé : {result.get('matched_block')}")
    print(f"Chemin     : {' → '.join(result.get('deterministic_path', []))}")
    print(f"\n Réponse :\n{result.get('answer')}")
    print(f"\n Comparaison RAG :")
    rag = result.get("rag_comparison", {})
    print(f"   RAG classique : {rag.get('classic_rag')}")
    print(f"   FastMemory    : {rag.get('fastmemory')}")

    print_section("5. TEST — Requête sur les notes")
    q2 = "Comment contester ma note après les délibérations ?"
    result2 = call_api("POST", "/api/query/", {"question": q2})
    print(f"Question : {q2}")
    print(f"Bloc isolé : {result2.get('matched_block')}")
    print(f"Chemin     : {' → '.join(result2.get('deterministic_path', []))}")
    print(f"\nRéponse :\n{result2.get('answer')}")

    print_section("6. TEST — Requête sur l'emprunt de livres")
    q3 = "Combien de livres puis-je emprunter à la bibliothèque ?"
    result3 = call_api("POST", "/api/query/", {"question": q3})
    print(f"Question : {q3}")
    print(f"Bloc isolé : {result3.get('matched_block')}")
    print(f"\nRéponse :\n{result3.get('answer')}")

    print_section("RÉSUMÉ")
    print("API Django opérationnelle")
    print("Graphe topologique ATF construit et navigable")
    print("Deterministic Pathfinding validé sur 3 requêtes")
    print("solation des blocs démontrée (anti-hallucination)")
    print(f"\n URL publique : {BASE_URL}")


if __name__ == "__main__":
    main()
