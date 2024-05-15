import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from functools import partial
from tkinter.colorchooser import askcolor

class MemeGenerator:
    def __init__(self):
        self.proj_path = os.getcwd()
        self.window = Tk()
        self.window.title('Генератор мемов')
        self.window.geometry('1920x1080')
        self.window.iconbitmap('')
        self.color = 'black'
        self.frame = Frame(
            self.window,
            padx=10,
            pady=10
        )
        self.frame.grid()
        self.open_button = Button(self.frame, text="Выберите картинку", command=self.open_file, font=("Arial", 20), anchor=CENTER)
        self.open_button.grid(row=2, column=1)
        # TODO за новой картинкой видно старую
        self.top_text_label = Label(
            self.frame,
            text="Введите верхний текст  ",
            font=("Arial", 20, )
        )
        self.top_text_label.grid(row=4, column=1)
        self.top_text_input = Entry(
            self.frame,
            font=("Arial", 20),
            width=100,
        )
        self.top_text_input.grid(row=4, column=2, pady=5)


        self.bottom_text_label = Label(
            self.frame,
            text="Введите нижний текст  ",
            font=("Arial", 20)
        )
        self.bottom_text_label.grid(row=5, column=1)
        self.bottom_text_input = Entry(
            self.frame,
            font=("Arial", 20),
            width=100
        )
        self.bottom_text_input.grid(row=5, column=2, pady=5)

        self.fonts = {}
        fonts_names = []
        for file in os.listdir(f"{self.proj_path}/Fonts"):
            if "ttf" in file:
                fnt = ImageFont.truetype(f"{self.proj_path}/Fonts/{file}", 14)
                font = fnt.getname()
                font_name = f"{font[0]} {font[1]}"
                self.fonts[font_name] = file
                fonts_names.append(font_name)
        self.font_selector = ttk.Combobox(self.frame, values=fonts_names, state="readonly", font=("Arial", 20))
        self.font_selector.grid(row=7, column=1)
        self.font_selector.current(0)
        self.font = 'Arial Regular'

        self.sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        self.size_chooser_label = Label(
            self.frame,
            text="Введите желаемый размер шрифта  ",
            font=("Arial", 20)
        )
        self.size_chooser_label.grid(row=6, column=1)
        self.size_chooser_input = Entry(
            self.frame,
            font=("Arial", 20),
            width=100
        )
        self.size_chooser_input.grid(row=6, column=2, pady=5)


        # self.set_font_button = Button(self.frame, text="Применить шрифт", command=self.set_font, font=("Arial", 20))
        # self.set_font_button.grid(row=8, column=1)

        self.fg_btn = tk.Button(self.frame, text="Выбрать цвет текста", font=("Arial", 20), command=partial(self.set_color))
        self.fg_btn.grid(row=7, column=2)


        self.generate_mem_button = Button(self.frame, text="Сгенерировать мем",
                                          command=self.generate_mem,
                                          font=("Arial", 30))
        self.generate_mem_button.grid(row=9, column=1)

        self.save_mem_button = Button(self.frame, text="Сохранить мем",
                                          command=self.save_picture,
                                          font=("Arial", 30))
        self.save_mem_button.grid(row=9, column=2)

        self.canvas_height = 650
        self.canvas_width = 1155
        self.canvas = Canvas(self.window, height=self.canvas_height, width=self.canvas_width)
        self.chosen_image = Image.open(f"{self.proj_path}/white.png")
        self.mem = Image.open(f"{self.proj_path}/white.png")
        self.width, self.height = self.chosen_image.size
        self.width_dif = self.width / self.canvas_width
        self.height_dif = self.height / self.canvas_height
        self.max_dif = max(self.width_dif, self.height_dif)
        self.scaled_image = self.chosen_image.resize((int(self.width / self.max_dif), int(self.height / self.max_dif)))
        self.photo = ImageTk.PhotoImage(self.scaled_image)
        self.scaled_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid()

        self.size_chooser_input.insert(0, str(self.height // 20))
        self.window.mainloop()

    def split_text(self, text):
        words = text.split()
        sentence = ""
        sentences = ""
        font_size = int(self.size_chooser_input.get())
        max_symbol_len = font_size * 30 / 36
        max_sentence_len = int(self.width / max_symbol_len)
        for word in words:
            if len(sentence) >= max_sentence_len or len(sentence + word) > max_sentence_len:
                sentences += f"{sentence}\n"
                sentence = ""
            if len(word) > max_sentence_len:
                for i in word:
                    sentence += i
                    if len(sentence) == max_sentence_len:
                        sentences += f"{sentence}\n"
                        sentence = ""
                sentences += " "
            else:
                sentence += f"{word} "
        if len(sentence) > 0:
            sentences += f"{sentence}"
        return sentences


    def save_picture(self):
        path = filedialog.asksaveasfile(defaultextension="png")
        print(path.name)
        self.mem.save(path.name)


    def set_color(self):
        self.color = askcolor()[1]
        self.generate_mem()
    def generate_mem(self):
        self.mem = self.chosen_image.copy()
        font_size = int(self.size_chooser_input.get())
        self.font = self.font_selector.get()
        font = ImageFont.truetype(self.fonts[self.font], font_size)
        drawer = ImageDraw.Draw(self.mem)
        drawer.text((self.width/2, 1.5 * font_size), self.split_text(self.top_text_input.get()), font=font, fill=self.color, anchor="ms")
        drawer.text((self.width / 2, self.height - 1.5 * font_size), self.split_text(self.bottom_text_input.get()), font=font, fill=self.color, anchor="md")
        self.scaled_image = self.mem.resize((int(self.width / self.max_dif), int(self.height / self.max_dif)))
        photo = ImageTk.PhotoImage(self.scaled_image)
        self.scaled_image = self.canvas.create_image(578, 325, image=photo)
        self.window.mainloop()

    def set_font(self):
        chosen_font_name = self.font_selector.get()
        self.font = chosen_font_name
        self.generate_mem()

    def open_file(self):
        path = filedialog.askopenfilename()
        self.chosen_image = Image.open(path)
        self.width, self.height = self.chosen_image.size
        width_dif = self.width / self.canvas_width
        height_dif = self.height / self.canvas_height
        self.max_dif = max(width_dif, height_dif)
        print(int(self.width / self.max_dif), int(self.height / self.max_dif))
        self.canvas.delete("all")
        self.scaled_image = self.chosen_image.resize((int(self.width / self.max_dif), int(self.height / self.max_dif)))
        photo = ImageTk.PhotoImage(self.scaled_image)
        scaled_image = self.canvas.create_image(578, 325, image=photo)
        self.window.mainloop()


meme_generator = MemeGenerator()

