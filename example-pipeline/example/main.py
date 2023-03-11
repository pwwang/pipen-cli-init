from pipen import Pipen
from pipen_args import install  # noqa: F401

from .processes import ExampleProcess


class Pipeline(Pipen):
    name = "example"
    desc = "An awesome pipeline"
    starts = ExampleProcess


def main():
    Pipeline().run()
