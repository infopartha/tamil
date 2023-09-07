from .ezhuthu import Ezhuthu, NonTamilEzhuthu
from .exceptions import NonTamilLetterException
from .rules import asai_dict, seer_vaaipaadu_dict

class Sol:
    """Class for Tamil Sol"""
    def __init__(self, word) -> None:
        self.word = word.strip()
        self.letters = self._get_letters(self.word, [])

    def __getitem__(self, index) -> Ezhuthu:
        return self.letters[index]

    def __setitem__(self, index, letter) -> None:
        try:
            ltr = Ezhuthu(letter)
        except NonTamilLetterException:
            ltr = NonTamilEzhuthu(letter)

        num_letters = len(self.letters)
        if num_letters < index:
            raise IndexError(f'The given index [{index}] is out of range. This Sol contains only {num_letters} letters')
        if num_letters == index:
            self.letters.append(ltr)
        else:
            self.letters[index] = ltr
        self._update_from_letters()

    def __repr__(self) -> str:
        return self.word

    def __len__(self) -> int:
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

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.word == other
        if isinstance(other, Sol):
            return self.word == other.word
        if isinstance(other, Ezhuthu) or isinstance(other, NonTamilEzhuthu):
            return self.word == other.ezhuthu
        return self.word == str(other)

    def _get_letters(self, word, letters = []) -> list:
        if len(word) < 1:
            return letters
        try:
            e = Ezhuthu(word)
        except NonTamilLetterException:
            e = NonTamilEzhuthu(word)

        letters.append(e)
        return self._get_letters(word[len(e):], letters)

    def _update_from_letters(self) -> None:
        word = ''
        for e in self.letters:
            word += str(e)
        self.word = word

    def _update_from_word(self) -> None:
        letters = self._get_letters(self.word)
        self.letters = letters

    def charlength(self) -> int:
        """Returns the number of unicode characters in the word"""
        return len(self.word)

    def tokenize(self) -> list:
        """Splits the word into letters and returns list of letters in str format"""
        return [l.ezhuthu for l in self.letters]

    def append(self, new_str) -> None:
        """Adding a letter or string to the existing word"""
        #TODO: Punarchi vidhigal can be implemented here if opted by function call
        if isinstance(new_str, str):
            letters_obj = self._get_letters(new_str.strip(), [])
            self.letters.extend(letters_obj)
        elif isinstance(new_str, Ezhuthu) or isinstance(new_str, NonTamilEzhuthu):
            self.letters.append(new_str)
        self._update_from_letters()

    def asaigal(self) -> list:
        """Returns syllables of the word"""
        out, cur = [], []
        for ltr in self.letters:
            if not cur:
                cur.append(ltr)
            elif ltr.alavu == 'ஒற்று':
                cur.append(ltr)
            elif len(cur) == 1 and cur[0].alavu == 'குறில்':
                cur.append(ltr)
            else:
                out.append(cur)
                cur = [ltr]
        else:
            if cur:
                out.append(cur)
        return out

    def seer_vagai(self) -> str:
        """Returns seer vagai from the syllables of the word"""
        def remove_consecutive_otru(alavu_list):
            if len(alavu_list) < 2: return alavu_list
            out_list, prev_alavu = [], ''
            for alavu in alavu_list:
                if alavu == 'ஒற்று' and prev_alavu == 'ஒற்று':
                    continue
                out_list.append(alavu)
                prev_alavu = alavu
            return out_list

        asaigal = self.asaigal()
        out = []
        for asai in asaigal:
            alavugal_list = [ltr.alavu for ltr in asai]
            alavugal_list = remove_consecutive_otru(alavugal_list)
            alavugal = ' '.join(alavugal_list)
            out.append(asai_dict.get(alavugal, ' '))
        return ' '.join(out)

    def seer_vaaipaadu(self) -> str:
        """Returns asai vaaipaadu of the word"""
        seer_vagai = self.seer_vagai()
        return seer_vaaipaadu_dict.get(seer_vagai)

    def show_attrs(self) -> None: # pragma: no cover
        """Shows the characteristics/attributes of the Word"""
        print(self.word)
        print(f'மொத்த எழுத்துகள் \t: {len(self.letters)}')
        print(f'மொத்த அசைகள் \t: {len(self.asaigal())}')
        print(f'சீர் வகை \t: {self.seer_vagai()}')
        seer_vaaipaadu = self.seer_vaaipaadu()
        if seer_vaaipaadu:
            print('சீர் வாய்பாடு : ' + seer_vaaipaadu)
