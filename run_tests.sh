#!/bin/bash

# Kjør enhetstester først
echo "Kjører enhetstester..."
pytest

# Hvis enhetstestene passerer, kjør integrasjonstester
if [ $? -eq 0 ]; then
    echo "Kjører integrasjonstester..."
    docker-compose -f docker-compose.test.yml build --no-cache
    docker-compose -f docker-compose.test.yml up
    docker-compose -f docker-compose.test.yml down
else
    echo "Enhetstester feilet. Stopper testing."
    exit 1
fi