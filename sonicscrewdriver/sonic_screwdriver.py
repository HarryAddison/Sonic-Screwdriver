from .gui import *
from .presets import *
from .sonification import *
from .spectrum import *
from .util import *


import customtkinter as ctk
import PIL.Image
from tkinter import *
from tkinter.ttk import Progressbar


def get_settings():

    # Spectrum sliders
    # Convert the slider values (1 - 100) to actual abundances
    # within the range of the models
    settings["spec_params"]["c"] = [scale_abundance(c.get(), train_params["c"])]
    settings["spec_params"]["o"] = [scale_abundance(o.get(), train_params["o"])]
    settings["spec_params"]["mg"] = [scale_abundance(mg.get(), train_params["mg"])]
    settings["spec_params"]["si"] = [scale_abundance(si.get(), train_params["si"])]
    settings["spec_params"]["s"] = [scale_abundance(s.get(), train_params["s"])]
    settings["spec_params"]["ca"] = [scale_abundance(ca.get(), train_params["ca"])]
    settings["spec_params"]["ti"] = [scale_abundance(ti.get(), train_params["ti"])]
    settings["spec_params"]["cr"] = [scale_abundance(cr.get(), train_params["cr"])]
    settings["spec_params"]["fe"] = [scale_abundance(fe.get(), train_params["fe"])]
    settings["spec_params"]["ni56"] = [scale_abundance(ni.get(), train_params["ni56"])]
    settings["spec_params"]["t_inner"] = [temp.get()]
    settings["spec_params"]["v_inner"] = [vel.get()]

    # Audio sliders
    settings["soni_params"]["R"] = audio_r.get()
    settings["soni_params"]["note_length"] = note_length.get()

    return


def set_preset(preset):

    c.set(preset["c"])
    o.set(preset["o"])
    mg.set(preset["mg"])
    si.set(preset["si"])
    s.set(preset["s"])
    ca.set(preset["ca"])
    ti.set(preset["ti"])
    cr.set(preset["cr"])
    fe.set(preset["fe"])
    ni.set(preset["ni"])
    temp.set(preset["temp"])
    vel.set(preset["vel"])

    return


def run_program():

    stop_audio(audio_progress)

    # Obtain the parameters from the GUI sliders
    get_settings()

    # Create the spectrum
    spec = create_spec(scaler_params, scaler_spec, networks, settings)

    # Plot the spectrum
    plot_spec(spec, train_spec_wl, plot_size, settings, config)

    # Update the spectrum on the GUI
    update_spec_plot(plot_window, f"{config.output_dir}/spectrum.PNG", image_size)

    # Sonification of the spectrum
    sonification(samplers, instrument_val, scale_val,
                 spec, train_spec_wl,
                 settings, config)

    return


