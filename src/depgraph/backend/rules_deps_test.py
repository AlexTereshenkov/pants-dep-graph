import json
from textwrap import dedent

import pytest
from pants.core.target_types import FileTarget, GenericTarget
from pants.testutil.rule_runner import RuleRunner

from depgraph.backend.goal import DependencyGraphGoal
from depgraph.backend.goal import rules as goal_rules
from depgraph.backend.rules import rules


@pytest.fixture
def rule_runner() -> RuleRunner:
    return RuleRunner(rules=(*rules(), *goal_rules()), target_types=[FileTarget, GenericTarget])


def test_depgraph_rule_direct_deps(rule_runner: RuleRunner) -> None:
    rule_runner.write_files(
        {
            "project/commons.py": "",
            "project/file1.py": "",
            "project/file2.py": "",
            "BUILD": dedent(
                """
                file(name="commons", source="project/commons.py")
                file(name="target1", source="project/file1.py", dependencies=[":commons"])
                file(name="target2", source="project/file2.py", dependencies=[":commons"])
                """
            ),
        }
    )

    result = rule_runner.run_goal_rule(
        DependencyGraphGoal,
        args=[
            "--deps",
            "project/file1.py",
            "project/file2.py",
            "project/commons.py",
        ],
    )

    assert json.loads(result.stdout) == {
        "project/commons.py": [],
        "project/file1.py": ["project/commons.py"],
        "project/file2.py": ["project/commons.py"],
    }


def test_depgraph_rule_transitive_deps(rule_runner: RuleRunner) -> None:
    rule_runner.write_files(
        {
            "project/file1.py": "",
            "project/file2.py": "",
            "project/file3.py": "",
            "BUILD": dedent(
                """
                file(name="target1", source="project/file1.py", dependencies=[":target2"])
                file(name="target2", source="project/file2.py", dependencies=[":target3"])
                file(name="target3", source="project/file3.py")
                """
            ),
        }
    )

    result = rule_runner.run_goal_rule(
        DependencyGraphGoal,
        args=[
            "--deps",
            "--transitive",
            "project/file1.py",
            "project/file2.py",
            "project/file3.py",
        ],
    )

    assert json.loads(result.stdout) == {
        "project/file1.py": ["project/file2.py", "project/file3.py"],
        "project/file2.py": ["project/file3.py"],
        "project/file3.py": [],
    }
