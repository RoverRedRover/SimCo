#! usr/bin/python3

''' First Simco curses screen: present a
    'main menu' of available options. This
    window could be a touchstone for the 
    application.
    RoverRedRover, 5/2020.
'''

import curses



##############################################

def menu(stdscr):

    curses.echo()

    last_row = 20
    last_col = 45
    start_row = 1
    start_col = 2

    #lines, columns, start line, start column
    main_menu = curses.newwin(
        last_row, last_col, 1, 1)

    main_menu.box()

    main_menu.addstr(
        start_row,
        start_col,
        'SIMCOMPANIES WHOLESALER ASSISTANT')

    main_menu.addstr(
        start_row + 2,
        start_col + 1,
        'MAIN MENU')

    menu_options = {
        1: 'VIEW/EDIT PRODUCTS',
        2: 'VIEW EXCHANGE PRICES',
        3: 'TBD',
        4: 'TBD',
        5: 'CLOSE MENU'
        }

    for menu_entry in menu_options:

        main_menu.addstr(
            start_row + menu_entry,
            start_col + 1,
            f'#{menu_entry}: '
                f'{menu_options[menu_entry]}')

    main_menu.addstr(
        start_row + 6,
        start_col,
        'Enter your selection:  ')

    main_menu.refresh()
    
    # event loop for main menu
    while True:

        c = chr(main_menu.getch()).lower()

        if c == '5':
            main_menu.addstr(
                start_row + 7,
                start_col,
                'Program ended. '
                'This window will close.')
            main_menu.refresh()
            curses.napms(2000)
            break

        else:
            try:
                main_menu.addstr(
                start_row + 7,
                start_col,
                menu_options[int(c)])

            except:
                main_menu.addstr(
                    7, 0,
                    'Invalid selection')
            main_menu.refresh()

        # todo restore cursor position



def src_costs(stdscr):

    last_row = 20
    last_col = 45
    start_row = 1
    start_col = 2

    #lines, columns, start line, start column
    src_costs_ui = curses.newwin(
        last_row, last_col, 1, 1)

    return


##############################################

curses.wrapper(menu)

