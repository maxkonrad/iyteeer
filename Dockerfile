FROM python:3.11-slim

WORKDIR /app

# Gereksinimleri kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# Render için ortam değişkeni ayarlaması (varsayılan)
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]