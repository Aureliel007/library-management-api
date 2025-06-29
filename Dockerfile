FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./alembic.ini /app/
COPY ./alembic /app/alembic
COPY ./entrypoint.sh /app/

COPY ./app /app/app

CMD ["sh", "/app/entrypoint.sh"]