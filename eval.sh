#!/bin/bash
docker-compose up -d --build

docker-compose run --rm web python assessment_app/utils/init_db.py

docker-compose run --rm \
  -v $(pwd)/assessment_app/data:/app/data \
  -e PYTHONPATH=/app \
  web python assessment_app/utils/load_prices.py