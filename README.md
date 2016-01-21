# Visvalingam-Wyatt

A Python implementation of the Visvalingam-Wyatt line simplification algorithm.

This implementation is due to [Eliot Hallmark](https://github.com/Permafacture/Py-Visvalingam-Whyatt/). This release simply packages it as a Python module.

## Use

```python
>>> import visvalingamwyatt as vw
>>> points = [(1, 2), (3, 4), ...]
>>> vwsimplify = vw.VWSimplifier(points)
>>> vwsimplify.simplify(method='threshold', factor=0.90)
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

## License

MIT