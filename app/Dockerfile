FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-pip

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

WORKDIR /app

COPY . /app

CMD ["python3", "main.py"]