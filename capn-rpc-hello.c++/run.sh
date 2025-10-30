#!/bin/bash

tmux -f .tmux.conf new-session -d -s session
tmux -f .tmux.conf split-window -h
tmux -f .tmux.conf send-keys -t session:0.0 "./server" C-m
tmux -f .tmux.conf send-keys -t session:0.1 "./client" C-m
tmux -f .tmux.conf attach-session -t session
