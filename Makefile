
# Installs all dependencies
setup:
	@make poetry-setup
	@make lakefs-setup

# Installs poetry and poetry dependencies
poetry-setup:
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
	@docker run --name lakefs -p 8000:8000 -d treeverse/lakefs:0.105.0 run --quickstart
	# Waiting until the container has started completely
	@sleep 3
	@poetry run python scripts/lakefs_setup.py


# Starts dagster development server
dagster-start:
	@poetry run dagster dev

# Starts all servers again
start:
	@make lakefs-start
	@make dagster-start
