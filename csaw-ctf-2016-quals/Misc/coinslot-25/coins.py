import random
import sys

class CoinSlot:
    def __init__(self, max_cents):
        self.cents = random.randint(1, max_cents)

    def get_input(self):
        print("$10,000 bills: ", end = "")
        self.d10000 = int(input())
        print("$5,000 bills: ", end = "")
        self.d5000 = int(input())
        print("$1,000 bills: ", end = "")
        self.d1000 = int(input())
        print("$500 bills: ", end = "")
        self.d500 = int(input())
        print("$100 bills: ", end = "")
        self.d100 = int(input())
        print("$50 bills: ", end = "")
        self.d50 = int(input())
        print("$20 bills: ", end = "")
        self.d20 = int(input())
        print("$10 bills: ", end = "")
        self.d10 = int(input())
        print("$5 bills: ", end = "")
        self.d5 = int(input())
        print("$1 bills: ", end = "")
        self.d1 = int(input())
        print("half-dollars (50c): ", end = "")
        self.c50 = int(input())
        print("quarters (25c): ", end = "")
        self.c25 = int(input())
        print("dimes (10c): ", end = "")
        self.c10 = int(input())
        print("nickels (5c): ", end = "")
        self.c5 = int(input())
        print("pennies (1c): ", end = "")
        self.c1 = int(input())

    def solution(self):
        cents = self.cents
        d10000 = int(cents / 1000000)
        cents -= d10000 * 1000000

        d5000 = int(cents / 500000)
        cents -= d5000 * 500000

        d1000 = int(cents / 100000)
        cents -= d1000 * 100000

        d500 = int(cents / 50000)
        cents -= d500 * 50000

        d100 = int(cents / 10000)
        cents -= d100 * 10000

        d50 = int(cents / 5000)
        cents -= d50 * 5000

        d20 = int(cents / 2000)
        cents -= d20 * 2000

        d10 = int(cents / 1000)
        cents -= d10 * 1000

        d5 = int(cents / 500)
        cents -= d5 * 500

        d1 = int(cents / 100)
        cents -= d1 * 100

        c50 = int(cents / 50)
        cents -= c50 * 50

        c25 = int(cents / 25)
        cents -= c25 * 25

        c10 = int(cents / 10)
        cents -= c10 * 10

        c5 = int(cents / 5)
        cents -= c5 * 5

        c1 = cents

        answer = self.cents
        if answer == self.cents:
            if d10000 != self.d10000:
                print("Incorrect number of $10,000 bills: expected {}, \
found {}".format(d10000, self.d10000))
                sys.exit(1)
            elif d5000 != self.d5000:
                print("Incorrect number of $5,000 bills: expected {}, \
found {}".format(d5000, self.d5000))
                sys.exit(1)
            elif d1000 != self.d1000:
                print("Incorrect number of $1,000 bills: expected {}, \
found {}".format(d1000, self.d1000))
                sys.exit(1)
            elif d500 != self.d500:
                print("Incorrect number of $500 bills: expected {}, \
found {}".format(d500, self.d500))
                sys.exit(1)
            elif d100 != self.d100:
                print("Incorrect number of $100 bills: expected {}, \
found {}".format(d100, self.d100))
                sys.exit(1)
            elif d50 != self.d50:
                print("Incorrect number of $50 bills: expected {}, \
found {}".format(d50, self.d50))
                sys.exit(1)
            elif d20 != self.d20:
                print("Incorrect number of $20 bills: expected {}, \
found {}".format(d20, self.d20))
                sys.exit(1)
            elif d10 != self.d10:
                print("Incorrect number of $10 bills: expected {}, \
found {}".format(d10, self.d10))
                sys.exit(1)
            elif d5 != self.d5:
                print("Incorrect number of $5 bills: expected {}, \
found {}".format(d5, self.d5))
                sys.exit(1)
            elif d1 != self.d1:
                print("Incorrect number of $1 bills: expected {}, \
found {}".format(d1, self.d1))
                sys.exit(1)
            elif c50 != self.c50:
                print("Incorrect number of half-dollars (50c): expected {}, \
found {}".format(c50, self.c50))
                sys.exit(1)
            elif c25 != self.c25:
                print("Incorrect number of quarters (25c): expected {}, \
found {}".format(c25, self.c25))
                sys.exit(1)
            elif c10 != self.c10:
                print("Incorrect number of dimes (10c): expected {}, \
found {}".format(c10, self.c10))
                sys.exit(1)
            elif c5 != self.c5:
                print("Incorrect number of nickels (5c): expected {}, \
found {}".format(c5, self.c5))
                sys.exit(1)
            elif c1 != self.c1:
                print("Incorrect number of pennies (1c): expected {}, \
found {}".format(c1, self.c1))
                sys.exit(1)
            else:
                print("correct!")
        else:
            print("incorrect, sorry :(")
            given = str(answer)
            expected = str(self)
            print("(answer given was {}, answer expected was {})".format(given,
                expected))
            sys.exit(1)

    def __str__(self):
        return "${}.{:0>2}".format(int(self.cents / 100), self.cents % 100)


def main():
    random.seed()
    max_cent_lst = [10**1, 10**3, 10**5, 10**7];
    for max_cents in max_cent_lst:
        for _ in range(0, 100):
            coinslot = CoinSlot(max_cents)
            print(coinslot)
            coinslot.get_input()
            coinslot.solution()
    flag = open("flag.txt", 'r')
    print(flag.read())
    flag.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
