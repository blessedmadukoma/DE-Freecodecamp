FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client cron

# Install python-dotenv
RUN pip install python-dotenv

COPY start.sh /app/start.sh

COPY elt_script.py .

COPY .env .

WORKDIR /app

# Run cron job by 3am in the morning
RUN "0 3 * * * python /app/elt_script.py" | crontab -

CMD [ "python", "elt_script.py" ]