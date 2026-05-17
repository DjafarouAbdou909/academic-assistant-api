# FastMemory Django API

Alternative au RAG classique basée sur un moteur topologique ATF (Component/Block/Function/Data/Access/Event).

## Pourquoi FastMemory ?

| RAG Classique | academic_assistant |
|---|---|
| Recherche par similarité vectorielle | Pathfinding déterministe dans un graphe |
| Peut mélanger des concepts non liés | Isole le bon bloc topologique |
| Hallucinations possibles | Réponses déterministes et traçables |

**Exemple :** La question *"Je n'arrive pas à me connecter, quel est le processus pour mon remboursement ?"* contient deux concepts (connexion + remboursement). Un RAG classique pourrait mélanger les deux. FastMemory isole uniquement `bloc_remboursement_frais`.

## Installation locale

```bash
git clone https://github.com/DjafarouAbdou909/academic-assistant-api.git
cd academic_assistant_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | Statut du serveur |
| GET | `/api/build/` | Charge le graphe ATF depuis `data/input.md` |
| POST | `/api/build/` | Charge un graphe ATF personnalisé (body: `{"markdown": "..."}`) |
| POST | `/api/query/` | Interroge le graphe (body: `{"question": "..."}`) |
| GET | `/api/graph/` | Résumé du graphe chargé |


```
cd academic_assistant_api/
├── memory_api/
│   ├── fastmemory_core.py   # Moteur topologique ATF
│   ├── views.py             # Endpoints Django
│   └── urls.py              # Routes API
├── data/
│   └── input.md             # Jeu de données ATF académique
├── test_client.py           # Script de test et démonstration
├── requirements.txt
├── Dockerfile
└── README.md
```

## Auteur

Djafarou Abdou — Stage GVIVA SERVICES 2026