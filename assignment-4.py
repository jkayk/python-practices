playing = True

while playing:
    first_number = int(input("Choose a number: " ))
    second_number = int(input("Choose another one: "))
    operation = input('''Choose an operation:
    Options are: +, -, * or /
    Write 'exit' to finish. 
''')
    if operation == "exit":
        playing = False
    elif operation == "+":
        result = first_number + second_number
        print(result)
    elif operation == "-":
        result = first_number - second_number
        print(result)
    elif operation == "*":
        result = first_number * second_number
        print(result)
    elif operation == "/":
        result = first_number / second_number
        print(result)