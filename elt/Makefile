# Run airlfow orchestration

airflow_up:
	docker-compose up init-airflow -d 

docker_up: airflow_up
	@echo "Waiting for 3 seconds..."
	sleep 3
	@echo "Running the rest..."
	docker-compose up -d

docker_down:
	docker-compose down -v

pg_destination:
	docker exec -it elt-destination_postgres-1 psql -U postgres

.PHONY: airflow_up docker_up docker_down