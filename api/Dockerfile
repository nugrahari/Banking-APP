FROM tiangolo/uvicorn-gunicorn:python3.7

# RUN apt-get clean && apt-get update && apt-get install -y libpq-dev python3-dev

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt

#RUN mkdir -p /var/log/

WORKDIR /app
