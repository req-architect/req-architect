# Frontend

This file describes the procedure for manually installing and running the web server.  
In most cases, it is recommended to deploy the entire application using Docker.  
Instructions can be found in the [README.md](../README.md) file.

## Installation

The system must have Node.js interpreter version 18 or higher installed.

```bash
npm install
```

## Environment Setup

Create a `.env` file in the current directory and set the environment variables.  
Sample `.env` file:

```text
VITE_APP_API_URL="http://localhost:8000"
```

## Running the Server

Before running the web application, make sure that the API server is up and running.

```bash
npm run dev
```