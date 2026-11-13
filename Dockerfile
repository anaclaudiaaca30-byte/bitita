FROM python:3.12-slim

WORKDIR /app

COPY webapp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "exec python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
