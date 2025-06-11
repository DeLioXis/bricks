import tkinter as tk
from tkinter import ttk, messagebox
import math

class BrickType:
    """Класс, представляющий тип кирпича с его размерами."""
    def __init__(self, name, length, width, height):
        """
        Инициализация типа кирпича.
        
        :param name: Название кирпича (например, 'Одинарный')
        :param length: Длина кирпича в метрах
        :param width: Ширина кирпича в метрах
        :param height: Высота кирпича в метрах
        """
        self.name = name
        self.length = length
        self.width = width
        self.height = height

class WallParameters:
    """Класс, представляющий параметры стены для расчёта."""
    def __init__(self, length, height, brick_type, joint_thickness,
                 windows_count, window_width, window_height,
                 doors_count, door_width, door_height, waste_percentage):
        """
        Инициализация параметров стены.
        
        :param length: Длина стены в метрах
        :param height: Высота стены в метрах
        :param brick_type: Объект BrickType
        :param joint_thickness: Толщина шва в миллиметрах
        :param windows_count: Количество окон
        :param window_width: Ширина одного окна в метрах
        :param window_height: Высота одного окна в метрах
        :param doors_count: Количество дверей
        :param door_width: Ширина одной двери в метрах
        :param door_height: Высота одной двери в метрах
        :param waste_percentage: Процент запаса кирпичей
        """
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
    """Класс для выполнения расчётов количества кирпичей."""
    @staticmethod
    def calculate_brick_count(wall_params):
        """
        Рассчитывает количество кирпичей, необходимое для постройки стены.
        
        :param wall_params: Объект WallParameters с параметрами стены
        :return: Количество кирпичей (округлённое вверх)
        :raises ValueError: Если чистая площадь стены отрицательна или равна нулю
        """
        # Общая площадь стены
        wall_area = wall_params.length * wall_params.height
        
        # Площадь проёмов
        windows_area = wall_params.windows_count * wall_params.window_width * wall_params.window_height
        doors_area = wall_params.doors_count * wall_params.door_width * wall_params.door_height
        openings_area = windows_area + doors_area
        
        # Чистая площадь стены
        net_area = wall_area - openings_area
        if net_area <= 0:
            raise ValueError("Чистая площадь стены не может быть меньше или равна нулю.")
        
        # Перевод толщины шва из мм в метры
        joint_meters = wall_params.joint_thickness / 1000
        
        # Расчёт количества кирпичей по длине и высоте с учётом швов
        bricks_per_length = wall_params.length / (wall_params.brick_type.length + joint_meters)
        bricks_per_height = wall_params.height / (wall_params.brick_type.height + joint_meters)
        
        # Общее количество кирпичей (округление вверх)
        brick_count = math.ceil(bricks_per_length) * math.ceil(bricks_per_height)
        
        # Учёт запаса
        total = brick_count * (1 + wall_params.waste_percentage / 100)
        return math.ceil(total)

def create_brick_types():
    """Создаёт список предопределённых типов кирпичей."""
    return [
        BrickType("Одинарный", 0.25, 0.12, 0.065),
        BrickType("Полуторный", 0.25, 0.12, 0.088),
        BrickType("Двойной", 0.25, 0.12, 0.138)
    ]

