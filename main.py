import random 

def play(num_cards):
    cards = [
        2,2,2,2,
        3,3,3,3,
        4,4,4,4,
        5,5,5,5,
        6,6,6,6,
        7,7,7,7,
        8,8,8,8,
        9,9,9,9,
        10,10,10,10,
        11,11,11,11,
        12,12,12,12,
        13,13,13,13,
        14,14,14,14
    ]

    random.shuffle(cards)

    market = select_initial_market(num_cards, cards)
    spread = select_spread()
    curr_card = 0
    
    for i in range(num_cards * 3):
        incoming_trade = computer_play()

        update_position(spread, incoming_trade)
        prompt_shift(spread)

        if (i+1) % 3 == 0:
            curr_card += 1
            reveal_card(curr_card, market)

    show_PnL(market)


# BASE FOUNDATION FOR GAME

long_positions = []
short_positions = []

def select_initial_market(market_size, cards):
    market = cards[:market_size]
    print("Market:" + "".join(" X " for _ in range(market_size)) + "\n")
    return market

def select_spread():
    lower_bound = float(input("Pick a lower bound: "))
    upper_bound = float(input("Pick an upper bound: "))
    return [lower_bound, upper_bound]

# Let a trade be represented by a 2-element array as follows: ["TRADE TYPE (B/S)", "TRADE AMOUNT"]
# and a spread be represented by a 2-element array as follows: ["LOW BOUND", "UPP BOUND"]

def update_position(spread, trade):
    if trade[0] == "B":
        short_positions.append(spread[1])
        # if they buy then we are obligated to pay them as needed, thus any buys they make 
    elif trade[0] == "S":
        long_positions.append(spread[0])
    
def reveal_card(index, market):
    print("Market: ", end='')
    for i in range(index):
        print(str(market[i]), end=' ')
    for j in range(len(market) - index):
        print(" X ", end='')
    print()

# MARKET: 1 X X
# MARKET: 1 10 X

def prompt_shift(spread):
    direction = input("Shift your bound (U or N or D): ")
    if direction == "U":
        shift_market(spread, 1)
    elif direction == "D":
        shift_market(spread, 0)
    elif direction != "N":
        print("Please enter either U (up), N (neutral), or D (down) as your direction")
        prompt_shift(spread)

def shift_market(spread, direction):
    if direction == 1:
        spread[1] += 1
        spread[0] += 1
    else:
        spread[1] -= 1
        spread[0] -= 1

def computer_play():
    # Currently will play random move and place order for one contract until
    # I implement the actual game logic
    move_choice = random.choice(["B", "S"])
    move_message = ""
    if move_choice == "B":
        move_message = "Bought "
    else:
        move_message = "Sold "
    print("Incoming trade!! " + move_message + str(1) + " contract")
    return [move_choice, 1]

def show_PnL(market):
    target = sum(market)
    PnL = 0
    for lp in long_positions:
        PnL += target - lp
    for sp in short_positions:
        PnL -= target - sp

    print("Your total PnL was: " + str(PnL))


play(3)