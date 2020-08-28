FROM python:3.8.5-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
