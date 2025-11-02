"""
File: urls.py
Destinazione: config/ (Bma-Mensa/config/urls.py)

Definizione degli URL principali del progetto (il "router" principale).
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Modulo 1 (Admin) -> http://192.168.1.9:8000/admin/
    path('admin/', admin.site.urls), 
    
    # Collega tutti gli URL della app 'mensa' (vedi mensa/urls.py)
    # per Modulo 2 (Fornitore), 3 (Home), 4 (Utente)
    # Questo reindirizza / a 'mensa/urls.py'
    path('', include('mensa.urls')), 
]

