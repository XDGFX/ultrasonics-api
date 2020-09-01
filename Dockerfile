FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

ENV FLASK_APP=ultrasonics_api USE_REDIS=False

RUN pip install -r requirements.txt 

EXPOSE 8003

ENTRYPOINT ["./app.sh"]
