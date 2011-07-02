bootstrap:
	python bootstrap.py

buildout:
	bin/buildout -v

# Create source distribution.
source_dist:
	python setup.py sdist
