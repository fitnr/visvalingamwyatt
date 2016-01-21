#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, fitnr <contact@fakeisthenewreal.org>
import json
import unittest
import visvalingamwyatt as vw
from visvalingamwyatt import cli

class TestCase(unittest.TestCase):
    def setUp(self):
        with open('tests/data/sample.json') as f:
            self.json = json.load(f)

    def testSimplifyFeature(self):
        fixture = self.json['features'][0]
        result = vw.simplify_feature(fixture)

        assert 'geometry' in result
        assert 'properties' in result
        assert result['properties'] == fixture['properties']

        assert fixture['geometry']['type'] == result['geometry']['type']

        assert fixture['geometry']['coordinates'][0] == result['geometry']['coordinates'][0]

        assert len(fixture['geometry']['coordinates']) > len(result['geometry']['coordinates'])
