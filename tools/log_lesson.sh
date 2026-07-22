#!/bin/bash
# log_lesson.sh - Add a lesson to wisdom corpus from command line
# Usage: log_lesson "Title" "Body text" "category" severity"

if [ $# -ne 4 ]; then
    echo "Usage: log_lesson \"TITLE\" \"BODY\" CATEGORY SEVERITY"
    echo "Severity options: info, warning, critical, discovery, bug"
    exit 1
fi

python3 /data/data/com.termux/files/home/une/wisdom/wisdom_query.py \
    --add-lesson "$1" "$2" "$3" "$4"
