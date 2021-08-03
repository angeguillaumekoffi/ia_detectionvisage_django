"""test_getsolupro Configuration des URLs """
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
# importation des vues à associer aux urls
from .views import page_inscription, page_accueil
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginView.as_view(template_name="page_connexion.html"), name='page_connexion'),
    path('se-deconnecter/', views.LogoutView.as_view(), name='deconnexion'),
    path('page-de-inscription/', page_inscription.as_view(), name='page_inscription'),
    path('page-accueil/', login_required(page_accueil.as_view(), login_url="page_connexion"), name='page_accueil'),
]
