import fire

from analytics.cycles import cycles as do_cycles


class Analytics(object):
    """Dependency graph analytics tools."""

    graph_filepath = "g.json"

    def cycles(self, graph: str = graph_filepath):
        do_cycles(graph)

    def paths(self, number):
        return


def main():
    fire.Fire(Analytics)


if __name__ == "__main__":
    main()
