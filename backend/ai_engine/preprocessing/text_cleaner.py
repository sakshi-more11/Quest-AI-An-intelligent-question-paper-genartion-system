"""
Text Cleaner

Removes:
- headers
- page numbers
- unwanted symbols
- extra spaces
"""


import re


class TextCleaner:


    def __init__(self):
        pass



    def clean(self, text):

        if not text:
            return ""



        # remove page numbers

        text = re.sub(
            r'\n\s*\d+\s*\n',
            '\n',
            text
        )



        # remove multiple spaces

        text = re.sub(
            r'\s+',
            ' ',
            text
        )



        # remove unwanted symbols

        text = re.sub(
            r'[^\w\s.,:;()\-]',
            '',
            text
        )



        # normalize new lines

        text = text.replace(
            "\n\n",
            "\n"
        )


        return text.strip()