#1 personal introduction program
name = input("What is your name?")
age = int(input("What is your age?"))
hobby = input("What is your hobby?")
print("Hello, my name is", name, "and I am", age, "years old.My hobby is", hobby, ".")

#2 Simple calculator program
num1 = float(input("Enter a number: "))
num2 = float(input("Enter another number: "))
print("The sum of", num1, "and", num2, "is", num1 + num2)
print("The difference of", num1, "and", num2, "is", num1 - num2)
print("The product of", num1, "and", num2, "is", num1 * num2)
if num2 != 0:
    print("The quotient of", num1, "and", num2, "is", num1 / num2)

#3 Age calculator program
year = int(input("Enter your birth year: "))
current_year = int(input("Enter the current year: "))
age = current_year - year
print("You are", age, "years old.")

#4 Temperature converter program
celsiustemp = float(input("Enter temperature in Celsius: "))
fahrenheittemp = (celsiustemp * 9/5) + 32
print("The temperature in Fahrenheit is:", fahrenheittemp)

#5 Mini bill calculator program
pen = float(input("Enter the number of pens you bought: "))
book = float(input("Enter the number of books you bought: "))
pen_price = 1.5
book_price = 5.0
total_cost = (pen * pen_price) + (book * book_price)
print("The total cost of your purchase is: $", total_cost)

#6 Simple interest calculator program
food = float(input("Enter the amount you spent on food: "))
transport = float(input("Enter the amount you spent on transport: "))
entertainment = float(input("Enter the amount you spent on entertainment: "))
total_expense = food + transport + entertainment
print("Your total expenses are: $", total_expense)
