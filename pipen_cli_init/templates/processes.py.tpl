"""Process definition"""

from pipen import Proc

# Write your processes
class Example(Proc):
    """An example process"""
    input = "message"
    output = "outfile:file:output.txt"
    script = "file://scripts/Example.sh"
    {%- if report %}
    plugin_opts = {
        "report": "file://reports/Example.svelte"
    }
    {%- endif %}
