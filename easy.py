def sum_even_numbers(*args):
    total = 0
    for num in args:
        if num % 2 == 0:
            total += num
    return total
print(sum_even_numbers(10,20,30,40,59))
