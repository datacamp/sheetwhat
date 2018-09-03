clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -rf sheetwhat.egg-info

build: clean
    pip install -r requirements.txt
    pip install -e .

test: 
	pytest --cov=sheetwhat
	codecov
