import array
import fcntl
import shutil
import subprocess
import termios

from PIL import Image
from rich import print as rprint

from utility.richtables import Tables

# image_path = "saves/default/exp/angry.png"
image_path = "saves/default/exp/makima/angry.png"
img = Image.open(image_path)

buf = array.array("H", [0, 0, 0, 0])
fcntl.ioctl(1, termios.TIOCGWINSZ, buf)

width = 30
height = (
    int(width * img.height / img.width) + 1
    if (int(width * img.height / img.width) != (width * img.height / img.width))
    else int(width * img.height / img.width)
)
char, lines = shutil.get_terminal_size()
displayresH = buf[3]
displayresW = buf[2]
required_lines = int(
    img.height / (((img.width / width) / (displayresW / char)) * (displayresH / lines))
)

print(f"Columns: {char}, Lines: {lines}")
print("Required lines: " + str(required_lines))
print("height: " + str(height))
print("width: " + str(width))
print("height: " + str(img.height))
print("width: " + str(img.width))

subprocess.run(["clear"])
for _ in range(lines):
    print("")
quit = input(":here you go:")
while quit != "q":
    rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
        int(lines - required_lines - 4)
    )

    ip = str(list(range(0, 150)))
    space = ""
    for _ in range(required_lines):
        for _ in range(width):
            space += " "
        space += "\n"
    rprint(Tables.table_with_emotion(ip, space))
    print("\n")
    subprocess.run(["kitten", "icat", "--place", rectangle, image_path])
    for _ in range(required_lines + 1):
        print("")
    quit = input(":here you go:")
