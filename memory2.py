# implementation of card game - Memory

import simplegui
import random

deck = 2 * [str(i) for i in range(8)]

# helper function to initialize globals
def new_game():
    global exposed, state, count, first_card, second_card
    state, count = 0, 0
    first_card, second_card = -1, -2
    random.shuffle(deck)
    exposed = [False for i in range(16)]
    label.set_text("Turns = " + str(count))

    
# define event handlers
def mouseclick(pos):
    global state, first_card, second_card, count
    index = pos[0] / 50
    
    if not exposed[index]:
        if state == 0:
            state = 1
            exposed[index] = True
            first_card = index
        elif state == 1:
            state = 2
            exposed[index] = True
            second_card = index
            count += 1
            label.set_text("Turns = " + str(count))
        else:
            state = 1
            if not deck[first_card] == deck[second_card]:
                exposed[first_card] = False
                exposed[second_card] = False
            exposed[index] = True
            first_card = index  

# cards are logically 50x100 pixels in size    
def draw(canvas):
    for index in range(16):
        pos = index * 50
        canvas.draw_text(deck[index], (pos+10, 75), 60, 'White')
        if not exposed[index]:
            canvas.draw_polygon([[pos, 0], [pos, 100], [pos + 50, 100], [pos + 50, 0]], 1, "Red", "Green")
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
