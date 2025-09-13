.PHONY: help install run-dev cloud-build clear code-formatting update-requirements cloud-build-test

help:
	@echo "Local examples:"
	@echo "    make run-dev       		# Starts a uvicorn development server locally."
	@echo "    make update-requirements	# Resolve versions for requirements.txt based on your previous installation."
	@echo "    make install       		# Install dependencies from requirements.txt."
	@echo "    make cloud-build   		# Submits a build to Google Cloud."
	@echo "    make clear         		# Removes cache directories."

update-requirements:
	python update_requirements.py

run-dev:
	uvicorn app.main:run --timeout-keep-alive 60 --port 8080

clear:
	find . -type d -name '__pycache__' -exec rm -rf {} + && \
	find . -type d -name 'pytest_cache' -exec rm -rf {} + && \
	find . -type d -name '.ipynb_checkpoints' -exec rm -rf {} + && \
	find . -type d -name '.ruff_cache' -exec rm -rf {} +