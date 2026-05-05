FROM python:3.11-slim

WORKDIR /app

# تثبيت dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع
COPY . .

# فتح البورت
EXPOSE 8000

# تشغيل السيرفر
CMD ["python", "-m", "http.server", "8000"]