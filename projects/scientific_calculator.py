import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x / y

def power(x, y):
    return math.pow(x, y)

def sqrt(x):
    return math.sqrt(x)

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def log(x):
    if x > 0:
        return math.log(x)
    else:
        return "Error! Logarithm of non-positive number."

def calculator():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Sine")
    print("8. Cosine")
    print("9. Tangent")
    print("10. Logarithm")

    while True:
        choice = input("Enter choice (1/2/3/4/5/6/7/8/9/10): ")

        if choice in ['1', '2', '3', '4', '5']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                if isinstance(result, str):
                    print(result)
                else:
                    print(f"{num1} / {num2} = {result}")
            elif choice == '5':
                print(f"{num1} ^ {num2} = {power(num1, num2)}")

        elif choice in ['6', '7', '8', '9', '10']:
            try:
                num = float(input("Enter number: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == '6':
                print(f"sqrt({num}) = {sqrt(num)}")
            elif choice == '7':
                print(f"sin({num}) = {sin(num)}")
            elif choice == '8':
                print(f"cos({num}) = {cos(num)}")
            elif choice == '9':
                print(f"tan({num}) = {tan(num)}")
            elif choice == '10':
                result = log(num)
                if isinstance(result, str):
                    print(result)
                else:
                    print(f"log({num}) = {result}")

        else:
            print("Invalid Input")

        next_calculation = input("Do you want to perform another calculation? (y/n): ")
        if next_calculation.lower() != 'y':
            break

if __name__ == "__main__":
    calculator()
