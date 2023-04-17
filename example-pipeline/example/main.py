from pipen import Pipen

from .processes import ExampleProcess


class Pipeline(Pipen):
    name = "example"
    desc = "An awesome pipeline"
    starts = ExampleProcess


def main():
    Pipeline().run()
