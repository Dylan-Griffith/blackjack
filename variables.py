from random import choice
from time import sleep
from os import path


class Player:

    def __init__(self, name, money=200):
        self.name = name
        self.money = money
        self.cards = []  # [suit, number]
        self.current_hand = []  # number only
        self.win = 0
        self.high_score = 0
        self.test = []
        self.max_money = 200
        self.bet = 0
        self.load_data()

    def set_up(self, deck):
        self.current_hand = []
        self.cards = []
        self.draw_card(deck)
        self.draw_card(deck)
        self.current_hand = [card[1] for card in self.cards]
        # self.display_cards()

    def draw_card(self, deck, display=False):
        deck.check_deck()
        random_suit = choice(list(deck.cards))
        random_number = choice(deck.cards[random_suit])
        deck.cards[random_suit].remove(random_number)
        self.cards.append([random_suit, random_number])
        self.current_hand.append(random_number)
        if display:
            print('--------------------------------')
            print('{name} draws {number} of {suit}\n'.format(name=self.name, number=random_number, suit=random_suit))
        return random_suit, random_number

    def display_cards(self):
        print('-------------------------')
        print("{name}'s cards are\n".format(name=self.name))
        for card in self.cards:
            if card[1] == 11 or card[1] == 1:
                print('{number} of {suit}'.format(number='Ace', suit=card[0]))
            else:
                print('{number} of {suit}'.format(number=card[1], suit=card[0]))

    def player_bet(self):
        print('You have {money} to bet'.format(money=self.money))
        while True:
            try:
                bet = int(input('what is your bet: '))
            except ValueError:
                print('Bet must be a number!')
            else:
                while bet > self.money:
                    try:
                        bet = int(input('Must bet {} or less: '.format(self.money)))
                    except ValueError:
                        print('Bet must be a number!')
                self.money -= bet
                self.bet = bet
                break
        return bet

    def check_blackjack(self, display=True):
        if len(self.current_hand) == 2:
            if 'Ace' in self.current_hand and 10 in self.current_hand:
                self.current_hand = [21]
                self.win += 1
                self.high_score += 1
                if display:
                    print('BlackJack!\n\nYou win {bet}\n'.format(bet=self.bet * 2))
                    if self.win >= self.high_score:
                        print('New win streak, {streak} games won in a row! '.format(streak=self.high_score))
                print('-------------------------')
                self.money += self.bet * 2
                return False
            elif 'Ace' in self.current_hand and 'Queen' in self.current_hand:
                self.current_hand = [21]
                self.win += 1
                self.high_score += 1
                print('BlackJack!\n\nYou win {bet}\n'.format(bet=self.bet * 2))
                if display:
                    if self.win >= self.high_score:
                        print('New win streak, {streak} games won in a row! '.format(streak=self.high_score))
                print('-------------------------')
                self.money += self.bet * 2
                return False
            elif 'Ace' in self.current_hand and 'King' in self.current_hand:
                self.current_hand = [21]
                self.win += 1
                self.high_score += 1
                if display:
                    print('BlackJack!\n\nYou win {bet}\n'.format(bet=self.bet * 2))
                    if self.win >= self.high_score:
                        print('New win streak, {streak} games won in a row! '.format(streak=self.high_score))
                print('-------------------------')
                self.money += self.bet * 2
                return False
            elif 'Ace' in self.current_hand and 'Jack' in self.current_hand:
                self.current_hand = [21]
                self.win += 1
                self.high_score += 1
                if display:
                    print('BlackJack!\n\nYou win {bet}\n'.format(bet=self.bet * 2))
                    if self.win >= self.high_score:
                        print('New win streak, {streak} games won in a row! '.format(streak=self.high_score))
                print('-------------------------')
                self.money += self.bet * 2
                return False
        return True

    def check_cards(self, deck):
        sleep(2)
        print('-------------------------')
        if len(self.current_hand) == 1:  # Check for one card meaning cards were split
            self.draw_card(deck, display=True)
            if not self.check_blackjack(self.bet):
                return False
        self.current_hand = []
        for number in self.cards:  # sorting cards and evaluating values
            if number[1] == 'Ace':
                continue
            else:
                self.current_hand.append(deck.values[number[1]])
        for number in self.cards:
            if number[1] == 'Ace':
                if sum(self.current_hand) >= 11:
                    self.current_hand.append(deck.values[number[1]][0])
                else:
                    self.display_cards()
                    print('Current total is {total} '.format(total=sum(self.current_hand)))
                    answer = ''
                    while answer != 11 and answer != 1:
                        try:
                            answer = int(input('Would you like your ace to be an 11 or 1? '))
                        except ValueError:
                            print('Must be a number!')
                    number[1] = answer
                    self.clear()
                    sleep(2)
                    self.current_hand.append(answer)
        total = sum(self.current_hand)
        if total == 21:
            self.display_cards()
            print('\nYou have 21\n')
            print('-------------------------')
            sleep(2)
            return False
        elif total > 21:
            print('\nBust!\nYou had {total}\n'.format(total=total))
            print('-------------------------')
            return False
        else:
            self.display_cards()
            print('\nTotaling {total}\n'.format(total=total))
            print('-------------------------')
            return True

    def hit(self, deck):
        if self.money >= self.bet:
            answer = input('Hit or Stand or Double Down  (h/s/dd) \n')
            while answer != 'h' and answer != 's' and answer != 'dd':
                answer = input('Must choose (h) for Hit and (s) for Stand or (dd) for Double Down')
            if answer == 'h':
                self.clear()
                card_suit, card_number = self.draw_card(deck)
                print('{name} draws a'.format(name=self.name))
                print('{number} of {suit}\n'.format(suit=card_suit, number=card_number))
                return True
            elif answer == 'dd':
                self.money -= self.bet
                self.bet = self.bet * 2
                self.clear()
                card_suit, card_number = self.draw_card(deck)
                print('{name} draws a'.format(name=self.name))
                print('{number} of {suit}\n'.format(suit=card_suit, number=card_number))
                self.check_cards(deck)
                sleep(2)
                return False
        else:
            answer = input('Hit or Stand  (h/s) \n')
            while answer != 'h' and answer != 's':
                answer = input('Must choose (h) for Hit and (s) for Stand ')
            if answer == 'h':
                self.clear()
                card_suit, card_number = self.draw_card(deck)
                print('{name} draws a'.format(name=self.name))
                print('{number} of {suit}\n'.format(suit=card_suit, number=card_number))
                return True
            sleep(2)
            return False

    def check_split(self):
        if self.money == 0:
            return False
        if self.current_hand.count(self.current_hand[0]) == 2:
            return True
        return False

    def clear(self):
        print('\n' * 50)

    def load_data(self):
        # load high score
        HS_FILE = 'highscore.txt'
        self.dir = path.dirname(__file__)
        try:
            open(path.join(self.dir, HS_FILE), 'r+')
        except FileNotFoundError:
            open(path.join(self.dir, HS_FILE), 'w+')

        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0


