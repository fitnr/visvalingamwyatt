#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, fitnr <contact@fakeisthenewreal.org>

import json
from copy import copy
from ..visvalingamwyatt import simplify_feature

def simplify(inp, output, **kwargs):
    with open(inp, 'r') as f:
        src = json.load(f)

        sink = copy(src)
        sink['features'] = []

        with open(output, 'w') as g:
            for f in src['features']:
                sink['features'].append(simplify_feature(f, **kwargs))

            json.dump(sink, g)

