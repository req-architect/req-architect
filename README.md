# PZSP2-KUKIWAKO

Projekt z przedmiotu PZSP2 w semestrze 23Z.  
Zespół nr 7 - KUKIWAKO

Skład:

-   Nel Kułakowska
-   Marcin Wawrzyniak
-   Jan Kowalczewski
-   Mateusz Kiełbus

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
GITHUB_CLIENT_ID="*************"
GITHUB_CLIENT_SECRET="*************"
GITLAB_CLIENT_ID="*************"
GITLAB_CLIENT_SECRET="*************"
JWT_SECRET="*************"
```

Aby umożliwić autoryzację należy utworzyć aplikacje na serwisie github.com oraz gitlab.com i wygenerować sekret JWT.

#### Tworzenie aplikacji na github.com

1. W [ustawieniach deweloperskich GitHub](https://github.com/settings/apps) przejść do OAuthApps > New OAuth App.
2. Wypełnić formularz:
    - Application name: dowolna nazwa
    - Homepage URL: `$FRONTEND_URL`
    - Authorization callback URL: `$BACKEND_URL/MyServer/login_callback/github`
3. Kliknąć "Register application".
4. Skopiować wartość "Client ID" do pliku `.env` jako wartość `GITHUB_CLIENT_ID`.
5. Kliknąć "Generate a new client secret".
6. Skopiować wartość "Client secret" do pliku `.env` jako wartość `GITHUB_CLIENT_SECRET`.

#### Tworzenie aplikacji na gitlab.com

1. W [ustawieniach Gitlab](https://gitlab.com/-/user_settings/profile) przejść do Applications > New application.
2. Wypełnić formularz:
    - Name: dowolna nazwa
    - Redirect URI: `$BACKEND_URL/MyServer/login_callback/gitlab`
    - Scopes: read_user, read_repository, write_repository, read_api
3. Kliknąć "Save application".
4. Skopiować wartość "Application ID" do pliku `.env` jako wartość `GITLAB_CLIENT_ID`.
5. Skopiować wartość "Secret" do pliku `.env` jako wartość `GITLAB_CLIENT_SECRET`.
6. Kliknąć "Continue"

#### Generowanie sekretu JWT

Sekret JWT można wygenerować za pomocą polecenia:

```bash
openssl rand -base64 256
```

LUB

```bash
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
```

Wynik należy skopiować do pliku `.env` jako wartość `JWT_SECRET`.

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
