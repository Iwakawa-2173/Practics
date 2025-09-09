import tkinter as tk
from tkinter import messagebox

# Окно
window = tk.Tk()
window.title("Калькулятор")
window.geometry("500x500")
window.resizable(False, False)
window.configure(bg="PINK")

import math

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

def taylor_sqrt(x, n=20):
    if x < 0:
        raise ValueError("sqrt(x) для x >= 0")
    t = x - 1
    result = 1
    term = 1
    for i in range(1, n):
        term *= (0.5 - (i - 1)) / i * t
        result += term
    return result


# Поле ввода
entry = tk.Entry(window, font=("Arial", 24), bg="WHITE", fg="BLACK", bd=0, justify="right")
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

# Кнопочки
buttons = [
    "7", "8", "9", "/", "^",
    "4", "5", "6", "*", "sin",
    "1", "2", "3", "-", "cos",
    "C", "0", "=", "+", "ln",
    "%", "sqrt", "(", ")"
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

# Функция для создания кнопки с нужным стилем
def create_button(text):
    return tk.Button(
        window, text=text, font=("Arial", 18), fg="PINK", bg="WHITE",
        width=5, height=2, bd=0, activebackground="BLACK", activeforeground="WHITE"
    )

# Функция обработки нажатия кнопок
def on_click(event):
    button_text = event.widget.cget("text")

    if button_text == "C":
        entry.delete(0, tk.END)
        expression_terms.clear()
        return

    if button_text == "=":
        # Выводим RPN для проверки
        try:
            rpn = parse_to_rpn()
            print("RPN:", rpn)
            result = calc(rpn)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        expression_terms.clear()
        return

    # Для остальных кнопок выводим символ и добавляем в выражение
    entry.insert(tk.END, button_text)
    expression_terms.append(button_text)

# Функция преобразования выражения в RPN
def parse_to_rpn():
    rpn_string = []
    stack = []
    functions = {"sin", "cos", "sqrt", "ln"}

    for token in expression_terms:
        # Если токен число (проверяем: строка состоит из цифр), добавляем в RPN
        if token.isdigit():
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
        else:  # оператор
            while stack and stack[-1] in pr and token in pr and pr[stack[-1]] >= pr[token]:
                rpn_string.append(stack.pop())
            stack.append(token)

    while stack:
        if stack[-1] in ("(", ")"):
            raise ValueError("Несоответствие скобок")
        rpn_string.append(stack.pop())

    return rpn_string

# Функция вычисления результата по RPN
def calc(rpn):
    stack = []
    functions = {
        "sin": taylor_sin,
        "cos": taylor_cos,
        "sqrt": taylor_sqrt,
        "ln": taylor_ln
    }

    for token in rpn:
        if token.isdigit():
            stack.append(float(token))
        elif token in functions:
            if not stack:
                raise ValueError("Недостаточно операндов для функции")
            a = stack.pop()
            stack.append(functions[token](a))
        else:
            # бинарные операции
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
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
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
def create_buttons():
    row = 1
    col = 0
    for button in buttons:
        but = create_button(button)
        but.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        but.bind("<Button-1>", on_click)
        col += 1
        if col > 4:
            col = 0
            row += 1

create_buttons()

for i in range(5):
    window.grid_columnconfigure(i, weight=1)
for i in range(6):
    window.grid_rowconfigure(i, weight=1)

window.mainloop()
