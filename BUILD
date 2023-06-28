python_distribution(
    name="depgraph-plugin",
    provides=python_artifact(
        name="pants-plugin-dep-graph",
        version="1.0.3",
        description="Pants plugin to export repository dependency graph.",
        long_description_content_type="text/markdown",
    ),
    dependencies=["src/depgraph"],
    entry_points={
        "pantsbuild.plugin": {
            "rules": "depgraph.register:rules",
            "target_types": "depgraph.register:target_types",
        }
    },
    long_description_path="README.md",
    repositories=["@pypi"],
    sdist=True,
    wheel=True,
)

python_distribution(
    name="analytics-tools",
    provides=python_artifact(
        name="dep-graph-analytics",
        version="1.0.3",
        description="A toolset to query codebase dependency graph data using networkx.",
        long_description_content_type="text/markdown",
    ),
    dependencies=["src/analytics", "3rdparty:networkx", "3rdparty:fire"],
    entry_points={
        "console_scripts": {
            "dep-graph-analytics": "analytics.main:main",
        },
    },
    long_description_path="README.md",
    repositories=["@pypi"],
    sdist=True,
    wheel=True,
)
