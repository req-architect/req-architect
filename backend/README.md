# Backend

This file describes the procedure for manually installing and running the API server.  
In most cases, it is recommended to deploy the entire application using Docker.  
Instructions can be found in the [README.md](../README.md) file.

## Installation

The system must have Python interpreter version 3.11 or higher installed.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the current directory and set the environment variables.  
Sample `.env` file:

```text
CORS_ALLOWED_ORIGINS="http://localhost:3000"
BACKEND_URL: http://localhost:8000
FRONTEND_URL: http://localhost:3000
GITHUB_CLIENT_ID: "**********"
GITHUB_CLIENT_SECRET: "**********"
GITLAB_CLIENT_ID: "**********"
GITLAB_CLIENT_SECRET: "**********"
JWT_SECRET: "**********"
REPOS_FOLDER="/repos"
```

The 'CORS_ALLOWED_ORIGINS' variable can take the form of a list of addresses separated by the `|` character, for example:

```text
CORS_ALLOWED_ORIGINS="http://localhost:3000|http://example.com"
```

To enable authorization, create applications on github.com and gitlab.com and generate a JWT secret.

### Creating an application on github.com

1. In [GitHub Developer settings](https://github.com/settings/apps), go to OAuthApps > New OAuth App.
2. Fill in the form:
   - Application name: any name
   - Homepage URL: `$FRONTEND_URL`
   - Authorization callback URL: `$BACKEND_URL/MyServer/login_callback/github`
3. Click "Register application."
4. Copy the "Client ID" value to the `.env` file as `GITHUB_CLIENT_ID`
5. Click "Generate a new client secret."
6. Copy the "Client secret" value to the `.env` file as `GITHUB_CLIENT_SECRET`

### Creating an application on gitlab.com

1. In [Gitlab settings](https://gitlab.com/-/user_settings/profile), go to Applications > New application.
2. Fill in the form:
   - Name: any name
   - Redirect URI: `$BACKEND_URL/MyServer/login_callback/gitlab`
   - Scopes: read_user, read_repository, write_repository, read_api
3. Click "Save application."
4. Copy the "Application ID" value to the `.env` file as `GITLAB_CLIENT_ID`
5. Copy the "Secret" value to the `.env` file as `GITLAB_CLIENT_SECRET`
6. Click "Continue."

### Generating JWT Secret

Generate the JWT secret using the command:

```bash
openssl rand -base64 256
```

OR

```bash
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
```

Copy the result to the `.env` file as `JWT_SECRET`

## Running the Server

```bash
python3 src/manage.py runserver
```

## Tests + Coverage
In the venv:

```bash
coverage run src/manage.py test
coverage html
coverage report
```