class Dealer:

    def __init__(self):
        self.name = 'Dealer'
        self.cards = []
        self.current_hand = []

    def draw_card(self, deck, display=False):
        deck.check_deck()
        random_suit = choice(list(deck.cards))
        random_number = choice(deck.cards[random_suit])
        deck.cards[random_suit].remove(random_number)
        self.cards.append([random_suit, random_number])
        self.current_hand.append(random_number)
        if display:
            print('{name} draws {number} of {suit}'.format(name=self.name, number=random_number, suit=random_suit))
        return random_suit, random_number

    def set_up(self, deck):
        self.current_hand = []
        self.cards = []
        self.draw_card(deck)
        self.draw_card(deck)
        self.current_hand = [card[1] for card in self.cards]
        self.display_cards()

    def display_cards(self):  # Dealer can only show one card at first
        self.clear()
        sleep(1)
        print('-------------------------')
        print('The Dealer is showing')
        print('{number} of {suit}'.format(number=self.cards[1][1], suit=self.cards[1][0]))
        print('-------------------------')

    def display_all_cards(self):
        print('-------------------------')
        print('The Dealer cards are:')
        for card in self.cards:
            print('{number} of {suit}'.format(number=card[1], suit=card[0]))

    def check_blackjack(self):
        if len(self.cards) == 2:
            temp = [card[1] for card in self.cards]
            if 'Ace' in temp and 10 in temp:
                print('Dealer BlackJack!')
                return True
            elif 'Ace' in temp and 'Queen' in temp:
                print('Dealer BlackJack!')
                return True
            elif 'Ace' in temp and 'King' in temp:
                print('Dealer BlackJack!')
                return True
            elif 'Ace' in temp and 'Jack' in temp:
                print('Dealer BlackJack!')
                return True

    def check_cards(self):  # Dealer's Ace will be 11 if sum of cards is less than 11. Else 1
        temp = []
        for number in self.current_hand:
            index = self.current_hand.index(number)
            if number == "Ace":
                continue
            if number == 'Queen' or number == 'Jack' or number == 'King':
                self.current_hand.remove(number)
                self.current_hand.insert(index, 10)
                temp.append(10)
            else:
                temp.append(number)
        for number in self.current_hand:  # Deciding what to do with the Ace
            total = sum(temp)
            index = self.current_hand.index(number)
            if number == 'Ace':
                self.current_hand.remove(number)
                if total < 11:
                    self.current_hand.insert(index, 11)
                    temp.append(11)
                else:
                    self.current_hand.insert(index, 1)
                    temp.append(1)
        total = sum(self.current_hand)
        # Evaluate hand
        if total == 21:
            self.display_all_cards()
            print('Dealer has 21')
            print('-------------------------')
            sleep(2)
            return False
        elif total > 21:
            self.display_all_cards()
            print('\nDealer Bust!')
            print('-------------------------')
            sleep(2)
            return False
        else:
            self.display_all_cards()
            print('Totaling {total}\n'.format(total=total))
            print('-------------------------')
            sleep(2)
            return True

    def hit(self, deck):
        dealer_total = sum(self.current_hand)
        if dealer_total < 17:
            card_suit, card_number = self.draw_card(deck)
            print('{name} draws {number} of {suit}\n'.format(name=self.name, suit=card_suit, number=card_number))
            sleep(2)
            return True
        return False

    def clear(self):
        print('\n' * 50)


class Deck:

    def __init__(self):
        self.cards = {'clubs': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                      'spades': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                      'hearts': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                      'diamonds': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']}

        self.values = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11,
                       'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]}

    def check_deck(self):
        for number, suit in self.cards.items():
            if not suit:
                print('\n---New deck added---\n')
                self.cards = {'clubs': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                              'spades': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                              'hearts': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
                              'diamonds': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']}
