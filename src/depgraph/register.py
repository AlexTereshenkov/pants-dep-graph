from depgraph.backend import goal as goal_rules
from depgraph.backend import rules as backend_rules


def target_types():
    return ()


def rules():
    return (
        *goal_rules.rules(),
        *backend_rules.rules(),
    )
