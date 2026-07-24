import re


class TopicExtractor:

    def extract(self, clean_text):

        lines = clean_text.split("\n")

        topics = []

        for line in lines:

            line = line.strip()

            if len(line) < 5:
                continue

            if re.match(r"^(Unit|Chapter|Module)", line, re.I):

                topics.append(line)

        return topics