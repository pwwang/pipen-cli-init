from pipen_args import Args

args = Args(
    # The group name of the options to show on help page
    pipen_opt_group="Pipeline options",
    prog="{{progname}}",
    # change the pipeline options you want hide/show here
    hide_args=[
        "scheduler-opts",
        "plugin-opts",
        "template-opts",
        "dirsig",
        "loglevel",
        "plugins",
        "submission-batch",
    ],
    help_on_void=False,
)

# Add more arguments if you want
# args.add_param(...)
