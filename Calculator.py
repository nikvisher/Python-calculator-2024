import tkinter as tk
import math

def is_operator(c):
    return c in "+-*/^÷."

def click(btn):
    display.config(state=tk.NORMAL)
    current_text = display.get()

    if btn == "=":
        try:
            expression = display.get().replace("^", "**").replace("÷", "/")
            expression = expression.replace("sin(", "math.sin(math.radians(")
            expression = expression.replace("cos(", "math.cos(math.radians(")
            expression = expression.replace("tan(", "math.tan(math.radians(")
            expression = expression.replace("sqrt(", "math.sqrt(")
            expression = expression.replace("lg(", "math.log10(")
            expression = expression.replace("ln(", "math.log(")
            expression = expression.replace("factorial(", "math.factorial(")

            # Автоматически закрывать скобки для тригонометрических функций и факториала
            open_parens = 0
            new_expression = ""
            for char in expression:
                if char == '(':
                    open_parens += 1
                elif char == ')':
                    open_parens -= 1
                new_expression += char
            new_expression += ")" * open_parens

            result = eval(new_expression, {"__builtins__": None}, {"math": math, "abs": abs})
            display.delete(0, tk.END)

            if isinstance(result, float):
                if abs(result) < 1e-10 or abs(result) > 1e10:
                    display.insert(tk.END, "{:g}".format(result))
                else:
                    display.insert(tk.END, f"{result:.10f}".rstrip('0').rstrip('.'))
            else:
                display.insert(tk.END, result)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(tk.END, "Ошибка")
    elif btn == "C":
        display.delete(0, tk.END)
        display.insert(tk.END, "0")
    elif btn == "←":
        if len(current_text) > 1:
            display.delete(len(current_text) - 1)
        else:
            display.delete(0, tk.END)
            display.insert(tk.END, "0")
    elif btn == "%":
        try:
            expression = display.get().replace("^", "**").replace("÷", "/")
            result = eval(expression, {"builtins": None}, {"math": math, "abs": abs}) / 100
            display.delete(0, tk.END)

            if isinstance(result, float):
                if abs(result) < 1e-10 or abs(result) > 1e10:
                    display.insert(tk.END, "{:g}".format(result))
                else:
                    display.insert(tk.END, f"{result:.10f}".rstrip('0').rstrip('.'))
            else:
                display.insert(tk.END, result)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(tk.END, "Ошибка")
    else:
        if current_text == "0":
            if btn == ".":
                display.insert(tk.END, btn)
            else:
                display.delete(0, tk.END)
                display.insert(tk.END, btn)
        else:
            if not (is_operator(current_text[-1]) and is_operator(btn)):
                display.insert(tk.END, btn)

    display.config(state='readonly')

def toggle_advanced():
    if adv_frame.winfo_ismapped():
        adv_frame.grid_remove()
    else:
        adv_frame.grid()

def adv_click(btn):
    display.config(state=tk.NORMAL)
    current_text = display.get()

    if current_text == "0":
        display.delete(0, tk.END)

    if btn == "sin":
        display.insert(tk.END, "sin(")
    elif btn == "cos":
        display.insert(tk.END, "cos(")
    elif btn == "tan":
        display.insert(tk.END, "tan(")
    elif btn == "sqrt":
        display.insert(tk.END, "sqrt(")
    elif btn == "lg":
        display.insert(tk.END, "lg(")
    elif btn == "ln":
        display.insert(tk.END, "ln(")
    elif btn == "x!":
        display.insert(tk.END, "factorial(")
    elif btn == "x^y":
        if not is_operator(current_text[-1]):
            display.insert(tk.END, "^")
    elif btn == "π":
        display.insert(tk.END, str(math.pi))
    elif btn == "abs":
        display.insert(tk.END, "abs(")

    display.config(state='readonly')

# Создание основного окна
root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x600")
root.resizable(False, False)

# Настройка темных цветов
bg_color = "#1e1e1e"
fg_color = "#ffffff"
button_color = "#333333"
highlight_color = "#ff8c00"
highlight_hover_color = "#666666"

root.configure(bg=bg_color)

# Дисплей для ввода и результата
display = tk.Entry(root, font=("Arial", 24), borderwidth=0, highlightthickness=0, bg=bg_color, fg=fg_color,
                   insertbackground=fg_color, justify='right', state='readonly', readonlybackground=bg_color)
display.grid(row=0, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")
display.config(state=tk.NORMAL)
display.insert(0, "0")
display.config(state='readonly')

# Определение кнопок
buttons = [
    '7', '8', '9', '÷', '←',
    '4', '5', '6', '*', '%',
    '1', '2', '3', '-', '(',
    '0', '.', 'C', '+', ')'
]

# Создание кнопок
for i, btn in enumerate(buttons):
    action = lambda x=btn: click(x)
    b = tk.Button(root, text=btn, font=("Arial", 18), bg=button_color, fg=fg_color, activebackground=highlight_color,
                  command=action)
    b.grid(row=(i // 5) + 1, column=i % 5, sticky="nsew", padx=5, pady=5)
    b.bind("<Enter>", lambda event, b=b: b.config(bg=highlight_hover_color))
    b.bind("<Leave>", lambda event, b=b: b.config(bg=button_color))

# Добавление кнопки равно
equal_button = tk.Button(root, text='=', font=("Arial", 18), bg=highlight_color, fg=fg_color,
                         command=lambda: click('='))
equal_button.grid(row=5, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

# Кнопка для дополнительных функций
adv_button = tk.Button(root, text='Доп. функции', font=("Arial", 18), bg=button_color, fg=fg_color,
                       command=toggle_advanced)
adv_button.grid(row=6, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
adv_button.bind("<Enter>", lambda event, b=adv_button: b.config(bg=highlight_hover_color))
adv_button.bind("<Leave>", lambda event, b=adv_button: b.config(bg=button_color))

# Дополнительные функции
adv_frame = tk.Frame(root, bg=bg_color)

adv_buttons = [
    'sin', 'cos', 'tan', 'x^y', 'sqrt',
    'lg', 'ln', 'x!', 'π', 'abs'
]

for i, btn in enumerate(adv_buttons):
    action = lambda x=btn: adv_click(x)
    b = tk.Button(adv_frame, text=btn, font=("Arial", 18), bg=button_color, fg=fg_color,
                  activebackground=highlight_color, command=action)
    b.grid(row=(i // 5) + 1, column=i % 5, sticky="nsew", padx=5, pady=5)
    b.bind("<Enter>", lambda event, b=b: b.config(bg=highlight_hover_color))
    b.bind("<Leave>", lambda event, b=b: b.config(bg=button_color))

# Настройка размеров сетки
for i in range(5):
    root.grid_columnconfigure(i, weight=1)
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    adv_frame.grid_columnconfigure(i, weight=1)
for i in range(3):
    adv_frame.grid_rowconfigure(i, weight=1)

adv_frame.grid(row=7, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
adv_frame.grid_remove()

root.mainloop()
