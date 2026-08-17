"""note.py: Append a quick note to lessons."""
import sys
from state_utils import append_lesson

def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Manual note"
    count = append_lesson(text, "info")
    print(f"[NOTE] Logged: {text} (Total lessons: {count})")

if __name__ == "__main__":
    main()
