FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Uygulama portunu aç
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"] 