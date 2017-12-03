#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, 2017, fitnr <contact@fakeisthenewreal.org>

from copy import copy
import json
from .visvalingamwyatt import simplify_feature
try:
    import fiona

    def simplify(inp, output, **kwargs):
        if output == '/dev/stdout':
            output = '/vsistdout'

        if inp == '/dev/stdin':
            output = '/vsistdin'

        with fiona.drivers():
            with fiona.open(inp, 'r') as src:
                with fiona.open(output, 'w', schema=src.schema, driver=src.driver, crs=src.crs) as sink:
                    for f in src:
                        sink.write(simplify_feature(f, **kwargs))

except ImportError:
    def simplify(inp, output, **kwargs):
        with open(inp, 'r') as f:
            src = json.load(f)

            sink = copy(src)
            sink['features'] = []

            with open(output, 'w') as g:
                for f in src['features']:
                    sink['features'].append(simplify_feature(f, **kwargs))

                json.dump(sink, g)

