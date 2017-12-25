def isprime(n):
    if n == 1:
        print("1 is special.")
    for x in range(2, n):
        if n % x == 0:
            print("{} equals {} x {}".format(n, x, n // x))

    else:
        print(n, "is a prime number.")


inputNumber = int(input("Please enter the number : "))
for n in range(1, inputNumber):
    isprime(n)
