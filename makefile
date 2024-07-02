# Makefile
PYTHON := python
PIP := pip
UVICORN := uvicorn
BLACK := black
PYTEST := pytest

SRC_DIR := app
APP := $(SRC_DIR)/main.py
TEST_DIR := __test__
.PHONY: all run test format install

install:
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=$(SRC_DIR) $(UVICORN) main:app --reload

test:
	$(PYTEST) $(TEST_DIR)

format:
	$(BLACK) $(SRC_DIR)

all: install format test run
