from .bloom_mapper import BloomMapper


def __getattr__(name):
    """Keep the legacy package exports lazy so Bloom mapping stays lightweight."""
    if name == "DuplicateDetector":
        from .duplicate_detector import DuplicateDetector
        return DuplicateDetector
    if name == "DifficultyValidator":
        from .difficulty_validator import DifficultyValidator
        return DifficultyValidator
    raise AttributeError(name)
