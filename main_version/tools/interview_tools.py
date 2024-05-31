import urllib3
import validators
import random
import re


class InvalidUrlPreambleError(Exception):
    pass


class InvalidUrlError(Exception):
    pass


class HTMLContentCleaner:
    def __init__(self, web_url, result_file, count_head=False):
        self.web_url = web_url
        self.web_content = None
        self.result_file = result_file
        self.count_head = count_head

    def validate_url(self):
        if validators.url(self.web_url):
            return True
        else:
            return False

    def get_web_content(self):
        if not self.validate_url():
            err_msg = ("""
            Cant process web content because of invalid url format.
            Valid formats:
                - http://www.example.com
                - https://www.example.com
            """)
            raise InvalidUrlError(err_msg)
        try:
            content_handler = urllib3.request("GET", self.web_url)
            page_content = content_handler.data.decode()
            self.web_content = page_content
            return self.web_content
        except urllib3.exceptions.HTTPError as err:
            print(f"http/https GET request failed, reason {err}")
            return False

    @staticmethod
    def inside_content_cleaner(input_string: str, left_d: str, right_d: str):
        result_content = []
        punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        while True:
            random_tag = ''.join([random.choice(punctuation_marks) for _ in range(5)])
            if random_tag not in input_string:
                break
        buff_string = input_string.replace(left_d, random_tag + left_d)
        buff_string = buff_string.replace(right_d, right_d + random_tag)
        buff_str_list = buff_string.split(random_tag)
        for buff_str in buff_str_list:
            if len(buff_str) != 0:
                if buff_str.find(left_d) == 0 and buff_str.rfind(right_d) == len(buff_str) - len(right_d):
                    result_content.append("<null>")
                else:
                    result_content.append(buff_str)
        result_string = "".join(result_content)
        result_string = result_string.replace('<null>', '')
        return result_string

    @staticmethod
    def remove_html_tags(text):
        result_content = []
        bool_tag = False
        for single_char in text:
            if single_char == '<':
                bool_tag = True
            elif single_char == '>':
                bool_tag = False
                result_content.append(' ')
            elif not bool_tag:
                result_content.append(single_char)
        return ''.join(result_content)

    @staticmethod
    def remove_punctuation_marks(text):
        result_content = ''
        punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        for single_char in text:
            if single_char not in punctuation_marks:
                result_content += single_char
        return result_content

    @staticmethod
    def remove_html_ampersand_entities(text):
        return re.sub(r"&(\w+|#\w+);", ' ', text)

    def clean_head(self):
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<head>', '</head>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_js_scripts(self):
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<script>', '</script>')
            self.web_content = self.inside_content_cleaner(self.web_content, '<script', '</script>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_css_stuff(self):
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<style', '</style>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_comments(self):
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<!--', '-->')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_ampersand_entities(self):
        if self.web_content:
            self.web_content = self.remove_html_ampersand_entities(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_tags(self):
        if self.web_content:
            self.web_content = self.remove_html_tags(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_punctuation_marks(self):
        if self.web_content:
            self.web_content = self.remove_punctuation_marks(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_all(self):
        if self.count_head:
            self.clean_head()
        self.clean_html_comments()
        self.clean_js_scripts()
        self.clean_css_stuff()
        self.clean_html_ampersand_entities()
        self.clean_html_tags()
        self.clean_punctuation_marks()
        return self.web_content

    def ret_all(self):
        return self.get_web_content()


class CountWordsFromUrl(HTMLContentCleaner):
    def __init__(self, web_url, result_file, count_head=False):
        super().__init__(web_url, result_file, count_head)
        self.get_web_content()
        self.clean_all()

    def get_unique_words_set(self):
        return set(self.web_content.lower().split())

    def get_all_words_list(self):
        return self.web_content.lower().split()

    def get_dict_with_counted_words(self):
        result_dict = {}
        unique_words_set = self.get_unique_words_set()
        all_words_list = self.get_all_words_list()
        for unique_word in unique_words_set:
            result_dict[unique_word] = all_words_list.count(unique_word)
        return result_dict

    def show_top_words(self, top_count=10):
        unsorted_dict = self.get_dict_with_counted_words()
        sorted_dict = sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)
        iterator = 0
        for word, count in sorted_dict[:top_count]:
            iterator += 1
            print(f"{iterator}. {word} --- {count}")
