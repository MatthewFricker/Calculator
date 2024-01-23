from tkinter import *
import math

root = Tk()
root.title("Calculator")

e = Entry(root, width=65, borderwidth=5)
e.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(number))

def clear():
    e.delete(0, END)

def calculate():
    question = e.get()
    if not e.get():
        return
    try:
        tokens = getTokens(question)
    except ValueError:
        e.delete(0, END)
        e.insert(0, "Syntax Error")
        return
    rpn = getRPN(tokens)
    try:
        answer = solveRPN(rpn)
    except ValueError:
        e.delete(0, END)
        e.insert(0, "Syntax Error")
        return
    except ZeroDivisionError:
        e.delete(0, END)
        e.insert(0, "Math Error")
        return
    e.delete(0, END)
    if math.floor(answer) == answer:
        answer = int(answer)
    e.insert(0, str(answer))

def getTokens(s: str):
    tokens = []
    i = 0
    while i < len(s):
        if s[i] == " ":
            i += 1
        elif s[i] in "+-*/()":
            if s[i] == "-":
                if i == 0 or tokens[-1] == "(":
                    tokens.append("0")
            tokens.append(s[i])
            i += 1
        elif s[i].isdigit() or s[i] == ".":
            number = ""
            while i < len(s) and (s[i].isdigit() or s[i] == "."):
                number += s[i]
                i += 1
            tokens.append(number)
        else:
            raise ValueError
    return tokens

def getRPN(tokens: list):
    priority = {"/":2,"*":2,"-":1,"+":1,"(":0,")":0}
    stack = []
    res = []
    for item in tokens:
        if item == "(":
            stack.append(item)
        elif item == ")":
            while stack[-1] != "(":
                res.append(stack.pop())
            stack.pop()
        elif item in "/*+-":
            while stack and priority[stack[-1]] >= priority[item]:
                res.append(stack.pop())
            stack.append(item)
        else:
            res.append(item)
    while stack:
        res.append(stack.pop())
    return res

def solveRPN(RPN: list):
    stack = []
    for item in RPN:
        if item in "+-*/":
            try:
                x = stack.pop()
                y = stack.pop()
            except:
                raise ValueError
            if item == "+":
                stack.append(x+y)
            elif item == "-":
                stack.append(y-x)
            elif item == "*":
                stack.append(x*y)
            elif item == "/":
                if x == 0:
                    raise ZeroDivisionError
                stack.append(y/x)
        else:
            stack.append(float(item))
    return stack.pop()

button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1)).grid(row=3, column=0)
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2)).grid(row=3, column=1)
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3)).grid(row=3, column=2)
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4)).grid(row=2, column=0)
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5)).grid(row=2, column=1)
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6)).grid(row=2, column=2)
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7)).grid(row=1, column=0)
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8)).grid(row=1, column=1)
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9)).grid(row=1, column=2)
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0)).grid(row=4, column=0)
button_add = Button(root, text="+", padx=50, pady=20, command=lambda: button_click("+")).grid(row=1, column=3)
button_subtract = Button(root, text="-", padx=50, pady=20, command=lambda: button_click("-")).grid(row=2, column=3)
button_multiply = Button(root, text="*", padx=50, pady=20, command=lambda: button_click("*")).grid(row=3, column=3)
button_divide = Button(root, text="/", padx=50, pady=20, command=lambda: button_click("/")).grid(row=4, column=3)
button_open_bracket = Button(root, text="(", padx=50, pady=20, command=lambda: button_click("(")).grid(row=2, column=4)
button_close_bracket = Button(root, text=")", padx=50, pady=20, command=lambda: button_click(")")).grid(row=3, column=4)
button_point = Button(root, text=".", padx=50, pady=20, command=lambda: button_click(".")).grid(row=4, column=4)
button_eq = Button(root, text="=", padx=90, pady=20, command=calculate).grid(row=4, column=1, columnspan=2)
button_clear = Button(root, text="Clear", padx=40, pady=20, command=clear).grid(row=1, column=4)


root.mainloop()

