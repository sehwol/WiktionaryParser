"""
This utility script runs WiktionaryParser using the list of test words and
saves the results as testOutput.json.
"""

from wiktionaryparser import WiktionaryParser
from tests import test_core

parser = WiktionaryParser()


def fetch_word(lang: str, word: str, old_id: int):
    parser.set_default_language(lang)
    return parser.fetch(word, old_id=old_id)


def write_test_output_json():
    test_words_table = test_core.get_test_words_table()

    for language, word, old_id in test_words_table:
        word = fetch_word(language, word, old_id)
        print(word)


if __name__ == '__main__':
    write_test_output_json()
