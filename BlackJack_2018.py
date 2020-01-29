from random import shuffle

def check_shuffle(current_deck, numDecks, get_buyin):

    shuffle_value = (int(numDecks) * 52) / 4
    if len(current_deck) <= shuffle_value:
        print("Shuffle time! Time for a new shoe!")
        print("Here we go!")
        deck = get_deck(numDecks)
        continuous_game(deck, get_buyin, numDecks)
    else:
        return

def continuous_game(deck, get_buyin, numDecks):
    '''Takes in input as wager & deals cards out to each player.'''
    while (True):
        try:
            wager = int(input("What's your wager?"))
            while wager > get_buyin or wager <= 0:
                wager = int(input("That's larger than your buyin or zero and below. Try again"))
            break
        except ValueError:
            print("Invalid number. Try again")

    deal = deal_blackjack(deck)
    user_cards = deal[0]
    dealer_cards = deal[1]
    remaining_deck = deal[2]
    # calls current_standing() to check positioning of each player
    current_standing(user_cards, dealer_cards, remaining_deck, wager, get_buyin, numDecks)

def get_deck(numDecks):
    '''Creates the deck'''
    deck_list = []
    card_suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    decks = 1
    while decks <= int(numDecks):

        for suits in card_suits:
            for cards in card_values:
                if deck_list == []:
                    deck_list = [[cards, suits]]
                else:
                    deck_list.append([cards, suits])
        decks += 1
    return deck_list

def deal_blackjack(the_deck):
    start_dealing = 1
    user_cards = []
    dealer_cards = []
    while start_dealing <= 2:
        if user_cards == []:
            user_cards = [the_deck.pop(0)]
            dealer_cards = [the_deck.pop(0)]
        else:
            user_cards.append(the_deck.pop(0))
            dealer_cards.append(the_deck.pop(0))
        start_dealing += 1
    return user_cards, dealer_cards, the_deck

def compute_value(card):
    '''Takes in the card as a parameter and computes
     the value for each card'''
    if card == '10' or card == 'Jack' or card == 'Queen' or card == 'King':
        return [10]
    elif card != 'Ace':
        return [int(card)]
    else:
        return 1, 11

def ask_again(deck, buyin, numDecks):
    '''Asks player if they would like to continue playing or cash out their winnings'''
    print("You currently have $" + str(buyin) + " to play with")
    ask_again = input("Would you like to play again? 'Y' for yes, 'N' for no: ").lower()
    while ask_again != 'y' and ask_again != 'n':
        # handling invalid input
        ask_again = input("Invalid response. Play again? 'Y' for yes, 'N' for no: ").lower()
    if ask_again == 'y':
        continuous_game(deck, buyin, numDecks)
    else:   # exit game
        print('\n')
        print("Thanks for playing!")
        print("You're leaving with $" + str(buyin))
        exit()

