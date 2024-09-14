import argparse
import importlib
import matplotlib.pyplot as plt


def parser_init():
    '''
    Function that allows the user to parse a initfile path via the
    command line.
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i",
        "--initfile",
        default=None,
        help="Python file containing the settings for sonic_screwdriver.py",
    )

    return parser


def get_config():
    '''
    Obtain the parameters from the python file that was parsed via the
    command line.
    '''

    # Call the parser function and obtain its arguments.
    args = parser_init().parse_args()

    # Print the initfile path that was provided to the parser
    print("Initfile: ", args.initfile, "\n")

    params = importlib.import_module(args.initfile)

    return params


def scale_abundance(percent, model_vals):

    # percent: 1 - 100
    # model: All values in the model.
    # want to map the slider value to the min/max value of the model

    # Convert the slider value to be normalised. i.e a value between 0-1.
    norm_slider_val = (percent - 1) / (100 - 1)

    # Obtain the min/max values allowed in the model
    min_model, max_model = min(model_vals), max(model_vals)

    # Scale the normalised slider value to the range of allowed model values
    abundance = norm_slider_val * (max_model - min_model) + min_model

    return abundance


def plot_empty(plot_size, config):
    fig, ax = plt.subplots(1,1, figsize=plot_size)
    ax.set_facecolor('k')

    plt.xlabel(r"$\rm{Wavelength}~[\AA]$")
    plt.ylabel(r"$\rm{Flux}~[erg\AA^{-1}cm^{-2}s^{-1}$]")
    plt.savefig(f"{config.output_dir}/spectrum.PNG", bbox_inches="tight")
    plt.close()

    return
