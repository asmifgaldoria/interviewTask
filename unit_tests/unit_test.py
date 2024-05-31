from ..main_version.tools.interview_tools import HTMLContentCleaner, CountWordsFromUrl
import urllib3
from bs4 import BeautifulSoup
import os


def test_inside_content_cleaner_staticmethod():
    example_content = """
    example left_d text_to_remove right_d
    rest
    """
    expected_content = """
    example 
    rest
    """
    returned_content = HTMLContentCleaner.inside_content_cleaner(example_content, "left_d", "right_d")
    assert returned_content == expected_content


def test_remove_html_tags_staticmethod():
    example_content = '<title>New Tab</title>'
    expected_content = ' New Tab '
    returned_content = HTMLContentCleaner.remove_html_tags(example_content)
    assert returned_content == expected_content


def test_clean_punctuation_marks_staticmethod():
    punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    punctuation_marks_free = HTMLContentCleaner.remove_punctuation_marks(punctuation_marks)
    for punctuation_mark in punctuation_marks:
        assert punctuation_marks_free.find(punctuation_mark) == -1


def test_remove_html_ampersand_entities_staticmethod():
    example_content = '&#160;&amp;&not_remove&remove;'
    expected_content = '  &not_remove '
    returned_content = HTMLContentCleaner.remove_html_ampersand_entities(example_content)
    assert returned_content == expected_content


def test_clean_head_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.get_web_content()
    example_content = class_handler.clean_head()
    assert_errors = []
    if not example_content.find('<head>') == -1:
        assert_errors.append("'<head>' tag detected")
    if not example_content.find('</head>') == -1:
        assert_errors.append("'</head>' tag detected")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_clean_js_scripts_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.web_content = """
    <script>
        document.getElementById("demo").innerHTML = "Hello JavaScript!";
    </script>
    """
    example_content = class_handler.clean_js_scripts()
    expected_content = '\n    \n    '
    assert_errors = []
    if not example_content.find('<script>') == -1:
        assert_errors.append("'<script>' tag detected")
    if not example_content.find('</script>') == -1:
        assert_errors.append("'</script>' tag detected")
    if not example_content == expected_content:
        assert_errors.append(f"Result '{example_content}' do not match expected string '{expected_content}'")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_clean_css_stuff_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.web_content = """
    <head>
    <style>
    body {background-color: powderblue;}
    h1   {color: blue;}
    p    {color: red;}
    </style>
    </head>"""
    expected_content = """
    <head>
    
    </head>"""
    example_content = class_handler.clean_css_stuff()
    assert_errors = []
    if not example_content.find('<style>') == -1:
        assert_errors.append("'<style>' tag detected")
    if not example_content.find('</style>') == -1:
        assert_errors.append("'</style>' tag detected")
    if not example_content == expected_content:
        assert_errors.append(f"Result '{example_content}' do not match expected string '{expected_content}'")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_clean_html_comments_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.web_content = "example<!-- This is a single line HTML comment. -->example"
    expected_content = "exampleexample"
    example_content = class_handler.clean_html_comments()
    assert example_content == expected_content


def test_clean_html_ampersand_entities_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.web_content = '&#160;&amp;&not_remove&remove;'
    expected_content = '  &not_remove '
    example_content = class_handler.clean_html_ampersand_entities()
    assert example_content == expected_content


def test_clean_html_tags_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    class_handler.web_content = '<title>New Tab</title>'
    expected_content = ' New Tab '
    example_content = class_handler.clean_html_tags()
    assert example_content == expected_content


def test_clean_punctuation_marks_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    class_handler.web_content = punctuation_marks
    punctuation_marks_free = class_handler.clean_punctuation_marks()
    for punctuation_mark in punctuation_marks:
        assert punctuation_marks_free.find(punctuation_mark) == -1


def test_clean_all_method():
    class_handler = HTMLContentCleaner("https://www.example.com", "result.txt")
    test_handler = urllib3.request("GET", "https://www.example.com")
    compare_content = BeautifulSoup(test_handler.data, 'html.parser')
    compare_content = compare_content.get_text()
    compare_content = HTMLContentCleaner.remove_punctuation_marks(compare_content)
    class_handler.get_web_content()
    not_formatted_text = class_handler.clean_all()
    assert not_formatted_text.split() == compare_content.split()


def test_class_count_words_from_url_init():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    assert_errors = []
    if not class_handler.web_content:
        assert_errors.append("Web content not present")
    if not class_handler.web_url:
        assert_errors.append("Web URL not present")
    if not class_handler.result_file:
        assert_errors.append("Result file name not present")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_get_unique_words_set_method():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    content_handler = class_handler.get_unique_words_set()
    assert_errors = []
    if not type(content_handler) == type(set()):
        assert_errors.append(f"Content type ({type(content_handler)}) not match expextations ({type(set())})")
    if not len(content_handler) > 0:
        assert_errors.append("Set is empty")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_get_all_words_list_method():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    content_handler = class_handler.get_all_words_list()
    assert_errors = []
    if not type(content_handler) == type(list()):
        assert_errors.append(f"Content type ({type(content_handler)}) not match expextations ({type(list())})")
    if not len(content_handler) > 0:
        assert_errors.append("List is empty")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_get_dict_with_counted_words_method():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    content_handler = class_handler.get_dict_with_counted_words()
    assert_errors = []
    if not type(content_handler) == type(dict()):
        assert_errors.append(f"Content type ({type(content_handler)}) not match expextations ({type(dict())})")
    if not len(content_handler) > 0:
        assert_errors.append("Dict is empty")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_get_top_words():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    content_handler = class_handler.get_top_words(top_count=3)
    assert_errors = []
    if not len(content_handler) == 3:
        assert_errors.append(f"Actual length ({len(content_handler)}) is not match 3. ")
    if not type(content_handler) == type(list()):
        assert_errors.append(f"Content type ({type(content_handler)}) not match expextations ({type(list())})")
    if not content_handler[0][0] == '1':
        assert_errors.append(f"Iterator issue.")
    if not content_handler[-1][0] == '3':
        assert_errors.append(f"Iterator issue.")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"


def test_save_top_words_to_file():
    class_handler = CountWordsFromUrl("https://www.example.com", "result.txt")
    result_file = class_handler.save_top_words_to_file(top_count=3)
    assert_errors = []
    if not os.path.isfile(result_file):
        assert_errors.append("File does not exist.")
    with open(result_file, 'r') as rfile:
        file_lines = rfile.readlines()
        if not file_lines[0][0] == '1':
            assert_errors.append(f"Iterator issue.")
        if not file_lines[-1][0] == '3':
            assert_errors.append(f"Iterator issue.")
    assert not assert_errors, f"Detected errors: {' '.join(assert_errors)}"
