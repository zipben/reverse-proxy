FROM python:3.9-slim

WORKDIR /app

COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp /app

CMD ["flask", "run", "--host=0.0.0.0"] 