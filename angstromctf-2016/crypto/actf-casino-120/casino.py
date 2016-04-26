#seed = xxxx
#flag = "REDACTED"

import random,time

random.seed(seed+time.time())

money = 100

print("Welcome to the angstromCTF casino, where luck rules supreme.")
print("The way the game works is that you specify a range, your guess for the number that the RNG chooses, and your wager.")
print("If your guess is correct you win (upper_bounds - lower_bounds) * wager dollars.")
print("As a token of appreciation for play our CTF we will give you 100 dollars to start off.")
print("If you win 1,000,000,000 you get the flag. Good luck.")
while money > 0:
    print("You have", money, "dollars")
    lower = int(input("Your lower bound for the range: "))
    upper = int(input("Your upper bound for the range: "))
    guess = int(input("Your guess: "))
    wager = int(input("Your wager: "))

    if wager > money:
        print("your wager was too high\n")
        continue
    if wager < 0:
        print("your wager was negative\n")
        continue
    if lower > upper:
        print("lower bounds must be less than upper bound\n")
        continue
    
    money -= wager
    
    num = random.randint(lower,upper)
    if num == guess:
        print("You guessed the right answer, you got", (upper-lower)*wager, "dollars")
        money += (upper-lower)*wager
    else:
        print("The correct number was", num)

    print()

    if money > 1000000000:
        print(flag)

print("You lose, better luck next time.")
