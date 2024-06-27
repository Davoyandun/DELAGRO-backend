# Makefile
PYTHON := python
PIP := pip
UVICORN := uvicorn
BLACK := black
PYTEST := pytest

SRC_DIR := src
APP := $(SRC_DIR)/main.py
TEST_DIR := tests
.PHONY: all run test format install

install:
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=$(SRC_DIR) $(UVICORN) main:app --reload

test:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(TEST_DIR)

format:
	$(BLACK) $(SRC_DIR)

all: install format test run
