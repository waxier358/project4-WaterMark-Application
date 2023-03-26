import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk, Image, ImageFont, ImageDraw
from tkinter import filedialog as fd


class WaterMark:
    def __init__(self):

        self.window = Tk()
        # application title
        self.window.title("WaterMark Application")
        # define GUI size
        self.window.minsize(width=1000, height=755)
        # GUI can't be resizable
        self.window.resizable(False, False)

        # create menu
        self.menubar = tkinter.Menu(self.window)

        self.menubar.add_cascade(label="About", command=self.about_menu)
        self.menubar.add_cascade(label="Help", command=self.help_menu)
        self.window.config(menu=self.menubar)

        # location and name for default image
        self.default_image_name = "images/default_image.PNG"
        # open default_image and resize it at 600,700
        self.default_image = ImageTk.PhotoImage((Image.open(self.default_image_name)).resize((600, 700)))
        # create a label, place it in GUI and inset in this label the default_image
        self.label_image = tkinter.Label(image=self.default_image, borderwidth=2, relief="solid")
        self.label_image.grid(column=0, row=0, padx=10, pady=10, columnspan=3, rowspan=10)
        # create button for import image and place it in GUI
        self.import_image_button = tkinter.Button(text="Import Image", bd=4, command=self.open_file, justify='center')
        self.import_image_button.grid(column=0, row=10, columnspan=3, pady=10)
        # create separator vertical line and place in GUI
        self.separator = ttk.Separator(self.window, orient='vertical')
        self.separator.grid(column=3, row=0, rowspan=11, sticky='ns', padx=0, pady=0)
        # create title label and place in GUI
        self.title = tkinter.Label(text="WaterMark Option:", justify='center')
        self.title.grid(column=4, row=0, columnspan=2)
        # create place label and place in GUI
        self.text = tkinter.Label(text="Text: ")
        self.text.grid(column=4, row=2)
        # create entry field for text use for watermarking and place in GUI
        self.text_entry = tkinter.Entry(width=45)
        self.text_entry.grid(column=5, row=2)
        # color
        self.color = tkinter.Label(text="Color: ")
        self.color.grid(column=4, row=3)
        self.combobox_color = Combobox(values=['red', 'green', 'blue', 'black', 'white', 'yellow'], width=42)
        self.combobox_color.set('red')
        self.combobox_color.grid(column=5, row=3)
        # font
        self.font = tkinter.Label(text="Font: ")
        self.font.grid(column=4, row=4)
        self.combobox_font = Combobox(values=['arial.ttf', 'ariali.ttf', 'arialbd.ttf', 'arialbi.ttf',
                                              'courbd.ttf', 'impact.ttf', 'segoesc.ttf', 'taile.ttf'], width=42)
        self.combobox_font.set('arial.ttf')
        self.combobox_font.grid(column=5, row=4)
        # size
        self.size = tkinter.Label(text="Size: ")
        self.size.grid(column=4, row=5)
        self.entry_size = tkinter.Entry(width=45)
        self.entry_size.insert(0, '50')
        self.entry_size.grid(column=5, row=5)
        # angle
        self.angle = tkinter.Label(text="Angle: ")
        self.angle.grid(column=4, row=6)
        self.angle_entry = tkinter.Entry(width=45)
        self.angle_entry.insert(0, '0')
        self.angle_entry.grid(column=5, row=6)
        # x and y (coordinates where mask image and original image join)
        self.x = tkinter.Label(text="Position X : ")
        self.x.grid(column=4, row=7)
        self.x_entry = tkinter.Entry(width=45)
        self.x_entry.insert(0, '0')
        self.x_entry.grid(column=5, row=7)

        self.y = tkinter.Label(text="Position Y : ")
        self.y.grid(column=4, row=8)
        self.y_entry = tkinter.Entry(width=45)
        self.y_entry.insert(0, '0')
        self.y_entry.grid(column=5, row=8)

        # create show on image button and place in GUI (when this button is pressed watermark apper in GUI )
        self.show_on_image_button = tkinter.Button(text="Show on  Image", bd=4, justify='center',
                                                   command=self.show_button)
        self.show_on_image_button.grid(column=4, row=9, columnspan=2)

        # create save image button and place in GUI (when this button is pressed user chose a path and save image )
        self.save_button = tkinter.Button(text="Save  Image", bd=4, justify='center', width=12, command=self.save_file)
        self.save_button.grid(column=4, row=10, columnspan=2, pady=10)

        # create an attribute to store my current image -- use for Image.Open()
        self.image = ""
        # create an attribute to convert my current image in ImageTK.PhotoImage
        self.image_for_gui = ""
        # create an attribute to store path and name for current image
        self.image_name = ""
        # extension name ex .jpeg
        self.extension_name = ""

        # define image type that can be opened
        self.filetypes = (('image files', '*.PNG'), ('image files', '*.jpeg'), ('image files', '*.bmp'),
                          ('All files', '*.*'))
        # define text font for watermark
        self.text_font = ""

    # open file attached to Import File button
    def open_file(self):
        self.image_name = fd.askopenfile(title="Select image file", filetypes=self.filetypes).name
        self.image = Image.open(self.image_name)
        self.image_for_gui = ImageTk.PhotoImage(self.image.resize((600, 700)))
        self.label_image.configure(image=self.image_for_gui)
        # update self.extension_name
        self.get_extension()
        # create a label with dimension of image
        self.dimension = tkinter.Label(text=f"Current image has width(x) {self.image.width} and height(y) {self.image.height}")
        self.dimension.grid(column=4, row=1, columnspan=2)

    # refresh gui
    def main_loop(self):
        self.window.mainloop()

    # show_button action
    def show_button(self):
        if self.check_image_is_imported():
            # open current image
            my_image = Image.open(self.image_name)
            # update self.text_font with value from self.combobox_font
            self.text_font = ImageFont.truetype(self.combobox_font.get(), int(self.entry_size.get()))
            # create a mask with same dimension like current image; last parameter  (0, 0, 128, 0) is color; I can
            # use any color, buy last number must be 0, this is the transparency
            mask = Image.new('RGBA', my_image.size, (0, 0, 128, 0))
            draw = ImageDraw.Draw(mask)
            # draw text from self.text_entry in mask at coordinates 0, my_image.height/2 (experimental value) with color
            # from self.combobox_color.get() and font from self.text_font
            draw.text((0, my_image.height/2), self.text_entry.get(), self.combobox_color.get(), font=self.text_font)
            # rotate mask with value form self.angle_entry expand must be True
            mask_rotate = mask.rotate(int(self.angle_entry.get()), expand=True)
            # paste mask at my_image at coordinates get from x_entry and y_entry (start with 0,0)
            my_image.paste(mask_rotate, (int(self.x_entry.get()), int(self.y_entry.get())), mask_rotate)
            # save image made from my_image and rotated mask
            my_image.save(f"images/try{self.extension_name}")
            # open image saved previous and convert it in ImageTk.PhotoImage
            image_edited = ImageTk.PhotoImage((Image.open(f"images/try{self.extension_name}")).resize((600, 700)))
            # update self.label_image with image_edited
            self.label_image.configure(image=image_edited)
            # update GUI
            self.main_loop()
        else:
            messagebox.showinfo(title="Error import image!", message=f"Before see any changes please import image!")

    # get extension of image
    def get_extension(self):
        extension = ""
        for char in self.image_name[::-1]:
            if char == ".":
                extension = self.image_name[::-1][:self.image_name[::-1].index(char) + 1]
        self.extension_name = extension[::-1]

    # save button function
    def save_file(self):
        if self.check_image_is_imported():
            try:
                my_image = Image.open(f"images/try{self.extension_name}")
            except FileNotFoundError:
                messagebox.showinfo(title="Error!", message=f"You deleted images/try{self.extension_name}\n"
                                                            f"This is a system file, please try again!")
            else:
                path_to_save_image = fd.asksaveasfile(mode='w', filetypes=self.filetypes,
                                                      defaultextension=self.extension_name)
                if path_to_save_image:
                    my_image.save(path_to_save_image.name)
        else:
            messagebox.showinfo(title="Save Error!", message=f"Before save any changes please import image and add "
                                                             f"watermark!")

    def check_image_is_imported(self):
        if self.image_name == "":
            return False
        else:
            return True

    @staticmethod
    def about_menu():
        about_window = Tk()
        about_window.title("About Watermark application")
        about_window.minsize(width=840, height=755)
        about_window.resizable(False, False)
        # create a text label in  about window
        text_label = tkinter.Label(about_window, text="This WaterMark Application was made by waxier385\n"
                                                      "for '100 days of Python Code' course Day 84 Project!"
                                               , justify='center')
        text_label.grid(column=0, row=0)
        # place an image in about window
        about_window_image = ImageTk.PhotoImage(Image.open("images/about_window_image.PNG").resize((800, 700)),
                                                master=about_window)
        label1 = tkinter.Label(about_window, image=about_window_image, borderwidth=2, relief="solid",
                               justify='center')
        label1.image = about_window_image
        label1.grid(column=0, row=1, padx=20, pady=20)

    @staticmethod
    def help_menu():
        help_window = Tk()
        help_window.title("About Watermark application")
        help_window.resizable(False, False)
        help_window.configure(background="white")

        # create a container frame
        container_frame = Frame(help_window, bg='white')
        # Create A Canvas
        my_canvas = Canvas(container_frame)
        # Add A Scrollbars to Canvas
        y_scrollbar = ttk.Scrollbar(container_frame, orient=VERTICAL, command=my_canvas.yview)
        # Configure the canvas
        my_canvas.configure(yscrollcommand=y_scrollbar.set, width=730, height=767)

        def on_mousewheel(event):
            my_canvas.yview_scroll(int(-1*(event.delta/60)), "units")

        # create another frame inside my_canvas
        scrollable_frame = Frame(my_canvas, bg='white')
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox(ALL)))
        my_canvas.bind_all("<MouseWheel>", on_mousewheel)
        my_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # place widgets on scrollable_frame
        text_label_1 = tkinter.Label(scrollable_frame, text="WaterMark Application Help\nWith this application you can inse"
                                                        "rt watermark in any image format. The application GUI looks li"
                                                        "ke this:\n", justify='left', background="white")
        text_label_1.pack()

        # create an image label in help_window
        import_image_1 = ImageTk.PhotoImage(Image.open("images/image1.PNG"), master=help_window)
        image_label_1 = tkinter.Label(scrollable_frame, image=import_image_1, justify='left')
        image_label_1.image = import_image_1
        image_label_1.pack()

        # create a text label in  help window
        text_label_2 = tkinter.Label(scrollable_frame,
                text="1 open About Window where you can find information about this application\n2 open Help Window whe"
                     "re you can find information about how to use this application\n"
                     "3 image label where image imported is displayed at size (600,700)\n"
                     "4 with this button you can choose an image to insert watermark in it; this image is imported in image "
                     "label (3)\n5 in text label you can insert text that will be inserted in imported image as "
                     "watermark\n6 choose color for watermark text\n7 font type for watermark text\n"
                     "8 size for watermark text\n9 watermark angle\n10, 11 x and y position where current image and "
                     "mask image (where text is written) join\n12 apply changes on current image\n13 save image from "
                     "image label on a specific location\n\n To understand how this application works first you must"
                     " know what image dimensions look like:\n",justify='left', background="white")
        text_label_2.pack()

        # create an image label in help_window
        import_image_2 = ImageTk.PhotoImage(Image.open("images/image2.PNG"), master=help_window)
        image_label_2 = tkinter.Label(scrollable_frame, image=import_image_2, justify='left')
        image_label_2.image = import_image_2
        image_label_2.pack()

        # create a text label in  help window
        text_label_3 = tkinter.Label(scrollable_frame,
                text="When you use an angle value equal to 0, text used for watermark is inserted in image at "
                     "coordinate (0, image.height/2).\nThis point is represented in above image with a green spot.\n"
                     "If we enter deep in algorithm, watermark text isn’t inserted in current image, but it is inserted "
                     "in a mask image (a transparent\n image with same size like current image) and this mask is pasted\n"
                     "over current image. Due to mask image transparency, only watermark text is visible on top of "
                     "current image.\n In next image we used test number 1 as watermark text and used 0 for angle"
                     " value.",justify='left', background="white")
        text_label_3.pack()

        # create an image label in help_window
        import_image_3 = ImageTk.PhotoImage(Image.open("images/image3.PNG"), master=help_window)
        image_label_3 = tkinter.Label(scrollable_frame, image=import_image_3, justify='left')
        image_label_3.image = import_image_3
        image_label_3.pack()

        # create a text label in  help window
        text_label_4 = tkinter.Label(scrollable_frame,
            text="If we want to move watermark text closer to the image center, we will move mask image above\n"
            "current image. By default, x position value is 0 and y position value is also 0, this means that mask\n"
            "image and current image is pasted on point (0,0); in other words, (0,0) on current image is in\n"
            "same place with (0,0) on mask image. This (0, 0) value is related on current image. If we want\n"
            "to move watermark text closer to the center of the image, we will move mask image on the right.\n"
            "To do this we will paste point (0,0) from mask image to the point (200,0) from current image. To\n"
            "obtain this step we will change x position value from 0 to 200. After we changed position x value\n"
            "to 200 and press button Show on Image result will be:",justify='left', background="white")
        text_label_4.pack()

        # create an image label in help_window
        import_image_4 = ImageTk.PhotoImage(Image.open("images/image4.PNG"), master=help_window)
        image_label_4 = tkinter.Label(scrollable_frame, image=import_image_4, justify='left')
        image_label_4.image = import_image_4
        image_label_4.pack()

        # create a text label in  help window
        text_label_5 = tkinter.Label(scrollable_frame,
            text=f"If we want to move watermark text up or down, we can change Position Y value. Also, if we want\n"
                 "to move up or left watermark text we can use negative values for Position Y and Position X.\n"
                 "If we want to use a value for angle is easy to start with a low angle value, move watermark text on\n"
                 "a specific position with Position X and Position Y and then continue to change angle value.\n"
                 "\nThank you!!!",justify='left', background="white")
        text_label_5.pack()

        container_frame.pack(fill='both', expand=True)
        my_canvas.pack(side='left', fill='both', expand=True)
        y_scrollbar.pack(side='right', fill='y')
