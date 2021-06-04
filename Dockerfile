FROM python:3.8.5

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

LABEL author='DmitriyReztsov' version=1

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000