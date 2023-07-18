# Single line comment
'''
Line 1 comment
Line 2 comment
'''

# Some operations
1 + 2
print(1 + 2)

# Work with variables
sum_var = 1 + 2
print(sum_var)
print("The sum of the 2 numbers is " + str(sum_var))
# Same but using fString
print(f"The sum of the 2 numbers is {sum_var}")


# Usual way of doing repeated operations
# 1. Importing libraries
# 2. Defining variables
n1 = 1
n2 = 2
# 3. Defining functions
def add2numbers(number1, number2):
    numbers_sum = number1 + number2
    return numbers_sum

# 4. Type the main code
n_sum = add2numbers(n1, n2)
print(f"The sum of {n1} and {n2} is {n_sum}")

# Other way
# 1. Importing libraries
# 2. Defining variables
n1 = 1
n2 = 2
# 3. Defining functions
def print2numberssum(number1, number2):
    numbers_sum = number1 + number2
    print(f"The sum of {number1} and {number2} is {numbers_sum}")
    return

# 4. Type the main code
print2numberssum(n1, n2)