import json

from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.internals.selectors import Get
from pants.engine.rules import collect_rules, goal_rule
from pants.engine.target import Targets
from pants.option.option_types import BoolOption

from depgraph.backend.structs import GraphDataDeps, GraphDataRequest, GraphDataReverseDeps


class DependencyGraphSubsystem(GoalSubsystem):
    name = "dep-graph"
    help = "Query dependency graph."

    transitive = BoolOption(
        default=False,
        help="Include transitive dependencies.",
    )

    sources_only = BoolOption(
        default=False,
        help="Only consider source code targets when querying dependencies.",
    )

    deps = BoolOption(
        default=False,
        help="Export dependencies.",
    )

    rdeps = BoolOption(
        default=False,
        help="Export reverse dependencies (aka dependents).",
    )


class DependencyGraphGoal(Goal):
    subsystem_cls = DependencyGraphSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule
async def export_graph(
    console: Console, targets: Targets, goal_subsystem: DependencyGraphSubsystem
) -> DependencyGraphGoal:
    if not (goal_subsystem.deps or goal_subsystem.rdeps) or (
        goal_subsystem.deps and goal_subsystem.rdeps
    ):
        raise ValueError("Choose to export graph data using either `--deps` or `--rdeps`.")

    request = GraphDataRequest(
        targets=targets,
        transitive=goal_subsystem.transitive,
        sources_only=goal_subsystem.sources_only,
    )
    if goal_subsystem.rdeps:
        graph_data = await Get(GraphDataReverseDeps, GraphDataRequest, request)
    elif goal_subsystem.deps:
        graph_data = await Get(GraphDataDeps, GraphDataRequest, request)  # type: ignore

    json_str = json.dumps(graph_data.data, indent=4)
    console.print_stdout(json_str)
    return DependencyGraphGoal(exit_code=0)


def rules():
    return collect_rules()
