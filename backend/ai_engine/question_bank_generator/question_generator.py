from .engineering_prompt import ENGINEERING_SYSTEM_PROMPT
from .bloom_allocator import BloomAllocator


class QuestionGenerator:

    def __init__(self):

        self.prompt = ENGINEERING_SYSTEM_PROMPT

        self.bloom = BloomAllocator()

    def prepare_request(self, topics, material):

        return {

            "system_prompt": self.prompt,

            "topics": topics,

            "material": material,

            "distribution": self.bloom.allocate()

        }