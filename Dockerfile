FROM python:3.11-slim

WORKDIR /usr/src/app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

EXPOSE 3000

CMD ["python","-m","uvicorn","app:app","--host","0.0.0.0","--port","3000"]
