#!/bin/sh


echo "Aspettando che il database sia disponibile..."
sleep 60

# Prova a connetterti fino a quando il DB non risponde sulla porta
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo "Ancora nessuna connessione su $DATABASE_HOST:$DATABASE_PORT, riprovo tra 1s..."
  sleep 1
done

echo "Database è disponibile! Continuo..."