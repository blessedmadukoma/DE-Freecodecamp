FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client

COPY elt_script .

CMD [ "python", "elt_script.py" ]