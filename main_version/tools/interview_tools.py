import urllib3
import validators
import random
import re


class InvalidUrlPreambleError(Exception):
    pass


class InvalidUrlError(Exception):
    pass


class HTMLContentCleaner:
    def __init__(self, web_url: str, result_file: str, count_head: bool = False):
        """
        Initializes the HTMLContentCleaner class instance.

        :param web_url: The URL of the web page to fetch and clean.
        :type web_url: str
        :param result_file: The file path where the cleaned content will be saved.
        :type result_file: str
        :param count_head: A flag indicating whether the <head> content should be counted or cleaned. Default is False.
        :type count_head: bool
        """
        self.web_url = web_url
        self.web_content = None
        self.result_file = result_file
        self.count_head = count_head

    def validate_url(self):
        """
        Validates the format of the given web URL.

        :return(bool): True if the URL is valid, otherwise False.
        """
        if validators.url(self.web_url):
            return True
        else:
            return False

    def get_web_content(self):
        """
        Fetches the web content from the specified URL if the URL is valid.

        :return:
            (str): The web content as a string if the request is successful.
            (bool): False if the request fails.
        :raise: InvalidUrlError: If the URL format is invalid.
        """
        if not self.validate_url():
            err_msg = ("""
            Can't process web content because of invalid URL format.
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
        """
        Removes content between specified delimiters from the input string.

        :param input_string: The input string to be cleaned.
        :type input_string: str
        :param left_d: The left delimiter.
        :type left_d: str
        :param right_d: The right delimiter.
        :type left_d: str
        :return(str): The cleaned string with content between the delimiters removed.
        """
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
    def remove_html_tags(text: str):
        """
        Removes HTML tags from the input text.

        :param text: The input text containing HTML tags.
        :type text: str
        :return(str): The text with HTML tags removed.
        """
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
    def remove_punctuation_marks(text: str):
        """
        Removes punctuation marks from the input text.

        :param text: The input text containing punctuation marks.
        :type text: str
        :return: The text with punctuation marks removed.
        """
        result_content = ''
        punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        for single_char in text:
            if single_char not in punctuation_marks:
                result_content += single_char
        return result_content

    @staticmethod
    def remove_html_ampersand_entities(text: str):
        """
        Removes HTML ampersand entities (e.g., &amp;, &lt;, &gt;) from the input text.

        :param text: The input text containing HTML ampersand entities.
        :type text: str
        :return: The text with ampersand entities removed.
        """
        return re.sub(r"&(\w+|#\w+);", ' ', text)

    def clean_head(self):
        """
        Cleans the <head> section of the web content if it exists.

        :return(str): The web content with the <head> section cleaned.
        """
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<head>', '</head>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_js_scripts(self):
        """
        Cleans JavaScript content from the web content if it exists.

        :return(str): The web content with JavaScript content cleaned.
        """
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<script>', '</script>')
            self.web_content = self.inside_content_cleaner(self.web_content, '<script', '</script>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_css_stuff(self):
        """
        Cleans CSS content from the web content if it exists.

        :return(str): The web content with CSS content cleaned.
        """
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<style', '</style>')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_comments(self):
        """
        Cleans HTML comments from the web content if they exist.

        :return(str): The web content with HTML comments cleaned.
        """
        if self.web_content:
            self.web_content = self.inside_content_cleaner(self.web_content, '<!--', '-->')
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_ampersand_entities(self):
        """
        Cleans HTML ampersand entities from the web content.

        :return(str): The web content with ampersand entities cleaned.
        """
        if self.web_content:
            self.web_content = self.remove_html_ampersand_entities(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_html_tags(self):
        """
        Cleans HTML tags from the web content if they exist.

        :return(str): The web content with HTML tags cleaned.
        """
        if self.web_content:
            self.web_content = self.remove_html_tags(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_punctuation_marks(self):
        """
        Cleans punctuation marks from the web content if they exist.

        :return(str): The web content with punctuation marks cleaned.
        """
        if self.web_content:
            self.web_content = self.remove_punctuation_marks(self.web_content)
            return self.web_content
        else:
            return self.web_content, "Web content is not present."

    def clean_all(self):
        """
        Cleans the web content by applying all available cleaning methods.

        :return(str): The fully cleaned web content.
        """
        if self.count_head:
            self.clean_head()
        self.clean_html_comments()
        self.clean_js_scripts()
        self.clean_css_stuff()
        self.clean_html_ampersand_entities()
        self.clean_html_tags()
        self.clean_punctuation_marks()
        return self.web_content


class CountWordsFromUrl(HTMLContentCleaner):
    """
    A class to count words from a web URL after cleaning the HTML content.
    Inherits from HTMLContentCleaner.
    """

    def __init__(self, web_url: str, result_file: str):
        """
        Initializes the CountWordsFromUrl instance and cleans the web content.

        :param web_url: The URL of the web page to fetch and clean.
        :type web_url: str
        :param result_file: The file path where the cleaned content will be saved.
        :type result_file: str
        """
        super().__init__(web_url, result_file)
        self.get_web_content()
        self.clean_all()

    def get_unique_words_set(self, print_to_console: bool = False):
        """
        Retrieves a set of unique words from the cleaned web content.

        :param print_to_console: If True, prints the set of unique words to the console. Default is False.
        :type print_to_console: bool
        :return(set): A set of unique words from the web content.
        """
        return_set = set(self.web_content.lower().split())
        if print_to_console:
            print(return_set)
        return return_set

    def get_all_words_list(self, print_to_console: bool = False):
        """
        Retrieves a list of all words from the cleaned web content.

        :param print_to_console: If True, prints the list of all words to the console. Default is False.
        :type print_to_console: bool
        :return: A list of all words from the web content.
        """
        all_words_list = self.web_content.lower().split()
        if print_to_console:
            print(all_words_list)
        return all_words_list

    def get_dict_with_counted_words(self, print_to_console: bool = False):
        """
        Retrieves a dictionary with words as keys and their counts as values.

        :param print_to_console: If True, prints the dictionary to the console. Default is False.
        :type print_to_console: bool
        :return(dict): A dictionary where keys are words and values are their counts.
        """
        result_dict = {}
        unique_words_set = self.get_unique_words_set()
        all_words_list = self.get_all_words_list()
        for unique_word in unique_words_set:
            result_dict[unique_word] = all_words_list.count(unique_word)
        if print_to_console:
            print(result_dict)
        return result_dict

    def get_top_words(self, top_count: int = 10, print_to_console: bool = False):
        """
        Retrieves a list of the top words by frequency.

        :param top_count: The number of top words to retrieve. Default is 10.
        :type top_count: int
        :param print_to_console: If True, prints the list of top words to the console. Default is False.
        :type print_to_console: bool
        :return(list): A list of strings representing the top words and their counts.
        """
        unsorted_dict = self.get_dict_with_counted_words()
        sorted_dict = sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)
        iterator = 0
        return_list = []
        if top_count == -1:
            top_count = len(sorted_dict)
        for word, count in sorted_dict[:top_count]:
            iterator += 1
            row = f"{iterator}. {word} --- {count}"
            if print_to_console:
                print(row)
            return_list.append(row)
        return return_list

    def save_top_words_to_file(self, top_count: int = 10, print_to_console: bool = False):
        """
        Saves the top words by frequency to the result file.

        :param top_count: The number of top words to save. Default is 10.
        :type top_count: int
        :param print_to_console: If True, prints the list of top words to the console. Default is False.
        :type print_to_console: bool
        :return: The path to the result file where the top words are saved.
        """
        top_words_list = self.get_top_words(top_count=top_count)
        with open(self.result_file, 'w') as f:
            for row in top_words_list:
                if print_to_console:
                    print(row)
                f.write(row + '\n')
        return self.result_file
