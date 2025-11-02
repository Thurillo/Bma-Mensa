"""
File: urls.py
Destinazione: mensa/ (Bma-Mensa/mensa/urls.py)

Definizione degli URL specifici per l'app 'mensa'.
Questo file gestirà le pagine Home, Area Utente e Area Fornitore.
"""
from django.urls import path
from . import views # Importa il file views.py

urlpatterns = [
    # Esempio per il futuro (da scommentare quando crei le funzioni in views.py):
    
    # Modulo 3: Home Page Pubblica
    # path('', views.home_page, name='home'),
    
    # Modulo 4: Area Utente (Ordinazione)
    # path('ordina/', views.area_utente, name='area_utente'),
    # path('i-miei-ordini/', views.storico_utente, name='storico_utente'),
    
    # Modulo 2: Area Fornitore
    # path('fornitore/', views.area_fornitore, name='area_fornitore'),
    # path('fornitore/report/', views.report_fornitore, name='report_fornitore'),
    
    # URL per il Login/Logout (Django li gestisce in gran parte)
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

