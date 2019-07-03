#!/bin/sh

mkdir $HOME/.diadon
cp diadon.py $HOME/.diadon
cp keys.json $HOME/.diadon
echo "alias diadon='python3 \$HOME/.diadon/diadon.py'" >> $HOME/.bashrc
source $HOME/.bashrc
