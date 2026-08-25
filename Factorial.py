
#  FACTORIAL NUMBER

n = int(input("Enter number: "))
fact = 1

for i in range(1, n + 1):
    fact = fact * i

print("Factorial =", fact)











# ================================
# 12. REVERSE A STRING
# ================================

text = input("Enter string: ")

print("Reversed String =", text[::-1])


# ================================
# 13. COUNT VOWELS
# ================================

text = input("Enter string: ").lower()

count = 0

for ch in text:
    if ch in "aeiou":
        count += 1

print("Total vowels =", count)


# ================================
# 14. SIMPLE GUI CALCULATOR
# ================================

from tkinter import *

def add():
    result.set(int(e1.get()) + int(e2.get()))

root = Tk()
root.title("Calculator")

Label(root, text="First Number").grid(row=0)
Label(root, text="Second Number").grid(row=1)

e1 = Entry(root)
e2 = Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

result = StringVar()

Button(root, text="Add", command=add).grid(row=2, column=1)

Label(root, textvariable=result).grid(row=3, column=1)

root.mainloop()