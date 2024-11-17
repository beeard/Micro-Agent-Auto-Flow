#!/bin/bash

# Kjør kun kritiske tester
pytest tests/test_critical.py -v

# Hvis kritiske tester passerer, kjør framework-tester
if [ $? -eq 0 ]; then
    pytest tests/test_framework.py -v
fi