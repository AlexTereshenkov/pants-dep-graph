# pants-dep-graph

Pants plugin to query and export repository dependency graph. 

## Examples

### Export dependencies 

```
# only for Python sources
pants dg --filter-target-type=python_sources --deps src::

# for every target
pants dg --deps src::

# for every target of source code nature
pants dg --deps --sources-only src::
```

### Export reverse dependencies (dependents)

```
# for every target
pants dg --rdeps src::

# include in the list of dependents only targets of source code nature
pants dg --deps --sources-only src::
```

## Debugging

```
pants --print-stacktrace --no-local-cache --no-pantsd dg --deps src::
pants --print-stacktrace --no-local-cache --no-pantsd dg --rdeps src::
```
