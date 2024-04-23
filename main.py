'''CSC160 / Gabriel Malone / Final Project'''

import poker_fun


if __name__ == '__main__':

#  MENU AND GAMEFLOW EXECUTE

    flow = poker_fun.GameFlow()
    # get starting info
    
    flow.welcome_screen()
    flow.start_info()
    
    # execute selection
    selection = flow.options()
    while selection != 6:
        if selection == 6:
            quit()
        elif selection == 2:
            flow.num_players_update()
        elif selection == 5:
            flow.menu_show_deck()
        elif selection == 4:
            flow.wait_mode()
        elif selection == 3:
            flow.player1.bots_only()
        elif selection == 7:
            flow.menu_mode()
        elif selection == 1:
            selection = flow.game_loop()
            print()
            print()
            flow.welcome_screen()
            flow.start_info()
            flow.dealer.end_game_statuses()
            # reset wait statuses
            poker_fun.waits = True
            flow.menu_off = False
    
        selection = flow.options()