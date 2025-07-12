#!/bin/bash

docker run -v /data:/data:ro -v ./src:/app -v ./data.json:/app/data.json:ro --network database_network --env-file .env $(docker build -q .) python3 /app/main.py $@