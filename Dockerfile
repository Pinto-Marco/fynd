FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# Installa netcat per lo script di wait-for-db
RUN apt-get update && apt-get install -y netcat-openbsd bash


COPY . .

# Expose port 8000 for Gunicorn
EXPOSE 8000

RUN useradd -m -s /bin/bash dockeruser \
    && echo "dockeruser:password" | chpasswd \
    && adduser dockeruser sudo

COPY init.sh /init.sh
COPY wait_for_db.sh /wait_for_db.sh

RUN chmod +x /init.sh /wait_for_db.sh

# Verifica i permessi
RUN ls -l /wait_for_db.sh

RUN which bash


CMD ["/bin/bash", "/init.sh"]
