# Makefile

# Variables
PYTHON := python
PIP := pip
UVICORN := uvicorn
BLACK := black
PYTEST := pytest

# Directorios y archivos
SRC_DIR := src
APP := $(SRC_DIR)/main.py
TEST_DIR := tests

# Reglas
.PHONY: all run test format install

# Instalar dependencias
install:
	$(PIP) install -r requirements.txt

# Correr la aplicación
run:
	PYTHONPATH=$(SRC_DIR) $(UVICORN) main:app --reload

# Ejecutar tests
test:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(TEST_DIR)

# Formatear el código
format:
	$(BLACK) $(SRC_DIR) $(TEST_DIR)

# Ejecutar todas las reglas
all: install format test run
