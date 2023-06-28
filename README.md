# pants-dep-graph

Pants plugin to query and export repository dependency graph. 

## Examples

### Export dependencies 

```
# only for Python sources
pants dep-graph --filter-target-type=python_sources --deps src::

# for every target
pants dep-graph --deps src::

# for every target of source code nature
pants dep-graph --deps --sources-only src::
```

### Export reverse dependencies (dependents)

```
# for every target
pants dep-graph --rdeps src::

# include in the list of dependents only targets of source code nature
pants dep-graph --deps --sources-only src::
```

## Debugging

```
pants --print-stacktrace --no-local-cache --no-pantsd dep-graph --deps src::
pants --print-stacktrace --no-local-cache --no-pantsd dep-graph --rdeps src::
```

## Analytics

### Install

```
$ pip install dep-graph-analytics
```

### Usage

```
$ dep-graph-analytics cycles tests/cycles.json
['src/moduleC.py', 'src/moduleA.py', 'src/moduleB.py']
```
