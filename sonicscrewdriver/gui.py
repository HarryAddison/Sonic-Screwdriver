import customtkinter as ctk
from PIL import Image


_spec_plot = None


class slider(ctk.CTkSlider):

    def __init__(self, parent=None, *args, **kw):

        self.name = kw.pop("name", None)

        self.val_type = kw.pop("val_type", None)

        self.label_format = kw.pop("label_format", "{}%")

        self.font = kw.pop("font", None)
        self.font_color = kw.pop("font_color", None)

        self.label_name = None
        self.slider = None
        self.label_val = None

        self.col = kw.pop("col", None)
        self.row = kw.pop("row", None)

        super().__init__(parent, *args, **kw)

        # Widgets
        self.label_name = ctk.CTkLabel(self.master, text=self.name,
                                       font=self.font,
                                       text_color=self.font_color)

        self.slider = ctk.CTkSlider(self.master, from_=self._from_, to=self._to,
                                    orientation="horizontal",
                                    command=self._update_label,
                                    progress_color= self._progress_color,
                                    fg_color=self._fg_color)
        self.slider.set(1)

        text = self._get_text()

        self.label_val = ctk.CTkLabel(self.master,
                                      text=text,
                                      font=self.font,
                                      text_color=self.font_color)

        # Widget postions
        self.label_name.grid(column=self.col, row=self.row)
        self.slider.grid(column=self.col+1, row=self.row)
        self.label_val.grid(column=self.col+2, row=self.row)


    def _update_label(self, _):
        text = self._get_text()
        self.label_val.configure(text=text)


    def _get_text(self):
        if self.val_type == "float":
            val = float(self.slider.get())
        else:
            val = int(self.slider.get())

        text = self.label_format.format(val)

        return text
    
    
    def get(self):
        return self.slider.get()


def update_spec_plot(widget, file_path, image_size):

    spec_plot = ctk.CTkImage(light_image=Image.open(file_path),
                              dark_image=Image.open(file_path), size=image_size)

    widget.configure(image=spec_plot)

    return
