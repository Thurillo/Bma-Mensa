"""
File: admin.py
Destinazione: mensa/ (Bma-Mensa/mensa/admin.py)

Questo file "registra" i tuoi modelli (da models.py)
nell'Area Admin di Django (Modulo 1).
"""

from django.contrib import admin
from .models import (
    PiattoCategoria, 
    Piatto, 
    MenuDelGiorno, 
    Ordine, 
    DettaglioOrdine, 
    LogAccessoErrato, 
    Configurazione
)

# Registrazione semplice: mostra i modelli nell'admin
# Vai su /admin/ e vedrai queste tabelle
admin.site.register(PiattoCategoria)
admin.site.register(Piatto)
admin.site.register(MenuDelGiorno)
admin.site.register(Ordine)
admin.site.register(DettaglioOrdine)
admin.site.register(LogAccessoErrato)
admin.site.register(Configurazione)

