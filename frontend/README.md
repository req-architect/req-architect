# Frontend

Ten plik opisuje procedurę manualnej instalacji i uruchomienia serwera webowego.  
W większości przypadków zaleca się postawienie całej aplikacji za pomocą środowiska Docker.  
Instrukcja znajduje się w pliku [README.md](../README.md).

## Instalacja

W systemie musi znajdować się interpreter Node.js w wersji 18 lub wyższej.

```bash
npm install
```

## Ustawienie środowiska

Należy utworzyć plik `.env` w aktualnym katalogu i ustawić w nim zmienne środowiskowe.  
Przykładowy plik `.env`:

```text
VITE_APP_API_URL="http://localhost:8000"
```

## Uruchomienie serwera

Przed uruchomieniem aplikacji webowej należy upewnić się, że serwer API jest uruchomiony.

```bash
npm run dev
```
