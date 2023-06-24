pants_requirements(name="pants")

python_distribution(
    name="dist",
    provides=python_artifact(
        name="pants-dep-graph",
        version="1.0.1",
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
