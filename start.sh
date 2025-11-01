#/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker weather_api.main:app
