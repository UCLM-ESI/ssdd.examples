#!/bin/bash

cd "$(dirname "$0")"

tmux new-session -d -s session

tmux set-option -g mouse on
tmux setw -g monitor-activity on
tmux set-option -g visual-activity on
tmux bind-key x kill-session
tmux set-option -g set-titles off

tmux split-window -h
tmux split-window -v -t session:0.1

tmux send-keys -t session:0.0 "./subscriber.py" C-m
tmux send-keys -t session:0.1 "sleep 1; ./publisher-temperature.py" C-m
tmux send-keys -t session:0.2 "sleep 1; ./publisher-humidity.py" C-m

tmux attach-session -t session
