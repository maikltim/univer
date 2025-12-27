import sys 


def main():
    current_word = None 

    for line in sys.stdin:
        line = line.strip()

        word, count = line.split('\t', 1)

        try:
            count = int(count)
        except ValueError:
            continue 

        if current_word != word:
            if current_word is not None:
                print(f"{current_word}\t1")
            current_word = word


    if current_word is not None:
        print(f"{current_word}\t1")

if __name__ == "__main__":
    main()