from pipen import Pipen
from pipen_args import install  # noqa: F401

from .processes import ExampleProcess


pipeline = Pipen(
    name="example",
    desc="An awesome pipeline",
)
pipeline.set_start(ExampleProcess)


def main():
    pipeline.run()
