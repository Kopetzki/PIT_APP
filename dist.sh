#!/bin/bash

rm -fr dist/
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*

