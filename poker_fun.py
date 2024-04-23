import random

waits = True

class GameFlow:
    def __init__(self, counter:int = 0, og_name:str = 'player1', menu_off:bool = False, dealer = '', pot ='', player1 = ''):
        self.counter = counter
        self.og_name = og_name
        self.menu_off = menu_off
        self.dealer = dealer
        self.pot = pot
        self.player1 = player1
    
 

    def all_checked_title(self) -> None:
        '''
            Title for displaing that the betting round has ended.
        '''
        print()
        print()
        print(f"{'BETTING ROUND OVER':>64}")

    def back_to_menu(self) -> int:
        '''
            Mid- and end-game menu for deciding to conintue to play
            or turning on bots. 
        '''
        if self.menu_off:
        # to let computr players play until 1 player left with no interruptions
            return
        print('', '-' * 63)
        print(' OPTIONS')
        print('', '-' * 63)
        self.dealer.all_computer_players_check()
        if self.dealer.all_computer_players:
            print(' 1) Let Computer Continue to Play')
        else:
            print(' 1) Continue Playing')
        print(' 2) Reset and Return to Menu')
        # turn bots selection off if human player broke. 
        if not self.player1.broke:
            print(' 3) Turn Bots-Only Mode on/off', end=' ')
            if self.player1.human:
                print('(OFF)')
            else:
                print('(ON)')
        print(' 4) Turn Wait-Mode on/off', end=' ')
        if waits:
            print('(ON)')
        else:
            print('(OFF)')
            if self.dealer.all_computer_players: 
                print('    7) Let Computer Play Uninterrupted Until One Remains')
        print(' 5) Quit')
        print()
        valid = ['1', '2', '3', '4', '5', '7']
        print(' Select: ', end ='')
        choice = input()
        while choice not in valid:
            print(' Select: ', end ='')
            choice = input() 
        choice = int(choice)
        return choice
    
    def bet_loop(self) -> None:    
        '''
            Controls the flow of logic for human and 
            computer players in each betting round.
        '''
        self. dealer.betting_round_counter += 1
        
        # bet loop will continue until:
        # each player has called
        # and any raise has been called by each player
        # or if players fold immediately and ony one player remains

        while len(self.dealer.needs_to_bet) > 0 and len(self.dealer.player_list) - len(self.dealer.folded_players) != 1:
    
            self.dealer.in_round_counter += 1
            
        #  GO AROUND THE TABLE

            for player in self.dealer.player_list:
                if player.needs_to_bet and not player.broke and len(self.dealer.player_list) - len(self.dealer.folded_players) != 1:
                    
        # IF HUMAN PRESENT AND NEEDS TO BET
                    
                    if player.human:
                        player.call_raise_fold(self.dealer)  
                    
        # COMPUTER BET AI

                    else:
                        player.computer_bet_ai(self.dealer)         
                    
        #  RAISED LOGIC

                    if player.raised:
                        
                        # prompt for response if human in game
                        if player.human:
                            player.raise_request(self.dealer, self.pot)
                        
                        else:
                            player.raise_ai(self.dealer, self.pot)
                        
                        # if the raise is valid, 
                        # all other places now need to respond to the raise:
                        if not player.call:
                            for other_players in self.dealer.player_list:
                                if not other_players.fold:
                                    other_players.needs_to_bet = True
                                    if other_players not in self.dealer.needs_to_bet:
                                        self.dealer.needs_to_bet.append(other_players)
                        # player who just finished calling/raising 
                        #removed from needs to bet list
                        # if raise was valid
                        if not player.call:
                            player.needs_to_bet = False 
                            self.dealer.needs_to_bet.remove(player) 
                            self.dealer.last_person_to_bet = player  
                    
        #  CALLED LOGIC

                    if player.call:
                        player.call_ai(self.dealer, self.pot)
                        # if valid call / not changed to a fold
                        if player.call:
                            player.needs_to_bet = False
                            self.dealer.needs_to_bet.remove(player)
                    
        #  FOLD LOGIC

                    if player.fold:
                        # player needs to stay in game if they are broke, no point in folding. 
                        if player.money == 0:
                            player.fold = False
                            player.call = True 
                            player.call_ai(self.dealer, self.pot)
                        # player needs to stay in the game if no one else has put in money, no point in folding.
                        elif self.dealer.round_raise_amnt == 0:
                            player.fold = False
                            player.call = True
                            player.call_ai(self.dealer, self.pot)
                        # need to at least call first bet even in fold in the first round of betting
                        # so again, might as well stay in since have to pay anyway.
                        elif self.dealer.in_round_counter == 1 and player.total_bet_amnt == 0 and self.dealer.betting_round_counter == 1:
                            player.fold = False
                            player.call = True
                            player.call_ai(self.dealer, self.pot)
                        # player who just folded removed from needs to bet and added
                        # to folded players list 
                        # (who will no longer participate in second round betting)
                        player.needs_to_bet = False
                        self.dealer.needs_to_bet.remove(player)
                        if player.fold:
                            self.dealer.folded_players.append(player)
                    
        #  PRINT BET INFO
                    
                    player.print_bet_info()
                    self.pot.print_pot()
                    if player.raised:
                        # if this isn't here, players who raise after someoeone who is broke calls, 
                        # will raise based off of the broke person's 0 ammount and no new money will enter the pot.
                        # not sure why since the broke person shouldn't be marked as the last person to bet. 
                        self.dealer.last_person_to_bet = player 
                    
                    if waits:
                        self.wait_mode_input()
        
        self.dealer.in_round_counter = 0

    def bet_round_initialize(self) -> None:  
        '''

            Selects a valid player to begin betting each round.
            This order will be maintained for each round of betting.
            Controls flow of logic for human and computer
            intial call/raise/fold decisions.

            Sets other player statuses as needing to bet, if players
            still in the game. 

        '''
        # FIND FIRST BETTER

            # players list will be mixed each round. 
            # iterate through list until find a player 
            # who has not folded
       
        i = 0
        first_better = self.dealer.player_list[i]
        while first_better.fold:
            i+=1
            first_better = self.dealer.player_list[i]
        # set some bet statuses for first better
        first_better.needs_to_bet = False
        first_better.first_to_bet = True

        # IF HUMAN FIRST BETTER
        
        if first_better.human:
            first_better.bet = self.player1.get_bet(self.dealer)

       # IF COMPUTER FIRST BETTER

        else:
            # calculate whether or not to bet more than the min:
            first_better.computer_bet_ai(self.dealer)

        # IF FOLDS

            if first_better.fold:
                if self.dealer.betting_round_counter == 0:
                # if first round of betting, still put in min
                # no point in folding if first to go and going to put in money anyway...
                    first_better.fold = False
                    first_better.call = True
                else:
                # if second round of betting, and first to go and decide to fold
                # doesn't make sense to fold, just put in 0 and wait to see what other players do. 
                    first_better.fold = False
                    first_better.bet = 0
       
        # IF CALLS

            if first_better.call:
                if self.dealer.betting_round_counter == 0:
                    # if first round need min
                    # no one to call since first, put in min, 10.
                    if first_better.money >= 10:
                        first_better.bet = 10
                        self.pot.update_pot(first_better.bet)
                        first_better.money -= first_better.bet
                    else:
                        # if not enough for 10, all in. 
                        first_better.bet = first_better.money
                        self.pot.update_pot(first_better.money)
                        first_better.money -= first_better.money
                else:
                # if second round, can just put in 0
                    first_better.bet = 0
        
        # IF RAISES                  
        
            elif first_better.raised:
                first_better.raise_ai(self.dealer, self.pot)
                # if rasied but the logic ended in call:
                if first_better.call:
                    if first_better.money >= 10:
                        first_better.bet = 10
                        self.pot.update_pot(first_better.bet)
                        first_better.money -= first_better.bet
                    else:
                        # if not enough for 10, all in. 
                        first_better.bet = first_better.money
                        self.pot.update_pot(first_better.money)
                        first_better.money -= first_better.money

        # UPDATE BET AMOUNTS AND POT
          
        first_better.total_bet_amnt = first_better.bet
        first_better.old_bet_amnt = first_better.bet
        self.dealer.last_person_to_bet = first_better
        self.dealer.round_raise_amnt = first_better.bet
        self.dealer.has_bet.append(first_better)
        if first_better.human:
           self. pot.update_pot(first_better.bet)
        
        #  SET OTHER PLAYERS AS NEED TO BET

        for players in self.dealer.player_list:
            if not players.first_to_bet and not players.fold:
                players.needs_to_bet = True
                self.dealer.needs_to_bet.append(players)
        if first_better.bet == 0 and self.dealer.betting_round_counter == 0:
            print('what the heck, yo')       
       
        #  DISPLAY FIRST BET
       
        first_better.call = False
        first_better.raised = False
        first_better.print_bet_info()
        # debugging a weird thing where someone can put in 0 to start
        pot_string = 'POT $' + str(self.pot.total)
        print(f"{pot_string:^65}")
        first_better.first_to_bet = False
        if waits:
            self.wait_mode_input()

    def bet_skip_title(self) -> None:
        '''
            When no player has money, second round of betting skipped.
        '''
        print()
        print(f"{' TOO MANY BROKE PLAYERS. BET ROUND SKIPPED':>64}")
    
    def bet_title(self) -> None:
        '''
            Indicates that the betting round has begun.
        '''
        print()
        print()
        print(f"{' BET':>64}")

    def card_reveal_title(self) -> None:
        '''
            Indicates that the second round of betting is over.
            Cards will be revealed.
        '''
        print()
        print(f"{' SHOW CARDS':>64}")
        print()

    def computer_replacing_title(self) -> None:
        '''
            Indicates that the computer has decided
            which cards to keep/replace.
        '''
        print()
        print(f"{' COMPUTER EXCHANGING CARDS':>64}")
        print()

    def create_dealer(self) -> object:
        '''
            Creates a new dealer object.
        '''
        # delear instance
        dealer = Dealer()
        return dealer

    def dealer_replace_cards(self) -> None:
        '''
            Flow of logic for gameplay section in which 
            players exchange cards.
        '''
        # human replace
        if not self.dealer.all_computer_players and not self.player1.fold:
            self.white_space()
            self.replacing_title()
            self.player1.print_name_score()
            self.player1.print_hand()
            self.player1.cards_replace_request()
            self.white_space()
        # computer replace
        self.white_space()
        self.computer_replacing_title()
        if self.player1.human and not self.player1.broke:
            self.player1.replace_cards(self.dealer.full_deck)
        # computer replace // show replacement for all players
        self.dealer.replace_computer_cards(self.dealer.full_deck)

    def deal_title(self) -> None:
        '''
            Title indicated that hands are being dealt.
        '''
        print(f"{' DEALING HANDS':>64}")
        print()
   
    def fold_check(self) -> bool:
        '''
            Flow of logic to determine if all but one player has folded.
            If so, declare that one player winner.
        '''
        if len(self.dealer.folded_players) == len(self.dealer.player_list) - 1:
            self.dealer.all_folded = True
            for player in self.dealer.player_list:
                if not player.fold:
                    player.win = True
                    self.dealer.winner = player
                    self.pot.payout(self.dealer.player_list)
            self.dealer.print_results()
            return True

    def game_loop(self) -> None:
        '''
            Flow of logic for the game. 

            1. count number of games played
            2. create dealer / deck / players
            3. deal hands
            4. bet round 1
            5. fold check to see if winner at this point.
            6. card exchange if no winner yet
            7. bet round 2 if players still have money
            8. reveal cards
            9. payout to winner
            10. menu to select next steps
        '''
        self.counter = 0
        # while more than one player in the game
        while len(self.dealer.player_list) > 1 :
            
            # game counter
            self.counter+=1

        # DEALER GETS DECK / SHUFFLES / DEALS / SORES

            self.start_duties_flow()
            print()
            self.deal_title()   
            #  DEALER SHOWS HANDS
            self.show_hands_flow()
        
        #  BET ROUND 1

            self.bet_title() 
            self.white_space()
            self.bet_round_initialize()
            self.bet_loop()
            self.all_checked_title()
            # if all but one player folds
            # end round, pay out money to winner, remove broke players
            if self.fold_check():
                self.dealer.broke_player_find_remove()
                self.dealer.end_game_statuses()
                self.dealer.print_remaining_players_info()
                # if round ends from fold and still more than one player left
                # give option to continue playing or return to menu
                if len(self.dealer.player_list) >= 2:
                    selection = self.back_to_menu()
                    while selection == 3 or selection == 4:
                        if selection == 3:
                            self.player1.bots_only()  
                        elif selection == 4:
                            self.wait_mode()
                        selection = self.back_to_menu() 
                    if selection == 7:
                        self.menu_mode()
                    if selection == 1:
                        continue   
                    if selection == 2:
                        break
                # if round ends and only one payer left
                # print victory info, loop will end after this at loop check
                if self.dealer.last_man_standing():
                    self.dealer.print_last_man()
                    self.print_game_count()
                continue

        #  REPLACE CARDS

            self.dealer_replace_cards()
            # dealer scores new hands
            self.dealer.assign_scores()
            # show new hand to player
            self.show_new_cards_flow()

        #  BET ROUND 2

            self.bet_title()
            # check to see if anyone has money left after round 1 betting. 
            # if no one or only 1 person has money, skip. 
            if self.dealer.anyone_have_money():
                self.white_space()
                self.dealer.reset_bet_statuses()
                self.bet_round_initialize()
                self.bet_loop()
                self.all_checked_title()
                self.white_space()
                # if all but one player folds
                # end round, pay out money to winner, remove broke players
                if self.fold_check():
                    self.dealer.broke_player_find_remove()
                    self.dealer.end_game_statuses()
                    self.dealer.print_remaining_players_info()
                    # if round ends from fold and still more than one player left
                    # give option to continue playing or return to menu
                    if len(self.dealer.player_list) >= 2:
                        selection = self.back_to_menu()
                        while selection == 3 or selection == 4:
                            if selection == 3:
                                self.player1.bots_only()  
                            elif selection == 4:
                                self.wait_mode()
                            selection = self.back_to_menu() 
                            if selection == 7:
                                self.menu_mode()
                        if selection == 1:
                            continue   
                        if selection == 2:
                            break
                    # if round ends and only one payer left
                    # print victory info, loop will end after this at loop check
                    if self.dealer.last_man_standing():
                        self.dealer.print_last_man()
                        self.print_game_count()
                    continue            
            else:
                self.bet_skip_title()
            self.card_reveal_title()
            self.dealer.show_computer_scores_and_hands()
            if not self.dealer.all_computer_players:
                self.player1.print_name_score()
                self.player1.print_hand()
            self.dealer.compare_scores()

        #  PAYOUT

            self.pot.payout(self.dealer.player_list)
            self.dealer.print_results()
            if waits:
                self.wait_mode_input()
            # reset win to false for all
            self.dealer.reset_bet_statuses()
            # remove players with no money
            self.dealer.broke_player_find_remove()
            self.dealer.end_game_statuses()
            # if only one player remains
            if self.dealer.last_man_standing():
                self.dealer.print_last_man()
                self.print_game_count()
                if waits:
                    self.wait_mode_input()
                break
            # if human player out but computer players still in
            if not self.dealer.human_friend_left():
                self.dealer.human_loses()
            # if anyone goes broke and is removed from game, display that. 
            self.dealer.print_broke_players()
            self.dealer.print_remaining_players_info()
            # give option to leave the table here
            self.print_game_count()
            if len(self.dealer.player_list) >= 2:
                selection = self.back_to_menu()
                while selection == 3 or selection == 4:
                    if selection == 3:
                        self.player1.bots_only()  
                    elif selection == 4:
                        self.wait_mode()
                    selection = self.back_to_menu() 
                if selection == 7:
                    self.menu_mode()
                if selection == 1:
                    continue   
                if selection == 2:
                    break

    def get_name(self) -> object:
        '''
            Gets player's name of an apppropriate length.
            Length limited by menu width limits. 
        '''
        print('  Your name: ', end='')
        # human player
        player1 = Player()
        player1.human = True
        player1.name = input('')
        while 1 > len(player1.name) < 10:
            print('  Enter a better sized name:', end=' ')
            player1.name = input('')
        return player1

    def get_num_opp(self) -> int:
        '''
            Gets number of opponents desired. 
            5 plyers max (4 opponents max)
        '''
        print('  Number of opponents? (4 max) ', end='')
        num_players = input()
        while not num_players.isnumeric() or int(num_players) > 4:
            print('  Enter a number 1 - 4', end=' ')
            num_players = input()
        num_players = int(num_players)
        return num_players

    def new_cards_title(self) -> None:
        '''
            Title indicating that new cards from the deck
            after the card exchange are being displayed.
        '''
        if not self.player1.fold:
            print()
            print(f"{'NEW CARDS':>63}")
            print()

    def print_pot(self) -> None:
        '''
            Displays the total pot amount in the current game. 
        '''
        print()
        string = 'TOTAL POT: $'+(str(self.pot.total))
        print(f'{string:>63}')
    
    def replacing_title(self) -> None:
        '''
            Title indicating that the card exchange is about to take place.
        '''
        print()
        print(f"{' EXCHANGING CARDS':>64}")
        print()
   
    def options(self) -> int:
        '''
            Main menu options

            1.  Start a new game with the current number of opponents,
                current wait-mode, and current human/bots mode.
            2.  Select number of opponents (4 opp max)
            3.  Turn bots-only on or off. 
                Bots only will let computer play itself.
                no hidden cards with bots-only. 
                Player has option to rejoin as human. 
            4.  Turning wait-mode off will speed up game-play in that user input 
                will no longer be required to step through priting information on 
                screen.
            7.  'Let Computer Play Uninterrupted Until One Remains' will 
                also remove the end game menu and play as many games in a 
                row as required to get to one player remaining. 
            5.  Show deck shows an entire deck of cards (created from a new Deck object). 
            6.  Quit. Exits the game.
        '''
        print()
        if self.counter == 0:
            player_str = 'WELCOME, ' + self.player1.name.upper()
            print(f"{player_str:>63}")
            print()
        options_string = ' ' + self.player1.name.upper() + '\'s OPTIONS'
        print('', '-' * 63)
        print(options_string)
        print('', '-' * 63)
        print()
        print(' 1) Start New Game')
        print(' 2) Change Number of Opponents', end = ' ')
        print(f"({self.player1.opponents - 1})")
        print(' 3) Turn Bots-Only Mode on/off', end=' ')
        if self.player1.human:
            print('(OFF)')
        else:
            print('(ON)')
        print(' 4) Turn Wait-Mode on/off', end=' ')
        if waits:
            print('(ON)')
            
        else:
            print('(OFF)')
            if not self.player1.human: 
                print('    7) Let Computer Play Uninterrupted Until One Remains', end=' ')
                if self.menu_off:
                    print('(ON)')
                else:
                    print('(OFF)')  
        print(' 5) Show deck')
        print(' 6) Quit')
        print()
        valid = ['1', '2','3','4', '5', '6', '7']
        print(' selection:', end= ' ')
        selection = input()
        while selection not in valid:
            print(' selection:', end= ' ')
            selection = input()
        print('', '-' * 63)
        print()
        self.counter += 1
        return int(selection)

    def print_game_count(self) -> None:
        if self.menu_off:
            print()
            print()
            print(' Total Games Played:', self.counter)

    def show_hands_flow(self) -> None:
        self.dealer.print_hands()
        # show human's hand
        if self.player1.human and not self.player1.broke:
            self.player1.sort_hand()
            self.player1.print_name_score()
            self.player1.print_hand()
            print()

    def show_new_cards_flow(self) -> None:
        if self.player1.human and not self.player1.broke:
            self.new_cards_title()
            self.player1.print_new_cards()
            self.player1.sort_hand()
            self.player1.print_name_score()
            self.player1.print_hand()
        # if all computer players, show new hands
        if self.dealer.all_computer_players:
            self.new_cards_title()
            self.dealer.show_computer_scores_and_hands()

    def start_duties_flow(self) -> None:
        # dealer deals and shuffles
        new_deck = Deck().create_deck()
        self.dealer.full_deck = new_deck
        self.dealer.shuffle_players()
        self.dealer.shuffle_deck()
        self.dealer.deal_hands()
        self.dealer.assign_hands()
        self.dealer.assign_scores()
        # check to see if a human present or not
        self.dealer.all_computer_players_check()

    def start_info(self) -> None: 
        print()
        if self.counter == 0:
            self.player1 = self.get_name()
            self.og_name = self.player1.name
        self.pot = Pot()
        self.player1 = Player()
        self.player1.name = self.og_name
        self.player1.human = True
        self.dealer = self.create_dealer()
        print()
        num_players = 2
        self.player1.opponents = num_players
        self.dealer.human_friend = self.player1
        self.dealer.num_players = num_players  
        self.dealer.create_player_list(self.player1)
        
    def menu_mode(self) -> None:
        if self.menu_off:
            self.menu_off = False
        else:
            self.menu_off = True

    def menu_show_deck(self) -> None:

        display_deck = Deck().create_deck()
        new_dealer = Dealer(display_deck)
        print()
        print()
        new_dealer.print_deck()
        print()

    def num_players_update(self) -> None:

        num_players = self.get_num_opp() + 1
        self.player1.opponents = num_players
        self.dealer.num_players = num_players
        self.dealer.player_list = []
        self.dealer.create_player_list(self.player1)

    def wait_mode(self) -> None:
       
        global waits
        if waits:
            waits = False
        else:
            waits = True

    def wait_mode_input(self) -> None:
       
        global waits
        wait = input()
        if wait == 'q':
            waits = False

    def welcome_screen(self) -> None:

        print()
        Dealer().menu_cards()

    def white_space(self) -> None:

        print()
        print()      


 
