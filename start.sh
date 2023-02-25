# Run this in a screen session for best experience
LATIOS_DIR="~/latios"
SESSION="latios"

#tmux kill-session -t $SESSION
tmux new-session -d -s $SESSION
tmux split-window -v -t $SESSION:0.0
tmux split-window -h -t $SESSION:0.0
tmux split-window -h -t $SESSION:0.2

tmux send-keys -t $SESSION:0.0 "cd $LATIOS_DIR && python3 -m latios.data_worker.Service" Enter
tmux send-keys -t $SESSION:0.1 "cd $LATIOS_DIR && python3 -m latios.client.Service" Enter
tmux send-keys -t $SESSION:0.2 "cd $LATIOS_DIR && python3 -m latios.ranker.Service" Enter
tmux send-keys -t $SESSION:0.3 "cd $LATIOS_DIR && python3 -m latios.links.ranker.Service" Enter

tmux attach-session -t $SESSION
