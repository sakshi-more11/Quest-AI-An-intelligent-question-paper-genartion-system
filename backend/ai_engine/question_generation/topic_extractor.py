class TopicExtractor:

    def extract(self, chunk):

        words = chunk.split()

        return words[:5]