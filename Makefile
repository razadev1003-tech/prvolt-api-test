.PHONY: run lint type install

# Run the FastAPI server (reload enabled for development)
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8800

# Install dependencies from requirements.txt
install:
	pip install -r requirements.txt

# Lint with flake8 + wemake-python-styleguide
lint:
	flake8 .

# Type checking with mypy (strict)
type:
	mypy --strict .