if __name__ == "__main__":

    # ~~~~~~~~~~~
    # Load config
    # ~~~~~~~~~~~
    config = get_config()

    config = check_config(config)

    settings = {"spec_params": {},
                "soni_params": {}}

    # ~~~~~~~~~~
    # Load Dalek
    # ~~~~~~~~~~
    train_params, train_spec_wl, networks, scaler_spec, scaler_params = load_dalek(config)

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # Load instrument samplers
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    samplers = load_samplers(config)

    pygame.mixer.init()

    # ~~~~~~~~~~~~~~
    # Program window
    # ~~~~~~~~~~~~~~

    # Setup the main window
    # ~~~~~~~~~~~~~~~~~~~~~
    root = ctk.CTk()

    # Set the theme and colours
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.title("Sonic Screwdriver")

    # Set the size of the window according to the display size
    height, width = get_display_size()
    root.geometry(f"{width}x{height}")

    # Set the widget scaling depending on window size
    # Normal scaling corresponds to a window size of 1980x1060

    # Calculate scaling needed
    w_scale = 1980 / width
    h_scale = 1060 / height

    scale = min(w_scale, h_scale)

    ctk.set_widget_scaling(scale)


    # GUI design options
    # ~~~~~~~~~~~~~~~~~~

    # Colors
    background_color = "#2e2d2d"
    slider_prog_color = "white"
    slider_back_color = "white"
    button_hover_color = "red"

    # Font
    font = "Helvetica"
    text_color = "white"

    font_size_headers = 20
    font_size_labels = 16

    font_header = ctk.CTkFont(family=font, size=font_size_headers, weight="bold",
                              underline=False)

    font_label = ctk.CTkFont(family=font, size=font_size_labels, weight="normal",
                              underline=False)

    # Plot
    plot_col = 0
    plot_row = 0
    plot_colspan = 4
    plot_rowspan = 1

    plot_size = (10, 6) # x,y
    plot_scale = 120
    image_size = (plot_size[0] * plot_scale, plot_size[1] * plot_scale)


    # Frames
    # ~~~~~~

    # Root
    root.configure(fg_color=background_color)

    # Info
    info_frame = ctk.CTkFrame(root, fg_color=background_color)
    info_frame.grid(column=0, row=0, columnspan=2, pady=20)

    # Spectrum presets
    spec_preset_frame = ctk.CTkFrame(root, fg_color=background_color)
    spec_preset_frame.grid(column=0, row=1, padx=80, pady=10)

    # Spectrum options
    spec_opt_frame = ctk.CTkFrame(root, fg_color=background_color)
    spec_opt_frame.grid(column=0, row=2, padx=80, pady=10)

    # Instrument options
    instru_opt_frame = ctk.CTkFrame(root, fg_color=background_color)
    instru_opt_frame.grid(column=0, row=3, padx=80, pady=10)

    # Output (plot and audio)
    output_frame = ctk.CTkFrame(root, fg_color=background_color)
    output_frame.grid(column=1, row=1, rowspan=3, padx=40, pady=10)

    # Run Button frame
    run_frame = ctk.CTkFrame(root, fg_color=background_color)
    run_frame.grid(column=1, row=4, pady=10)


    # Info Frame
    # ~~~~~~~~~~

    # Program title
    ctk.CTkLabel(info_frame, text="Sonic Screwdriver", font=(font,40),
                text_color=text_color,
                anchor="center").grid(column=0, row=0)


    # Spectrum Options
    # ~~~~~~~~~~~~~~~~
    ctk.CTkLabel(spec_opt_frame, text="Supernova Spectrum Options",
                 font=font_header,
                 text_color=text_color).grid(column=0, row=2,
                                             columnspan=3,
                                             pady=20, padx=10)

    # Carbon
    c = slider(spec_opt_frame, name="Carbon",
               from_=1, to=100, val_type="percent",
               font=font_label, font_color=text_color,
               progress_color=slider_prog_color, fg_color=slider_back_color,
               col=0, row=3)

    # oxygen
    o = slider(spec_opt_frame, name="Oxygen",
               from_=1, to=100, val_type="percent",
               font=font_label, font_color=text_color,
               progress_color=slider_prog_color, fg_color=slider_back_color,
               col=0, row=4)

    # Magnesium
    mg = slider(spec_opt_frame, name="Magnesium",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=5)

    # silicon
    si = slider(spec_opt_frame, name="Silicon",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=6)

    # sulphur
    s = slider(spec_opt_frame, name="Sulphur",
               from_=1, to=100, val_type="percent",
               font=font_label, font_color=text_color,
               progress_color=slider_prog_color, fg_color=slider_back_color,
               col=0, row=7)

    # calcium
    ca = slider(spec_opt_frame, name="Calcium",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=8)

    # titanium
    ti = slider(spec_opt_frame, name="Titanium",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=9)

    # chromium
    cr = slider(spec_opt_frame, name="Chromium",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=10)

    # iron
    fe = slider(spec_opt_frame, name="Iron",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=11)

    # nickel 56
    ni = slider(spec_opt_frame, name="Nickel",
                from_=1, to=100, val_type="percent",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                col=0, row=12)

    # temperature
    temp = slider(spec_opt_frame, name="Temperature",
                from_=10000, to=14000, val_type="integer",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                label_format="{}K",
                col=0, row=13)

    # velocity
    vel = slider(spec_opt_frame, name="Velocity",
                from_=10000, to=15000, val_type="integer",
                font=font_label, font_color=text_color,
                progress_color=slider_prog_color, fg_color=slider_back_color,
                label_format="{}km/s",
                col=0, row=14)

    # Preset Options
    # ~~~~~~~~~~~~~~

    ctk.CTkLabel(spec_preset_frame, text="Supernova Spectrum Presets",
                 font=font_header, text_color=text_color).grid(column=0, row=0,
                                                               columnspan=3,
                                                               pady=10)


    # Early time SN Ia
    ctk.CTkButton(spec_preset_frame, text='Early SN Ia', font=font_label,
                  width=50, height=30, hover_color=button_hover_color,
                  command=lambda: set_preset(early_sn_preset)).grid(column=0,
                                                                     row=1,
                                                                     padx=5,
                                                                     pady=0)

    # Peak SN Ia
    ctk.CTkButton(spec_preset_frame, text='Peak SN Ia', font=font_label,
                  width=50, height=30, hover_color=button_hover_color,
                  command=lambda: set_preset(peak_sn_preset)).grid(column=1,
                                                                     row=1,
                                                                     padx=5,
                                                                     pady=0)

    # Late time SN Ia
    ctk.CTkButton(spec_preset_frame, text='Late SN Ia', font=font_label,
                  width=50, height=30,  hover_color = button_hover_color,
                  command=lambda: set_preset(late_sn_preset)).grid(column=2,
                                                                     row=1,
                                                                     padx=5,
                                                                     pady=0)

    # Sonification options
    # ~~~~~~~~~~~~~~~~~~

    # Instruments
    ctk.CTkLabel(instru_opt_frame, text="Instruments",
                font=font_header, text_color=text_color).grid(column=0, row=0,
                                                              pady=10)

    instrument_val = ctk.StringVar(value="flute")

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="flute",
                       text="Flute", font=font_label,
                       text_color=text_color).grid(column=0, row=1, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="guitar",
                       text="Guitar", font=font_label,
                       text_color=text_color).grid(column=0, row=2, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="piano",
                       text="Piano", font=font_label,
                       text_color=text_color).grid(column=0, row=3, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="choir",
                       text="Choir", font=font_label,
                       text_color=text_color).grid(column=0, row=4, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="cello",
                       text="Cello", font=font_label,
                       text_color=text_color).grid(column=0, row=5, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, variable=instrument_val, value="oboe",
                       text="Oboe", font=font_label,
                       text_color=text_color).grid(column=0, row=6, pady=5)


    # Note scaling
    ctk.CTkLabel(instru_opt_frame, text="Note Scaling",
                font=font_header, text_color=text_color).grid(column=0, row=12,
                                                              columnspan=3,
                                                              pady=10)

    audio_r = slider(instru_opt_frame, name="Sustain",
                     from_=0, to=1, val_type="float",
                     font=font_label, font_color=text_color,
                     progress_color=slider_prog_color, fg_color=slider_back_color,
                     label_format=" {:.2f}s",
                     col=0, row=13)

    note_length = slider(instru_opt_frame, name="Note Length",
                         from_=0.01, to=1, val_type="float",
                         font=font_label, font_color=text_color,
                         progress_color=slider_prog_color, fg_color=slider_back_color,
                         label_format=" {:.2f}s",
                         col=0, row=14)

    # Scales
    ctk.CTkLabel(instru_opt_frame, text="Scales",
                 font=font_header, text_color=text_color).grid(column=1, row=0,
                                                               pady=10, padx=5)

    scale_val = StringVar()
    scale_val.set("major")

    ctk.CTkRadioButton(instru_opt_frame, text='Major', variable=scale_val,
                       value="major", font=font_label,
                       text_color=text_color).grid(column=1, row=1, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, text='Minor', variable=scale_val,
                       value="minor",
                       font=font_label,
                       text_color=text_color).grid(column=1, row=2, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, text='Pentatonic', variable=scale_val,
                       value="pentatonic",
                       font=font_label,
                       text_color=text_color).grid(column=1, row=3, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, text='Blues', variable=scale_val,
                       value="blues",
                       font=font_label,
                       text_color=text_color).grid(column=1, row=4, pady=5)

    ctk.CTkRadioButton(instru_opt_frame, text='Chromatic', variable=scale_val,
                       value="chromatic",
                       font=font_label,
                       text_color=text_color).grid(column=1, row=5, pady=5)

    # Play audio file
    # ~~~~~~~~~~~~~~~
    ctk.CTkLabel(output_frame, text="").grid(column=3, row=2, padx=10)
    audio_progress = Progressbar(output_frame, orient="horizontal",
                                 length=image_size[0]-120, mode="determinate")
    audio_progress.grid(column=2, row=2, pady=5)

    ctk.CTkButton(output_frame, text='Play', font=(font, 16), width=5,
                  hover_color=button_hover_color,
                  command=lambda: play_audio_clicked(audio_progress,
                                                   config)).grid(column=0, row=2,
                                                                 padx=5, pady=5)

    ctk.CTkButton(output_frame, text='Stop', font=(font, 16), width=5,
                  hover_color=button_hover_color,
                  command=lambda: stop_audio(audio_progress)).grid(column=1,
                                                                   row=2,
                                                                   padx=5,
                                                                   pady=5)

    # Spectrum plot window/area
    # ~~~~~~~~~~~~~~~~~~~~~~~~~

    # Create empty plot to diplay as a placholder for the simulated spectrum
    plot_empty(plot_size, config)

    _spec_plot = ctk.CTkImage(light_image=PIL.Image.open(f"{config.output_dir}/spectrum.PNG"),
                              dark_image=PIL.Image.open(f"{config.output_dir}/spectrum.PNG"),
                              size=image_size)

    plot_window = ctk.CTkLabel(output_frame, text="", image=_spec_plot)
    plot_window.grid(column=plot_col, row=plot_row,
                     columnspan=plot_colspan, rowspan=plot_rowspan)

    # Run spectrum creation and sonification
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Create "GO" button
    ctk.CTkButton(output_frame, text='Simulate Supernova Spectrum',
                  font=(font, 25),
                  width=500, height=50,
                  hover_color=button_hover_color,
                  command=run_program).grid(column=0, row=3, columnspan=3,
                                            pady=50)

    # Create the window
    # ~~~~~~~~~~~~~~~~~
    root.mainloop()
