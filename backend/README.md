# Backend

Ten plik opisuje procedurę manualnej instalacji i uruchomienia serwera API.  
W większości przypadków zaleca się postawienie całej aplikacji za pomocą środowiska Docker.  
Instrukcja znajduje się w pliku [README.md](../README.md).

## Instalacja

W systemie musi znajdować się interpreter Pythona w wersji 3.11 lub wyższej.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ustawienie środowiska

Należy utworzyć plik `.env` w aktualnym katalogu i ustawić w nim zmienne środowiskowe.    
Przykładowy plik `.env`:

```text
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="pass"
DB_HOST="localhost"
DB_PORT="5432"
CORS_ALLOWED_ORIGINS="http://localhost:3000"
```

Zmienna 'CORS_ALLOWED_ORIGINS' może przyjąć formę listy adresów oddzielonych znakiem `|`, np
    
```text
CORS_ALLOWED_ORIGINS="http://localhost:3000|http://example.com"
```

## Uruchomienie serwera

Przed uruchomieniem serwera należy upewnić się, że baza danych jest uruchomiona.  
Minimalna wersja to PostgreSQL 16.

```bash
python3 src/manage.py runserver
```
