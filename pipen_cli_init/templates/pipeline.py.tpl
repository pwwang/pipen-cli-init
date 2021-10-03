"""Assemable the pipeline"""
from pipen import Pipen
from . import args
# Import your processeses
from .processes import Example

# Set the input data of the start processes
Example.input_data = ["Hello World!"]

# Set the name and description of your pipeline here
pipeline = Pipen(
    name="My Pipeline",
    desc="My first awesome pipeline!"
)

def main():
    """Run the pipeline"""
    pipeline.set_starts(Example).run()
