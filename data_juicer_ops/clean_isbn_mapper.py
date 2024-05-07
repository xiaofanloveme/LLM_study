import regex as re
from ..base_op import OPERATORS, Mapper

@OPERATORS.register_module('clean_isbn_mapper')
class CleanISBNMapper(Mapper):
    """Mapper to clean copyright comments at the beginning of the text
    samples."""

    def __init__(self, pattern: str = None, 
                 repl: str = '', *args, **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        if pattern is None:
            # 匹配ISBN号
            #self.pattern = r'(\d{1,3}-?\d{1,5}-?\d{1,7}-?\d{1,9}-?[\dX]|\d{3}-\d{1,5}-\d{1,7}-\d{1,9}-\d)' 
            self.pattern = r'(\d{1,5}-?\d{1,5}-?\d{1,7}-?\d{1,9}-?[\dX]|\d{1,5}-?\d{1,7}-?\d{1,9}-?\d{1,12}-?\d|\bISBN-(10|13)\b)' 
            #self.isbn_13_pattern = r'\d{1,5}-?\d{1,7}-?\d{1,9}-?\d{1,12}-?\d
            #self.isbn_10_pattern = \d{1,3}-?\d{1,5}-?\d{1,7}-?\d{1,9}-?[\dX]


        else:
            self.pattern = pattern
            if ((len(pattern) > 2) and
                (pattern.startswith("r'") and pattern.endswith("'")
                 or pattern.startswith('r"') and pattern.endswith('"'))):
                self.pattern = pattern[2:-1]

        self.repl = repl
       

    def process(self, sample):

        if not re.search(self.pattern, sample[self.text_key], flags=re.DOTALL):
            return sample

        sample[self.text_key] = re.sub(pattern=self.pattern,
                                       repl=self.repl,
                                       string=sample[self.text_key],
                                       flags=re.DOTALL)
        return sample