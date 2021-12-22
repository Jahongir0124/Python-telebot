#Calculator for brother

while True:
    a = int(input('Введите первой число:'))
    b = int(input('Введите второе число:'))

    #Действий +,-,*,/

    c = input('Выбрайте действию...')

    if c == "+":
        print("Rezultat",a+b)
    if c == "-":
        print("Rezultat",a-b)
    if c == "*":
        print("Rezultat",a*b)
    if c == "/":
        print("Rezultat",a/b)
