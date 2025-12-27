import sys 


def main():
    for line in sys.stdin:
        line = line.strip().lower()
        words = line.split()

        for word in words:
            print(f"{word}\t1")

if __name__ == "__main__":
    main()
     