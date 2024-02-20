FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client

# Install python-dotenv
RUN pip install python-dotenv

COPY elt_script.py .

COPY .env .

CMD [ "python", "elt_script.py" ]