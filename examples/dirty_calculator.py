import math

def calc(a,b,op):
    if op == "add":
        return a+b
    elif op == "sub":
        return a-b
    elif op == "mul":
        return a*b
    elif op == "div":
        if b == 0:
            print("cant divide by zero!!")
            return None
        return a/b
    elif op == "pow":
        return a**b
    elif op == "sqrt":
        if a < 0:
            print("no negative sqrt")
            return None
        return math.sqrt(a)
    elif op == "mod":
        if b == 0:
            print("cant mod by zero")
            return None
        return a % b
    else:
        print("unknown op")
        return None

# quick test
if __name__ == "__main__":
    x = calc(10, 5, "add")
    print(x)
    y = calc(10, 0, "div")
    print(y)
    z = calc(25, 0, "sqrt")
    print(z)
    w = calc(2, 10, "pow")
    print(w)
    print(calc(10, 3, "mod"))
    print(calc(1, 1, "nope"))
