import tkinter as tk
from tkinter import ttk, messagebox
import math

class BrickType:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height

class WallParameters:
    def __init__(self, length, height, brick_type, joint_thickness,
                 windows_count, window_width, window_height,
                 doors_count, door_width, door_height, waste_percentage):
        self.length = length
        self.height = height
        self.brick_type = brick_type
        self.joint_thickness = joint_thickness
        self.windows_count = windows_count
        self.window_width = window_width
        self.window_height = window_height
        self.doors_count = doors_count
        self.door_width = door_width
        self.door_height = door_height
        self.waste_percentage = waste_percentage

class Calculator:
    @staticmethod
    def calculate_brick_count(wall_params):
        wall_area = wall_params.length * wall_params.height
        windows_area = wall_params.windows_count * wall_params.window_width * wall_params.window_height
        doors_area = wall_params.doors_count * wall_params.door_width * wall_params.door_height
        openings_area = windows_area + doors_area
        net_area = wall_area - openings_area
        if net_area <= 0:
            raise ValueError("Чистая площадь стены не может быть меньше или равна нулю.")
        joint_meters = wall_params.joint_thickness / 1000
        effective_length = wall_params.brick_type.length + joint_meters
        effective_height = wall_params.brick_type.height + joint_meters
        brick_area = effective_length * effective_height
        brick_count = net_area / brick_area
        total_before_round = brick_count * (1 + wall_params.waste_percentage / 100)
        return math.ceil(total_before_round)

def create_brick_types():
    return [
        BrickType("Одинарный", 0.25, 0.12, 0.065),
        BrickType("Полуторный", 0.25, 0.12, 0.088),
        BrickType("Двойной", 0.25, 0.12, 0.138)
    ]

class BrickCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор кирпичей")
        self.brick_types = create_brick_types()
        self.brick_type_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Длина стены (м):").grid(row=0, column=0, sticky='w')
        self.wall_length_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=self.wall_length_var).grid(row=0, column=1)
        tk.Label(self.root, text="Высота стены (м):").grid(row=1, column=0, sticky='w')
        self.wall_height_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=self.wall_height_var).grid(row=1, column=1)
        tk.Label(self.root, text="Тип кирпича:").grid(row=2, column=0, sticky='w')
        self.brick_type_combobox = ttk.Combobox(self.root, textvariable=self.brick_type_var)
        self.brick_type_combobox['values'] = [brick.name for brick in self.brick_types]
        self.brick_type_combobox.current(0)
        self.brick_type_combobox.grid(row=2, column=1)
        tk.Label(self.root, text="Толщина шва (мм):").grid(row=3, column=0, sticky='w')
        self.joint_var = tk.IntVar(value=10)
        tk.Entry(self.root, textvariable=self.joint_var).grid(row=3, column=1)
        tk.Label(self.root, text="Количество окон:").grid(row=4, column=0, sticky='w')
        self.windows_count_var = tk.IntVar(value=0)
        tk.Entry(self.root, textvariable=self.windows_count_var).grid(row=4, column=1)
        tk.Label(self.root, text="Ширина окна (м):").grid(row=5, column=0, sticky='w')
        self.window_width_var = tk.DoubleVar(value=1.0)
        tk.Entry(self.root, textvariable=self.window_width_var).grid(row=5, column=1)
        tk.Label(self.root, text="Высота окна (м):").grid(row=6, column=0, sticky='w')
        self.window_height_var = tk.DoubleVar(value=1.0)
        tk.Entry(self.root, textvariable=self.window_height_var).grid(row=6, column=1)
        tk.Label(self.root, text="Количество дверей:").grid(row=7, column=0, sticky='w')
        self.doors_count_var = tk.IntVar(value=0)
        tk.Entry(self.root, textvariable=self.doors_count_var).grid(row=7, column=1)
        tk.Label(self.root, text="Ширина двери (м):").grid(row=8, column=0, sticky='w')
        self.door_width_var = tk.DoubleVar(value=0.9)
        tk.Entry(self.root, textvariable=self.door_width_var).grid(row=8, column=1)
        tk.Label(self.root, text="Высота двери (м):").grid(row=9, column=0, sticky='w')
        self.door_height_var = tk.DoubleVar(value=2.0)
        tk.Entry(self.root, textvariable=self.door_height_var).grid(row=9, column=1)
        tk.Label(self.root, text="Запас (%)").grid(row=10, column=0, sticky='w')
        self.waste_var = tk.IntVar(value=5)
        tk.Entry(self.root, textvariable=self.waste_var).grid(row=10, column=1)
        self.calculate_button = tk.Button(self.root, text="Рассчитать", command=self.calculate)
        self.calculate_button.grid(row=11, column=0, columnspan=2)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=12, column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            wall_length = self.wall_length_var.get()
            wall_height = self.wall_height_var.get()
            brick_name = self.brick_type_var.get()
            joint_thickness = self.joint_var.get()
            windows_count = self.windows_count_var.get()
            window_width = self.window_width_var.get()
            window_height = self.window_height_var.get()
            doors_count = self.doors_count_var.get()
            door_width = self.door_width_var.get()
            door_height = self.door_height_var.get()
            waste_percentage = self.waste_var.get()
            if wall_length <= 0 or wall_height <= 0:
                raise ValueError("Длина и высота стены должны быть положительными числами.")
            if joint_thickness < 0:
                raise ValueError("Толщина шва не может быть отрицательной.")
            if windows_count < 0 or doors_count < 0:
                raise ValueError("Количество окон и дверей не может быть отрицательным.")
            if window_width <= 0 or window_height <= 0 or door_width <= 0 or door_height <= 0:
                raise ValueError("Размеры окон и дверей должны быть положительными.")
            if waste_percentage < 0:
                raise ValueError("Процент запаса не может быть отрицательным.")
            brick_type = next((bt for bt in self.brick_types if bt.name == brick_name), None)
            if not brick_type:
                raise ValueError("Выбранный тип кирпича не найден.")
            wall_params = WallParameters(
                length=wall_length,
                height=wall_height,
                brick_type=brick_type,
                joint_thickness=joint_thickness,
                windows_count=windows_count,
                window_width=window_width,
                window_height=window_height,
                doors_count=doors_count,
                door_width=door_width,
                door_height=door_height,
                waste_percentage=waste_percentage
            )
            total = Calculator.calculate_brick_count(wall_params)
            self.result_label.config(text=f"Необходимо кирпичей: {total}")
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BrickCalculatorApp(root)
    root.mainloop()
