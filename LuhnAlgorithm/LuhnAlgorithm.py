# coding=utf-8

__author__ = "ipetrash"

if __name__ == "__main__":
    number_card = input("Number card: ")
    sum = 0
    digits = [int(x) for x in number_card if x.isdigit()]
    digits.reverse()
    for i in range(len(digits)):
        p = digits[i]
        if i % 2 is not 0:
            p *= 2
            if p > 9:
                p -= 9
        sum += p

    print(f"sum: {sum}")
    sum = 10 - (sum % 10)
    sum = 0 if sum is 10 else sum

    print(f"checksum: {sum}")
    print("card number is correct" if (sum % 10 is 0) else "card number is incorrect")
