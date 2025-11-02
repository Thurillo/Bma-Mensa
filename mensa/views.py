"""
File: views.py
Destinazione: mensa/ (Bma-Mensa/mensa/views.py)

Questo file conterrà la logica Python per ogni pagina web.
Ogni funzione 'def' qui corrisponde a una pagina o a un'azione.
"""

from django.shortcuts import render
from django.http import HttpResponse
# Importa i modelli per usarli
from .models import MenuDelGiorno, Ordine, Piatto
# Importa i "decorators" per la sicurezza
from django.contrib.auth.decorators import login_required, user_passes_test


# --- Modulo 3: Home Page (Visualizzazione Menù) ---
# (Questa sarà la tua pagina principale, scommentala in mensa/urls.py)
#
# def home_page(request):
#   # Cerca il menù più recente che è impostato come 'visibile'
#   menu = MenuDelGiorno.objects.filter(visibile=True).order_by('-data').first()
#   # Passa il menù al file HTML (che dovrai creare in 'templates/home.html')
#   return render(request, 'home.html', {'menu': menu})

# --- Modulo 4: Area Utente (Ordinazione) ---
# @login_required # Richiede che l'utente sia loggato
# def area_utente(request):
#   ... qui la logica per permettere all'utente di creare/modificare l'ordine ...
#   return render(request, 'area_utente.html', {...})

# @login_required
# def storico_utente(request): # Req 4.2
#   ... qui la logica per vedere lo storico ordini ...
#   return render(request, 'storico_utente.html', {...})


# --- Modulo 2: Area Fornitore ---
# Funzione test per vedere se l'utente è nel gruppo "Fornitori"
# def is_fornitore(user):
#    return user.groups.filter(name='Fornitori').exists()

# @login_required
# @user_passes_test(is_fornitore) # Blocca se non è "Fornitore"
# def area_fornitore(request): # Req 2.1, 2.3
#   ... qui la logica per creare/confermare i menù ...
#   return render(request, 'area_fornitore.html', {...})


# --- Modulo 1: Report Admin (Esportazioni) ---
# (Queste viste saranno chiamate dall'Area Admin)
#
# @login_required
# @staff_member_required # Richiede che l'utente sia Admin ('is_staff')
# def report_giornaliero_excel(request, data): # Req 1.6
#   ... logica per creare il file Excel ...
#   return HttpResponse(...) # Restituisce il file

# @login_required
# @staff_member_required
# def report_periodo_pdf(request, data_inizio, data_fine): # Req 1.7
#   ... logica per creare il PDF con WeasyPrint ...
#   return HttpResponse(...) # Restituisce il file

