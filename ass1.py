# # E-commerce Checkout System

# # Multiple variable assignment
# discount, tax_rate = 5.00, 0.08

# # Read input from the user
# price = float(input("Enter item price: $"))
# quantity = int(input("Enter quantity: "))

# # Calculate subtotal
# subtotal = price * quantity

# # Apply flat discount
# discounted_amount = subtotal - discount

# # Calculate tax
# tax = discounted_amount * tax_rate

# # Calculate total payable
# total = discounted_amount + tax

# # Multi-line log output using triple quotes
# print(f"""
# ========== E-COMMERCE CHECKOUT ==========
# Item Price       : ${price:.2f}
# Quantity         : {quantity}
# Subtotal         : ${subtotal:.2f}
# Discount         : ${discount:.2f}
# Tax (8%)         : ${tax:.2f}
# Total Payable    : ${total:.2f}
# =========================================
# """)

# Smart Security Door Authentication

# Secret authentication details
# SECRET_KEY = 1234
# ACTIVE_BADGES = ["RFID101", "RFID202", "RFID303"]

# # Permission flags using bitwise operators
# READ_PERMISSION = 1      # 001
# WRITE_PERMISSION = 2     # 010
# ADMIN_PERMISSION = 4     # 100

# # User input
# try:
#     passcode = int(input("Enter numeric passcode: "))
# except ValueError:
#     passcode = -1

# badge_id = str(input("Enter RFID badge ID: ")).strip().upper()
# role = str(input("Enter your role: ")).strip().upper()

# # Bitwise permission flag
# # Example: READ + WRITE permission = 1 | 2 = 3
# user_permissions = READ_PERMISSION | WRITE_PERMISSION

# # Authentication conditions
# passcode_match = (passcode == SECRET_KEY)
# badge_valid = (badge_id in ACTIVE_BADGES)
# role_allowed = (role is not "GUEST")   # Identity operator

# # Bitwise check: verify READ permission exists
# has_read_permission = (user_permissions & READ_PERMISSION) != 0

# # Final decision using logical AND
# unlock = (
#     passcode_match
#     and badge_valid
#     and role_allowed
#     and has_read_permission
# )

# # Output boolean decision
# print("\nAuthentication Result:")
# print("Passcode Match:", passcode_match)
# print("Valid Badge:", badge_valid)
# print("Role Allowed:", role_allowed)
# print("Read Permission:", has_read_permission)
# print("Unlock:", bool(unlock))

# # Character Frequency Counter

# text = input("Enter a string: ").strip().lower()

# frequency = {}

# for char in text:
#     if char in frequency:
#         frequency[char] += 1
#     else:
#         frequency[char] = 1
   
# print("\nCharacter Frequency:")

# for char, count in frequency.items():
#     print(char, ":", count)

# list1 = [1,2,2,3,4]
# list2 = [2,3,3,5]
# set1 = set(list1)
# set2 = set(list2)
# intersection = set1.intersection(set2)
# common=set1 & set2
# print("common elements:",common)

# def twin_prime_decorator(func):
#     def wrapper(n):
#         result = func(n)

#         print("Twin Prime Numbers:")
#         for a, b in result:
#             print(a, b)

#     return wrapper


# def is_prime(n):
#     if n < 2:
#         return False

#     for i in range(2, n):
#         if n % i == 0:
#             return False

#     return True


# @twin_prime_decorator
# def twin_primes(n):
#     pairs = []

#     for i in range(2, n):
#         if is_prime(i) and is_prime(i + 2):
#             pairs.append((i, i + 2))

#     return pairs


# n = int(input("Enter the limit: "))
# twin_primes(n)


# students = {
#     "Avinash": "A",
#     "Rahul": "B",
#     "Kiran": "A",
#     "Priya": "C",
#     "Aman": "B"
# }

# inverted = {}

# for name, grade in students.items():
#     if grade not in inverted:
#         inverted[grade] = []

#     inverted[grade].append(name)

# print("Original Dictionary:")
# print(students)

# print("\nInverted Dictionary:")
# print(inverted)
print("ଓଡ଼ିଆ")
print("Hello")