from time import sleep
import tkinter as tk
from tkinter import messagebox


# Окно
window = tk.Tk()
window.title("Калькулятор")
window.geometry("500x600")
window.resizable(False, False)
window.configure(bg="PINK")

import math

interval = 1000 
interface_switch = True
def XLII():
    global interval
    global interface_switch
    entry.insert(tk.END, '9')
    # ускоряем интервал, уменьшая время задержки, минимальное время, например, 200 мс
    if interval < 500:
        if interface_switch == True:
            window["bg"] = "BLACK"
            create_buttons("dos")
            interface_switch = False
        else:
            window["bg"] = "PINK"
            create_buttons("kawaii")
            interface_switch = True
    if interval == 0:
        messagebox.showerror("42", "БЕЗНОГNМ")
        window.destroy()
        return 42
    interval = max(0, int(interval * 0.9))
    window.after(interval, XLII)

# Функция для проверки, является ли строка числом
def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def taylor_sin(x, n=10):
    x = x % (2 * math.pi)  # нормализация
    result = 0
    sign = 1
    for i in range(n):
        term = x**(2*i+1) / math.factorial(2*i+1)
        result += sign * term
        sign *= -1
    return result

def taylor_cos(x, n=10):
    x = x % (2 * math.pi)
    result = 0
    sign = 1
    for i in range(n):
        term = x**(2*i) / math.factorial(2*i)
        result += sign * term
        sign *= -1
    return result

def taylor_ln(x, n=20):
    if x <= 0:
        raise ValueError("ln(x) для x > 0")
    y = (x - 1) / (x + 1)
    result = 0
    for i in range(n):
        term = (y**(2*i+1)) / (2*i+1)
        result += term
    return 2 * result

def sqrt_newton(x, epsilon=1e-10):
    if x < 0:
        raise ValueError("x должно быть >= 0")
    if x == 0:
        return 0
    y = x
    while True:
        y_next = 0.5 * (y + x / y)
        if abs(y - y_next) < epsilon:
            break
        y = y_next
    return y



# Поле ввода
entry = tk.Entry(window, font=("Arial", 24), bg="WHITE", fg="BLACK", bd=0, justify="right")
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

# Кнопочки
buttons = [
    "7", "8", "9", "/", "^",
    "4", "5", "6", "*", "sin",
    "1", "2", "3", "-", "cos",
    "C", "0", "=", "+", "ln",
    "%", "sqrt", "(", ")", ".",
    "Kawaii", "DOS"
]

pr = {
    "sin": 3,
    "cos": 3,
    "sqrt": 3,
    "ln": 3,
    "^": 2,
    "*": 1,
    "/": 1,
    "%": 1,
    "+": 0,
    "-": 0
}

expression_terms = []  # Массив для элементов выражения

# Функции для создания кнопки с нужным стилем
def create_button(text, style):
    if style == "kawaii":
        return tk.Button(
            window, text=text, font=("Arial", 18), fg="PINK", bg="WHITE",
            width=5, height=2, bd=0, activebackground="BLACK", activeforeground="WHITE"
        )
    elif style == "dos":
        return tk.Button(
            window, text=text, font=("Arial", 18), fg="BLUE", bg="BLACK",
            width=5, height=2, bd=0, activebackground="BLACK", activeforeground="WHITE"
        )
def create_big_button(text, style):
    if style == "kawaii":
        return tk.Button(
            window, text=text, font=("Arial", 9), fg="PINK", bg="WHITE",
            width=5, height=2, bd=0, activebackground="BLACK", activeforeground="WHITE"
        )
    elif style == "dos":
        return tk.Button(
            window, text=text, font=("Arial", 18), fg="BLUE", bg="BLACK",
            width=5, height=2, bd=0, activebackground="WHITE", activeforeground="BLACK"
        )

