from tools.interview_tools import CountWordsFromUrl
import argparse


def main():
    description = """
    This program is designed to retrieve web pages and analyze
    their content by counting the words present on the page.
    
    Example of use:
        - python main.py -u https://example.com/\n
        - python main.py -u https://example.com/ -o result_file.txt\n
        - python main.py -u https://example.com/ -s -n 3
        
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    required = parser.add_argument_group("REQUIRED ARGUMENTS")
    optional = parser.add_argument_group("Optional arguments")
    required.add_argument('-u', '--url',
                          metavar='<url>',
                          help='Web URL.',
                          required=True)
    optional.add_argument('-o', '--output-file',
                          metavar='<output_file_path>',
                          help='Output file path.',
                          default="result.txt")
    optional.add_argument('-s', '--show',
                          action='store_true',
                          help="Print result to console.",
                          default=False)
    optional.add_argument('-n', '--number-of-words',
                          metavar='<count>',
                          help='Count of top words.',
                          type=int,
                          default=10)
    args = parser.parse_args()

    CountWordsFromUrl(args.url, args.output_file).save_top_words_to_file(args.number_of_words, args.show)


if __name__ == '__main__':
    main()
