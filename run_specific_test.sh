#!/bin/bash

TEST_NAME=$1

if [ -z "$TEST_NAME" ]; then
    echo "Vennligst spesifiser test navn"
    echo "Tilgjengelige tester:"
    echo "- env_vars"
    echo "- api_connection"
    echo "- model_list"
    echo "- code_analysis"
    exit 1
fi

docker-compose -f docker-compose.test.yml run --rm ai-test python tools/test_suite.py --test $TEST_NAME