#! usr/bin/python3

''' First Simco curses screen: present a
    'main menu' of available options. This
    window could be a touchstone for the
    application.
    RoverRedRover, 5/2020.
'''

import curses

main_menu_options = [
    'View/edit products',
    'View Exchange prices',
    'Exit Assistant'
    ]

def draw_main_menu(window, selected_row):

    window.clear()
    window.box()

    window.addstr(
        1,     # start row
        2,     # start column
        'SIMCOMPANIES WHOLESALER ASSISTANT',
        curses.A_BOLD
        )

    window.addstr(
        2,
        2,
        'Main Menu'
        )

    start_row = 4       # need to start menu entries 4th row down

    for index, entry in enumerate(main_menu_options):

        if index + 1 == selected_row:
            window.attron(curses.color_pair(1))
            window.addstr(
                start_row + index,
                2,
                f'{entry}'
                )
            window.attroff(curses.color_pair(1))

        else:
            window.addstr(
                start_row + index,
                2,
                f'{entry}')

    window.refresh()

def draw_test_area(window, key):

    window.clear()
    window.box()

    if key == None:
        # initial display: draw window void of content.
        pass

    elif key == 10:
        window.addstr(1, 2, 'ENTER')

    else:
        window.addstr(
            1,
            2,
            f'You typed {key} aka "{chr(key)}".'
            )

    window.refresh()

def main(screen):

    # turn off blinking cursor
    curses.curs_set(0)

    # initialize color pair for selected item
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # initialize windows
    # args: rows, columns, start line, start column
    main_menu = curses.newwin(20, 45, 1, 1)
    test_area = curses.newwin(3, 45, 21, 1)

    # initialize currently selected row
    current_row = 1

    # set key to None to present initial test window
    key = None

    # event loop for main menu
    while True:

        screen.refresh()    # for some reason I have to put this here...
        draw_main_menu(main_menu, current_row)
        draw_test_area(test_area, key)

        key = screen.getch()

        if key == curses.KEY_UP and current_row == 1:
            # if press up at row 1, highlight last row
            current_row = len(main_menu_options)

        elif key == curses.KEY_UP and current_row > 1:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(main_menu_options):
            current_row += 1

        elif key == curses.KEY_DOWN and current_row == len(main_menu_options):
            # if press down at last row, highlight first row
            current_row = 1

        elif key == 10:   # i.e., Enter; curses.KEY_ENTER not working in Win10
            if main_menu_options[current_row - 1] == 'Exit Assistant':
                test_area.clear()
                test_area.box()
                test_area.addstr(1, 2, "Goodbye!")
                test_area.refresh()
                curses.napms(3000)
                break

        elif key == ord('q'):
            # kill switch for testing purposes
            break

curses.wrapper(main)