def check_blackjack(user, dealer, dealer_cards, user_cards, deck, wager, buyin, numDecks):
    wager = int(wager)
    buyin = int(buyin)
    if dealer_cards[1][0] == 'Ace':
        # Asks player if they want to even money b/c the dealer has an ace
        if 21 in user:
            ask_even = input("Even Money? (Y for Yes, N for No)")
            while ask_even != 'Y' and ask_even != 'y' and ask_even != 'N' and ask_even != 'n':
                #handling invalid input
                ask_even = input("Invalid Response. Even Money? (Y for Yes, N for No")
            if ask_even == 'Y' or ask_even == 'y':
                print("Here is even money!")
                buyin = buyin + wager
                print(dealer_cards)
                check_shuffle(deck, numDecks, buyin)
                ask_again(deck, buyin)
            elif ask_even == 'N' or ask_even == 'n':
                # returns 1 for a push
                if 21 in dealer:
                    print("Push!")
                    print(dealer_cards)
                    check_shuffle(deck, numDecks, buyin)
                    ask_again(deck, buyin)
                else:
                    # returns 2 for a win of blackjack
                    print("You got blackjack!")
                    print(dealer_cards)
                    buyin = buyin + (wager * 1.5)
                    check_shuffle(deck, numDecks, buyin)
                    ask_again(deck, buyin)

        else:
            ask_insurance = input("Insurance? (Y for Yes, N for No)")
            while ask_insurance != 'Y' and ask_insurance != 'y' and ask_insurance != 'N' and ask_insurance != 'n':
                # handling invalid input
                ask_insurance = input("Invalid Response. Insurance? (Y for Yes, N for No")

            if ask_insurance == 'Y' or ask_insurance == 'y':
                ask_value = input("How much insurance would you like to add?")
                max_wager = wager / 2    # sets max wager as half of original wager
                while int(ask_value) > max_wager or int(ask_value) == False or int(ask_value) < 0:
                    # handling invalid input - wager can't exceed more than half of original wager
                    ask_value = input("Invalid response. Please try again for insurance! ")

                if dealer_cards == 21:
                    # user does not lose because of insurance with dealers blackjack
                    print("You won insurance")
                    buyin = buyin - wager
                    buyin = buyin + (ask_value * 2)
                    print(dealer_cards)
                    check_shuffle(deck, numDecks, buyin)
                    ask_again(deck, buyin)
                else:
                    print("You lost your insurance")
                    play_blackjack(user, dealer, user_cards, dealer_cards, wager, buyin, deck, numDecks)

            elif ask_insurance == 'N' or ask_insurance == 'n':

                if 21 in dealer:
                    print("You lose!")
                    print(dealer_cards)
                    buyin = buyin - wager   # user loses wager
                    check_shuffle(deck, numDecks, buyin)
                    ask_again(deck, buyin, numDecks)
                else:
                    play_blackjack(user, dealer, user_cards, dealer_cards, deck, wager, buyin, numDecks)
    elif 21 in user:
        if 21 in dealer:
            # in instance of a tie, the player has a push
            print("Push!")
            print(dealer_cards)
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)
        else:
            print("Blackjack!")
            print(dealer_cards)
            buyin = (wager * 1.5) + buyin   # player wins 1 & a half times their wager
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)

    elif 21 in dealer:
        print("Dealer has blackjack! You lose!")
        print("Dealer's hand: %s of %s " % (dealer_cards[1][0], dealer_cards[1][1]))
        buyin = buyin - wager        # player loses their wager
        check_shuffle(deck, numDecks, buyin)
        ask_again(deck, buyin, numDecks)
    else:
        play_blackjack(user, dealer, user_cards, dealer_cards, deck, wager, buyin, numDecks)

# value is the list in this case
def compute_all_values(count, two_values):
    index = 0
    new_list = []
    for number in two_values:

        indexing_current_count = 0
        for the_num in count:

            get_value = count[indexing_current_count] + two_values[index]

            if new_list == []:
                new_list = [get_value]
            else:
                new_list.append(get_value)
            indexing_current_count += 1
        index += 1
    final_index = 0
    for values in new_list:
        if new_list[final_index] > 21:
            new_list.pop(final_index)
        final_index += 1

    new_list = list(set(new_list))
    return new_list

def current_standing(user_cards, dealer_cards, remaining_deck, wager, buyin, numDecks):
    get_dealer_value = [dealer_cards[0][0], dealer_cards[1][0]]
    get_user_value = [user_cards[0][0], user_cards[1][0]]
    user_count = [0]
    dealer_count = [0]

    for number in get_dealer_value:
        # calculates values of dealer's hand
        num = compute_value(number)
        dealer_count = compute_all_values(dealer_count, num)

    for number in get_user_value:
        # calculates values of user's hand
        num = compute_value(number)
        user_count = compute_all_values(user_count, num)
    print('\n')
    print("Dealer's hand: %s of %s " % (dealer_cards[1][0], dealer_cards[1][1]))
    print('Your hand: %s of %s & %s of %s' % (user_cards[0][0], user_cards[0][1], user_cards[1][0], user_cards[1][1]))
    print('Value of your hand:', user_count[0])
    print('-' * 80)

    check_blackjack(user_count, dealer_count, dealer_cards, user_cards, remaining_deck, wager, buyin, numDecks)

