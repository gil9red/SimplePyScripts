while True:
    options = input("Enter 'add', 'substract','multiply',divide','quit',power")

    if options == 'quit':
        break
    elif options == 'add':
        x = int(input("Enter 1st num"))
        y = int(input("Enter 2nd num"))
        print(x + y)
    elif options == 'substract':
        x = int(input("Enter 1st num"))
        y = int(input("Enter 2nd num"))
        print(x - y)
    elif options == 'multiply':
        x = int(input("Enter 1st num"))
        y = int(input("Enter 2nd num"))
        print(x * y)
    elif options == 'divide':
        x = int(input("Enter 1st num"))
        y = int(input("Enter 2nd num"))
        print(x / y)
    elif options == 'power':
        x = int(input("Enter Enter the base"))
        y = int(input("Enter the exponent"))
        print(x ** y)
    else:
        print("ma error")
print("look i am out the loop")