def rlog(x):
    if x > 0.5 and x < 0.9:
        re = 5

    elif x <= 0.5:
        re = 1

    else:
        re = int(round(10 ** x, -1))

    return int(re)

# y = rlog(0.9)
# print(y)