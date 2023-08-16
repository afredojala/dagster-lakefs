# Dagster LakeFS

This is an example and playground repository for utilizing Dagster, LakeFS and dbt together.
The aim of the repository is to investigate if it is possible to run dbt tests before committing the transformed data
into the data lake

## Prerequisites

You need to have poetry, docker and Make installed to easily run the project

## Start the project

Before starting the project, create a .env file with the following variables

```bash
LAKEFS_ACCESS_KEY=AKIAIOSFOLQUICKSTART
LAKEFS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
LAKEFS_HOST=localhost:8000
LAKEFS_REPO=example-repo
```

Then run the following commands

```bash
make setup
make start
```

and the project should be up and running
