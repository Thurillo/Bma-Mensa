-- Questo file descrive la struttura SQL generata da Django.
-- NOTA: Django gestisce automaticamente la creazione di queste tabelle
-- usando il file 'models.py'. Non è necessario eseguire questo SQL manualmente.

-- 1. Categorie Piatti (Req 1.8 - "ogni gruppo... hanno sempre lo stesso costo")
CREATE TABLE IF NOT EXISTS mensa_piattocategoria (
id SERIAL PRIMARY KEY,
nome VARCHAR(100) NOT NULL UNIQUE, -- 'Antipasto', 'Primo', 'Secondo', 'Contorno', 'Dolce'
costo_unitario DECIMAL(6, 2) NOT NULL
);

-- 2. Piatti (Req 1.2, 2.1 - anagrafica di tutti i piatti)
CREATE TABLE IF NOT EXISTS mensa_piatto (
id SERIAL PRIMARY KEY, -- Codice univoco
nome VARCHAR(255) NOT NULL, -- Descrizione rapida
descrizione_estesa TEXT,
is_attivo BOOLEAN DEFAULT TRUE, -- Per 'disattivare' un piatto senza cancellarlo
categoria_id INTEGER NOT NULL REFERENCES mensa_piattocategoria(id) ON DELETE RESTRICT
);

-- 3. Menù del Giorno (Req 2.1, 2.3, 3 - cosa è ordinabile in un dato giorno)
CREATE TABLE IF NOT EXISTS mensa_menudelgiorno (
id SERIAL PRIMARY KEY,
data DATE NOT NULL UNIQUE, -- Data in cui questo menù è valido
confermato BOOLEAN DEFAULT FALSE, -- Confermato dal fornitore (Req 2.3)
visibile BOOLEAN DEFAULT FALSE -- Impostato a True dal cron job delle 06:00 (Req 1.5)
);

-- Tabella "ponte" per la relazione Molti-a-Molti tra Menù e Piatti
CREATE TABLE IF NOT EXISTS mensa_menudelgiorno_piatti (
id SERIAL PRIMARY KEY,
menudelgiorno_id INTEGER NOT NULL REFERENCES mensa_menudelgiorno(id) ON DELETE CASCADE,
piatto_id INTEGER NOT NULL REFERENCES mensa_piatto(id) ON DELETE CASCADE,
UNIQUE(menudelgiorno_id, piatto_id)
);

-- 4. Utenti (Django gestisce questo, ma ecco una versione semplificata)
-- Django usa la sua tabella 'auth_user'.
-- 'username' sarà la MATRICOLA (Req 1.1, 4)
-- 'is_staff' = Admin (Req 1)
-- L'appartenenza al gruppo 'Fornitori' = Fornitore (Req 2)
CREATE TABLE IF NOT EXISTS auth_user (
id SERIAL PRIMARY KEY,
password VARCHAR(128) NOT NULL,
last_login TIMESTAMP WITH TIME ZONE,
is_superuser BOOLEAN DEFAULT FALSE,
username VARCHAR(150) NOT NULL UNIQUE, -- MATRICOLA
first_name VARCHAR(150), -- NOME
last_name VARCHAR(150), -- COGNOME
email VARCHAR(254),
is_staff BOOLEAN DEFAULT FALSE, -- Accesso Area Admin
is_active BOOLEAN DEFAULT TRUE, -- Utente abilitato
date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

-- 5. Ordini (Req 4.1 - L'ordine 'master' di un utente per un giorno)
-- Un utente ha UN solo ordine per un dato giorno.
-- Se modifica, aggiorna questo record e i suoi dettagli.
CREATE TABLE IF NOT EXISTS mensa_ordine (
id SERIAL PRIMARY KEY,
utente_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE RESTRICT,
data_pasto DATE NOT NULL, -- Il giorno per cui è il pasto
data_creazione TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
data_modifica TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
UNIQUE(utente_id, data_pasto) -- Garanzia: 1 solo ordine per utente al giorno
);

-- 6. Dettaglio Ordine (Req 4.1 - Le righe dell'ordine)
CREATE TABLE IF NOT EXISTS mensa_dettaglioordine (
id SERIAL PRIMARY KEY,
ordine_id INTEGER NOT NULL REFERENCES mensa_ordine(id) ON DELETE CASCADE,
piatto_id INTEGER NOT NULL REFERENCES mensa_piatto(id) ON DELETE RESTRICT,
quantita INTEGER NOT NULL CHECK (quantita > 0 AND quantita <= 3), -- Max 3 portate (Req 4.1)
costo_al_momento DECIMAL(6, 2) NOT NULL, -- 'Fotografa' il costo al momento dell'ordine
UNIQUE(ordine_id, piatto_id) -- Un piatto può essere aggiunto solo una volta, si modifica la quantità
);

-- 7. Log Accessi Errati (Req 1.9, 4)
CREATE TABLE IF NOT EXISTS mensa_logaccessoerrato (
id SERIAL PRIMARY KEY,
timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
matricola_usata VARCHAR(150) NOT NULL,
ip_address INET,
motivo TEXT
);

-- 8. Configurazione (Req 1.5)
-- Come discusso, SOLO i dati non sensibili.
CREATE TABLE IF NOT EXISTS mensa_configurazione (
id SERIAL PRIMARY KEY,
orario_limite_ordini TIME NOT NULL DEFAULT '20:00:00',
orario_visibilita_menu TIME NOT NULL DEFAULT '06:00:00'
);

-- NOTA: Le tabelle 'auth_group' e 'auth_user_groups' per la gestione
-- dei Fornitori sono create automaticamente da Django.
