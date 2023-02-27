"""Define processes for the pipeline"""

from pipen import Proc


# Define your processes here
class ExampleProcess(Proc):
    """Example process

    Input:
        invar: Input variables

    Output:
        outfile: Output file
    """
    input = "invar:var"
    output = "outfile:file:output.txt"
    script = "file://scripts/ExampleProcess.sh"
    plugin_opts = {
        "report": "file://reports/ExampleProcess.svelte",
    }
