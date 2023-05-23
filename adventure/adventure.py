import os
from random import randint
from time import sleep
import winsound


DAYS = 1
INFLATION = 1
HIGHSCORE = 0


class Sfx():
    def __init__(self, tuning=440, rangeStart=-21, rangeEnd=75):
        self.tuning = tuning
        self.mod = 1.059463094359
        self.notes = {}
        for i in range(rangeStart, rangeEnd):
            self.notes[i] = round(self.tuning * self.mod ** i)

    def play(self, sound):
        if sound == 'intro':
            winsound.Beep(self.notes[11], 175)
            winsound.Beep(self.notes[9], 175)
            winsound.Beep(self.notes[8], 700)
        if sound == 'gameOver':
            sleep(0.4)
            winsound.Beep(self.notes[19], 200)
            winsound.Beep(self.notes[18], 80)
            winsound.Beep(self.notes[18], 800)
            sleep(1.3)
        if sound == 'newDay':
            winsound.Beep(self.notes[-9 + DAYS], 80)
            winsound.Beep(self.notes[-10 + DAYS], 80)
        if sound == 'useItem':
            winsound.Beep(self.notes[3], 80)
            winsound.Beep(self.notes[19], 80)
            winsound.Beep(self.notes[30], 80)
        if sound == 'foundItem':
            winsound.Beep(self.notes[21], 90)
            winsound.Beep(self.notes[24], 600)


sfx = Sfx()


class Player():
    def __init__(self):
        self.inv = []
        self.gold = 0
        self.hunger = 0  # Die if this reaches 7
        self.thirst = 0  # Die if this reaches 3

    # Buy/Eat food
    def eat(self):
        if self.hunger <= 0:
            print("You are not hungry")
            return False
        elif self.gold >= foodCost:
            self.gold = self.gold - foodCost
            self.hunger = self.hunger - 2
            return True
        else:
            print("\nYou do not have enough money!\n")
            return False

    # Buy/Drink
    def drink(self):
        if self.thirst <= 0:
            print("You are not thirsty")
            return False
        elif self.gold >= drinkCost:
            self.gold = self.gold - drinkCost
            self.thirst = self.thirst - 2
            return True
        else:
            print("\nYou do not have enough money!\n")
            return False

    def use(self, item):
        if item in self.inv:
            item.effect(self)
            self.inv.remove(item)
            sfx.play('useItem')

    # Reset PLayer
    def reset(self):
        self.inv = []
        self.gold = 0
        self.hunger = 0
        self.thirst = 0


class Item():
    def __init__(self, name, value, desc):
        self.name = name
        self.value = value
        self.desc = desc

    def effect(self, user):
        if self.name == "Magic Fruit":
            user.hunger = -1
            user.thirst = -1
        elif self.name == "Water Bottle":
            user.thirst = -1
        elif self.name == "Sandwich":
            user.hunger = -1
        elif self.name == "Gold Coin":
            user.gold = user.gold + (self.value * INFLATION) - self.value


p = Player()


def printStats(p, hs=None):
    sleep(0.2)
    print("ʭ"*42)
    sleep(0.2)
    sfx.play('newDay')
    print("\n")
    print(f"        ⋦DAY {DAYS}⋩        ", end='')
    if DAYS > hs:
        print("   NEW HIGH SCORE")
    else:
        print("\n")
    print(f"  Inflation rate is {INFLATION}")
    print(f"  • You have {p.gold} gold.")
    if p.inv:
        print(f"  • Inventory: ")
        for i in range(len(p.inv)):
            print(f" {i+1}. {p.inv[i].name}   -   {p.inv[i].desc}")
    print(
        f"  • Your hunger level is {p.hunger}.    Your thirst level is {p.thirst}.")


def choose(choice):
    if choice == "a":
        return randint(0, 2)
    elif choice == "b":
        return randint(-2, 5)
    elif choice == "c":
        return randint(-6, 10)


