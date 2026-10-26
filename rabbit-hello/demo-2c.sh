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

tmux send-keys -t session:0.1 "./consumer.py" C-m
tmux send-keys -t session:0.2 "./consumer.py" C-m
tmux send-keys -t session:0.0 "sleep 1; for i in 1 2 3 4; do ./producer.py; sleep 1; done" C-m

tmux select-pane -t session:0.0
tmux attach-session -t session
