FROM python:3

WORKDIR /data

COPY . .
RUN pip install -r requirements.txt

CMD gunicorn -k eventlet -b 0.0.0.0:5000 -w 1 --threads 5 app:app
