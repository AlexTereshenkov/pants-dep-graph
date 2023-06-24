from pants.backend.project_info.dependents import Dependents, DependentsRequest
from pants.engine.addresses import Addresses
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.rules import collect_rules, rule
from pants.engine.target import (
    Dependencies,
    DependenciesRequest,
    HydratedSources,
    HydrateSourcesRequest,
    SourcesField,
    Targets,
    TransitiveTargets,
    TransitiveTargetsRequest,
)

from depgraph.backend.structs import (
    AddressWithFilter,
    GraphDataDeps,
    GraphDataRequest,
    GraphDataReverseDeps,
    SourceFiles,
)

PYTHON_SOURCE_CODE_TARGETS = (
    "python_source",
    "python_sources",
    "python_test",
    "python_tests",
    "python_test_utils",
)


@rule(
    desc="Get source files from an address, optionally keeping only targets of source code nature."
)
async def get_source_files_from_address_with_filter(
    address_with_filter: AddressWithFilter,
) -> SourceFiles:
    files: list[str] = []
    targets = await Get(Targets, Addresses([address_with_filter.address]))
    target = targets[0]
    if target.alias in ("file", "resource", *PYTHON_SOURCE_CODE_TARGETS):
        all_sources = await Get(HydratedSources, HydrateSourcesRequest(target.get(SourcesField)))
        files.extend(all_sources.snapshot.files)
    elif not address_with_filter.sources_only:
        files.append(str(target.address))
    return SourceFiles(files)


@rule(desc="Get dependents data out of the dependency graph.")
async def get_dependents(graph_data_request: GraphDataRequest) -> GraphDataReverseDeps:
    target_to_deps: dict[str, list[str]] = {}
    for target in graph_data_request.targets:
        total_files: set[str] = set()
        dependents = await Get(
            Dependents,
            DependentsRequest(
                (target.address,),
                transitive=graph_data_request.transitive,
                include_roots=False,
            ),
        )
        results = await MultiGet(
            Get(
                SourceFiles,
                AddressWithFilter,
                AddressWithFilter(address=d, sources_only=graph_data_request.sources_only),
            )
            for d in dependents
        )
        for result in results:
            total_files.update(result)
        target_filepath_or_address = next(
            iter(
                await Get(SourceFiles, AddressWithFilter, AddressWithFilter(address=target.address))
            )
        )
        target_to_deps[target_filepath_or_address] = sorted(total_files)

    return GraphDataReverseDeps(data=target_to_deps)


@rule(desc="Get dependencies data out of the dependency graph.")
async def get_dependencies(graph_data_request: GraphDataRequest) -> GraphDataDeps:
    # to only analyze dependencies that have dependencies -> if t.has_fields([Dependencies])]
    valid_targets = [t for t in graph_data_request.targets]
    target_to_deps: dict[str, list[str]] = {}

    for target in valid_targets:
        total_files: list[str] = []
        if graph_data_request.transitive:
            transitive_deps_request_result = await Get(
                TransitiveTargets, TransitiveTargetsRequest([target.address])
            )
            targets = transitive_deps_request_result.dependencies
        else:  # direct dependencies only
            targets = await Get(
                Targets,  # type: ignore
                DependenciesRequest(target.get(Dependencies)),
            )

        # ignore non-sources targets, if requested
        relevant_targets = (
            (t for t in targets if t.alias in PYTHON_SOURCE_CODE_TARGETS)
            if graph_data_request.sources_only
            else (t for t in targets)
        )

        results = await MultiGet(
            Get(SourceFiles, AddressWithFilter, AddressWithFilter(address=d.address))
            for d in relevant_targets
        )
        for result in results:
            total_files.extend(result)

        # convert object to filepath, if applicable
        target_filepath_or_address = next(
            iter(
                await Get(SourceFiles, AddressWithFilter, AddressWithFilter(address=target.address))
            )
        )
        target_to_deps[target_filepath_or_address] = sorted(total_files)
    return GraphDataDeps(data=target_to_deps)


def rules():
    return collect_rules()
