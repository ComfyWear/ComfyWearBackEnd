from django.urls import include, path

urlpatterns = [
    path("api/", include("app.api_router", namespace="api")),
]