def take_largest(counts):
    if type(counts) == int:
        return counts
    else:
        highest_value = 0
        for values in counts:
            if values > highest_value:
                highest_value = values
        return highest_value

def dealers_turn(user, dealer, user_c, dealer_c, deck, wager, buyin, numDecks):
    '''Takes in dealer's decisions & plays the hand - dealer version of play_blackjack()'''
    wager = int(wager)
    buyin = int(buyin)
    if dealer_c == []:
        indexing = 0
        print("Dealer has:")
        for stuff in dealer:
            print("%s of %s" % (dealer[indexing][0], dealer[indexing][1]))
            indexing += 1
        print("Dealer busts!")
        buyin = buyin + wager
        check_shuffle(deck, numDecks, buyin)
        ask_again(deck, buyin, numDecks)
    finish_dealer = take_largest(dealer_c)
    if type(user_c) != int:
        user_c = take_largest(user_c)
    if finish_dealer >= 17:

        if user_c > finish_dealer:
            indexing = 0
            print("Dealer has:")
            for stuff in dealer:
                print("%s of %s" % (dealer[indexing][0], dealer[indexing][1]))
                indexing += 1
            print("Dealer count: " + str(finish_dealer))
            print("User wins!")
            buyin = buyin + wager
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)
        elif user_c < finish_dealer:
            indexing = 0
            print("Dealer has:")
            for stuff in dealer:
                print("%s of %s" % (dealer[indexing][0], dealer[indexing][1]))
                indexing += 1

            print("Dealer count: " + str(finish_dealer))
            print("Dealer wins!")
            buyin = buyin - wager
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)
        else:
            indexing = 0
            print("Dealer has:")
            for stuff in dealer:
                print("%s of %s" % (dealer[indexing][0], dealer[indexing][1]))
                indexing += 1
            print("Dealer count: " + str(finish_dealer))
            print("Push!")
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)
    else:
        indexing = 0
        print("Dealer has:")
        for stuff in dealer:
            print("%s of %s" % (dealer[indexing][0], dealer[indexing][1]))
            indexing += 1
        if len(dealer_c) > 1:
            index = 0
            for possible_values in dealer_c[:-1]:
                print('Dealer value = ' + str(dealer_c[index]) + " or")
                index += 1
            print('Dealer value = ' + str(dealer_c[-1]))
        else:
            print("dealer count: " + str(dealer_c[0]))
        dealer.append(deck.pop(0))
        new_value = compute_value(dealer[-1][0])
        dealer_c = compute_all_values(dealer_c, new_value)

        dealers_turn(user, dealer, user_c, dealer_c, deck, wager, buyin, numDecks)

def bust_value(cards):
    index = 0
    count = 0
    for value in cards:
        value = compute_value(cards[index][0])
        if value == [1,11]:
            value = [1]
            count += value[0]
        else:
            count += value[0]
        index += 1
    print("Count: " +str(count))

