# Kuidas programmi avada?
Programmi tuleb jooksutada terminal emulatoris ja installitud peab olema kasutajaliides ncurses jaoks. Linuxi ja Maci puhul peaks kõik vajalik installeeritud olema, kuid Windowsi korral on vaja eraldi installida windows-curses kasutajaliides. Seda saab teha järgmiselt:

```
python -m pip install windows-curses
```
<br>
Juhul, kui terminal emulator ei toeta transparent väärtus, siis tuleks värvide seast kõik -1 väärtused muuta (näiteks 0 ehk musta jaoks).

```
HEAD_TEXT_BG = -1
DIR_TEXT_BG = -1
IMG_TEXT_BG = -1
ETC_TEXT_BG = -1
```

```
HEAD_TEXT_BG = 0
DIR_TEXT_BG = 0
IMG_TEXT_BG = 0
ETC_TEXT_BG = 0
```

<br>
<details>
<summary><strong>Pilt programmist</strong></summary>

![1](https://u.cubeupload.com/earl_/filemanager.png)
</details>
