import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def load_dalek(config):

    # Loading the grids
    print("\nLoading grids")

    train_spectra = np.load(config.dalek_train_spec_path)
    train_spec_wl = np.load(config.dalek_train_spec_wave_path)
    train_params_og = pd.read_hdf(config.dalek_train_params_path)

    # Load in the neural networks
    print("\nLoading models")

    networks = []
    for network_fn in config.dalek_network_fns:

        network = load_model("%s/%s"%(config.dalek_network_dir, network_fn))
        networks.append(network)

    # Preprocess the training spectra/parameters so that the scaling can be
    # applied to the desired input parameters and the outputs reconstructed.
    print("\nApplying pre-processing to models")

    # Take log10 of values
    train_spectra = np.log10(train_spectra)
    train_params = np.log10(train_params_og)

    # Standardise spectra using the "StandardScaler"
    scaler_spec = StandardScaler(with_mean=True, with_std=True)
    scaler_params = StandardScaler(with_mean=True, with_std=True)

    scaler_spec.fit(train_spectra)
    scaler_params.fit(train_params)

    return train_params_og, train_spec_wl, networks, scaler_spec, scaler_params


def create_spec(scaler_params, scaler_spec, networks, settings):

    # Put spectrum parameters into an astropy table
    spec_params = pd.DataFrame.from_dict(settings["spec_params"])

    # Apply pre-processing to the desired input prarameters
    spec_params = np.log10(spec_params)
    spec_params = scaler_params.transform(spec_params)

    # Predict spectra using the desired pre-processed input parameters
    predicted_spectra = []
    for network in networks:
        predicted_spectra.append(network.predict(spec_params))

    # Average and predictioned spectra
    mean_predicted_spec = np.mean(np.array(predicted_spectra), axis=0)

    # Inverse the pre-processing scaling
    mean_predicted_spec = np.array(scaler_spec.inverse_transform(mean_predicted_spec)[0])
    # mean_predicted_spec = 10**mean_predicted_spec

    return mean_predicted_spec


def plot_spec(spec, wave, plot_size, config):

    x = wave
    y = 10**np.array(spec, dtype=float)

    # Create line segments
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(1,1, figsize=plot_size)
    ax.set_facecolor('k')

    # Plot a solid grey line to fill in the gaps of the later created
    # coloured line segments.
    plt.plot(x, y, c="grey", linewidth=2)

    norm = plt.Normalize(min(x), max(x))

    lc = LineCollection(segments, cmap='Spectral', norm=norm)

    lc.set_array(x)
    lc.set_linewidth(3)
    ax.add_collection(lc)

    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y)-min(y)*0.1, max(y)+min(y)*0.1)

    plt.xlabel(r"$\rm{Wavelength}~[\AA]$")
    plt.ylabel(r"$\rm{Flux}~[erg\AA^{-1}cm^{-2}s^{-1}$]")

    plt.savefig(config.plot_path, bbox_inches="tight")
    plt.close()

    return