class BrickCalculatorApp:
    """Класс для создания графического интерфейса приложения."""
    def __init__(self, root):
        """
        Инициализация приложения.
        
        :param root: Корневое окно Tkinter
        """
        self.root = root
        self.root.title("Калькулятор кирпичей")
        self.brick_types = create_brick_types()
        self.brick_type_var = tk.StringVar()
        self.setup_ui()
    
    def setup_ui(self):
        """Создание элементов интерфейса."""
        self.create_wall_inputs()
        self.create_brick_type_input()
        self.create_joint_input()
        self.create_openings_inputs()
        self.create_waste_input()
        self.create_buttons()
        self.create_result_label()
    
    def create_wall_inputs(self):
        """Создание полей ввода для параметров стены."""
        tk.Label(self.root, text="Длина стены (м):").grid(row=0, column=0, sticky='w')
        self.wall_length_var = tk.DoubleVar()
        self._create_entry(0, 1, self.wall_length_var)
        
        tk.Label(self.root, text="Высота стены (м):").grid(row=1, column=0, sticky='w')
        self.wall_height_var = tk.DoubleVar()
        self._create_entry(1, 1, self.wall_height_var)
    
    def create_brick_type_input(self):
        """Создание поля выбора типа кирпича."""
        tk.Label(self.root, text="Тип кирпича:").grid(row=2, column=0, sticky='w')
        self.brick_type_combobox = ttk.Combobox(
            self.root, 
            textvariable=self.brick_type_var,
            values=[brick.name for brick in self.brick_types]
        )
        self.brick_type_combobox.current(0)
        self.brick_type_combobox.grid(row=2, column=1)
    
    def create_joint_input(self):
        """Создание поля ввода толщины шва."""
        tk.Label(self.root, text="Толщина шва (мм):").grid(row=3, column=0, sticky='w')
        self.joint_var = tk.IntVar(value=10)
        self._create_entry(3, 1, self.joint_var)
    
    def create_openings_inputs(self):
        """Создание полей ввода для проёмов."""
        # Окна
        tk.Label(self.root, text="Количество окон:").grid(row=4, column=0, sticky='w')
        self.windows_count_var = tk.IntVar(value=0)
        self._create_entry(4, 1, self.windows_count_var)
        
        tk.Label(self.root, text="Ширина окна (м):").grid(row=5, column=0, sticky='w')
        self.window_width_var = tk.DoubleVar(value=1.0)
        self._create_entry(5, 1, self.window_width_var)
        
        tk.Label(self.root, text="Высота окна (м):").grid(row=6, column=0, sticky='w')
        self.window_height_var = tk.DoubleVar(value=1.0)
        self._create_entry(6, 1, self.window_height_var)
        
        # Двери
        tk.Label(self.root, text="Количество дверей:").grid(row=7, column=0, sticky='w')
        self.doors_count_var = tk.IntVar(value=0)
        self._create_entry(7, 1, self.doors_count_var)
        
        tk.Label(self.root, text="Ширина двери (м):").grid(row=8, column=0, sticky='w')
        self.door_width_var = tk.DoubleVar(value=0.9)
        self._create_entry(8, 1, self.door_width_var)
        
        tk.Label(self.root, text="Высота двери (м):").grid(row=9, column=0, sticky='w')
        self.door_height_var = tk.DoubleVar(value=2.0)
        self._create_entry(9, 1, self.door_height_var)
    
    def create_waste_input(self):
        """Создание поля ввода процента запаса."""
        tk.Label(self.root, text="Запас (%)").grid(row=10, column=0, sticky='w')
        self.waste_var = tk.IntVar(value=5)
        self._create_entry(10, 1, self.waste_var)
    
    def create_buttons(self):
        """Создание кнопки расчёта."""
        self.calculate_button = tk.Button(self.root, text="Рассчитать", command=self.calculate)
        self.calculate_button.grid(row=11, column=0, columnspan=2)
    
    def create_result_label(self):
        """Создание метки для отображения результата."""
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=12, column=0, columnspan=2, pady=10)
    
    def _create_entry(self, row, column, variable):
        """Создание поля ввода с валидацией."""
        vcmd = (self.root.register(self.validate_numeric_input), '%P')
        entry = tk.Entry(
            self.root,
            textvariable=variable,
            validate='all',
            validatecommand=(vcmd, '%P')
        )
        entry.grid(row=row, column=column)
        return entry
    
    def validate_numeric_input(self, value):
        """Проверяет, является ли ввод числом."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def calculate(self):
        """Обработчик события нажатия на кнопку 'Рассчитать'."""
        self.result_label.config(text="")
        
        try:
            # Получаем значения из полей ввода
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
            
            # Проверка корректности ввода
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
            
            # Найти выбранный тип кирпича
            brick_type = next((bt for bt in self.brick_types if bt.name == brick_name), None)
            if not brick_type:
                raise ValueError("Выбранный тип кирпича не найден.")
            
            # Создать объект параметров стены
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
            
            # Выполнить расчёт
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