from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "name": "Academic Assistant API 🧠",
        "version": "1.0.0",
        "description": "Alternative au RAG classique via un graphe topologique ATF",
        "author": "Djafarou Abdou",
        "endpoints": {
            "health": "/api/health/",
            "build":  "/api/build/",
            "query":  "/api/query/",
            "graph":  "/api/graph/"
        },
        "demo": {
            "question": "Je narrive pas a me connecter, quel est le processus pour mon remboursement ?",
            "url": "/api/query/"
        },
        "deployed_on": "Render",
        "github": "https://github.com/DjafarouAbdou909/academic-assistant-api"
    }, json_dumps_params={"ensure_ascii": False, "indent": 2})

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include("memory_api.urls")),
]