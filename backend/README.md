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
CORS_ALLOWED_ORIGINS="http://localhost:3000"
BACKEND_URL: http://localhost:8000
FRONTEND_URL: http://localhost:3000
GITHUB_CLIENT_ID: "**********"
GITHUB_CLIENT_SECRET: "**********"
GITLAB_CLIENT_ID: "**********"
GITLAB_CLIENT_SECRET: "**********"
JWT_SECRET: "**********"
```

Zmienna 'CORS_ALLOWED_ORIGINS' może przyjąć formę listy adresów oddzielonych znakiem `|`, np

```text
CORS_ALLOWED_ORIGINS="http://localhost:3000|http://example.com"
```

Aby umożliwić autoryzację należy utworzyć aplikacje na serwisie github.com oraz gitlab.com i wygenerować sekret JWT.

### Tworzenie aplikacji na github.com

1. W [ustawieniach deweloperskich GitHub](https://github.com/settings/apps) przejść do OAuthApps > New OAuth App.
2. Wypełnić formularz:
    - Application name: dowolna nazwa
    - Homepage URL: `$FRONTEND_URL`
    - Authorization callback URL: `$BACKEND_URL/MyServer/login_callback/github`
3. Kliknąć "Register application".
4. Skopiować wartość "Client ID" do pliku `.env` jako wartość `GITHUB_CLIENT_ID`.
5. Kliknąć "Generate a new client secret".
6. Skopiować wartość "Client secret" do pliku `.env` jako wartość `GITHUB_CLIENT_SECRET`.

### Tworzenie aplikacji na gitlab.com

1. W [ustawieniach Gitlab](https://gitlab.com/-/user_settings/profile) przejść do Applications > New application.
2. Wypełnić formularz:
    - Name: dowolna nazwa
    - Redirect URI: `$BACKEND_URL/MyServer/login_callback/gitlab`
    - Scopes: read_user, read_repository, write_repository
3. Kliknąć "Save application".
4. Skopiować wartość "Application ID" do pliku `.env` jako wartość `GITLAB_CLIENT_ID`.
5. Skopiować wartość "Secret" do pliku `.env` jako wartość `GITLAB_CLIENT_SECRET`.
6. Kliknąć "Continue"

### Generowanie sekretu JWT

Sekret JWT można wygenerować za pomocą polecenia:

```bash
openssl rand -base64 256
```
LUB
```bash
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
```

Wynik należy skopiować do pliku `.env` jako wartość `JWT_SECRET`.

## Uruchomienie serwera

```bash
python3 src/manage.py runserver
```

## Testy + coverage
W venv:   
```bash
pip install coverage
coverage run src/manage.py test
coverage html
coverage report
```