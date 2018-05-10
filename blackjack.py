# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
msg = "Hit or stand? "
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    # return the suit
    def get_suit(self):
        return self.suit

    # return the rank
    def get_rank(self):
        return self.rank

    # draw the card
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []

    def __str__(self):
        hand_mes = ""
        for card in self.hand_list:
            hand_mes += str(card) + " "
        return hand_mes

    # add a card in list hand_list
    def add_card(self, card):
        self.hand_list.append(card)

    # return the value hand
    def get_value(self):
        value = 0
        is_as = False
        
        for key in self.hand_list:
            value += VALUES[key.get_rank()]
            if key.get_rank() == 'A':
                is_as = True
        
        if is_as and value + 10 <= 21:
            value += 10
        return value

    # draw the hand
    def draw(self, canvas, pos):
        for card in self.hand_list:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(i, j) for i in SUITS for j in RANKS]

    # shuffle the deck 
    def shuffle(self):
        random.shuffle(self.deck)

    # deal a card of deck
    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        msg = "Deck contains "
        for i in self.deck:
            msg += str(i) + " "
        return msg

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, msg

    if in_play:
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

    outcome = ""
    msg = "Hit or stand?"
    in_play = True
    
def hit():
    global outcome, score, in_play, msg
    
    if in_play:
        player.add_card(deck.deal_card())
        
        if player.get_value() > 21:
            outcome = "You have busted and dealer won"
            msg = "New deal? "
            score -= 1
            in_play = False
    
def stand():
    global outcome, msg, in_play, score

    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "dealer busted and you won"
            score += 1
        elif dealer.get_value() >= player.get_value():
            outcome = "dealer won"
            score -= 1
        else:
            outcome = "you won"
            score += 1
        msg = "New deal? "
        in_play = False
    
# draw handler    
def draw(canvas):
    player.draw(canvas, [100, 350])
    dealer.draw(canvas, [100, 150])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (100 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)
    
    canvas.draw_text("Blackjack", (100, 80), 48, "Blue")
    canvas.draw_text("Dealer", (100, 140), 24, "Black")
    canvas.draw_text("Player", (100, 340), 24, "Black")
    canvas.draw_text(outcome, (250, 140), 24, "Black")
    canvas.draw_text(msg, (250, 340), 24, "Black")
    canvas.draw_text("Score: " + str(score), (500, 50), 24, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
