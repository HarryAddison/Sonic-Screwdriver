# Installation with pip

Install Sonic Screwdriver with pip:
`pip3 install Sonic-Screwdriver`

Install additional dependencies:
`pip3 install typing_extensions==4.12.2`

Note: Ignore the error regarding dependency conflicts.


# Setup

### Tkinter
Sonic Screwdriver uses Tkinter as the source of the program interface.
Tkinter will need to be installed:

- Debian systems:

    `sudo apt-get install python3-tk`

- Fedora systems:

    `sudo dnf install python3-tkinter`


### Dalek
Sonic Screwdriver is built upon [Dalek](https://iopscience.iop.org/article/10.3847/2041-8213/abeb1b),
an emulator for [Tardis](https://tardis-sn.github.io/tardis/) an open-source Monte Carlo radiative-transfer spectral synthesis code.
Sonic Screwdriver makes use of the Dalek created neural networks to generate
type Ia supernova spectra from given inputs.

Download the Dalek neural networks from [Dalek data](https://drive.google.com/drive/folders/1DfY7GcQ6TSNBLighvct0uRPMCpMLTfs-).
Lastly unzip the downloaded file.


### Configuration file
Create a configuration file:

- Create file called {my_config}.py
- Setup the following variables:
    - `dalek_dir = {dalek_data_dir}` where `{dalek_data_dir}` is the path to the directory containing the Dalek data downloaded in the previous setup step.
    - `instruments_dir = {instruments_dir}` where `{instruments_dir}` is the path to the directory where the instrument sound files will be downloaded to and stored.
    - `output_dir = {output_dir}` where `{output_dir}` is the directory for which the output files of Sonic Screwdriver will be stored. (Only two files are stored at any given time.)

An example configuration file is provided [here](https://github.com/HarryAddison/Sonic-Screwdriver/blob/main/examples/example_config.py)


# Running Sonic Screwdriver

Sonic Screwdriver is run directly from the command line:

`cd directory_containing_{my_config.py}`

`python3 -m sonicscrewdriver.sonic_screwdriver -i {my_config}`


# Using Sonic Screwdriver

Using Sonic Screwdriver is simple! 

Simply change the supernova option sliders, select an instrument, select a musical scale, and then hit "Simulate".
Sonic Screwdriver will then use [Dalek](https://iopscience.iop.org/article/10.3847/2041-8213/abeb1b) to
produce a supernova spectrum from the options you chose, which will be
displayed on the right. Sonic Screwdriver will also sonify the spectrum using
[Strauss](https://github.com/james-trayford/strauss/). To play the spectrum sonifcation hit the "play" button and to stop the audio hit the "stop" button.

Have fun producing and sonifying supernova spectra!




