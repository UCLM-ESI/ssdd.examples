#!/bin/bash

tmux -f .tmux.conf new-session -d -s session
tmux -f .tmux.conf split-window -h
tmux -f .tmux.conf send-keys -t session:0.0 "uv run ./server.py 6000" C-m
tmux -f .tmux.conf send-keys -t session:0.1 "uv run ./client.py 127.0.0.1 6000" C-m
tmux -f .tmux.conf attach-session -t session
