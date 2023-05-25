FROM python:3.10 AS builder

WORKDIR /app

EXPOSE 5000

RUN apt-get update -y

RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'libgl1' \
    'libglib2.0-0' -y

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python src/app.py
