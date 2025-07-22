from django.urls import path
from .views import dashboard_view, deconnexion_view, documents_view, infos_personnelles_view, inscription_view, connexion_view, supprimer_document

urlpatterns = [
    path('inscription/', inscription_view, name='inscription'),
    path('connexion/', connexion_view, name='connexion'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('deconnexion/', deconnexion_view, name='deconnexion'),
    path('infos/', infos_personnelles_view, name='infos_personnelles'),
    path('documents/', documents_view, name='documents'),
    path('documents/supprimer/<int:document_id>/', supprimer_document, name='supprimer_document'),
]