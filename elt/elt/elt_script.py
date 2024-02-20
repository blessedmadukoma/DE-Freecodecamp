import subprocess
import time
import os
from dotenv import load_dotenv

# load_dotenv("../.env")
load_dotenv()


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
  print(f"ENV configs: {os.environ.get('POSTGRES_SOURCE_DB')}, {os.environ.get('POSTGRES_DESTINATION_DB')}, {os.environ.get('POSTGRES_USER')}, {os.environ.get('POSTGRES_PASSWORD')}")
  retries = 0

  while retries < max_retries:
    try:
      result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
      if "accepting connections" in result.stdout:
        print("Successfully connected to Postgres")
        return True
      
    except subprocess.CalledProcessError as e:
      print(f"Error connecting to Postgres: {e}")

      retries += 1

      print(f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")

      time.sleep(delay_seconds)
  
  print("Max retries reached. Exiting")
  return False

if not wait_for_postgres(host="source_postgres"):
  print("Cant wait for postgres")
  exit(1)

print("Starting ELT Script...")

source_config = {
  "dbname": os.environ.get("POSTGRES_SOURCE_DB"),
  "user": os.environ.get("POSTGRES_USER"),
  "password": os.environ.get("POSTGRES_PASSWORD"),
  "host": "source_postgres"
}

destination_config = {
  "dbname": os.environ.get("POSTGRES_DESTINATION_DB"),
  "user": os.environ.get("POSTGRES_USER"),
  "password": os.environ.get("POSTGRES_PASSWORD"),
  "host": "destination_postgres"
}

dump_command = [
  "pg_dump",
  "-h", source_config["host"],
  "-U", source_config["user"],
  "-d", source_config["dbname"],
  "-f", "data_dump.sql",
  "-w"
]

subprocess_env = dict(PGPASSWORD=source_config["password"])

subprocess.run(dump_command, env=subprocess_env, check=True)

# Load to destination
load_command = [
  'psql',
  '-h', destination_config["host"],
  '-U', destination_config["user"],
  '-d', destination_config["dbname"],
  '-a', '-f', 'data_dump.sql'
]

subprocess_env = dict(PGPASSWORD=destination_config["password"])

subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending ELT Script...")