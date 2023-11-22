# PZSP2-KUKIWAKO

Projekt z przedmiotu PZSP2 w semestrze 23Z.  
Zespół nr 10 - KUKIWAKO  

Skład:

- Nel Kułakowska
- Marcin Wawrzyniak
- Jan Kowalczewski
- Mateusz Kiełbus

## Cel projektu
Celem naszego projektu jest stworzenie serwisu internetowego umożlwiającego zarządzanie wymaganiami w projektach informatycznych z pomocą nakładki graficznej na narzędzie „doorstop”. Aplikacja będzie skierowana dla osób nietechnicznych, aby nie musiały wykonywać poszczególnych komend z poziomu konsoli. Przedstawi im strukturę wymagań w postaci czytelnego diagramu UML. Pozwoli na integrację z wybranym zdalnym repozytorium git.

## Instalacja i uruchamianie w trybie deweloperskim

Instrukcje dotyczące manualnej instalacji i uruchomienia wszystkich komponentów oddzielnie znajdują się w plikach [Frontend](frontend/README.md) i [Backend](backend/README.md).

Niniejsza instrukcja dotyczy uruchomienia aplikacji za pomocą środowiska Docker.  
Należy upewnić się, że w systemie zainstalowane są `docker` oraz `docker-compose`.

### Przygotowanie środowiska

W katalogu głównym projektu należy utworzyć plik `.env` i ustawić w nim zmienne środowiskowe.

Przykładowy plik `.env`:

```text
APP_ADDRESS="http://localhost"
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
