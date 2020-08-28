FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt 

EXPOSE 8003

ENTRYPOINT ["./app.sh"]
