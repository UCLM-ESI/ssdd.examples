#!/bin/bash

cd "$(dirname "$0")"

# use the virtualenv if active, or a local .venv if present
VENV=${VIRTUAL_ENV:-$PWD/.venv}
[ -f "$VENV/bin/activate" ] && ACT=". $VENV/bin/activate; " || ACT=""

tmux new-session -d -s session

tmux set-option -g mouse on
tmux setw -g monitor-activity on
tmux set-option -g visual-activity on
tmux bind-key x kill-session
tmux set-option -g set-titles off

tmux split-window -h

tmux send-keys -t session:0.0 "${ACT}make && ./server.py" C-m
tmux send-keys -t session:0.1 "${ACT}sleep 2; ./client.py localhost 2000" C-m

tmux attach-session -t session
