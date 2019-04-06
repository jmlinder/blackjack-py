#! /Users/JoeLinder/anaconda3/bin/python
# To play a hand of Blackjack the following steps must be followed:
# Create a deck of 52 cards
# Shuffle the deck
# Ask the Player for their bet
# Make sure that the Player's bet does not exceed their available chips
# Deal two cards to the Dealer and two cards to the Player
# Show only one of the Dealer's cards, the other remains hidden
# Show both of the Player's cards
# Ask the Player if they wish to Hit, and take another card
# If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# Determine the winner and adjust the Player's chips accordingly
# Ask the Player if they'd like to play again

#GAME VARIABLES
import random
suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
cvalues = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True
old_chips = open("/Users/JoeLinder/Desktop/Coding/Python/Blackjack/chips.txt", "r")
player_one_chips = int(old_chips.read())

if player_one_chips <= 0:
    player_one_chips = 100

#GAME OBJECTS
class Card:
    # creates a card with a suit and rank
    def __init__(self, suit, rank):
        self.suit  = suit
        self.rank = rank
    
    # prints the name of the card
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    # creates a deck class with 52 unique cards
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    # prints the deck contents
    def __str__(self):
        comp_deck = ''
        for card in self.deck:
            comp_deck += '\n   ' + card.__str__()
        return 'This deck has: ' + comp_deck

    # shuffles the deck
    def shuffle(self):
        random.shuffle(self.deck)

    # deals one card from deck
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Shoe(Deck):
    
    def __init__(self):
        Deck.__init__(self)
    
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,somecard):
        self.cards.append(somecard)
        self.value += cvalues[somecard.rank]
        if somecard.rank == 'Ace':
            self.aces += 1
    
    def ace_adjust(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        handcards = ''
        for card in self.cards:
            handcards += '\n ' + card
            return handcards

class Chips:

    def __init__(self, player_one_chips):
        self.total = player_one_chips
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#GAME FUNCTIONS
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('please take your bet: '))
        except ValueError:
            print('sorry, value must be an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry, your bet cannot exceed', chips.total)
            elif chips.bet <= 0:
                print("Please pick a positive number.")
            else:
                break


def hit(hand, deck):
    hand.add_card(deck.deal())
    hand.ace_adjust()

def hit_or_stand(hand, deck):
    global playing

    while True:

        answer = input("Will you hit or stand? Please enter 'h' or 's': ")

        if answer.lower() =='h':
            hit(hand, deck)
        elif answer.lower() =='s':
            print("Player stands. Dealer is playing")
            playing = False
        else:
            print("Sorry, please try again")
        break

def show_some(player, dealer):
    print("\nDealer's hand:")
    print(" <card hidden>")
    print(" ", dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n')
    print("Dealer's hand = ", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n')
    print("Player's hand = ", player.value)

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("Player and Dealer tie! It's a push.")

############################################GAMEPLAY##################################################

while True:

    print("Welcome to Blackjack! Get as close to 21 as you can without going over")
    print("Your current number of chips are", player_one_chips)

    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips(player_one_chips)

    if player_one_chips == 0:
        print("Sorry, you are out of chips. Come back again!")
        remaining_chips = player_chips.total
        save = open("/Users/JoeLinder/Desktop/Coding/Python/Blackjack/chips.txt", "w")
        save.write(str(remaining_chips))
        break

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_stand(player_hand, deck)

        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
        
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(dealer_hand, deck)
        
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)
        
    print("\nPlayer's winnings stand at", player_chips.total)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game.lower()=='y':
        playing=True
        player_one_chips = player_chips.total
        continue
    else:
        print("Thanks for playing!")
        remaining_chips = player_chips.total
        save = open("/Users/JoeLinder/Desktop/Coding/Python/Blackjack/chips.txt", "w")
        save.write(str(remaining_chips))
        break