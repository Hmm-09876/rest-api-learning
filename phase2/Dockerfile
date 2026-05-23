FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


############################################################################################
FROM python:3.10-slim

WORKDIR /app 

COPY app/ .

COPY requirements.txt .

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

EXPOSE 5000

COPY wait-for-db.py .

CMD ["sh", "-c", "python -u wait-for-db.py && python -u app.py"]
