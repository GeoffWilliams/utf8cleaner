test:
	python -m pytest --capture=no --cov=utf8cleaner tests/

package:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

clean:
	rm dist/*

dev_env:
	pip3 install -e .
