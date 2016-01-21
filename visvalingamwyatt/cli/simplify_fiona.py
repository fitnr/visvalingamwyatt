#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, fitnr <contact@fakeisthenewreal.org>

from ..visvalingamwyatt import simplify_geometry
import fiona

def simplify(inp, output, **kwargs):
    with fiona.drivers():
        with fiona.open(inp, 'r') as src:
            with fiona.open(output, 'w', schema=src.schema, driver=src.driver, crs=src.crs) as sink:
                for feature in src:
                    feature['geometry'] = simplify_geometry(feature['geometry'], **kwargs)
                    sink.write(feature)
