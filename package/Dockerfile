FROM python:3.9.11

WORKDIR /app
COPY . /app

RUN pip3 --no-cache  install Flask Flask-Mail flask-ipban datetime SQLAlchemy psycopg2

EXPOSE 5004
ENTRYPOINT ["python3"]
CMD ["server.py"]
