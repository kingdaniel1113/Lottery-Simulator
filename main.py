import random
import os

powerPlay = 1



def main():

    options = ['help [option]', 'accuracyByVolume', 'setOutcome', 'exit']
    userInput = input(f'What would you like to do? \nOptions: {options}\n')
    os.system('cls')

    if userInput == 'help accuracyByVolume':
        print(f'accuracyByVolume option runs accuracyByVolume simulation')
        print(f'accuracyByVolume compares a set list of tickets (quantity set by user) against one winning number.\nAll numbers are distributed evenly between tickets\n')
        input('Press enter to continue...')
        os.system('cls')
        main()
    elif userInput == 'help setOutcome':
        print(f'option setOutcome runs setOutcome simulation')
        print('setOutcome buys one ticket and compares it to the same winning number each time.\n')
        input('Press enter to continue...')
        os.system('cls')
        main()
    elif userInput == 'accuracyByVolume':
        accuracyByVolume()
    elif userInput == 'setOutcome':
        setOutcome()
    elif userInput == 'help help':
        print('help displays a brief description of other options')
    elif userInput == 'exit':
        quit()
    else:
        print('unknown command. Please try again')
        input('Press enter to continue...')
        os.system('cls')
        main()
    




def accuracyByVolume():
    Player = player()
    Lottery = lottery()
    ticks = 0
    printSpeed = 10000
    numberUsage = {}
    for i in range(1, 70):
        numberUsage[i] = 0
    currentPowerball = 1
    while len(Player.numbers) < 26*69:
        temp = []
        while len(temp) < 5:
            number = random.choice([j for j in numberUsage if numberUsage[j]==min(numberUsage.values())])
            if number in temp:
                continue
            numberUsage[number] += 1
            temp.append(number)
        temp.sort()
        temp.append(currentPowerball)
        if temp not in Player.numbers:
            Player.numbers.append(temp)
            currentPowerball = (currentPowerball % 26) + 1
        else:
            for i in range(5):
                numberUsage[temp[i]] += 1
    while Player.balance > 0:
        ticks += 1
        Lottery.generateWinningNumbers()
        for i in Player.numbers:
            Player.balance -= 2
            Player.invested += 2
            a,b, payout = compareNumbers(i[0:5], Lottery.winningNumbers, i[-1], Lottery.powerball)
            if payout == 'jackpot':
                print("JACKPOT")
                print(Player.numbers, Lottery.winningNumbers)
                Player.stats()
                payout = Lottery.balance
                distributeFunds(payout, Player, Lottery)
                break
            distributeFunds(payout, Player, Lottery)

        if ticks % printSpeed == 0:
            os.system('cls')
            Player.stats()

    os.system('cls')
    Player.stats()
    print('You ran out of money!')
    main()




def setOutcome():
    """Buys 1 ticket every cycle and compares it to a set outcome. Not profitable"""
    Player = player()
    Lottery = lottery()
    printSpeed = 100000
    tick = 0
    startingBalance = 1000000000
    Lottery.winningNumbers = [9,35, 54, 63, 64]
    Lottery.powerball = 1
    while Player.balance > 0:
        tick += 1
        if Lottery.balance > 1600000000:
            Lottery.balance = startingBalance
        Player.generateNumbers()
        matching, powerball, payout = compareNumbers(Player.numbers, Lottery.winningNumbers, Player.powerball, Lottery.powerball)
        if payout == 'jackpot':
            payout = Lottery.balance
            Lottery.balance = startingBalance
            print('JACKPOT')
            print(f'Payout(total): {Lottery.balance}')
            print(f'Payout (after tax): {Lottery.balance * .40}')
            Player.stats()
            print()
            input('Press enter to continue')
            print(Player.invested, Player.earned, Player.earned, Player.invested)
            print()

        distributeFunds(payout, Player, Lottery)

        Lottery.balance += Lottery.balance * .0845

        if tick % printSpeed == 0:
            print(Lottery.winningNumbers, Lottery.powerball)
            print(Player.numbers, Player.powerball)
            Player.stats()

def compareNumbers(playerNumbers, lotteryNumbers, playerPowerball, lotteryPowerball):
    
        matching = 0
        for i in lotteryNumbers:
            if i in playerNumbers:
                matching += 1 
        if lotteryPowerball == playerPowerball:
            powerball = True
        else:
            powerball = False

        if powerball and matching == 5:
            return [matching, powerball, 'jackpot']
        elif matching == 5:
            return [matching, powerball, 1000000]
        elif powerball and matching == 4:
            return [matching, powerball, 50000]
        elif matching == 4:
            return [matching, powerball, 100]
        elif powerball and matching == 3:
            return [matching, powerball, 100]
        elif matching == 3:
            return [matching, powerball, 7]
        elif powerball and matching == 2:
            return [matching, powerball, 7]
        elif powerball and matching == 1:
            return [matching, powerball, 4]
        elif powerball:
            return [matching, powerball, 4]
        else:
            return [matching, powerball, 0]

def distributeFunds(payout, Player, Lottery):
    global powerPlay
    if payout < 5000:
        Player.earned += payout * powerPlay
        Player.balance += payout * powerPlay
        Lottery.balance -= payout * powerPlay
    else:
        if payout == 1000000:
            if powerPlay >= 2:
                balanceChange = payout * powerPlay
                Player.earned += balanceChange * 40
                Player.balance += balanceChange * 40
                Lottery.balance -= balanceChange
                return
            
        Player.earned += payout * .40
        Player.balance += payout * .40
        Lottery.balance -= payout

class lottery():
    def __init__(self):
        self.winningNumbers = []
        self.balance = 5000000
        self.powerball = 0


    def generateWinningNumbers(self):
        self.winningNumbers = []
        while len(self.winningNumbers) < 5:
            pass
            number = random.randrange(1,70)
            if number not in self.winningNumbers:
                self.winningNumbers.append(number)

        self.powerball = random.randrange(1, 27)


class player():
    def __init__(self):
        self.balance = 1000000000000
        self.numbers = []
        self.powerball = 0
        self.earned = 0
        self.invested = 0
    
    def stats(self):
        os.system('cls')
        tracking= {
            'Invested Cash': self.invested,
            'Earned Cash': self.earned,
            'P/L': self.earned - self.invested,
            'Balance': self.balance,
            }
        
        for key in tracking.keys():
            print(f'{key}: {round(tracking[key], 2):,}')
            

    def generateNumbers(self):
        self.invested += 2
        self.balance -= 2
        self.numbers = []
        while len(self.numbers) < 5:
            number = random.randrange(1,70)
            if number not in self.numbers:
                self.numbers.append(number)
        self.powerball = random.randrange(1,27)
        self.numbers.sort()

    def formatNumbers(self, number):
        number = str(number)
        number = list(number)

        for i in range(len(number), 0, -1):
            if i%3 == 0:
                number.insert(i - 1, ',')


        number = ''.join(number)
        return number



while True:
    main()