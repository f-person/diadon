import os

print("installing dependecies...\n\n")
os.system("pip3 install Mastodon.py")

os.system("git clone https://github.com/marekjm/diaspy && cd diaspy")
os.system("sudo python3 setup.py install && cd ..")

print("\n\nall dependecies satisfied")

os.system("mkdir ~/.diadon")
os.system("cp diadon.py ~/.diadon")
os.system("cp keys.json ~/.diadon")
os.system("cp .git ~/.diadon")

bashrc_path = os.path.expanduser("~") + "/.bashrc"

with open(bashrc_path, "a") as bashrc:
    bashrc.write("alias diadon='python3 ~/.diadon/diadon.py'")

os.system(". {}".format(bashrc_path))

print("all done. now just type diadon or diadon -h to get help")
