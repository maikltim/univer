import sys


def main():
    count = 0

    for line in sys.stdin:
        count += 1 
    print(f"Unique words: {count}")

if __name__ == "__main__":
    main()