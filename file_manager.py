import os
import imghdr
import curses
from curses import wrapper
from time import sleep 

# -1. Transparent 0. Black 1. Blue 2. Green 3. Cyan 4. Red 5. Magenta 6. Brown 7. White ("Light Gray") 8. Bright Black ("Gray") 9. Bright Blue 10. Bright Green 11. Bright Cyan 12. Bright Red 13. Bright Magenta 14. Yellow 15. Bright White 
# leidub terminal emulator-eid, mis ei toeta läbipaistvat väärtust. sel juhul peaks kasutama muid väärtusi (nt. 0).
SEL_TEXT_FG = 0
SEL_TEXT_BG = 15
DIR_TEXT_FG = 11
DIR_TEXT_BG = -1
IMG_TEXT_FG = 1
IMG_TEXT_BG = -1
ETC_TEXT_FG = 15
ETC_TEXT_BG = -1

HEAD_TEXT_FG = 11
HEAD_TEXT_BG = -1

# global muutujad
current_files = None
selected = None

def files(path="."):
    # dict failitüüpide (kaust, pilt, muu) jaoks
    contents = {}
    imgs = set()
    dirs = set()
    etc = set()
    for el in os.listdir(path):
        if os.path.isdir(el):
            dirs.add(el)
            continue
        try:
            img = imghdr.what(el)
        except:
            img = 0
        if img:
            imgs.add(el)
        else: 
            etc.add(el)
    
    contents[1] = dirs
    contents[2] = imgs
    contents[3] = etc
    return contents       

# prindib kausta sisu tähestikulises järjekorras (võttes arvesse prioriteete), prioriteet: kaustad -> pildid -> muu. 
def print_menu(main_window, current_row):
    main_window.clear()
    height = n_rows - 3
    multiplier = current_row // height
    current_list = []
    j = 0

    for i in range(1, 4):
        for el in sorted(current_files[i]):
            current_list.append(el)

    # muutujad multiplier ja height aitavad üles ja alla liikuda, millal kausta sisu ei mahu vertikaalselt ekraanile.
    # muutuja selected aitab järge hoida, et millise faili/kausta peal kasutaja on. selle abil toimub ka liikumine kaustast-kaussa.
    for el in current_list[(height*multiplier):(height*(multiplier + 1))]:
        if j == current_row - multiplier*height:
                global selected 
                selected = el
                main_window.addstr(j, 10, str(el), curses.color_pair(10))
        else:
            for i in range(1, 4):
                if el in current_files[i]:
                    main_window.addstr(j, 10, str(el), curses.color_pair(i))
        j += 1
            
    main_window.refresh()

def main(stdscr):
    curses.curs_set(0)
    # värvide jaoks, default_colors võimaldab kasutada transparent (-1) väärtust.
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(10, SEL_TEXT_FG, SEL_TEXT_BG)
    curses.init_pair(1, DIR_TEXT_FG, DIR_TEXT_BG)
    curses.init_pair(2, IMG_TEXT_FG, IMG_TEXT_BG)
    curses.init_pair(3, ETC_TEXT_FG, ETC_TEXT_BG)
    curses.init_pair(4, HEAD_TEXT_FG, HEAD_TEXT_BG)

    # terminal-i akna suurus
    global n_rows, n_cols
    n_rows, n_cols = stdscr.getmaxyx()

    # praeguse kausta failid
    global current_files
    current_files = files()
    menu_len = len(current_files[1]) + len(current_files[2]) + len(current_files[3])

    # read, teksti pikkus, algus rida (lükkab alla), algus veerg (lükkab paremale)
    main_window = curses.newwin(menu_len + 1, n_cols - 10, 2, 10)
    head_window = curses.newwin(1, n_rows*3, 0, 0)

    current_row = 0

    stdscr.refresh()
    print_menu(main_window, current_row)

    
    while True:
        cwd = os.getcwd()

        # head_window on praegu asukoha jaoks (põhimõtteliselt pwd)
        head_window.clear()
        head_window.addstr(0, 1, str(cwd), curses.color_pair(4))
        head_window.refresh()
        
        # vastab ascii tabelile
        key = stdscr.getch()

        # nool üles või k - liigub üles praeguses kaustas (kõige ülemise korral läheb alla)
        if key == curses.KEY_UP or key == 107:
            if current_row > 0:
                current_row -= 1
            else:
                current_row = menu_len - 1

        # nool alla või j - liigub alla praeguses kaustas (kõige madalama korral läheb üles)
        elif key == curses.KEY_DOWN or key == 106:
            if current_row < menu_len - 1:
                current_row += 1
            else:
                current_row = 0

        # nool paremale või l - liigub edasi failistruktuuris
        elif key == curses.KEY_RIGHT or key == 108:
            if selected in current_files[1]:
                main_window.clear()
                main_window.refresh()
                new_path = os.getcwd() + "/" + selected
                os.chdir(new_path)
                current_files.clear()
                current_files = files(new_path)
                current_row = 0

                menu_len = len(current_files[1]) + len(current_files[2]) + len(current_files[3])
                main_window = curses.newwin(menu_len + 1, n_cols - 10, 2, 10)

        # nool vasakule või h - liigub tagasi failistruktuuris. kasutaja jääb valikuga samale kaustale, kust ta lahkus. vajutades pildil "h"-d, avatakse see image viewer-is (ei pruugi töötada kõigil juhtudel, mistõttu on juurde lisatud erand)
        elif key == curses.KEY_LEFT or key == 104:
            if os.path.isdir(os.getcwd() + "/" + ".."):
                prev_dir = (os.getcwd()).split("/")
                main_window.clear()
                main_window.refresh()
                new_path = os.getcwd() + "/" + ".."
                os.chdir(new_path)
                current_files.clear()
                current_files = files(new_path)
                i = 0
                for el in sorted(current_files[1]):
                    if el == prev_dir[-1]:
                        current_row = i
                        break
                    i += 1

                menu_len = len(current_files[1]) + len(current_files[2]) + len(current_files[3])
                main_window = curses.newwin(menu_len + 1, n_cols - 10, 2, 10)
            else:
                try:
                    (Image.open(os.getcwd() + "/" + selected)).show
                except:
                    pass
        
        # x - kustutab faili (küsib ka "nõrgalt" üle ehk ainult tähega "n" saab tegevust katkestada)
        elif key == 120:
            if selected in current_files[2] or selected in current_files[3]:
                main_window.clear()
                main_window.addstr(current_row, 10, str("delete " + selected + " [Y/n]"))
                main_window.refresh()
                key = stdscr.getch()
                # n
                if key == 110:
                    pass
                else:
                    os.remove(os.getcwd() + "/" + selected)
                    current_files.clear()
                    current_files = files()
                    menu_len = len(current_files[1]) + len(current_files[2]) + len(current_files[3])
                    main_window = curses.newwin(menu_len + 1, n_cols - 10, 2, 10)

        # g
        elif key == 103:
            current_row = 0

        # G
        elif key == 71:
            current_row = len(current_files[1]) + len(current_files[2]) + len(current_files[3]) - 1

        # enter
        elif key == curses.KEY_ENTER or key in [10, 13]:
            pass

        # q/z
        elif key == 113 or key == 122:
            return

        print_menu(main_window, current_row)

# taastab terminal emulator-i sätted pärast programmi sulgumist, veel seadistab värve, lülitab echo välja jne.
curses.wrapper(main)
