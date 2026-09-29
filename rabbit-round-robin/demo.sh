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

tmux send-keys -t session:0.0 "./worker.py" C-m
tmux send-keys -t session:0.1 "./worker.py" C-m
tmux send-keys -t session:0.2 "sleep 2; ./producer.py job1.... job2. job3... job4." C-m

tmux attach-session -t session
