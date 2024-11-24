from django.urls import path
from . import views

urlpatterns = [
    # Page principale
    path(
        "", views.accueil_site, name="accueil_site"
    ),  # Route pour la vue générale (Accueil)
    # Page accueil associé à un personnage selectionné
    path("accueil_detail/<str:pk>", views.accueil_detail, name="accueil_detail"),
    # Page immersive
    path("vue_immersive/<str:pk>", views.vue_immersive, name="vue_immersive"),
    path("grimper_bloc/", views.grimper_bloc, name="grimper_bloc"),
]
