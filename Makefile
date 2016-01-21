# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, fitnr <contact@fakeisthenewreal.org>

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

.PHONY: install test upload
install: README.rst
	python setup.py install

test: README.rst
	python setup.py install	
	
upload: README.rst | clean
	python setup.py register
	python setup.py bdist_wheel
	python3 setup.py bdist_wheel
	twine upload dist/*
	git push
	git push --tags

clean: ; rm -rf dist