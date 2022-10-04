import random
from string import punctuation
import numpy as np
import nltk


def create_dict(sentence, corpus, n):
    """Create a dictionary of words and their following words from the corpus based on n.

    Args:
        sentence (str): The sentence to finish.
        corpus (list): The corpus to use.
        n (int): The order of the Markov chain.

    Returns:
        dict: The dictionary of words and their following words.
    """
    corpus_dict = {}
    matching_words = []
    for i in range(0, len(corpus)):
        window = corpus[i:i+(n-1)]
        if window == sentence[-(n-1):]:
            matching_words.append(corpus[i+(n-1)])

    for word in matching_words:
        if word not in corpus_dict:
            corpus_dict[word] = 1
        else:
            corpus_dict[word] += 1
    return corpus_dict


def stupid_backoff(sentence, corpus, n):
    """Stupid backoff if the word is not in the dictionary of the corpus based on
     n (n-1, .....)."""
    if n > 0:
        corpus_dict = create_dict(sentence, corpus, n)
        if len(corpus_dict) > 0:
            return corpus_dict
        else:
            return stupid_backoff(sentence, corpus, n-1)
    else:
        return {}


def finish_sentence(sentence, n, corpus, deterministic=False):
    """Finish a sentence using a Markov chain.

    Args:
        sentence (str): The sentence to finish.
        n (int): The order of the Markov chain.
        corpus (list): The corpus to use.
        deterministic (bool): Whether to use a deterministic Markov chain


    Returns:
        str: returns an extended sentence until the first ., ?, or ! is found OR until it has 10 total
tokens.

    """
    punctuation = [".", "?", "!"]
    while len(sentence) < 10:
        corpus_dict = stupid_backoff(sentence, corpus, n)
        if len(corpus_dict) > 0:
            if deterministic:
                word = max(corpus_dict, key=corpus_dict.get)
            else:
                prob = np.array(list(corpus_dict.values()))
                prob = prob / prob.sum()
                word = np.random.choice(list(corpus_dict.keys()), p=prob)
            sentence.append(word)
            if word in punctuation:
                break
        else:
            break
    return " ".join(sentence).split()


def main():
    """Main function."""
    # Read in the corpus and tokenize it, lowercase it
    corpus = nltk.word_tokenize(
        nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    sentence = ["she", "was", "not"]
    n = 5
    print(finish_sentence(sentence, n, corpus, deterministic=True))
    print(finish_sentence(sentence, n, corpus, deterministic=False))


if __name__ == "__main__":
    main()

# End of file mtg.py