def play_blackjack(user_c, dealer_c, user, dealer, deck, wager, buyin, numDecks):
    wager = int(wager)
    buyin = int(buyin)
    if len(user) == 2:
        # takes in user decision on the hand
        user_decision = input("Press 'Sp' to split, 'H' to hit, 'S' to stand, 'D' to double, 'Su' to surrender: ")
        if user_decision.lower() == 's':
            dealers_turn(user, dealer, user_c, dealer_c, deck, wager, buyin, numDecks)
        elif user_decision.lower() == 'h':
            user.append(deck.pop(0))
            if user[-1][0] == 'Ace':
                user_c = hit_ace(user_c)
            else:
                new_value = compute_value(user[-1][0])
                user_c = compute_all_values(user_c, new_value)

            print('Your hand: ')

            indexing=  0
            for stuff in user:
                print("%s of %s" %(user[indexing][0], user[indexing][1]))
                indexing += 1

            check_b = check_bust(user, user_c)  # evaluates whether or not user has busted
            if check_b == True:
                print("Value of your hand: " + str(take_largest(user_c)))
                play_blackjack(user_c, dealer_c, user, dealer, deck, wager, buyin, numDecks)
            else:
                bust_value(user)
                print("You bust!")
                buyin = buyin - wager
                check_shuffle(deck, numDecks, buyin)
                ask_again(deck, buyin, numDecks)
        elif user_decision.lower() == 'su':
            print("You surrender!")
            buyin = buyin - (wager / 2)
            check_shuffle(deck, numDecks, buyin)
            ask_again(deck, buyin, numDecks)
        elif user_decision.lower() == 'd':
            wager = wager * 2
            user.append(deck.pop(0))
            new_value = compute_value(user[-1][0])
            user_c = compute_all_values(user_c, new_value)
            indexing = 0
            for stuff in user:
                print("%s of %s" % (user[indexing][0], user[indexing][1]))
                indexing += 1
            print("User Count: " + str(user_c))
            dealers_turn(user, dealer, user_c, dealer_c, deck, wager, buyin, numDecks)
    else:
        user_decision = input("Press 'H' to hit or 'S' to stand: ")
        if user_decision.lower() == 's':
            dealers_turn(user, dealer, user_c, dealer_c, deck, wager, buyin, numDecks)
        elif user_decision.lower() == 'h':
            user.append(deck.pop(0))
            new_value = compute_value(user[-1][0])
            if type(user_c) == int:
                user_c = [user_c]
            user_c = compute_all_values(user_c, new_value)
            print(user[-1])
            print('Your hand: ')
            indexing = 0
            for stuff in user:
                print("%s of %s" % (user[indexing][0], user[indexing][1]))
                indexing += 1

            check_b = check_bust(user, user_c)
            if check_b == True:
                print("Value of your hand: " + str(take_largest(user_c)))
                play_blackjack(user_c, dealer_c, user, dealer, deck, wager, buyin, numDecks)
            else:
                bust_value(user)
                print("You bust!")
                buyin = buyin - wager
                check_shuffle(deck, numDecks, buyin)
                ask_again(deck, buyin, numDecks)

def hit_ace(user_count):
    '''Evaluates user hand to determine if the ace should be played as 1 or 11.'''

    new_list = []

    user_count = list(user_count)

    index = 0
    for values in user_count:

        user_count[index] += 11
        if user_count[index] > 21:
            if new_list == []:
                new_list = user_count[index] - 10
            else:
                new_list.append(user_count[index])
        elif user_count[index] <= 21:
            if new_list == []:
                new_list == [user_count[index]]
                new_list.append(user_count[index] - 10)
            else:
                new_list.append(user_count[index])
                new_list.append(user_count[index]- 10)
        index += 1
    return new_list

def check_bust(cards, count):
    if count == []:
        return False
    else:
        return True


def main():
    print('Welcome to Blackjack!')
    print('-' * 80)

    while (True):
        try:
            numDecks = int(input("How many decks do you want in this game? "))
            while numDecks > 8 or numDecks < 1:
                numDecks = int(input("Either smaller than 0 or larger than 8. Try again!"))
            break
        except ValueError:
            print("Invalid number. Try again")
    while (True):
        try:
            get_buyin = int(input("What's your buyin? "))
            while get_buyin <= 0:
                get_buyin = int(input("Negative value or 0! Try again"))
            break
        except ValueError:
            print("Invalid number. Try again")


    deck = get_deck(numDecks)
    shuffle(deck)
    continuous_game(deck, get_buyin, numDecks)


if __name__ == '__main__': main()