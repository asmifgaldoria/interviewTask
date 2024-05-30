# interviewTask
Interview Task

## Interview task description

Complete the tasks listed below and publish the solution on your github. Send us a link to your
repository at least 1 day before the interview. We will discuss the proposed solution during the
interview. You should be ready to present the working application on your local machine.

Your task is to create a Python program that will perform text analysis from any url with an html page.

Text analysis means text that is directed to be read by a human on a web page and is not any html, css, js
etc. tags. The program should perform the following steps:

1. open the page with the given url.
2. read the content of the page.
3. clear the page source of all html, css, js, etc. tags, leaving text that contains human-readable content.
4. remove all punctuation marks (such as commas, full stops, exclamation marks, etc.) and special
characters from the text.
5. Divide the text into individual words.
6. Calculate the number of occurrences of each word in the text.
7. display the 10 most frequent words with their number of occurrences, in descending order.
8. save this information to a file named &#39;results.txt&#39;.
9. Write unit tests for the solution you have written.

Note: Your aim is to produce efficient and readable code. Avoid using standard or off-the-shelf libraries
and tools to analyse text or remove tags from html code.

Do not use tools such as nltk or spacy. Instead, focus on implementing algorithms and data structures in
Python.
