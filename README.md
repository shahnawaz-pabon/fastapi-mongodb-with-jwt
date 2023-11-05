<div align="center">
  <img alt="fastapi-jwt" height="100px" width="100px" src="logo.png" />
  <h1>JWT implementation with FastAPI, MongoDB</h1>
</div>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/Awesome-FastAPI-informational?style=for-the-badge&logo=fastapi&labelColor=17202A&color=1abc9c&logoColor=1abc9c" alt="Awesome">
  </a>
</p>

# Table of Contents

- [Project Structure](#project-structure)
- [Up and Run](#up-and-run)

## Project Structure

```sh
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── core
│       ├── __init__.py
│       ├── config.py
│       └── ...
│   ├── db
│       ├── __init__.py
│       ├── database.py
│       └── ...
│   ├── models
│       ├── __init__.py
│       ├── user.py
│       └── ...
│   └── endpoints
│       ├── __init__.py
│       ├── user.py
│       └── ...
├── docker-compose.yml
├── Dockerfile
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Up and Run

```sh
git clone https://github.com/shahnawaz-pabon/fastapi-mongodb-with-jwt.git
cd fastapi-mongodb-with-jwt
docker-compose up --build
```
Behold the swagger of our application, gracefully accessible at [http://0.0.0.0:8081/docs/](http://0.0.0.0:8081/docs/).