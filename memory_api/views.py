import os
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .fastmemory_core import FastMemoryEngine

engine = FastMemoryEngine()
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "input.md")


@method_decorator(csrf_exempt, name="dispatch")
class BuildView(View):
    def post(self, request):
        try:
            body = json.loads(request.body or "{}")
            markdown_text = body.get("markdown", None)
            if not markdown_text:
                if not os.path.exists(DATA_FILE):
                    return JsonResponse({"error": "Fichier data/input.md introuvable."}, status=404)
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    markdown_text = f.read()
            result = engine.build(markdown_text)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request):
        try:
            if not os.path.exists(DATA_FILE):
                return JsonResponse({"error": "Fichier data/input.md introuvable."}, status=404)
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                markdown_text = f.read()
            result = engine.build(markdown_text)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class QueryView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            question = body.get("question", "").strip()
            if not question:
                return JsonResponse({"error": "Le champ 'question' est requis."}, status=400)
            if not engine.loaded:
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        engine.build(f.read())
                else:
                    return JsonResponse({"error": "Graphe non chargé. Appelez /api/build/ d'abord."}, status=400)
            result = engine.query(question)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalide."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class GraphView(View):
    def get(self, request):
        if not engine.loaded:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    engine.build(f.read())
        return JsonResponse(engine.get_graph_summary())


class HealthView(View):
    def get(self, request):
        return JsonResponse({
            "status": "ok",
            "engine_loaded": engine.loaded,
            "nodes_count": len(engine.graph),
            "message": "FastMemory Django API operationnelle"
        })
