end = 1

def print_numbers(end):
    if (end < 0):
        return False
        print("less then zero")
    else:
        count = 1
        print("print all ints to: ", end)
        while (count <= end):
            print(count)
            count = count + 1
print_numbers(3)

p = [1,2]
p.append(3)
p = p + [4,5]
print(p)
print(len(p))