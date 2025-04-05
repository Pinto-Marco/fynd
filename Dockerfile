FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn


COPY . .

# Expose port 8000 for Gunicorn
EXPOSE 8000

RUN useradd -m -s /bin/bash dockeruser \
    && echo "dockeruser:password" | chpasswd \
    && adduser dockeruser sudo


# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# CMD [ "/init.sh" ]

COPY init.sh /init.sh
RUN chmod +x /init.sh
CMD ["/bin/bash", "/init.sh"]
