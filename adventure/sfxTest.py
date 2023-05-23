from time import sleep
import winsound

# Musical notes list (-21 to 74)


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
            winsound.Beep(self.notes[-9], 80)
            winsound.Beep(self.notes[-10], 80)
        if sound == 'useItem':
            winsound.Beep(self.notes[3], 80)
            winsound.Beep(self.notes[19], 80)
            winsound.Beep(self.notes[30], 80)
        if sound == 'foundItem':
            winsound.Beep(self.notes[21], 90)
            winsound.Beep(self.notes[24], 600)


sfx = Sfx()

while True:
    userInput = input("Test sound: ")
    sfx.play(userInput)
    if userInput == 'exit':
        break
