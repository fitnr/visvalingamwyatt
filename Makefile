# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, 2021, fitnr <contact@fakeisthenewreal.org>

.PHONY: install test upload build cov

install:
	python setup.py install

cov:
	- coverage run --include='visvalingamwyatt/*' -m unittest
	coverage report
	coverage html

test:
	tox
	
upload: | clean build
	twine upload dist/*
	git push
	git push --tags

build: ; python3 setup.py sdist bdist_wheel --universal

clean: ; rm -rf dist