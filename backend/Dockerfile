FROM python:3.9.16-slim

COPY . /app
WORKDIR /app

# runs virtual env
RUN python3 -m venv /opt/venv

# this installs and makes sure things can run
RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]