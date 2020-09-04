from parameterized import parameterized
import unittest
import json
from wiktionaryparser import WiktionaryParser
from deepdiff import DeepDiff
from typing import Dict
import os

parser = WiktionaryParser()

current_dir = os.path.dirname(__file__)
markdown_files_dir = os.path.join(current_dir, 'markdown_files')



class TestParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.expected_results = {}
        with open('tests/testOutput.json', 'r') as f:
            self.expected_results = json.load(f)

        super(TestParser, self).__init__(*args, **kwargs)

    def test_fetch_wikitext(self):
        expected = "{{also|nööp|no-op}}\n==Dutch==\n\n===Pronunciation===\n* {{audio|nl|Nl-noop.ogg|Audio}}\n\n===Verb===\n{{head|nl|verb form}}\n\n# {{nl-verb form of|p=1|n=sg|t=pres|m=ind|nopen}}\n# {{nl-verb form of|m=imp|nopen}}"
        result = parser.fetch_wikitext('noop')

        self.assertEqual(expected, result)

    @parameterized.expand([
        ('Swedish', 'house', 50356446)
    ])
    def test_parse_wikitext(self, language: str, word: str, old_id: int):
        wikitext = self.__get_test_wikitext(word, old_id)
        word_dto = parser.parse_wikitext(wikitext, word, language)
        self.__test_word_dto(word_dto, word, language)

    @parameterized.expand([
        ('grapple', 50080840),
        ('test', 50342756),
        ('patronise', 49023308),
        ('abiologically', 43781266),
        ('alexin', 50152026),
        ('song', 50235564),
        ('house', 50356446),
    ])
    def test_words_from_english(self, word: str, old_id: int):
        self.__test_word(word, old_id, 'English')

    @parameterized.expand([
        ('video', 50291344),
    ])
    def test_words_from_latin(self, word: str, old_id: int):
        self.__test_word(word, old_id, 'Latin')

    @parameterized.expand([
        ('seg', 50359832),
        ('aldersblandet', 38616917),
        ('by', 50399022),
        ('for', 50363295),
        ('admiral', 50357597),
        ('heis', 49469949),
        ('konkurs', 48269433),
        ('pantergaupe', 46717478),
        ('maldivisk', 49859434),
    ])
    def test_words_from_norwegian_bokmal(self, word: str, old_id: int):
        self.__test_word(word, old_id, 'Norwegian Bokmål')

    @parameterized.expand([
        ('house', 50356446)
    ])
    def test_words_from_swedish(self, word: str, old_id: int):
        self.__test_word(word, old_id, 'Swedish')

    @parameterized.expand([
        ('ἀγγελία', 47719496)
    ])
    def test_words_from_ancient_greek(self, word: str, old_id: int):
        self.__test_word(word, old_id, 'Ancient Greek')

    def __test_words(self, words_and_ids: Dict[str, int], lang: str):
        for word, old_id in words_and_ids.items():
            self.__test_word(word, old_id, lang)

    def __test_word(self, word: str, old_id: int, lang: str):
        parser.set_default_language(lang)
        word_dto = parser.fetch(word, old_id=old_id)

        self.__test_word_dto(word_dto, word, lang)

    def __test_word_dto(self, word_dto, word: str, lang: str):
        print("Testing \"{}\" in \"{}\"".format(word, lang))
        expected_result = self.expected_results[lang][word]

        diff = DeepDiff(word_dto,
                        expected_result,
                        ignore_order=True)

        if diff != {}:
            print("Found mismatch in \"{}\" in \"{}\"".format(word, lang))
            print(json.dumps(json.loads(diff.json), indent=4))

        self.assertEqual(diff, {})

    def __get_test_wikitext(self, page_name: str, old_id: int) -> str:
        file_path = os.path.join(markdown_files_dir, '{}-{}.md'.format(page_name, old_id))

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == '__main__':
    unittest.main()
