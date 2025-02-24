# ReqArchitect

Project for the PZSP2 course in the 23Z semester, Warsaw University of Technology.

Team members:

-   Nel Kułakowska
-   Marcin Wawrzyniak
-   Jan Kowalczewski
-   Mateusz Kiełbus

## License

MIT License

Copyright (c) 2024 Jan Kowalczewski, Marcin Wawrzyniak, Nel Kułakowska and Mateusz Kiełbus, Warsaw University of Technology, 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Project Objective

The goal of our project is to create a web service that serves as a graphical interface for the "doorstop" tool. The application is designed for non-technical users, eliminating the need for executing commands through the console. It will facilitate the generation of UML diagrams from doorstop requirement files and integrate with a chosen remote Git repository.

## Installation and Running in Developer Mode

Instructions for manually installing and running each component separately can be found in the [Frontend](frontend/README.md) and [Backend](backend/README.md) directories.

This guide covers running the application using Docker.  
Make sure that `docker` and `docker-compose` are installed on your system.

### Environment Setup

In the project's root directory, create a `.env` file and set the environment variables.

Sample `.env` file:

```text
FRONTEND_URL="http://localhost:3000"
BACKEND_URL="http://localhost:8000"
GITHUB_CLIENT_ID="*************"
GITHUB_CLIENT_SECRET="*************"
GITLAB_CLIENT_ID="*************"
GITLAB_CLIENT_SECRET="*************"
JWT_SECRET="*************"
SERVER_TEST_MODE=0
```

To enable authorization, create applications on github.com and gitlab.com and generate a JWT secret.

#### Creating an application on github.com

1. In [GitHub Developer settings](https://github.com/settings/apps), go to OAuthApps > New OAuth App.
2. Fill in the form:
   - Application name: any name
   - Homepage URL: `$FRONTEND_URL`
   - Authorization callback URL: `$BACKEND_URL/api/login_callback/github`
3. Click "Register application."
4. Copy the "Client ID" value to the `.env` file as `GITHUB_CLIENT_ID`
5. Click "Generate a new client secret."
6. Copy the "Client secret" value to the `.env` file as `GITHUB_CLIENT_SECRET`

#### Creating an application on gitlab.com

1. In [Gitlab settings](https://gitlab.com/-/user_settings/profile), go to Applications > New application.
2. Fill in the form:
   - Name: any name
   - Redirect URI: `$BACKEND_URL/api/login_callback/gitlab`
   - Scopes: read_user, read_repository, write_repository, read_api
3. Click "Save application."
4. Copy the "Application ID" value to the `.env` file as `GITLAB_CLIENT_ID`
5. Copy the "Secret" value to the `.env` file as `GITLAB_CLIENT_SECRET`
6. Click "Continue."

#### Generating JWT Secret

Generate the JWT secret using the command:

```bash
openssl rand -base64 256
```

OR

```bash
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
```

Copy the result to the `.env` file as `JWT_SECRET`

### Building Containers

```bash
docker-compose build
```

### Running and Stopping in Normal Mode

To run:

```bash
docker-compose up
```

Stop by pressing `Ctrl+C`.

### Running and Stopping in the Background

To run:

```bash
docker-compose up -d
```

To stop:

```bash
docker-compose down
```

### Code Changes During Application Runtime

All changes in the `frontend/src` and `backend/src` directories are automatically detected and applied in the containers.

## Running a "Non-local" Server

`.env` file:

```text
FRONTEND_URL="https://kukiwako.serveo.net"
BACKEND_URL="https://kukiwakobackend.serveo.net"
```

```bash
docker-compose build
docker-compose up -d
```

In one terminal:

```bash
ssh -R kukiwakobackend.serveo.net:80:localhost:8000 serveo.net
```

In another:

```bash
ssh -R kukiwako.serveo.net:80:localhost:3000 serveo.net
```

Or in one command:

```bash
ssh -R kukiwakobackend.serveo.net:80:localhost:8000 -R kukiwako.serveo.net:80:localhost:3000 serveo.net
```

## Running the Server in Test Mode

To run the server in test mode (for conducting integration tests), set the environment variable `SERVER_TEST_MODE=1`. The test mode completely ignores Git integrations (authorization, operations on the remote repository).

## Running the Server in Production Mode

Copy the `.env` file to `.env.prod`.  
Then add environment variables:

```text
BACKEND_PORT=8000
FRONTEND_PORT=3000
REPOS_HOST_FOLDER="/home/jani/pzsp2-repos"
```

Run:

```bash
docker compose -f docker-compose-prod.yml --env-file .env.prod up --build
```

After starting, redirect the frontend and backend URLs to the declared ports, e.g.,:

```bash
ssh -R kukiwakobackend.serveo.net:80:localhost:8000 -R kukiwako.serveo.net:80:localhost:3000 serveo.net
```

Communication from the public network must be done over HTTPS.
