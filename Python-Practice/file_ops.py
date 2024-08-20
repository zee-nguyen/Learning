"""
Practice working with File I/O and Error Handling

Write a Python function that reads a text file line by line, counts the number of occurrences of each word, and prints the 5 most common words along with their counts. Handle potential errors such as the file not existing.
"""

from collections import Counter


def count_words(filename):
    try:
        with open(filename, "r") as f:
            words = f.read().strip().split()
        word_counts = Counter(words)
        return word_counts.most_common(5)
    except FileNotFoundError:
        print(f"{filename} not found")
    except Exception as e:
        print(f"An error occurred: {e}")


print(count_words("words.txt"))
