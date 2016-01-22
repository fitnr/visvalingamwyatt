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
            self.fixture = json.load(f).get('features')[0]

    def standard(self, **kwargs):
        result = vw.simplify_feature(self.fixture, **kwargs)

        assert 'geometry' in result
        assert 'properties' in result
        assert result['properties'] == self.fixture['properties']
        assert self.fixture['geometry']['type'] == result['geometry']['type']
        assert self.fixture['geometry']['coordinates'][0] == result['geometry']['coordinates'][0]

        assert len(self.fixture['geometry']['coordinates']) > len(result['geometry']['coordinates'])

        return result

    def testSimplifyFeature(self):
        self.standard()

    def testSimplifyFeatureThreshold(self):
        self.standard(threshold=0.1)

    def testSimplifyFeatureRatio(self):
        result = self.standard(ratio=0.1)

        b = vw.simplify_feature(self.fixture, ratio=0.90)
        assert len(b['geometry']['coordinates']) > len(result['geometry']['coordinates'])
        for i, j in zip(range(1, 9), range(2, 10)):
            r = vw.simplify_feature(self.fixture, ratio=float(i) / 10)
            s = vw.simplify_feature(self.fixture, ratio=float(j) / 10)
            assert len(r['geometry']['coordinates']) <= len(s['geometry']['coordinates'])


    def testSimplifyFeatureNumber(self):
        self.standard(number=10)

    def test3dCoords(self):
        coordinates = [[0.0, 0.0, 0.0], [1.1, 0, 1], [2.1, 3, 0], [4.1, 5, 10], [1.1, 2, 0], [5.1, 2, 0]]
        a = vw.simplify(coordinates)
        assert a[0] == [0, 0, 0]
        assert len(a) <= len(coordinates)
