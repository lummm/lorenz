FROM tengelisconsulting/num:3.8-buster
WORKDIR /app
COPY app.py app.py
COPY lorenz.py lorenz.py
ENTRYPOINT ["gunicorn", "app:server"]
