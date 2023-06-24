from dataclasses import dataclass

from pants.build_graph.address import Address
from pants.engine.collection import DeduplicatedCollection
from pants.engine.target import Targets


class SourceFiles(DeduplicatedCollection[str]):
    sort_input = True


@dataclass(frozen=True)
class AddressWithFilter:
    address: Address
    sources_only: bool = False


@dataclass(frozen=True)
class GraphDataDeps:
    data: dict[str, list[str]]


@dataclass(frozen=True)
class GraphDataReverseDeps:
    data: dict[str, list[str]]


@dataclass(frozen=True)
class GraphDataRequest:
    targets: Targets
    transitive: bool
    sources_only: bool
