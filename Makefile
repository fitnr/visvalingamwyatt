# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, fitnr <contact@fakeisthenewreal.org>

QUIET = -q

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	- python setup.py check --restructuredtext --strict

.PHONY: install test upload build
install: README.rst
	python setup.py install

cov:
	- coverage run --include='visvalingamwyatt/*' setup.py $(QUIET) test
	coverage report
	coverage html

test:
	tox
	
upload: README.rst | clean build
	twine upload dist/*
	git push
	git push --tags

build: ; python3 setup.py sdist bdist_wheel --universal

clean: ; rm -rf dist