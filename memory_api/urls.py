from django.urls import path
from .views import BuildView, QueryView, GraphView, HealthView

urlpatterns = [
    path("build/", BuildView.as_view(), name="build"),
    path("query/", QueryView.as_view(), name="query"),
    path("graph/", GraphView.as_view(), name="graph"),
    path("health/", HealthView.as_view(), name="health"),
]