def printIntro(p):
    os.system('cls')
    print("         #########################")
    print("         | Welcome to Adventure! |")
    print("         #########################\n")
    sfx.play('intro')
    sleep(0.5)
    print("The object of Adventure is to survive as many days as possible.")
    sleep(0.2)
    print("You can survive until either your hunger reaches 7, or your thirst reaches 3.")
    sleep(0.2)
    print("Each choice you make takes one day.")
    print("Everything comes at a price, so choose wisely!\n")
    sleep(0.55)
    p.name = input("Enter your name: ")
    print(f"Hello {p.name}")
    if p.name == '$':
        p.gold = 1000
    print("\n")


def playGame(p):

    while p.hunger < 7 and p.thirst < 3:
        global INFLATION, DAYS, foodCost, drinkCost, HIGHSCORE
        drinkCost = 1 * INFLATION
        foodCost = 2 * INFLATION

        # printStats(p)

        if DAYS % 5 == 0:
            itemRoll = randint(0, 4)
            if itemRoll > 0:
                print("\n    *** You found an item!! ***\n")
                sfx.play('foundItem')

            if itemRoll == 1:
                p.inv.append(
                    Item("Magic Fruit", 10, "Hunger and thirst reset to 0. Takes 1 day."))
            elif itemRoll == 2:
                p.inv.append(
                    Item("Water Bottle", 2, "Satisfies thirst in no time."))
            elif itemRoll == 3:
                p.inv.append(
                    Item("Sandwich", 3, "Satisfies hunger in no time."))
            elif itemRoll == 4:
                p.inv.append(
                    Item("Gold Coin", 5, f"Valuable currency. Trade instantly for {5 * INFLATION} gold"))
            else:
                print("   Nothing found...\n")

        printStats(p, HIGHSCORE)

        if DAYS % 5 == 0:
            INFLATION = INFLATION + 1

        print("\nYour options are:")
        print(" • A (low risk)")
        print(" • B (some risk)")
        print(" • C (big risk)")
        print(f" • Drink (costs {drinkCost} gold)")
        print(f" • Eat (costs {foodCost} gold)")
        if len(p.inv):
            print(f" • Use Item #")

        while True:
            endDay = False
            choice = input("\nEnter choice: ").lower()
            print("\n")
            if choice == "a":
                p.gold = p.gold + choose(choice)
                endDay = True
            elif choice == "b":
                p.gold = p.gold + choose(choice)
                endDay = True
            elif choice == "c":
                p.gold = p.gold + choose(choice)
                endDay = True
            elif choice == "drink" or choice == "d":
                endDay = p.drink()
            elif choice == "eat" or choice == "e":
                endDay = p.eat()
            # If player has inventory
            elif len(p.inv):
                for i in range(len(p.inv)):
                    if choice == str(i+1):
                        print(f"You used {p.inv[i].name}\n")
                        if p.inv[i].name == "Magic Fruit":
                            endDay = True
                        p.use(p.inv[i])
            else:
                print("Please enter A, B, C, (D)rink or (E)at")
            if endDay:
                break

        DAYS = DAYS + 1
        p.hunger = p.hunger + 1
        p.thirst = p.thirst + 1

    HIGHSCORE = DAYS if DAYS > HIGHSCORE else HIGHSCORE

    if p.thirst >= 3 and p.hunger >= 7:
        sfx.play('gameOver')
        print("\n\nYou died of hunger and thirst...",
              f" You lasted {DAYS} days\n\n")
    elif p.thirst >= 3:
        sfx.play('gameOver')
        print("\n\nYou died of thirst...", f" You lasted {DAYS} days\n\n")
    elif p.hunger >= 7:
        sfx.play('gameOver')
        print("\n\nYou died of hunger...", f" You lasted {DAYS} days\n\n")

    print("Would you like to play again?\n")
    anotherRound = input("Y or N: ").lower()
    if anotherRound == "y" or anotherRound == "yes":
        DAYS = 1
        INFLATION = 1
        p.reset()
        print("\n\n\n")
        playGame(p)


printIntro(p)
playGame(p)


print("Thanks for playing!")
sleep(1.5)