current_number = ""
# Функция обработки нажатия кнопок
def on_click(event):
    global current_number
    first_negative = False
    button_text = event.widget.cget("text")

    if button_text.isdigit() or button_text == ".":
        current_number += button_text
        entry['state'] = 'normal'
        entry.insert(tk.END, button_text)
        entry['state'] = 'readonly'
        return

    if current_number != "":
        expression_terms.append(current_number)
        current_number = ""

    if button_text == "C":
        entry['state'] = 'normal'
        entry.delete(0, tk.END)
        entry['state'] = 'readonly'
        expression_terms.clear()
        return
    
    if button_text == "-" and len(expression_terms) == 0:
        current_number += "-"
        first_negative = True

    if button_text == "=":
        try:
            rpn = parse_to_rpn()
            result = calc(rpn)
            entry['state'] = 'normal'
            entry.delete(0, tk.END)
            if (result - int(result) == 0): # Проверяем, является ли результат целым числом, проверяя равенство его дробной части нулю
                entry.insert(tk.END, str(int(result))) #Если результат целый, нет необходимости выводить точку и нули
            else:
                entry.insert(tk.END, str("{:.5f}".format(result)))
            entry['state'] = 'readonly'
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        expression_terms.clear()
        expression_terms.append(str(result))
        return
    if button_text == "Kawaii":
        window["bg"] = "PINK"
        create_buttons("kawaii")
        return
    if button_text == "DOS":
        window["bg"] = "BLUE"
        create_buttons("dos")
        return
    # Для операторов, функций, скобок
    if not first_negative:
        expression_terms.append(button_text)
    
    entry['state'] = 'normal'
    entry.insert(tk.END, button_text)
    entry['state'] = 'readonly'


# Функция преобразования выражения в RPN
def parse_to_rpn():
    rpn_string = []
    stack = []
    functions = {"sin", "cos", "sqrt", "ln"}

    for token in expression_terms:
        if is_digit(token):
            rpn_string.append(token)
        elif token in functions or token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                rpn_string.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
            else:
                raise ValueError("Несоответствие скобок")
        else:  # Оператор
            while stack and stack[-1] in pr and token in pr and pr[stack[-1]] >= pr[token]:
                rpn_string.append(stack.pop())
            stack.append(token)

    while stack:
        if stack[-1] in ("(", ")"):
            raise ValueError("Несоответствие скобок")
        rpn_string.append(stack.pop())
    print(rpn_string)
    return rpn_string

# Функция вычисления результата по RPN
def calc(rpn):
    stack = []
    functions = {
        "sin": taylor_sin,
        "cos": taylor_cos,
        "sqrt": sqrt_newton,
        "ln": taylor_ln
    }

    for token in rpn:
        if is_digit(token):
            stack.append(float(token))
        elif token in functions:
            if not stack:
                raise ValueError("Недостаточно операндов для функции")
            a = stack.pop()
            stack.append(functions[token](a))
        else:
            # Бинарные операции
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для оператора")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0: # Обработка деления на ноль
                    entry['state'] = 'normal'
                    entry.delete(0, tk.END)
                    XLII()
                    raise WindowsError("Oh, shit...")
                else:
                    stack.append(a / b)
            elif token == "%":
                stack.append(a % b)
            elif token == "^":
                stack.append(a ** b)
            else:
                raise ValueError(f"Неизвестный оператор {token}")

    if len(stack) != 1:
        raise ValueError("Ошибка в вычислении выражения")

    return stack[0]

# Создание и размещение кнопок
def create_buttons(style):
    row = 1
    col = 0
    for button in buttons:
        if button != "Kawaii theme" and button != "Dark theme":
            but = create_button(button, style)
        else:
            but = create_big_button(button, style)
        but.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        but.bind("<Button-1>", on_click)
        col += 1
        if col > 4:
            col = 0
            row += 1

create_buttons("kawaii")

for i in range(5):
    window.grid_columnconfigure(i, weight=1)
for i in range(6):
    window.grid_rowconfigure(i, weight=1)

window.mainloop()
