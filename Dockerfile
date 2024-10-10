FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.lock

CMD ["python3", "./app/run.py"]