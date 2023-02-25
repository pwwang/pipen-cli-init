from pipen import Pipen
import pipen_args  # noqa: F401

from .processes import ExampleProcess


pipeline = Pipen(
    name="example",
    desc="An awesome pipeline",
)
pipeline.set_start(ExampleProcess)


def main():
    pipeline.run()
