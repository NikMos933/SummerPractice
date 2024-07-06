import cv2
from tkinter import *
from tkinter import filedialog, IntVar, StringVar
from tkinter.messagebox import showerror
from PIL import ImageTk, Image
from Functions import *


class MainWindow:
    """Это класс главного окна реализующая логику приложения"""

    def __init__(self):
        self.root = Tk()
        self.__menu_pos="Main"
        self.image = None
        self.canvas_width = 700
        self.canvas_height = 500
        self.var = IntVar()
        self.var.set(0)
        self.angle = 0
        self.lang = IntVar(value=1)
        self.name = StringVar(value="")
        self.root.title("Image redactor")
        self.root.geometry(f"{800}x{600}")
        self.root.resizable(False, False)
        self.load_button = Button(self.root, text="Загрузить\n фото", command=self.load)
        self.load_from_web_cam_button = Button(self.root, text="Загрузить фото с \nвеб-камеры",
                                               command=self.capture_image)
        self.show_canal_button = Button(self.root, text="Показать цветовой канал", command=self.show_canal)
        self.red = Radiobutton(text="Красный", variable=self.var, value=0)
        self.green = Radiobutton(text="Зелёный", variable=self.var, value=1)
        self.blue = Radiobutton(text="Синий", variable=self.var, value=2)
        self.show_grey_picture = Button(self.root, text="Показать рисунок в серых оттенках",command=self.show_grey_pic)
        self.angle_lbl = Label(self.root, text="угол поворота:")
        self.angle_entry = Entry(self.root, width=7)
        self.rotate_picture = Button(self.root, text="Повернуть рисунок",command=self.rotate)
        self.print_rectangle = Button(self.root, text="Нарисовать прямоугольтник",command=self.print_rectangle)
        self.x1_lbl = Label(self.root, text="x1:")
        self.x1_entry = Entry(self.root, width=7)
        self.y1_lbl = Label(self.root, text="y1:")
        self.y1_entry = Entry(self.root, width=7)
        self.x2_lbl = Label(self.root, text="x2:")
        self.x2_entry = Entry(self.root, width=7)
        self.y2_lbl = Label(self.root, text="y2:")
        self.y2_entry = Entry(self.root, width=7)
        self.image_canvas = Canvas(self.root,width=self.canvas_width, height=self.canvas_height, bg="white")
        self.quit_button = Button(self.root, text="Выход",command=self.quit)


    def run(self):
        """Это функция для иницаиалиации окна"""
        self.load_button.place(x=10, y=10)
        self.load_from_web_cam_button.place(x=88, y=10)
        self.show_canal_button.place(x=10, y=55)
        self.red.place(x=160, y=55)
        self.green.place(x=235, y=55)
        self.blue.place(x=315, y=55)
        self.show_grey_picture.place(x=240, y=10)
        self.rotate_picture.place(x=460, y=10)
        self.angle_lbl.place(x=460, y=37)
        self.angle_entry.place(x=460, y=60)
        self.print_rectangle.place(x=600, y=10)
        self.x1_lbl.place(x=600, y=37)
        self.x1_entry.place(x=618, y=37)
        self.y1_lbl.place(x=600, y=60)
        self.y1_entry.place(x=618, y=60)
        self.x2_lbl.place(x=670, y=37)
        self.x2_entry.place(x=688, y=37)
        self.y2_lbl.place(x=670, y=60)
        self.y2_entry.place(x=688, y=60)
        self.image_canvas.place(x=10, y=90)
        self.quit_button.place(x=750, y=550)
        self.root.mainloop()


    def load(self):
        """Это функция для загрузи изображения с компютера"""
        fl = filedialog.askopenfile(filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        self.image = Image.open(str(fl.name))
        self.image = self.image.resize((self.canvas_width, self.canvas_height))
        photo = ImageTk.PhotoImage(self.image)
        self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
        self.image_canvas.image = photo


    def capture_image(self):
        """Это функция для загрузи изображения с веб-камеры"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            showerror("Ошибка", "Веб-камера не найдена")
            return
        ret, frame = cap.read()
        cap.release()
        if not ret:
            showerror("Ошибка", "Неполуается получить фото")
            return
        self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.image = self.image.resize((self.canvas_width, self.canvas_height))
        photo = ImageTk.PhotoImage(self.image)
        self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
        self.image_canvas.image = photo

    def show_canal(self):
        """Это функция для выведение одного из цветных каналов изображения"""
        if self.image is None:
            self.open_error()
        else:
            channels = self.image.split()
            dark = channels[0].point(lambda _: 0)
            match self.var.get():
                case 0:
                    krasnoye_sliyaniye = Image.merge("RGB", (channels[0], dark, dark))
                    photo = ImageTk.PhotoImage(krasnoye_sliyaniye)
                    self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.image_canvas.image = photo
                case 1:
                    zelenoye_sliyaniye = Image.merge("RGB", (dark, channels[1], dark))
                    photo = ImageTk.PhotoImage(zelenoye_sliyaniye)
                    self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.image_canvas.image = photo
                case 2:
                    sineye_sliyaniye = Image.merge("RGB", (dark, dark, channels[2]))
                    photo = ImageTk.PhotoImage(sineye_sliyaniye)
                    self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.image_canvas.image = photo



    def show_grey_pic(self):
        """Это функция для вывода изобрадения в серых тонах"""
        if self.image is None:
            self.open_error()
        else:
            gray_img = self.image.convert("L")
            photo = ImageTk.PhotoImage(gray_img)
            self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
            self.image_canvas.image = photo

    def rotate(self):
        """Это функция для поворота картинки"""
        if self.image is None:
            self.open_error()
        elif check(self.angle_entry.get()):
            angle = int(self.angle_entry.get())
            rotated_image = self.image.rotate(angle, expand=True)
            rotated_image = rotated_image.resize((self.canvas_width, self.canvas_height))
            photo = ImageTk.PhotoImage(rotated_image)
            self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
            self.image_canvas.image = photo
        else:
            self.check_error()


    def print_rectangle(self):
        """Это функция для рисования прямоугольника"""
        if self.image is None:
            self.open_error()
        elif (check(self.x1_entry.get()) and check(self.y1_entry.get()) and check(self.y2_entry.get())
              and check(self.x1_entry.get())):
            photo = ImageTk.PhotoImage(self.image)
            self.image_canvas.create_image(0, 0, anchor=NW, image=photo)
            self.image_canvas.image = photo
            self.image_canvas.create_rectangle(int(self.x1_entry.get()),int(self.y1_entry.get()),
                                               int(self.x2_entry.get()),int(self.y2_entry.get()), fill = "blue")
        else:
            self.check_error()


    def open_error(self):
        """Это окно ошибки при отсутствии рисунка"""
        showerror(title="Ошибка", message="фото ещё не загружено")

    def check_error(self):
        """Это окно ошибки при неверного типа данных"""
        showerror(title="Ошибка", message="Неверный ввод: Введите целое число")

    def quit(self):
        """Это функиця закрытия окна"""
        self.root.destroy()
