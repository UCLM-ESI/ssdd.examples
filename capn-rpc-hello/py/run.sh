#!/bin/bash

tmux set-option -g mouse on
tmux setw -g monitor-activity on
tmux set-option -g visual-activity on
tmux bind-key x kill-session
tmux set-option -g set-titles off

tmux new-session -d -s session
tmux split-window -h
tmux send-keys -t session:0.0 "uv run ./server.py 6000" C-m
tmux send-keys -t session:0.1 "uv run ./client.py 127.0.0.1 6000" C-m
tmux attach-session -t session
