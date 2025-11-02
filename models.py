import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# Req 1.8: Categoria piatto, con costo a livello di gruppo
class PiattoCategoria(models.Model):
    """
    Categoria di un piatto (es. Antipasto, Primo, Secondo).
    Il costo è definito a livello di categoria (Req 1.8).
    """
    nome = models.CharField(max_length=100, unique=True, help_text="Es. Antipasto, Primo, Secondo, Contorno, Dolce")
    costo_unitario = models.DecimalField(max_digits=6, decimal_places=2, help_text="Costo per tutti i piatti di questa categoria")

    def __str__(self):
        return f"{self.nome} (€{self.costo_unitario})"

    class Meta:
        verbose_name = "Categoria Piatto"
        verbose_name_plural = "Categorie Piatti"

# Req 1.2, 2.1: Anagrafica di tutti i piatti
class Piatto(models.Model):
    """
    Anagrafica di tutti i piatti disponibili, passati e futuri.
    Il Fornitore ne sceglierà alcuni per il menù del giorno.
    """
    id = models.AutoField(primary_key=True) # Codice univoco (Req 1.2)
    categoria = models.ForeignKey(PiattoCategoria, on_delete=models.PROTECT, related_name="piatti")
    nome = models.CharField(max_length=255, help_text="Descrizione rapida (es. Pasta al Pesto)")
    descrizione_estesa = models.TextField(blank=True, null=True, help_text="Descrizione estesa (ingredienti, allergeni, ecc.)")
    is_attivo = models.BooleanField(default=True, help_text="Se deselezionato, il piatto non è più disponibile per nuovi menù")

    def __str__(self):
        return f"[{self.categoria.nome}] {self.nome}"
    
    @property
    def costo(self):
        # Il costo è ereditato dalla categoria
        return self.categoria.costo_unitario

    class Meta:
        verbose_name = "Piatto"
        verbose_name_plural = "Anagrafica Piatti"

# Req 2.1, 2.3, 3: Menù selezionato per un giorno specifico
class MenuDelGiorno(models.Model):
    """
    Rappresenta i piatti selezionati dal Fornitore per un dato giorno.
    """
    data = models.DateField(unique=True, help_text="Data in cui questo menù sarà servito")
    piatti = models.ManyToManyField(Piatto, help_text="Piatti selezionati per questo giorno")
    confermato = models.BooleanField(default=False, help_text="Selezionare per confermare il menù (Req 2.3)")
    visibile = models.BooleanField(default=False, help_text="Impostato automaticamente alle 06:00 (Req 1.5)")

    def __str__(self):
        return f"Menù del {self.data.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = "Menù del Giorno"
        verbose_name_plural = "Menù del Giorno"
        ordering = ['-data']

# Req 4.1: Ordine di un utente per un giorno
class Ordine(models.Model):
    """
    L'ordine 'master' di un singolo utente per un singolo giorno.
    Contiene le righe di dettaglio.
    """
    utente = models.ForeignKey(User, on_delete=models.PROTECT, related_name="ordini", help_text="Utente (dipendente) che ha fatto l'ordine")
    data_pasto = models.DateField(help_text="Il giorno per cui è il pasto")
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_modifica = models.DateTimeField(auto_now=True)

    class Meta:
        # Garanzia: 1 solo ordine per utente al giorno (Req 4.1)
        unique_together = ('utente', 'data_pasto')
        verbose_name = "Ordine"
        verbose_name_plural = "Ordini"
        ordering = ['-data_pasto', 'utente']

    def __str__(self):
        return f"Ordine di {self.utente.username} per {self.data_pasto.strftime('%d/%m/%Y')}"

    def get_totale_ordine(self):
        return sum(dettaglio.get_totale_riga() for dettaglio in self.dettagli.all())

# Req 4.1: Righe d'ordine (piatto e quantità)
class DettaglioOrdine(models.Model):
    """
    Una singola riga di un ordine (es. 2 x Pasta al Pesto).
    """
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name="dettagli")
    piatto = models.ForeignKey(Piatto, on_delete=models.PROTECT, related_name="in_ordini")
    quantita = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3) # Limite per piatto (Req 4.1)
        ]
    )
    # 'Fotografa' il costo al momento dell'ordine per storicità
    costo_al_momento = models.DecimalField(max_digits=6, decimal_places=2, editable=False)

    class Meta:
        # Un piatto può comparire solo una volta per ordine
        unique_together = ('ordine', 'piatto')
        verbose_name = "Dettaglio Ordine"
        verbose_name_plural = "Dettagli Ordine"

    def __str__(self):
        return f"{self.quantita}x {self.piatto.nome}"

    def get_totale_riga(self):
        return self.costo_al_momento * self.quantita

    def save(self, *args, **kwargs):
        # Salva automaticamente il costo dalla categoria del piatto
        if not self.id:
            self.costo_al_momento = self.piatto.costo
        super().save(*args, **kwargs)

# Req 1.9, 4: Log degli accessi errati
class LogAccessoErrato(models.Model):
    """
    Logga i tentativi di login falliti.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    matricola_usata = models.CharField(max_length=150, help_text="Username/Matricola usata")
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP da cui è stato fatto il tentativo")
    motivo = models.TextField(blank=True, null=True, help_text="Es. Password errata, Utente non trovato")

    def __str__(self):
        return f"Fallito: {self.matricola_usata} @ {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Log Accesso Errato"
        verbose_name_plural = "Log Accessi Errati"
        ordering = ['-timestamp']

# Req 1.5: Configurazione orari
class Configurazione(models.Model):
    """
    Configurazioni globali (non sensibili) dell'applicazione.
    Ci sarà una sola riga in questa tabella.
    """
    orario_limite_ordini = models.TimeField(default=datetime.time(20, 0, 0), help_text="Orario massimo per ordini (per giorno dopo)")
    orario_visibilita_menu = models.TimeField(default=datetime.time(6, 0, 0), help_text="Orario in cui il menù del giorno dopo diventa visibile")

    def __str__(self):
        return "Configurazione Orari"

    class Meta:
        verbose_name = "Configurazione"
        verbose_name_plural = "Configurazione"

    def save(self, *args, **kwargs):
        # Forza la tabella ad avere una sola riga (Singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
