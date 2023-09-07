from .ezhuthu import Ezhuthu, NonTamilEzhuthu
from .exceptions import NonTamilLetterException

class Sol:
    def __init__(self, word) -> None:
        self.word = word.strip()
        self.letters = self._get_letters(self.word, [])
    
    def __getitem__(self, index):
        return self.letters[index]
    
    def __setitem__(self, index, letter):
        try:
            ltr = Ezhuthu(letter)
        except NonTamilLetterException:
            ltr = NonTamilEzhuthu(letter)

        if len(self.letters) == index:
            self.letters.append(ltr)
        elif len(self.letters) < index:
            self.letters[index] = ltr
        else:
            self.letters[index] = ltr
        self._update_from_letters()
    
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
        if isinstance(other, Ezhuthu) or isinstance(other, NonTamilEzhuthu):
            return self.word + ' ' + other.ezhuthu    
        return self.word + ' ' + str(other)
    
    def __iadd__(self, other) -> str:
        if isinstance(other, str):
            self.word = self.word + other
        elif isinstance(other, Ezhuthu) or isinstance(other, NonTamilEzhuthu):
            self.word = self.word + other.ezhuthu
        else:  
            self.word = self.word + str(other)
        self.word = self.word.strip()
        self.letters = self._get_letters(self.word, [])
        return self
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.word == other
        if isinstance(other, Sol):
            return self.word == other.word
        if isinstance(other, Ezhuthu) or isinstance(other, NonTamilEzhuthu):
            return self.word == other.ezhuthu
        return self.word == str(other)

    def _get_letter_object(self, letter):
        try:
            e = Ezhuthu(letter)
        except NonTamilLetterException:
            e = NonTamilEzhuthu(letter)
        
        return e

    def _get_letters(self, word, letters = []):
        if len(word) < 1:
            return letters

        e = self._get_letter_object(word)
        letters.append(e)
        return self._get_letters(word[len(e):], letters)

    def _update_from_letters(self):
        word = ''
        for e in self.letters:
            word += str(e)
        self.word = word
    
    def _update_from_word(self):
        letters = self._get_letters(self.word)
        self.letters = letters

    def charlength(self) -> int:
        """Returns the number of unicode characters in the word"""
        return len(self.word)
    
    def tokenize(self):
        """Splits the word into letters and returns list of letters in str format"""
        return [l.ezhuthu for l in self.letters]
    
    def append(self, new_str):
        if isinstance(new_str, str):
            letters_obj = self._get_letters(new_str, [])
            self.letters.extend(letters_obj)
        elif isinstance(new_str, Ezhuthu) or isinstance(new_str, NonTamilEzhuthu):
            self.letters.append(new_str)
        self._update_from_letters()
