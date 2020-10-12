FROM python:3.8.6-slim-buster
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN apt update \
        && apt install --assume-yes \
        build-essential \
        && python3 -m pip install -r ./requirements.txt \
        && apt autoremove --assume-yes build-essential
COPY app.py app.py
COPY lorenz.py lorenz.py
ENTRYPOINT ["gunicorn", "app:server"]
