# Makefile for GenAI Bedrock Microservice

.PHONY: help init plan apply destroy test lint format clean install-deps

# Default target
help:
	@echo "Available targets:"
	@echo "  init         - Initialize Terraform"
	@echo "  plan         - Plan Terraform deployment"
	@echo "  apply        - Apply Terraform configuration"
	@echo "  destroy      - Destroy Terraform resources"
	@echo "  test         - Run Python tests"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean build artifacts"
	@echo "  install-deps - Install Python dependencies"

# Terraform targets
init:
	terraform init

plan:
	terraform plan

apply:
	terraform apply

destroy:
	terraform destroy

# Python targets
install-deps:
	pip install -r lambda/requirements.txt
	pip install -r tests/requirements.txt

test:
	cd tests && python -m pytest test_lambda_function.py -v --cov=../lambda --cov-report=html

lint:
	flake8 lambda/ tests/ --max-line-length=120
	bandit -r lambda/

format:
	black lambda/ tests/ --line-length=120
	isort lambda/ tests/

# Cleanup
clean:
	rm -f lambda_function.zip
	rm -rf __pycache__/
	rm -rf lambda/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage

# Package Lambda function
package:
	cd lambda && zip -r ../lambda_function.zip . -x "*.pyc" "__pycache__/*"

# Validate Terraform
validate:
	terraform validate
	terraform fmt -check
