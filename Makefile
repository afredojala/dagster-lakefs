
# Installs all dependencies
setup:
	@poetry self add poetry-dotenv-plugin
	@poetry install

# Starts the lakefs container if it is not already running
lakefs-start:
	@if [ -z "$(shell docker ps -q -f name=lakefs)" ]; then \
		docker start lakefs; \
	else \
		echo "LakeFS is already running"; \
	fi


# Sets up lakefs container and creates a repository
lakefs-setup:
	@docker --name lakefs -p 8000:8000 -d treeverse/lakefs:latest run --quickstart
	@poetry run python scripts/lakefs_setup.py


# Starts dagster development server
dagster-start:
	@poetry run dagster dev -m dagster_lakefs
