'''
v1.8 - Pretty Much works except a few game mechanisms I will add in later versions.
To-do for v2.0 - (a). Double value Aces (1 or 11) - DONE
                    (a).1 For both the dealer and the player - DONE
                 (b). Split same cards into two hands {this is fine if its only for the player, no need to do it for the dealer}

'''

import random

def clear_console():
    print("\n" *40)

#introductory output
clear_console()
print("🃏 Welcome to the Casino!! 🎰")

#create the deck
card_suit_names = [' of Clubs ♣️ ', ' of Spades ♠️ ', ' of Hearts ♥️ ', ' of Diamonds ♦️ '] 

card_values = {'Ace' : 11, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 
 'Eight' : 8, 'Nine' : 9, 'Ten' : 10, 'Joker' : 10, 'Queen' : 10, 'King' : 10} #All suits use the same card values

all_cards_dict = {}
for i in range(len(card_suit_names)):
    for key in card_values:
        value = card_values[key]
        all_cards_dict[key + card_suit_names[i]] = value
        

#initialize and define values
value_of_players_hand = 0
value_of_dealers_hand = 0
players_hand = []
dealers_hand = []
deck_key_list = list(all_cards_dict.keys())
deck_value_list = list(all_cards_dict.values())

#Player's initial hand
for i in range(2):
    random_card = random.choice(deck_key_list) #draws a card from the deck
    individual_card_index = deck_key_list.index(random_card) #gets the index of the drawn card
    individual_card_value = deck_value_list[individual_card_index] #uses the index to get the value from a different but synced list
    deck_key_list.remove(random_card) #takes out the drawn card from the deck like irl to avoid same card being pulled
    deck_value_list.pop(individual_card_index) #takes out the value of the card from the value list for same reason
    players_hand.append(random_card) #adds the drawn card to the player's hand
    value_of_players_hand += individual_card_value #updates the value of the player's hand

print(players_hand) #prints the initial hand
print(f"The total value of your hand is: {value_of_players_hand}")

def draw_card(): #draws a single card
    drawn_card = random.choice(deck_key_list) 
    individual_card_index = deck_key_list.index(drawn_card)
    individual_card_value = deck_value_list[individual_card_index]
    deck_key_list.remove(drawn_card)
    deck_value_list.pop(individual_card_index)
    return drawn_card, individual_card_value

def update_hand_after_draw(drawn_card, individual_card_value, value_of_players_hand): #updates players hand with drawn card and new value
    players_hand.append(drawn_card)
    value_of_players_hand += individual_card_value
    clear_console()
    print(players_hand)
    print(f"The total value of your hand is: {value_of_players_hand}")
    return value_of_players_hand

def stand(): 
    if value_of_players_hand < value_of_dealers_hand or value_of_players_hand > 21:
        print("You lose, dealer had a closer value")
    elif value_of_players_hand >= value_of_dealers_hand and value_of_players_hand <= 21:
        print("You win!")

def update_dealers_hand_after_draw(drawn_card, individual_card_value, value_of_dealers_hand):
    dealers_hand.append(drawn_card)
    value_of_dealers_hand += individual_card_value
    return value_of_dealers_hand

def dealers_turn(value_of_dealers_hand):
    while value_of_dealers_hand < 17:
        drawn_card, individual_card_value = draw_card()
        value_of_dealers_hand = update_dealers_hand_after_draw(drawn_card, individual_card_value, value_of_dealers_hand)
    print(f"Dealer's hand is: {dealers_hand} with a value of {value_of_dealers_hand}")
    if value_of_dealers_hand > 21:
        value_of_dealers_hand = 0
        print("Dealer Busts!!!")
    return(value_of_dealers_hand)
    

def check_aces(players_hand, value_of_players_hand):
    ace_count = sum(1 for card in players_hand if "Ace" in card)
    
    while value_of_players_hand > 21 and ace_count > 0:
        value_of_players_hand -= 10
        ace_count -= 1

    return value_of_players_hand

#dealer's inital hand:
drawn_card, individual_card_value = draw_card()
value_of_dealers_hand = update_dealers_hand_after_draw(drawn_card, individual_card_value, value_of_dealers_hand)
print(f"Dealer's hand is: {dealers_hand} with a value of {value_of_dealers_hand}")




#actual game mech (crude)
while value_of_players_hand < 21: 
    user_input = input("Do you want to hit or stand? Enter \"1\" to hit and \"2\" to stand: ")
    try:
        user_choice = int(user_input)
    except ValueError:
        print("❌ Invalid input, please enter either 1 or 2")
        continue

    if user_choice == 1:
        
        drawn_card, individual_card_value = draw_card()
        value_of_players_hand = update_hand_after_draw(drawn_card, individual_card_value, value_of_players_hand)
        if value_of_players_hand > 21:
            value_of_players_hand = check_aces(players_hand, value_of_players_hand)
            if value_of_players_hand > 21:
                print("YOU BUST. DEALER WINS")
            else:
                print("Your ace was reduced to 1.")
                print(f"Your updated value is {value_of_players_hand}!!!")

    elif user_choice == 2:
        value_of_dealers_hand = dealers_turn(value_of_dealers_hand)
        stand()
        
        break

if value_of_players_hand == 21:
    print("Perfect Score! You win!!")