class Pot:

    def __init__(self, total:int = 0):
        self.total = total
   
    def update_pot(self, bet) -> None:
        '''
            Updates the game pot with the current player's bet.
        '''
        self.total += bet
    
    def payout(self, player_list) -> None:
        '''
            Pays out money to the winner.
            If tie, divides money evenly between the winners. 
        '''
        tied_players = []
        for player in player_list:
            if player.tie:
                tied_players.append(player)
        for player in tied_players:
            split_pot = (self.total // (len(tied_players)))
            player.money += split_pot
        else:
            for player in player_list:
                if player.win:
                    player.money += self.total   
        self.total -= self.total

    def print_pot(self) -> None: 
        '''
            Prints pot info during gameplay.
        '''
        pot_string = 'POT $' + str(self.total)
        print(f"{pot_string:^65}")         

 
        
class Player:
    def __init__(self, name:str = 'unknown', money:int = 100, hand:list = [] , score:int = 0, high_card:int = 0, win:bool = False, tie:bool = False, fold:bool = False, call:bool = False, bet:int = 0, human:bool = False, raised:bool = False, raise_amnt:int = 0, total_bet_amnt:int = 0, needs_to_bet:bool = True, old_bet_amnt:int = 0, remove:list = [], last_man_standing:bool = False, cards_to_discard:list = [], opponents:int = 0, broke:bool = False, first_to_bet:bool = False, call_amnt:int = 0):
        self.name = name
        self.money = money
        self.hand = hand
        self.score = score 
        self.high_card = high_card
        self.win = win
        self.tie = tie
        self.call = call
        self.fold = fold
        self.bet = bet
        self.human = human
        self.raised = raised
        self.raise_amnt = raise_amnt
        self.total_bet_amnt = total_bet_amnt
        self.needs_to_bet = needs_to_bet
        self.old_bet_amnt = old_bet_amnt
        self.remove = remove
        self.last_man_standing = last_man_standing
        self.cards_to_discard = cards_to_discard
        self.opponents = opponents
        self.broke = broke
        self.first_to_bet = first_to_bet
        self.call_amnt = call_amnt
        
        self.hand_score_dict = {

            8 : "Straight Flush",
            7 : "Four Kind",
            6 : "Full House",
            5 : "Flush",
            4 : "Straight",
            3 : "Three Kind",
            2 : "Two Pair",
            1 : "One Pair",
            0 : "Nothing"

        }

    def bots_only(self) -> None:
        '''
            Used to determine if a human player is present or not.
            Gameplay functions will differ if bots-only vs human present.
        '''
        if self.human:
            self.human = False
        elif not self.human:
            self.human = True

    def build_cards(self) -> None:
        '''
            builds the card matrix based on how many cards
            are currently present in the player's hand.
        '''
        # builds the matrix in which cards are printed
        card_matrix_row = []
        self.card_matrix = []
        white_space = ' '
        card_gap = ' '
        border = '\''
        card_height = 9
        card_width = 11
        num_cards = len(self.hand)
        i=0 # rows mover
        column = ((card_gap + border + (white_space * (card_width-2)) + border + card_gap) * num_cards)
        while i in range(card_height):
            # fill in column in matrix
            for space in column:
                card_matrix_row.append(space)
            self.card_matrix.append(card_matrix_row)
            card_matrix_row = []
            i += 1
        bottom_row = card_height
        top_row = 0
        column_mover = 1
        for card in self.hand:
            for space in self.card_matrix[0][0:card_width]:
                self.card_matrix[top_row][column_mover] = border
                self.card_matrix[bottom_row-1][column_mover] = border
                column_mover += 1
            column_mover += len(card_gap)+1

    def buil_new_cards(self) -> None:
        '''
            Builds the card matrix to display the new cards
            being given to the player. 
        '''
        if not self.fold:
            # builds the matrix in which cards are printed
            card_matrix_row = []
            self.card_matrix = []
            white_space = ' '
            card_gap = ' '
            border = '\''
            card_height = 9
            card_width = 11
            num_cards = len(self.new_cards)
            i=0 # rows mover
            column = ((card_gap + border + (white_space * (card_width-2)) + border + card_gap) * num_cards)
            while i in range(card_height):
                # fill in column in matrix
                for space in column:
                    card_matrix_row.append(space)
                self.card_matrix.append(card_matrix_row)
                card_matrix_row = []
                i += 1
            bottom_row = card_height
            top_row = 0
            column_mover = 1
            for card in self.new_cards:
                for space in self.card_matrix[0][0:card_width]:
                    self.card_matrix[top_row][column_mover] = border
                    self.card_matrix[bottom_row-1][column_mover] = border
                    column_mover += 1
                column_mover += len(card_gap)+1

    def card_matrix_fill(self) -> None:
        '''
            Fill the card matrix with player's card info.
        '''
        top_left_mark = 2
        middle_mark = 4
        bottom_mark = 6
        top_left_mover = 4
        middle_mover = 6
        bottom_right_mover = 8 
        for self.suit, self.rank in self.rank_suit:
            if self.rank == 10:
                # use another index space for the extra digit if 10 
                self.card_matrix[top_left_mark][top_left_mover] = 1 
                self.card_matrix[top_left_mark][top_left_mover+1] = 0 
                self.card_matrix[middle_mark][middle_mover] = self.suit
                self.card_matrix[bottom_mark][bottom_right_mover-1] = 1
                self.card_matrix[bottom_mark][bottom_right_mover] = 0
            else:
                self.card_matrix[top_left_mark][top_left_mover] = self.rank 
                self.card_matrix[middle_mark][middle_mover] = self.suit
                self.card_matrix[bottom_mark][bottom_right_mover] = self.rank   
            # move right, along the column
            top_left_mover += 13
            middle_mover += 13
            bottom_right_mover += 13     

    def total_raise_calc(self, dealer) -> int:
        '''
            Determines how much other players have raised. Used in calculating how much current player needs to call. 
        '''
        total_raise = []
        for player in dealer.player_list:
            if player.raised == True and player != self:
                total_raise.append(player.raise_amnt)
        return total_raise

    def call_raise_fold(self, dealer) -> None:
        '''
            During betting round this function asks human player
            how they want to respond to the computer's betting
            action.
        '''
        total_raise = self.total_raise_calc(dealer)
        raised_string = 'YOU WERE RAISED $' + str(sum(total_raise))
        have_string = 'YOU HAVE $' + str(self.money)
        initial_bet = ' ' + 'CALL AMOUNT: $' + str(dealer.last_person_to_bet.bet)
        if self.money == 0:
            self.call = True
            self.raised = False
            return
        print()
        print()
        # player will be responding to the computer's ante
        if dealer.in_round_counter == 1:
            print(f"{initial_bet}", end = ' | ')
            print(f"{have_string}")
        else:
            print(f" {raised_string}", end = ' | ')
            print(f"{have_string}")
        print()
        self.print_name_score()
        self.print_hand()
        print()
        print(' (C)ALL | (R)AISE | (F)OLD', end=' ')
        valid_input = ['c','r','f']
        call_raise_fold = input()
        while not call_raise_fold.isalpha() or call_raise_fold.lower() not in valid_input:
            print(' (C)ALL | (R)AISE | (F)OLD', end=' ')
            call_raise_fold = input()
        call_raise_fold = call_raise_fold.lower()
        if call_raise_fold == 'c':
            self.call = True
            self.raised = False
        elif call_raise_fold == 'f':
            self.fold = True
            self.call = False
            self.raised = False
        elif call_raise_fold == 'r':
            self.raised = True
            self.call = False

    def cards_replace_request(self) -> None :
        '''
            Accepts input from user to determine which cards
            they want to replace. Users can enter the number
            of the card they want to replace (seperated by spaces).
            order does not matter. 
        '''
        if not self.fold:
            print('','-' * 63)
            print(f"{'Enter card(s) to replace: ':>53}", end='')
            # put input into a list (spaces separating)
            remove_input = input().split(' ')
            # convert input to integer if number / less than/equal to 5
            removed = [int(i) for i in remove_input if i.isnumeric() and int(i) <= 5]
            # check to see no duplicate replacement requests
            self.remove = []
            for i in removed:
                if i not in self.remove:
                    self.remove.append(i)
            while len(self.remove) != len(remove_input):
                print(f"{'Enter card(s) to replace: ':>53}", end='')
                remove_input = input().split(' ')
                removed = [int(i) for i in remove_input if i.isnumeric() and int(i) <= 5]
                self.remove = []
                for i in removed:
                    if i not in self.remove:
                        self.remove.append(i)
            # if 0 entered with other numbers, ignore 0
            if len(self.remove) > 1 and 0 in self.remove:
                self.remove.remove(0)   

    def computer_bet_ai(self, dealer) -> bool:
        '''
            The logic the computer uses to decide whether
            to call, raise, or fold. 
        '''
        
        #  CHANCE FOR CALL/RAISE/FOLD/ALL-IN AND SIZE OF RAISE
        #  DEPENDS ON PLAYER SCORE

        chance = random.randint(0,100)
        
        if self.score == 0:
            # 75/20 chance to call or fold if nothing
            if chance in range(0,75):
                self.fold = True
                self.call = False
                self.raised = False
            elif chance in range(75,95):
                self.call = True
                self.raised = False
            # 5% chance to raise for someone who has nothing
            else:
                self.raised = True
                self.call = False
        elif self.score == 1:
            # 25% chance to raise if score is 1
            # 75 % chance to call
            if chance in range(0,75):
                self.call = True 
                self.raised = False
            else:
                self.raised = True 
                self.call = False
        elif self.score == 2:
            # 40% chance to raise if score is 2
            # 60 % chance to call
            if chance in range(0,60):
                self.call = True 
                self.raised = False
            else:
                self.raised = True 
                self.call = False   
        elif self.score == 3:
            # 60% chance to raise if score is 3 or more
            # 40% chance to call
            if chance in range(0,40):
                self.call = True 
                self.raised = False
            else:
                self.raised = True 
                self.call = False
        elif self.score == 4:
            # 70% chance to raise if score is 3 or more
            # 30% chance to call
            if chance in range(0,30):
                self.call = True 
                self.raised = False
            else:
                self.raised = True 
                self.call = False
        elif self.score >=5:
            # 80% chance to raise if score is 3 or more
            # 20% chance to call
            if chance in range(0,20):
                self.call = True 
                self.raised = False
            else:
                self.raised = True 
                self.call = False

    def computer_replace(self, new_deck:list, dealer) -> None:
        '''
            The logic the computer uses to decide which 
            cards to replace.
        '''
        self.old_hand = self.hand
        # going to first collect all the cards that need to be discarded.
        discard_rank_value = [] 
        rank_list = [0] * 14 
        for card in self.hand:
            rank_list[card[0]] += 1
        # ^ to see how many cards are at which value 
        # index values of rank_list = card values 
        if self.score == 3: 
        # Three of a kind 
            for index in range(len(rank_list)): # replace 2
            # get the value of the two cards...
            # not in three pair to try for four of a kind
                if rank_list[index] == 1:  
                    discard_rank_value.append(index)   
        elif self.score == 2: 
        # two of a kind, replace 1 
            for index in range(len(rank_list)):
            # get the value of the one card not in two pair
                if rank_list[index] == 1: 
                    discard_rank_value.append(index)
        elif self.score == 1: 
        # one pair,  replace 3 
            for index in range(len(rank_list)):
            # get the value of the three cards not in the pair
                if rank_list[index] == 1:
                    discard_rank_value.append(index)
        elif self.score == 0: 
            # replace 4, keep high card
            rank_list.pop(self.high_card) 
            # discard the rest
            for index in range(len(rank_list)):
                if rank_list[index] == 1: 
                    discard_rank_value.append(index)
        # now compare current hand to the cards marked for deletion
        self.cards_to_discard = [] # actual cards needing to be replaced
        for card in self.hand:
            if card[0] in discard_rank_value:
                self.cards_to_discard.append(card)
        cards_to_keep = [] 
        for card in self.hand: 
            # ignore what is shared
            if card not in self.cards_to_discard: 
            # keep what was not in discard list 
                cards_to_keep.append(card) 
        for index in range(len(discard_rank_value)):
            cards_to_keep.append(new_deck.pop(0))
        self.hand = self.cards_to_discard

        self.print_computer_replace_info()
        if dealer.all_computer_players:
            self.print_hand()
        else:
            self.print_hidden_hand()
        self.hand = cards_to_keep

    def get_bet(self, dealer) -> int:
        '''
            Gets bet information from human player.
        '''
        #  WHEN HUMAN FIRST-TO-BET :
        
        #  MONEY STATUS STRINGS

        print('\n','-' * 63)
        string = 'PURSE: $'+(str(self.money))+ ' | BET $'
        string_extra_help = 'PURSE: $'+(str(self.money))+ ' | BET $ ($10 min / multiples of 5 only)'
        if dealer.betting_round_counter != 0:
            string_extra_help = 'PURSE: $'+(str(self.money))+ ' | BET $ (multiples of 5 only, no minimum)'
            
        #  IF FIRST ROUND, DISPLAY MIN BET REQUIRED 

        if dealer.betting_round_counter == 0:
            string = 'PURSE: $'+(str(self.money))+ ' | BET $ ($10 min)'
        print(f"{string:>60}", end= ' ')
        self.bet = input()
        
        # bet must be a number, must be within your purse,cannot be below 10 if starting the round in the first round and must be a multiple of 5. 
        while not self.bet.isnumeric() or int(self.bet) > self.money or (self.first_to_bet and int(self.bet) < 10 and dealer.betting_round_counter == 0) or (int(self.bet) % 5 > 0):
            print(f"{string_extra_help:>60}",end=' ')     
            self.bet = input()
        print()
        print()
        self.bet = int(self.bet)    
        self.money -= self.bet
        return self.bet

    def call_ai(self, dealer, pot) -> None:
        '''
            The logic to determine how much a player needs to call when calling. Updates the player's money and pot as well.
            May result in a computer player folding if calling 
            does not make sense.
        '''
        #call the last person to bet
        self.call_amnt = dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt
        # computer agressive betting detector
        # if you have a poor hand and the call amount 
        # is more than half your purse, high chance to fold (unless broke, then no reason to fold, call will be 0)
        chance = random.randint(0,100)
        if not self.human and not self.money == 0 and self.score < 3 and self.call_amnt > (self.money * .5) and chance in range(0,80):
            self.fold = True
            self.call = False
            return
        # for printing info
        self.bet = self.call_amnt
        # if not enough - all in
        if self.bet > self.money:
            self.bet = self.money
            self.call_amnt = self.money
            self.total_bet_amnt += self.bet
            pot.update_pot(self.bet)
            self.money -= self.bet
            dealer.round_raise_amnt += self.bet
            return
        # update pot and self money total
        self.total_bet_amnt += self.bet
        pot.update_pot(self.bet)
        self.money -= self.bet
        dealer.round_raise_amnt += self.bet
       
    def get_card_info(self) -> None:
        '''
            Gets rank and value information from cards in 
            player's hand.
        '''
        RED = "\033[0;31m"
        BLUE = "\033[0;34m"
        YELLOW = "\033[1;33m"
        ESC = "\033[0m"
        HEART = "\u2665"
        DIAMOND = "\u2666"
        GREEN = "\033[0;32m"
        CLOVER = "\u2663"
        YELLOW = "\033[1;33m"
        SPADE = "\u2660"
        FACE_CARDS = {

                1  : "A",
                11 : "J",
                12 : "Q",
                13 : "K"
            }
        SUITS =  {
                
                0: RED + HEART + ESC, 
                1: BLUE + DIAMOND + ESC, 
                2: GREEN + CLOVER + ESC, 
                3: YELLOW + SPADE + ESC
            }
        self.rank_suit = []
        for self.card in self.hand:
            self.suit = SUITS[self.card[1]] 
            # get info for each card 
            if self.card[0] in FACE_CARDS:  
                self.rank = FACE_CARDS[self.card[0]]     
            else: 
                self.rank = self.card[0]  
            rs = self.suit, self.rank
            self.rank_suit.append(rs)

    def get_new_card_info(self) -> None:
        '''
            Gets rank and value information for new cards
            given to player during card exchange.
        '''
        if not self.fold:
            RED = "\033[0;31m"
            BLUE = "\033[0;34m"
            YELLOW = "\033[1;33m"
            ESC = "\033[0m"
            HEART = "\u2665"
            DIAMOND = "\u2666"
            GREEN = "\033[0;32m"
            CLOVER = "\u2663"
            YELLOW = "\033[1;33m"
            SPADE = "\u2660"
            FACE_CARDS = {

                    1  : "A",
                    11 : "J",
                    12 : "Q",
                    13 : "K"
                }
            SUITS =  {
                    
                    0: RED + HEART + ESC, 
                    1: BLUE + DIAMOND + ESC, 
                    2: GREEN + CLOVER + ESC, 
                    3: YELLOW + SPADE + ESC
                }
            self.rank_suit = []
            for self.card in self.new_cards:
                self.suit = SUITS[self.card[1]] 
                # get info for each card 
                if self.card[0] in FACE_CARDS:  
                    self.rank = FACE_CARDS[self.card[0]]     
                else: 
                    self.rank = self.card[0]  
                rs = self.suit, self.rank
                self.rank_suit.append(rs) 

    def organize_by_suit(self) -> None:
        '''
            Organizes a player's hand by suit.
        '''
        # for sorting purposes
        self.card_dic = {}
        for card in self.hand:
            # suits made to be the keys
            if card[1] not in self.card_dic:
                self.card_dic[card[1]] = [card[0]]
            else:
            # then make a list of each rank in that suit
                self.card_dic[card[1]].append(card[0])

    def organize_ranks_in_suit(self) -> None:
        '''
            After a hand has been organized by suit,
            organize the ranks within suits.
        '''
        # sort by suit, and then ranks in each suit
        self.sorted_hand = []
        # sort the dictionary keys ascending order
        # i.e. get all suits together
        self.sorted_dic = sorted(self.card_dic.items())
        # get the list from each key (values[1])
        # so then can sort the ranks in each suit
        for ranks in self.sorted_dic:
            ranks[1].sort()

    def print_bet_info(self) -> None:
        '''
            Prints the information for each player's
            bet decision.
        '''
        raised_string = 'CALLED $' + str(self.call_amnt) + ' AND RAISED $' + str(self.raise_amnt)
        call_string   = 'CALLED $' + str(self.call_amnt)
        purse_string  = 'PURSE $'  + str(self.money)
        bet_string    = 'PUT IN $' + str(self.bet)
       
        print('','-' * 63)
        print(f' {self.name.upper():<12}', end=' ')
        if self.first_to_bet and not self.fold:
            print(f"{bet_string:<37}", end = ' ')
            print(f" {purse_string}")
        elif self.call:
            print(f"{call_string:<37}", end = ' ')
            print(f" {purse_string}")
        elif self.fold:
            print(f"{'FOLDS':<37}", end = ' ')
            print(f" {purse_string}")
            print()
            self.print_folded_hand()
        elif self.raised:
            print(f"{raised_string:<37}", end = ' ')
            print(f" {purse_string}")
        print('','-' * 63)

    def print_folded_hand(self) -> None:
        '''
            Prints the display for a folded hand.
        '''
        self.build_cards()
        HEART = "\u2665"
        DIAMOND = "\u2666"
        CLOVER = "\u2663"
        SPADE = "\u2660"
        self.card_matrix[2][3] = HEART
        self.card_matrix[4][6] = 'F'
        self.card_matrix[6][9] =  HEART
        self.card_matrix[2][16] = DIAMOND
        self.card_matrix[4][19] = '0'
        self.card_matrix[6][22] = DIAMOND
        self.card_matrix[2][29] = SPADE
        self.card_matrix[4][32] = 'L'
        self.card_matrix[6][35] = SPADE   
        self.card_matrix[2][42] = CLOVER
        self.card_matrix[4][45] = 'D'
        self.card_matrix[6][48] = CLOVER
        self.card_matrix[2][55] = '$'
        self.card_matrix[4][58] = 'S'
        self.card_matrix[6][61] = '$'  
        self.print_matrix()

    def print_computer_replace_info(self) -> None:
        '''
            Prints the computers replace info during card exchange.
        '''
        if self.fold:
            print('','-' * 63)
            print(f' {self.name.upper():<13}', end = '')
            print(f"FOLDED   ${self.money} remaining ")
            print('','-' * 63)
            
        else:
            print('','-' * 63)
            print(f' {self.name.upper():<13}', end = '')
            if self.score < 4:
                print(f"{'Replacing'} {len(self.cards_to_discard)} cards...")
                print('','-' * 63)
            else:
                print(f"{'Replacing 0 cards...'}")
                print('','-' * 63)

    def print_hand(self) -> None:
        '''
            The flow of logic to print a player's hand
        '''
        if not self.fold:
            self.build_cards()
            self.get_card_info()
            self.card_matrix_fill()    
            # print the final matrix 
            self.print_matrix()
   
    def print_hidden_hand(self) -> None:
        '''
            The flow of logic to print hands face down.
        '''
        # build the matrix 
        self.build_cards()
        # print the matrix 
        self.print_matrix()

    def print_matrix(self) -> None:
        '''
            Prints the basic structure of a hand of cards.
        '''
        card_gap = ' '
        white_space = '*'
        for row in self.card_matrix:
            for index in row:
                if index == ' ':
                    #time.sleep(.001)
                    print(card_gap, end='')
                elif index == '*':
                    #time.sleep(.001)
                    print(white_space, end='') 
                else:
                    #time.sleep(.001)
                    print(index, end='')
            print()

    def print_name(self) -> None:
        '''
            Prints a player's name and their current purse.
        '''
        print('','-' * 63)
        print(f' {self.name.upper():<13}  ${self.money}')
        print('','-' * 63)

    def print_name_score(self) -> None:
        '''
            Prints a player's name and their score.
        '''
        if not self.fold:
            print('','-' * 63)
            print(f' {self.name.upper():<13}',end='')
            print(f"${self.money} | ", end = '')
            self.print_score_info()
            print('','-' * 63)

    def print_new_cards(self) -> None:
        '''
            Flow of logic to print new cards.
        '''
        if not self.fold:
            self.buil_new_cards()
            self.get_new_card_info()
            self.card_matrix_fill()
            self.print_matrix()

    def print_replace_info(self) -> None:
        '''
            Prints how many cards a human player is replacing.
        '''
        print('','-' * 63)
        print(f' {self.name.upper():<13}', end = '')
        print(f"{'Replacing'} {len(self.delenda)} cards...")
        print('','-' * 63)

    def print_score_info(self) -> None:
        '''
            Prints player's score information.
        '''
        print(f'Score: {(self.score)} - {self.hand_score_dict[self.score]} | High card: {self.high_card}')

    def put_sorted_hand_together(self) -> None:
        '''
            Final step in organizing a hand by suit and rank.
        '''
        # put the cards back together:
        for suit, ranks in self.sorted_dic:
        # get the suit and rank(s) (rank(s) still in a list) from dict
            for rank in ranks:
                card = rank, suit
                # make new list of sorted cards
                self.sorted_hand.append(card)
                self.hand = self.sorted_hand 

    def round_to_5(self) -> None:
        '''
            Used to make all bets multiples of 5.
        '''
        while self.raise_amnt % 5 > 0:
            self.raise_amnt = round(self.raise_amnt + 1)
            
    def raise_ai(self, dealer, pot) -> None:
        '''
            The flow of logic for a computer who has decided
            to raise. Computer now determines how big of a 
            raise to make.
        '''
        small_raise   = round(( self.money * .5)  // 5)
        normal_raise  = ( self.money * 1 )  // 5
        big_raise     = ( self.money * 2 )  // 5
        bigger_raise  = ( self.money * 3 )  // 5
        biggest_raise = ( self.money * 4 )  // 5

        #  DECISIONS AFFECTED BY CHANCE PERCENTAGE
        
        chance = random.randint(0,100)
        
        #  DECISION LOGIC BASED ON SCORE AND CHANCE:
        
        if self.score == 0:

            chance = random.randint(0,100)   
            if chance == (0):
                # 1 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(1,75):
                # 75% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(75,91):
                # 15% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(91,96):
                # 5% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(96,99):
                # 3% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(99,100):
                # 1% chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5()

        if self.score == 1:

            chance = random.randint(0,100)   
            if chance == (0):
                # 1 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(1,70):
                # 70% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(70,91):
                # 20% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(91,96):
                # 5% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(96,99):
                # 3% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(99,100):
                # 1% chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5()      

        if self.score == 2:

            chance = random.randint(0,100)   
            if chance == (0):
                # 1 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(1,51):
                # 50% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(51,91):
                # 40% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(91,96):
                # 5% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(96,99):
                # 3% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(99,100):
                # 1% chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5()  
    
        if self.score == 3:

            chance = random.randint(0,100)   
            if chance == (0,2):
                # 2 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(2,8):
                # 5% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(8,19):
                # 10% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(19,40):
                # 20% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(40,81):
                # 40% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(81,100):
                # 18% chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5()  

        if self.score == 4:

            chance = random.randint(0,100)   
            if chance == (0,4):
                # 3 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(4,8):
                # 3% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(8,14):
                # 5% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(14,30):
                # 15% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(30,71):
                # 40% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(71,100):
                # 28 % chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5() 

        if self.score >= 5:

            chance = random.randint(0,100)   
            if chance == (0,4):
                # 3 % chance to go all in
                self.raise_amnt = self.money
            elif chance in range(4,8):
                # 3% chance for a small raise
                self.raise_amnt = small_raise
                self.round_to_5()
            elif chance in range(8,14):
                # 5% chance for a normal raise
                self.raise_amnt = normal_raise
                self.round_to_5()
            elif chance in range(14,30):
                # 15% chance for a big raise
                self.raise_amnt = big_raise
                self.round_to_5()
            elif chance in range(30,49):
                # 20% chance for a bigger raise
                self.raise_amnt = bigger_raise
                self.round_to_5()
            elif chance in range(49,100):
                # 50 % chance for biggest raise
                self.raise_amnt = biggest_raise
                self.round_to_5()

        #  LOGIC FOR SITIUATIONS IN WHICH RAISING DOES NOT MAKE SENSE OR THE RAISE AMOUNT DOES NOT MAKE SENSE:

            # no point in a computer player raising when no one else has money 
            # or raising more money than anyone else has.
            # check for max amount (or zero amount) here
        
        max_money = 0
        # go through the player's list
        if self.first_to_bet:
            for player in dealer.player_list:
                # if player has folded skip, if player is done betting (why? I forgot)
                if not player.fold and player != self:
                    if player.money > max_money:
                        max_money = player.money
        else:
            for player in dealer.player_list:
                if not player.needs_to_bet and not player.fold:
                    if player != self:
                        if player.money > max_money:
                            max_money = player.money
        # if no one has money, no point in raising. just call if need to do that. 
        if max_money == 0:
            self.call = True
            self.raised = False
            return   
        # if others have money and your raise is more, limit raise to their max purse amnt.  
        if self.raise_amnt > max_money:
            self.raise_amnt = max_money
        # this might be redundant, but if a rounding error or something results in 0:
        if self.raise_amnt == 0:
            self.call = True
            self.raised = False
            return   
        # if first to bet in the round, no other players data needed
        self.bet = self.raise_amnt
        self.old_bet_amnt += self.bet
        if not self.first_to_bet:
            self.old_bet_amnt += self.bet
            # call amnt for print info
            self.call_amnt = dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt
            self.bet = dealer.last_person_to_bet.total_bet_amnt + self.raise_amnt - self.total_bet_amnt
        # if player can't afford their raise, put in as much as they can. 
        # if self.money > dealer.last_person_to_bet.bet and self.bet > self.money:	
        if self.bet > self.money:
            self.call = True
            self.raised = False
            #self.bet = self.money
            return
        
        #  IF VALID RAISE, UPDATE POT AND BET INFO

        pot.update_pot(self.bet)
        self.total_bet_amnt += self.bet
        self.money -= self.bet
        dealer.round_raise_amnt += self.bet

    def raise_request(self, dealer, pot) -> None:    
        '''
            Raise logic for human player.
        '''
        #  IF NOT ENOUGH MONEY TO RAISE

        call_amnt = dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt
        if call_amnt >= self.money:
            print()
            print(' NOT ENOUGH MONEY TO RAISE. CALLING ')
            self.call = True
            self.raised = False
            return
        
        # GET RAISE AMOUNT // MULTIPLE OF 5

        print()
        print(' CALL AMOUNT $', call_amnt, end=' ')
        print('| ENTER RAISE $ ', end='')
        self.raise_amnt = input()
        while not self.raise_amnt.isnumeric() or int(self.raise_amnt) % 5 > 0:
            print(' ENTER RAISE (multiples of 5 only) $ ', end='')
            self.raise_amnt = input()
        self.raise_amnt = int(self.raise_amnt)
        
        #  IF NOT ENOUGH TO COVER DESIRED RAISE // ALL IN
        
        if self.money < dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt + self.raise_amnt:
            print()
            print(' NOT ENOUGH MONEY TO COVER THAT RAISE. GOIN ALL IN.')
            # raise amount = total money - call amount. 
            self.raise_amnt = self.money - ( dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt )
            
        # I think this part is redundant now // never reaches this point

        print()
        if self.raise_amnt == 0:
            self.call_ai(dealer, pot)
            self.call = True
            self.raised = False
            return
        
        #  IF VALID RAISE, UPDATE POT AND BET INFO 

        self.old_bet_amnt = self.bet
        self.bet = dealer.last_person_to_bet.total_bet_amnt + self.raise_amnt - self.total_bet_amnt
        self.call_amnt = dealer.last_person_to_bet.total_bet_amnt - self.total_bet_amnt
        pot.update_pot(self.bet)
        self.total_bet_amnt += self.bet
        self.money -= self.bet

    def replace_cards(self, new_deck:list) -> None:
        '''
            Card replace logic for human player.
        '''
        if not self.fold:

        #  IF REPLACING 0 CARDS // SHOW 'POKER' HAND

            if self.remove[0] == 0:
                self.new_cards = []
                self.delenda = []
                self.print_replace_info()
                Dealer().menu_cards()

        #  REPLACE THE SELECTED CARDS

            else:
                self.delenda = []  # card indexes selected to deletee
                self.servanda = []  # cards to keep // then updated with new cards from deck. 
                # renamed to self.hand at end
                for index in self.remove: 
                    # check which cards to remove
                    # put the removed cards in a list
                    self.delenda.append(self.hand[index-1]) 
                for card in self.hand: # check which cards to keep 
                    # if the card in current hand not in the cards to be removed, 
                    # keep it // discard rest
                    if card not in self.delenda:
                        self.servanda.append(card)

        #  SHOW THE CARDS PULLED FROM THE HAND ON SCREEN (FACE UP/DOWN DEPENDING)

                self.hand = self.delenda
                self.print_replace_info()
                self.print_hand()
                # add new cards from deck
                for cards in self.remove:
                    self.servanda.append(new_deck.pop(0))
        
        #  COMPLETE REPALCEMENT

                self.hand = self.servanda
                self.new_cards = self.hand[-len(self.remove):]

    def sort_hand(self) -> None:
       '''
          Flow of logic to sort a hand by suit and rank.
       '''
       if not self.fold:
            # sort by suit, then sort by rank in each suit
            self.organize_by_suit()
            self.organize_ranks_in_suit()
            self.put_sorted_hand_together()

    def wait_mode(self) -> None:
        '''
            Turn wait mode on/off.
        '''
        global waits
        if waits:
            waits = False
        else:
            waits = True

    def wait_mode_input(self) -> None:
        '''
            Secret option to disable wait mode in
            middle of the game.
        '''
        global waits
        wait = input()
        if wait == 'q':
            waits = False



class Deck:

    def __init__(self):
        pass
     
    def create_deck(self) -> list[tuple]:  
        '''
            Creates a deck of 52 cards.

            Returns (list):
                Returns a list of 52 tuple pairs.  
        '''
        RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13) 
        full_deck = [] 
        # list for full deck of tuples 
        suit = 0  
        # nested loop mover
        while suit in range(4): 
            # for each suit ...
            for number in RANKS:   
                card_tuple = number, suit 
                #... add ranks. 
                full_deck.append(card_tuple) 
                # append each card to full_deck list
            suit+=1
        return full_deck


           
class Dealer(Player):
    def __init__(self, full_deck:list = [], num_players = 0, has_bet:list =[], needs_to_bet:list =[],betting_round_counter:int = 0, round_raise_amnt:int = 0, in_round_counter:int = 0, last_person_to_bet:object = 'unknown', folded_players:list = [], broke_players:list = [], all_folded:bool = False, winner:object = 'unknown', all_computer_players:bool = False, computer_names = {}):
        self.full_deck = full_deck
        self.num_players = num_players
        self.has_bet = has_bet
        self.needs_to_bet = needs_to_bet
        self.betting_round_counter = betting_round_counter
        self.round_raise_amnt = round_raise_amnt
        self.in_round_counter = in_round_counter
        self.last_person_to_bet = last_person_to_bet
        self.folded_players = folded_players
        self.broke_players = broke_players
        self.all_folded = all_folded
        self.winner = winner
        self.all_computer_players = all_computer_players
        self.computer_names = computer_names

        self.computer_names = {

            1 : 'Lizzo',
            2 : 'Caesar',
            3 : 'Theo',
            4 : 'Moose',
            5 : 'Stella',
            6 : 'Hannibal',
            7 : 'Piccard',
            8 : 'Ms Tarzan',
            9 : 'Galena'

        }

    def all_computer_players_check(self) -> bool:
        '''
            Checks to see if only computer players present.
            If so, bots-only mode enabled.
        '''
        comp_players = [player for player in self.player_list if not player.human or player.broke]  
        if len(comp_players) == len(self.player_list):
            self.all_computer_players = True
        else:
            self.all_computer_players = False
    
    def all_fold_check(self) -> bool:
        
        fold_list = [player for player in self.player_list if not player.human and player.fold]
        if len(fold_list) == len(self.player_list) - 1:
            return True

    def anyone_have_money(self) -> bool:
        
        players_with_money = [player for player in self.player_list if not player.fold and player.money > 0]
        # only bet if more than one person has money
        if len(players_with_money) > 1:
            return True

    def assign_hands(self) -> None:
        # give hand to each player 
        i=0
        for player in self.player_list:
            player.hand = self.hands_for_score[i]
            i+=1        

    def assign_scores(self) -> None:
        for player in self.player_list:
            if not player.fold:
                player.score = Score(player.hand).score_hand()
                player.high_card = Score(player.hand).high_card()

    def broke_player_find_remove(self) -> None:
        self.broke_players = [player for player in self.player_list if player.money == 0]
        for player in self.broke_players:
            player.broke = True
            self.player_list.remove(player)

    def create_player_list(self, player1) -> None:
        self.player_list = []
        # add human to list
        self.player_list.append(player1)
        # randomly assign computer names
        random_int_cache = []
        index = 0
        while index in range(self.num_players-1):
            player = str(index)
            player = Player()
            rand_selection = random.randint(1,9)
            if rand_selection not in random_int_cache:
                player.name = self.computer_names[rand_selection]
                random_int_cache.append(rand_selection)
                self.player_list.append(player)
                index+=1
            else:
                continue
     
    def compare_scores(self) -> str:
        scores_dic = {}

        #  GET EACH PLAYER'S SCORE // INFO

        scores = [(player.score, player.name, player.high_card, player) for player in self.player_list if not player.fold]
        # put info into dict: keys  =  scores 
        for info in scores:
            score = info[0] 
            name  = info[1] 
            high_card = info[2]  
            player_instance = info[3]
            if score not in scores_dic:
                scores_dic[score] = [(name, high_card, score, player_instance)]
            else:
                scores_dic[score].append([name, high_card, score, 
                player_instance])
       
       #  IF NO TIES
      
        winner = max(scores_dic)
        # if there is NOT more than one person in the max score spot :
        if len(scores_dic[winner]) == 1:
            # print information
            self.winner = scores_dic[winner]
            # assign win = True to winning player's instance
            self.winner[0][3].win = True
            return 'win_no_tie'
        
        # IF TIE

            # if score 4 or more, pot is split. If 3 or under, high card determines winner. 
        
        elif len(scores_dic[winner]) > 1 and max(scores_dic) < 4:    
            potential_winner = []
            high_card_ties = []
            # check to see which of the winners has a higher high_card
            high_card = 0
            # data is tuple of score, high_card, full_hand, player_instance
            for data in scores_dic[winner]:
                # data[1] = high card
                if data[1] >= high_card:
                    # add high card to list
                    potential_winner.append(data)
                    # their high card becomes the new high
                    high_card = data[1]
            # see if anyone else had same high card/
            # if so, append to high_card_ties list
            highest_high_card = potential_winner[-1]
            i=0
            for i in range(len(potential_winner)):
                if potential_winner[i][1] == highest_high_card[1]:
                    high_card_ties.append(potential_winner[i])
                    i+=1
            
        # LEGITIMATE TIE

                # if more than one person have same high score and same high_card, then tie. 
                # return list of ties     
                    
            if len(high_card_ties) > 1:
                # dealer assigns ties
                self.ties_list = high_card_ties
                for player in high_card_ties:
                # player instance assigned tie value
                # earn half pot
                    player[3].tie = True
                return 'tie' 
        
        # HIGH CARD TIE WINNER

            # if only one_high_card, then...
      
            self.winner = potential_winner[-1]
            # player isntance assigned winner value
            # earn full pot
            potential_winner[-1][3].win = True
            # tie_winner = tuple
            return 'tie_winner' 

    def deal_hands(self) -> None:
        # up to 5 players
        # dictionary for one card per one person dealing
        hands_in_play_dict = {1:[],2:[],3:[],4:[],5:[]}
        for card in range(5): #nuber of cards per hand
            for player in range(1, self.num_players+1): 
             # remove first card in deck, put in dictionary, move index each time to new player
                hands_in_play_dict [player].append(self.full_deck.pop(0)) 
        # form full hands from the dictionary
        self.hands_for_score = []
        hand = []
        for index in range(1, self.num_players+1):
            for card in hands_in_play_dict[index]:
                hand.append(card)
            self.hands_for_score.append(hand)
            hand = [] # empty the container

    def end_game_statuses(self) -> None:

        #  RESET ALL DEALER AND PLAYER STATS


        self.has_bet = []
        self.needs_to_bet = []
        self.betting_round_counter = 0
        self.round_raise_amnt = 0
        self.in_round_counter = 0
        self.last_person_to_bet = 'unkown'  
        self.folded_players = []
        self.winner = 'unknown'
        self.all_folded = False
        # only data that shouldn't reset is player's money.
        for player in self.player_list:
            player.call = False
            player.fold = False
            player.needs_to_bet = False
            player.tie = False
            player.win = False
            player.raised = False
            player.bet = 0
            player.high_card = ''
            player.raise_amnt = 0
            player.score = 0
            player.old_bet_amnt = 0
            player.total_bet_amnt = 0
            player.hand = []
            player.remove = []
            player.last_man_standing = False
            player.cards_to_discard = []
            player.first_to_bet = False
            player.call_amn = 0
 
    def hands_clear(self) -> None:
        for player in self.player_list:
            player.hand = []

    def last_man_standing(self) -> bool:
        if len(self.player_list) == 1:
            return True
        
    def print_last_man(self) -> None:  
         for player in self.player_list:
                string = player.name.upper() + ' HAS DEFEATED ALL OPPONENTS'
                print()
                print(f"{string:^65}")
                print()

    def human_friend_left(self) -> bool:
        for player in self.player_list:
            if player.human:
                return True

    def human_loses(self) -> None:
         for player in self.player_list:
             if player.human:
                string = player.name.upper() + ', YOU\'RE BROKE AND OUT'
                print(f"{string:^65}")

    def menu_cards(self) -> None:
        self.hand = [(''),(''),(''),(''),('')]
        self.build_cards()
        RED = "\033[0;31m"
        BLUE = "\033[0;34m"
        YELLOW = "\033[1;33m"
        ESC = "\033[0m"
        HEART = "\u2665"
        DIAMOND = "\u2666"
        GREEN = "\033[0;32m"
        CLOVER = "\u2663"
        YELLOW = "\033[1;33m"
        SPADE = "\u2660"
        CYAN = "\033[0;36m"
        self.card_matrix[2][3] = RED + HEART + ESC 
        self.card_matrix[4][6] = 'P'
        self.card_matrix[6][9] = RED + HEART + ESC
        self.card_matrix[2][16] = BLUE + DIAMOND + ESC 
        self.card_matrix[4][19] = '0'
        self.card_matrix[6][22] = BLUE + DIAMOND + ESC
        self.card_matrix[2][29] = YELLOW + SPADE + ESC 
        self.card_matrix[4][32] = 'K'
        self.card_matrix[6][35] = YELLOW + SPADE + ESC    
        self.card_matrix[2][42] = GREEN + CLOVER + ESC 
        self.card_matrix[4][45] = 'E'
        self.card_matrix[6][48] = GREEN + CLOVER + ESC
        self.card_matrix[2][55] = CYAN +'$' + ESC
        self.card_matrix[4][58] = 'R'
        self.card_matrix[6][61] = CYAN +'$' + ESC  
        # print the matrix 
        self.print_matrix()

    def print_broke_players(self) -> None:
        print()
        for players in self.broke_players:
            string = players.name.upper() + ' IS BROKE AND OUT'
            print(f"{string:^65}")
            print()
        print()
    
    def print_remaining_players_info(self) -> None:
        print(f"{' REMAINING PLAYERS':>64}")
        print()
        print(' ' + '-' * 63)
        for player in self.player_list:
            money_string = '$' + str(player.money)
            print(f" {player.name.upper():<57}{money_string:>4}")
            print(' ' + '-' * 63)
        print()
        print()
        print()
        if waits:
            self.wait_mode_input()

    def print_deck(self) -> None:
        i=0 # start of hand
        e=5 # end of hand
        while i <= 52:
            # move through deck 5 cards at a time
            self.hand = self.full_deck[i:e]
            self.build_cards()
            self.get_card_info()
            self.card_matrix_fill()
            i+=5
            e+=5   
            self.print_matrix()
            print()
            # print the matrix     

    def print_hands(self) -> None:
        self.all_computer_players_check()
        # if all computer players, show cards and score info from the start
        if self.all_computer_players:
            for player in self.player_list:
                player.print_name_score()
                player.print_hand()
                if waits:
                    self.wait_mode_input()
 
        # if human preesent, hide computer info untll the end
        else:
            for player in self.player_list:
                if not player.human:
                    player.print_name()
                    player.print_hidden_hand()
                    if waits:
                        self.wait_mode_input()

    def print_results(self) -> None:
        if not self.all_folded:
            result = self.compare_scores()
        if self.all_folded:
            result = 'folded'
            for those in self.player_list:
                if those.win:
                    player = those
        if result == 'win_no_tie' or result == 'tie_winner':
            if result == 'win_no_tie':
            # get player instance 
                player = self.winner[0][3]
            if result == 'tie_winner':
                player = self.winner[3]
            print()
            print('','-' * 63)
            print(f"{'WINNER:':>9} {player.name.upper():7} | Score: {player.score} | PURSE: ${player.money} | Hand: {player.hand_score_dict[player.score]}")
            print('','-' * 63)
            print()
        if result == 'folded':
            print()
            print('','-' * 63)
            print(f"{'WINNER:':>9} {player.name.upper():7} | Score: {player.score} | PURSE: ${player.money} | Hand: {player.hand_score_dict[player.score]}")
            print('','-' * 63)
            print()
        # show which players tied
        elif result == 'tie':
            print()
            print('','-' * 63)
            for player_data in self.ties_list:
                     # get player instance from list
                     player_instance = player_data[3]
                     print(f"{'TIE:':>9} {player_instance.name.upper():<10} | Score: {player_instance.score} | High card: {player_instance.high_card} | PURSE: ${player_instance.money}")
            print('','-' * 63)

    def reset_bet_statuses(self) -> None:
        for player in self.player_list:
            player.call = False
            player.tie = False
            player.raised = False
            player.bet = 0
            player.raise_amnt = 0
            player.old_bet_amnt = 0
            player.total_bet_amnt = 0
            player.call_amnt = 0
       
    def replace_computer_cards(self, new_deck) -> None:
        for player in self.player_list:
            if not player.human and not player.fold:
                if player.score < 4:
                    player.computer_replace(new_deck, self)
                    if waits:
                        self.wait_mode_input()
                else:
                    player.print_computer_replace_info()
                    Dealer().menu_cards()
                    if waits:
                        self.wait_mode_input()                    
            
    def shuffle_deck(self) -> None:
        shuffle_times = 0 #shuffle counter
        while shuffle_times < 10000: #mix 'em good
            rand_1 = random.randint(0, len(self.full_deck)-1) 
            # get card at index of random number 1
            rand_2 = random.randint(0, len(self.full_deck)-1) 
            # get card at index of random number 1
            first_card_to_swap  = self.full_deck.pop(rand_1) 
            # take card 1 out
            self.full_deck.append(first_card_to_swap) 
            # put it at the back of the deck
            second_card_to_swap = self.full_deck.pop(rand_2)
             # take card 2 out
            self.full_deck.append(second_card_to_swap) 
            # put it at the back of the deck
            shuffle_times +=1 # repeat 

    def shuffle_players(self) -> None:
        shuffle_times = 0 #shuffle counter
        while shuffle_times < 10:
            rand_1 = random.randint(0, len(self.player_list)-1) 
            rand_2 = random.randint(0, len(self.player_list)-1) 
            first_person_to_swap  = self.player_list.pop(rand_1) 
            self.player_list.append(first_person_to_swap) 
            second_person_to_swap = self.player_list.pop(rand_2)
            self.player_list.append(second_person_to_swap) 
            shuffle_times +=1 # repeat 

    def show_computer_scores_and_hands(self) -> None:
        for player in self.player_list:
            if not player.human and not player.fold:
                player.print_name_score()
                player.sort_hand()
                player.print_hand()
                print()
                if waits:
                    self.wait_mode_input()

    def update_player_list(self) -> None:
        
        player_not_broke = [player for player in self.player_list if not player.broke]
        self.num_players = len(player_not_broke)
        self.player_list = player_not_broke

    def wait_mode(self) -> None:
        global waits
        if waits:
            waits = False
        else:
            waits = True

    def wait_mode_input(self) -> None:
        global waits
        wait = input()
        if wait == 'q':
            waits = False



class Score:
    def __init__(self, hand:list = []):
        self.hand = hand

    def straight_flush(self) -> bool:
        suit_list = []
        for card in self.hand:
            suit_list.append(card[1])
        for suit in suit_list:
            if suit != suit_list[0]:
                return False 
        rank_list = []
        for card in self.hand:
            rank_list.append(card[0])
        rank_list.sort()
        # iterate from the back 
        # if straight, the difference between 
        # each sorted cards will be 1 
        index = len(rank_list) - 1
        while index > 0:
            if rank_list[index] - rank_list[index - 1] != 1:
                return False
            else:
                index -= 1
        return True
    
    def four_of_kind(self) -> bool:
        rank_list = []
        twins = {}
        # create dictionary of keys = ranks 
        # and values = twins of those ranks
        for card in self.hand:
            rank_list.append(card[0])
        for rank in rank_list:
            if rank not in twins:
                twins[rank] = []
            else:
                twins[rank].append(rank)
        # if 3 'twins' exists (plus the one made for key)
        # 3 + 1 = 4 of a kind     
        for key in twins:
            if len(twins[key]) == 3:
                return True
        return False
    
    def full_house(self) -> bool:
        rank_list = []
        twins = {}
        # create dictionary of keys = ranks 
        # and values = twins of those ranks
        for card in self.hand:
            rank_list.append(card[0])
        for rank in rank_list:
            if rank not in twins:
                twins[rank] = []
            else:
                twins[rank].append(rank)
        for key in twins:
            # if 3 of a kind exists...
            if len(twins[key]) == 2:
            # clear that key/value...
                twins[key] = []
            # go through again and check for pair...
                for key in twins:
                    if len(twins[key]) == 1:
                        return True
        return False
        
    def flush(self) -> bool:
        suit_list = []
        for card in self.hand:
            suit_list.append(card[1])
        for suit in suit_list:
            if suit != suit_list[0]:
                return False
        return True
    
    def straight(self) -> bool:
        rank_list = []
        for card in self.hand:
            rank_list.append(card[0])
        rank_list.sort()
        index = len(rank_list) - 1
        while index > 0:
            if rank_list[index] - rank_list[index - 1] != 1:
                return False
            else:
                index -= 1
        return True
      
    def three_kind(self) -> bool:
        rank_list = []
        twins = {}
        for card in self.hand:
            rank_list.append(card[0])
        for rank in rank_list:
            if rank not in twins:
                twins[rank] = []
            else:
                twins[rank].append(rank)
        for key in twins:
            if len(twins[key]) == 2:
                return True
        return False
    
    def two_pair(self) -> bool:
        rank_list = []
        twins = {}
        for card in self.hand:
            rank_list.append(card[0])
        for rank in rank_list:
            if rank not in twins:
                twins[rank] = []
            else:
                twins[rank].append(rank)
        for key in twins:
            if len(twins[key]) == 1:
            # one pair found...
            # clear that key/value...
                twins[key] = []
            # go through again and check for second pair...
                for key in twins:
                    if len(twins[key]) == 1:
                        return True
        return False        
     
    def one_pair(self) -> bool:
        rank_list = []
        twins = {}
        for card in self.hand:
            rank_list.append(card[0])
        for rank in rank_list:
            if rank not in twins:
                twins[rank] = []
            else:
                twins[rank].append(rank)
        for key in twins:
            if len(twins[key]) == 1:
                return True
        return False

    def score_hand(self) -> int:
        if self.straight_flush():
            return 8
        elif self.four_of_kind():
            return 7
        elif self.full_house():
            return 6
        elif self.flush():
            return 5
        elif self.straight():
            return 4
        elif self.three_kind():
            return 3
        elif self.two_pair():
            return 2
        elif self.one_pair():
            return 1
        else:
            return 0

    def high_card(self) -> int:
        rank_list = []
        for card in self.hand:
            rank_list.append(card[0])
        high_card = max(rank_list)
        return high_card
