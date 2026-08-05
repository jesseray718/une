# 02 — Essential Commands
bash $HOME/une/core/offline_first_cycle.sh
bash $HOME/une/core/rapid_recycle.sh 12
python3 $HOME/une/bin/analyze_network.py
python3 $HOME/une/core/push_agape_core.py
python3 -c "import json; print(json.load(open('$HOME/une/config/agape_state.json'))['R'])"
