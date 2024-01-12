FROM python:3.10.13-alpine3.19

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]