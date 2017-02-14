# The MIT License (MIT)

# Copyright (c) 2014 Elliot Hallmark

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

'''
Visvalingam-Whyatt method of poly-line vertex reduction

Visvalingam, M and Whyatt J D (1993)
"Line Generalisation by Repeated Elimination of Points", Cartographic J., 30 (1), 46 - 51

Described here:
http://web.archive.org/web/20100428020453/http://www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html

source: https://github.com/Permafacture/Py-Visvalingam-Whyatt/
'''


def triangle_area(p1, p2, p3):
    """
    calculates the area of a triangle given its vertices
    """
    return abs(p1[0]*(p2[1]-p3[1])+p2[0]*(p3[1]-p1[1])+p3[0]*(p1[1]-p2[1]))/2.


def triangle_areas_from_array(arr):
    '''
    take an (N,2) array of points and return an (N,1)
    array of the areas of those triangles, where the first
    and last areas are np.inf

    see triangle_area for algorithm
    '''

    result = np.empty((len(arr),), arr.dtype)
    result[0] = np.inf
    result[-1] = np.inf

    p1 = arr[:-2]
    p2 = arr[1:-1]
    p3 = arr[2:]

    # an accumulators to avoid unnecessary intermediate arrays
    accr = result[1:-1]  # Accumulate directly into result
    acc1 = np.empty_like(accr)

    np.subtract(p2[:, 1], p3[:, 1], out=accr)
    np.multiply(p1[:, 0], accr, out=accr)
    np.subtract(p3[:, 1], p1[:, 1], out=acc1)
    np.multiply(p2[:, 0], acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.subtract(p1[:, 1], p2[:, 1], out=acc1)
    np.multiply(p3[:, 0], acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.abs(accr, out=accr)
    accr /= 2.
    # Notice: accr was writing into result, so the answer is in there
    return result

# the final value in thresholds is np.inf, which will never be
# the min value.  So, I am safe in "deleting" an index by
# just shifting the array over on top of it


def remove(s, i):
    '''
    Quick trick to remove an item from a numpy array without
    creating a new object.  Rather than the array shape changing,
    the final value just gets repeated to fill the space.

    ~3.5x faster than numpy.delete
    '''
    s[i:-1] = s[i+1:]


class Simplifier(object):

    def __init__(self, pts):
        '''Initialize with points. takes some time to build
        the thresholds but then all threshold filtering later
        is ultra fast'''
        self.pts_in = np.array(pts)
        self.pts = np.array([tuple(map(float, pt)) for pt in pts])
        self.thresholds = self.build_thresholds()
        self.ordered_thresholds = sorted(self.thresholds, reverse=True)

    def build_thresholds(self):
        '''compute the area value of each vertex, which one would
        use to mask an array of points for any threshold value.

        returns a numpy.array (length of pts)  of the areas.
        '''
        nmax = len(self.pts)
        real_areas = triangle_areas_from_array(self.pts)
        real_indices = list(range(nmax))

        # destructable copies
        # ARG! areas=real_areas[:] doesn't make a copy!
        areas = np.copy(real_areas)
        i = real_indices[:]

        # pick first point and set up for loop
        min_vert = np.argmin(areas)
        this_area = areas[min_vert]
        #  areas and i are modified for each point finished
        remove(areas, min_vert)  # faster
        # areas = np.delete(areas,min_vert) #slower
        _ = i.pop(min_vert)

        #cntr = 3
        while this_area < np.inf:
            '''min_vert was removed from areas and i.  Now,
            adjust the adjacent areas and remove the new
            min_vert.

            Now that min_vert was filtered out, min_vert points
            to the point after the deleted point.'''

            skip = False  # modified area may be the next minvert

            try:
                right_area = triangle_area(self.pts[i[min_vert-1]],
                                           self.pts[i[min_vert]], self.pts[i[min_vert+1]])
            except IndexError:
                # trying to update area of endpoint. Don't do it
                pass
            else:
                right_idx = i[min_vert]
                if right_area <= this_area:
                    # even if the point now has a smaller area,
                    # it ultimately is not more significant than
                    # the last point, which needs to be removed
                    # first to justify removing this point.
                    # Though this point is the next most significant
                    right_area = this_area

                    # min_vert refers to the point to the right of
                    # the previous min_vert, so we can leave it
                    # unchanged if it is still the min_vert
                    skip = min_vert

                # update both collections of areas
                real_areas[right_idx] = right_area
                areas[min_vert] = right_area

            if min_vert > 1:
                # cant try/except because 0-1=-1 is a valid index
                left_area = triangle_area(self.pts[i[min_vert-2]],
                                          self.pts[i[min_vert-1]], self.pts[i[min_vert]])
                if left_area <= this_area:
                    # same justification as above
                    left_area = this_area
                    skip = min_vert-1
                real_areas[i[min_vert-1]] = left_area
                areas[min_vert-1] = left_area

            # only argmin if we have too.
            min_vert = skip or np.argmin(areas)

            _ = i.pop(min_vert)

            this_area = areas[min_vert]
            # areas = np.delete(areas,min_vert) #slower
            remove(areas, min_vert)  # faster

        return real_areas

    def simplify(self, number=None, ratio=None, threshold=None):
        if threshold is not None:
            return self.by_threshold(threshold)

        elif number is not None:
            return self.by_number(number)

        else:
            ratio = ratio or 0.90
            return self.by_ratio(ratio)

    def by_threshold(self, threshold):
        return self.pts_in[self.thresholds >= threshold]

    def by_number(self, n):
        try:
            threshold = self.ordered_thresholds[int(n)]
        except IndexError:
            return self.pts_in

        return self.by_threshold(threshold)

    def by_ratio(self, r):
        if r <= 0 or r > 1:
            raise ValueError("Ratio must be 0<r<=1. Got {}".format(r))
        else:
            return self.by_number(r*len(self.thresholds))


def simplify_geometry(geom, **kwargs):
    '''Simplify a GeoJSON-like geometry object.'''
    g = dict(geom.items())

    # Ignore point geometries
    if geom['type'] in ('Point', 'MultiPoint'):
        pass

    elif geom['type'] == 'MultiPolygon':
        g['coordinates'] = [simplify_rings(rings, **kwargs) for rings in geom['coordinates']]

    elif geom['type'] in ('Polygon', 'MultiLineString'):
        g['coordinates'] = simplify_rings(geom['coordinates'], **kwargs)

    elif geom['type'] == 'LineString':
        g['coordinates'] = simplify(geom['coordinates'], **kwargs)

    elif geom['type'] == 'GeometryCollection':
        g['geometries'] = [simplify_geometry(g, **kwargs) for g in geom['geometries']]

    else:
        raise NotImplementedError("Unknown geometry type " + geom.get('type'))

    return g


def simplify_rings(rings, **kwargs):
    return [simplify(ring, **kwargs) for ring in rings]


def simplify(coordinates, number=None, ratio=None, threshold=None):
    '''Simplify a list of coordinates'''
    return Simplifier(coordinates).simplify(number=number, ratio=ratio, threshold=threshold).tolist()


def simplify_feature(feat, number=None, ratio=None, threshold=None):
    '''Simplify the geometry of a GeoJSON-like feature.'''
    return {
        'properties': feat.get('properties'),
        'geometry': simplify_geometry(feat['geometry'], number=number, ratio=ratio, threshold=threshold),
    }
