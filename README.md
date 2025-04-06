**Fynd Project**

Questo progetto è un'applicazione Django che utilizza Docker per il deployment di un database PostgreSQL e il server web Django. Di seguito sono descritti i passaggi per eseguire il setup e avviare il progetto.


**Prerequisiti**

Docker e Docker Compose installati.

Python 3.11 (incluso nel container Docker).

File di configurazione .env.docker per l'ambiente Docker e .env per l'ambiente locale di Django.


**Set Up**

Crea un file .env.docker nella cartella config/ con le seguenti variabili d'ambiente:


```
DATABASE_NAME=fynd_db
DATABASE_USER=fynd_user
DATABASE_PASSWORD=fynd_password
DATABASE_HOST=db
DATABASE_PORT=5433
```
Nota: Modifica questi valori se necessario per il tuo ambiente.


Crea il file di configurazione .env locale
Crea un file .env nella root del progetto per configurare l'ambiente locale di Django. Ecco un esempio di configurazione:


```python
# DATABASE
DATABASE_NAME=fynd_db
DATABASE_USER=fynd_user
DATABASE_PASSWORD=fynd_password
DATABASE_HOST=db
DATABASE_PORT=5432

# Social Auth
GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET
APPLE_CLIENT_ID=APPLE_CLIENT_ID
APPLE_CLIENT_SECRET=APPLE_CLIENT_SECRET
APPLE_TEAM_ID=APPLE_TEAM_ID
APPLE_KEY_ID=APPLE_KEY_ID
APPLE_PRIVATE_KEY=APPLE_PRIVATE_KEY

# JWT
JWT_AUTH_HTTPONLY=True

# MAIL
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM_NAME=
```
Nota: Assicurati di sostituire le variabili GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ecc., con i tuoi valori reali per l'integrazione con i social media. Aggiungi anche le credenziali per l'invio delle email.

**Costruisci e avvia i container**

Esegui il seguente comando per avviare Docker Compose, che costruirà e avvierà i container definiti nel file docker-compose.yml:


```
    docker compose --env-file ./config/.env.docker up -d --build
```

Questo comando farà quanto segue:

Costruirà le immagini Docker per il servizio web e il database PostgreSQL.

Avvierà i container in background.

**Accedi al container web**

Per interagire con il container web, puoi eseguire il comando seguente:


```python
docker exec -it fynd_web bash
```
Questo comando ti permetterà di entrare nella shell del container fynd_web.

**Interagisci con il database**

Se hai bisogno di eseguire comandi relativi al database, puoi accedere alle variabili d'ambiente nel container web con il comando:

```python
docker exec -it fynd_web env | grep DATABASE
```
Questo ti mostrerà le variabili di configurazione del database attualmente in uso.

**Visualizza i log**

Per visualizzare i log del container web, puoi utilizzare il comando:

```python
docker logs fynd_web
```
Questo ti permetterà di monitorare l'output del server Django, utile per il debug e la verifica dello stato del servizio.

**Fermare i container**

Per fermare i container senza rimuoverli, puoi usare:

```python
docker compose down
```
Se desideri fermare i container e rimuovere le immagini, i volumi e i container orfani, puoi eseguire:


```python
docker compose down --rmi all --volumes --remove-orphans
```
Nota: Questo comando rimuove anche i volumi associati al progetto, quindi fai attenzione se hai dati importanti.

# Gestione del database
Se desideri rimuovere i volumi dei dati del database (per esempio, per ripartire da zero), puoi eseguire:

```python
docker volume rm fynd_postgres_data
```
Nota: Questo comando cancellerà tutti i dati del database, quindi usalo con cautela.


