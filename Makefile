PACKAGES={package_name}

test:
	bin/test $(PACKAGES) \
		--with-coverage --cover-package="$(PACKAGES)" \
		--cover-erase --cover-html --cover-html-dir=parts/html

show-coverage: test
	xdg-open parts/html/index.html

# Check code quality.
check:
	bin/pylint --rcfile .pylintrc $(PACKAGES) > parts/pylint.html

show-check: check
	xdg-open parts/pylint.html

# Creating environment.

bootstrap:
	python bootstrap.py

buildout:
	bin/buildout -v

# Create source distribution.
source_dist:
	python setup.py sdist
