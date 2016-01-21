# Visvalingam-Wyatt

A Python implementation of the Visvalingam-Wyatt line simplification algorithm.

This implementation is due to [Eliot Hallmark](https://github.com/Permafacture/Py-Visvalingam-Whyatt/). This release simply packages it as a Python module.

## Use

```python
>>> import visvalingamwyatt as vw
>>> points = [(1, 2), (3, 4), ...]
>>> vwsimplify = vw.VWSimplifier(points)
>>> vwsimplify.simplify(method='ratio', factor=0.90)
[(1, 2), (3, 4), ...]
```

Shorthands for working with geo data:
````python
import visvalingamwyatt as vw

geometry = {
    "type": "Polygon",
    "coordinates": [...]
}

# returns a copy of the geometry, simplified with the default method (threshold) and 
# factor (0.90)
vw.simplify_geometry(geometry)
````

The command line tools `vwsimplify` is available to simplify GeoJSON files:

````
# Simplify using a ratio of points
vwsimplify --ratio 0.90 in.geojson -o simple.geojson

# Simplify using the number of points to keep
vwsimplify --number 1000 in.geojson -o simple.geojson

# Simplify using a minimum area
vwsimplify --threshold 0.001 in.geojson -o simple.geojson
````

Install [Fiona](https://github.com/Toblerity/Fiona) for the additional ability to simplify any geodata layer.

## License

MIT
