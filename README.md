# PZSP2-KUKIWAKO

Projekt z przedmiotu PZSP2 w semestrze 23Z.  
Zespół nr 7 - KUKIWAKO

Skład:

- Nel Kułakowska
- Marcin Wawrzyniak
- Jan Kowalczewski
- Mateusz Kiełbus

## Cel projektu

Celem naszego projektu jest stworzenie serwisu internetowego będącego nakładką graficzną na narzędzie "doorstop". Aplikacja będzie skierowana dla osób nietechnicznych, aby nie musiały wykonywać poszczególnych komend z poziomu konsoli. Pozwoli na generowanie diagramów UML zawarte w plikach z wymaganiami doorstop i integrację z wybranym zdalnym repozytorium git.

## Instalacja i uruchamianie w trybie deweloperskim

Instrukcje dotyczące manualnej instalacji i uruchomienia wszystkich komponentów oddzielnie znajdują się w plikach [Frontend](frontend/README.md) i [Backend](backend/README.md).

Niniejsza instrukcja dotyczy uruchomienia aplikacji za pomocą środowiska Docker.  
Należy upewnić się, że w systemie zainstalowane są `docker` oraz `docker-compose`.

### Przygotowanie środowiska

W katalogu głównym projektu należy utworzyć plik `.env` i ustawić w nim zmienne środowiskowe.

Przykładowy plik `.env`:

```text
FRONTEND_URL="http://localhost:3000"
BACKEND_URL="http://localhost:8000"
```

### Zbudowanie kontenerów

```bash
docker-compose build
```

### Uruchomienie i zatrzymanie w trybie zwykłym

Uruchomienie:

```bash
docker-compose up
```

Zatrzymanie poprzez wciśnięcie `Ctrl+C`.

### Uruchomienie i zatrzymanie w tle

Uruchomienie:

```bash
docker-compose up -d
```

Zatrzymanie:

```bash
docker-compose down
```

### Zmiany w kodzie podczas działania aplikacji

Wszystkie zmiany w katalogach `frontend/src` i `backend/src` są automatycznie wykrywane i aplikowane w kontenerach.

## Uruchomienie "nielokalnego" serwera

Plik ".env":

```text
FRONTEND_URL="https://kukiwako.serveo.net"
BACKEND_URL="https://kukiwakobackend.serveo.net"
```

```bash
docker-compose up
```

w jednym terminalu:

```bash
 ssh -R kukiwakobackend.serveo.net:80:localhost:8000 serveo.net
```

w drugim:

```bash
 ssh -R kukiwako.serveo.net:80:localhost:3000 serveo.net
```
