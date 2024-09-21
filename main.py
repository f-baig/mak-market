import random 

def play(num_cards, turns_per_round):
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
    curr_sum = 0
    expected_value_per_turn = random_noise(7.5)
    expected_target = expected_value_per_turn * num_cards
    
    for i in range(num_cards * turns_per_round):
        incoming_trade = computer_play(expected_target, spread)

        update_position(spread, incoming_trade)
        prompt_shift(spread)

        if (i+1) % turns_per_round == 0:
            curr_card += 1
            curr_sum += market[(i+1) % turns_per_round];
            reveal_card(curr_card, market)
            expected_target += update_expected_target(curr_sum, expected_value_per_turn, market, (i+1) % turns_per_round)

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

def random_noise(num):
    scalar = random.randrange(0,2)
    return num * scalar

def update_expected_target(curr_sum, expected_value_per_turn, market, index):
    if curr_sum < expected_value_per_turn * index:
        return -1 * (expected_value_per_turn - market[index])
    else:
        return expected_value_per_turn + market[index]


def computer_play(expected_target, spread):
    # Currently will play random move and place order for one contract until
    # I implement the actual game logic

    # Maybe make a player/bot class to do all this more efficiently
    
    # LOGIC:
    # Keep track of current sum
    # Keep track of expected ending target (this is intialized at expected value of turn * num_cards) w some noise added
    # Update current sum on reveal card call
    # Change expected ending target, and buy and sell accordingly
    # If expected value is above/close to buy, then buy, otherwise sell if close to/below sell (close to is defined by some arbitrary threshold determined after testing)
    # If in the middle of range add heavier noise
    # OR
    # Try to minimize market maker PnL by playing sell/buy to decrease market maker PnL as much as possible
    # Essentially hedge your previous trades, so keep track of previous trades (not implemented)

    # To hedge our trades, we should be tracking expected PnL which is updated based on card reveals and then execute trades that way

    move_choice = ""

    threshold = 0.5

    expected_PnL += (expected_target - lp for lp in long_positions) - (expected_target - sp for sp in short_positions)
    
    if expected_target < spread[1] - random_noise(threshold):
        move_choice = "S"
    elif expected_target > spread[0] + random_noise(threshold):
        move_choice = "B"
    else:
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


play(3, 2)
