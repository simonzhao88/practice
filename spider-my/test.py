

def fib(n):
    a, b = 0, 1
    print(a, end=' ')
    for i in range(n):
        a, b = b, a+b
        print(a, end=' ')


fib(10)
