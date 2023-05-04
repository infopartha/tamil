from .ezhuthu import Ezhuthu, NonTamilEzhuthu
from .exceptions import NonTamilLetterException

class Sol:
    def __init__(self, word) -> None:
        self.word = word.strip()
        self.letters = self._get_letters(self.word, [])
    
    def __getitem__(self, index):
        return self.letters[index]
    
    def __setitem__(self, index, letter):
        ltr = Ezhuthu(letter)
        self.letters[index] = ltr
    
    def __repr__(self):
        return self.word
    
    def __len__(self):
        return len(self.letters)
    
    def __iter__(self):
        for letter in self.letters:
            yield letter
        
    def __add__(self, other) -> str:
        if isinstance(other, str):
            return self.word + ' ' + other
        if isinstance(other, Sol):
            return self.word + ' ' + other.word    
        if isinstance(other, Ezhuthu):
            return self.word + ' ' + other.ezhuthu    
        return self.word + ' ' + str(other)
    
    def __iadd__(self, other) -> str:
        if isinstance(other, str):
            self.ezhuthu = self.ezhuthu + other
        elif isinstance(other, Ezhuthu):
            self.ezhuthu = self.ezhuthu + other.ezhuthu
        else:  
            self.ezhuthu = self.ezhuthu + str(other)
        return self
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.word == other
        if isinstance(other, Sol):
            return self.word == other.word
        if isinstance(other, Ezhuthu):
            return self.word == other.ezhuthu
        return self.word == str(other)

    def _get_letters(self, word, letters = []):
        if len(word) < 1:
            return letters
        try:
            e = Ezhuthu(word)
        except NonTamilLetterException:
            e = NonTamilEzhuthu(word)

        letters.append(e)
        return self._get_letters(word[len(e):], letters)
    
    def charlength(self) -> int:
        """Returns the number of unicode characters in the word"""
        return len(self.word)
    
    def tokenize(self):
        """Splits the word into letters and returns list of letters in str format"""
        return [l.ezhuthu for l in self.letters]
    
