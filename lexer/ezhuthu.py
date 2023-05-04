from .arichuvadi import tamil_ezhuthu, empty_char
from .exceptions import NonTamilLetterException, InvalidLetterAddition

class Letter:
    """Base class for any letter object"""
    def __init__(self, letter, attrs=None) -> None:
        self.letter = letter
        self.attrs = attrs
        if not attrs:
            attrs = empty_char
            attrs['ezhuthu'] = letter
            attrs['ucode'] = [ord(letter)]

        for key, val in attrs.items():
            self.__dict__[key] = val

    def __repr__(self) -> str:
        return self.ezhuthu

    def __len__(self) -> int:
        return len(self.ezhuthu)

    def show_attrs(self) -> None:
        """Shows the characteristics/attributes of the Letter"""
        for key, val in self.attrs.items():
            print(f'{key}\t: {val}')


class Ezhuthu(Letter):
    """Class for Tamil Ezhuthukal"""
    def __init__(self, letter, co_letter=None, strict=False) -> None:
        letter = letter.strip()
        if len(letter) > 1:
            letter, co_letter = self._get_valid_ezhuthu(letter, co_letter)

        self.letter = letter
        self.strict = strict
        if self.letter not in tamil_ezhuthu:
            raise NonTamilLetterException(self.letter)

        self.attrs = tamil_ezhuthu[letter]

        super().__init__(letter, self.attrs)

        self.coLetter = None
        if co_letter:
            coLetter = Ezhuthu(co_letter)
            if strict:
                if coLetter.thaniEzhuthu:
                    raise ValueError(
                        f'இரண்டாம் எழுத்து [{coLetter.ezhuthu}] துணையெழுத்தல்ல \
                        \nThe second letter [{coLetter.ezhuthu}] is not a valid co-letter'
                    )
                if self.vagai == 'ஆய்தம்':
                    raise ValueError('ஆய்த எழுத்து துணையெழுத்துடன் சேராது')

            if not coLetter.thaniEzhuthu:
                self.coLetter = coLetter
                self.ezhuthu += self.coLetter.ezhuthu
                self.ucode += coLetter.ucode
                self.vagai = coLetter.vagai if self.vagai != 'கிரந்தம்' else self.vagai
                self.alavu = coLetter.alavu

    def __add__(self, other) -> str:
        if isinstance(other, str):
            return self.ezhuthu + other
        elif isinstance(other, Ezhuthu):
            return self.ezhuthu + other.ezhuthu
        return self.ezhuthu + str(other)

    def __iadd__(self, other):
        if isinstance(other, str):
            other = Ezhuthu(other)
        if not self.coLetter and not other.thaniEzhuthu:
            self.__init__(self.ezhuthu + other.ezhuthu)
            return self
        else:
            raise InvalidLetterAddition(self, other)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.ezhuthu == other
        if isinstance(other, Ezhuthu):
            return self.ezhuthu == other.ezhuthu
        return self.ezhuthu == str(other)

    def _get_valid_ezhuthu(self, letter, co_letter=None):
        l = len(letter)
        fe, ne = None, co_letter
        for i in range(l):
            if letter[:l-i] in tamil_ezhuthu:
                fe = letter[:l-i]
                try:
                    ne = letter[l-i]
                except:
                    ne = co_letter
                break
        else:
            raise NonTamilLetterException(letter)
        return fe, ne

    def show_attrs(self) -> None:
        """Shows the characteristics/attributes of the Letter"""
        print(self.get_name())
        print(f'எழுத்து \t: {self.ezhuthu}')
        if self.coLetter:
            print(f'முதல் எழுத்து \t: {self.letter}')
            print(f'துணையெழுத்து \t: {self.coLetter}')
        if self.inam:
            print(f'இனம் \t\t: {self.inam}')
        print(f'வகை \t\t: {self.vagai}')
        print(f'அளவு \t\t: {self.alavu}')
        print(f'ucode\t\t: {self.ucode}')

    def get_name(self) -> str:
        """Returns the name of the Letter"""
        out = self.ezhuthu
        alavu, vagai = None, None
        if self.ezhuthu == 'ஃ':
            return 'ஆய்தம்'
        if self.coLetter:
            alavu = self.coLetter.alavu
            vagai = self.coLetter.vagai
            if self.coLetter.vagai == 'ஒற்று':
                out = self.letter
        else:
            alavu = self.alavu
            vagai = self.vagai
        out += 'கார' if alavu == 'நெடில்' else 'கர'
        out += ' ஒற்று' if vagai == 'ஒற்று' else 'ம்'

        return out


class NonTamilEzhuthu(Letter):
    def __init__(self, letter) -> None:
        letter = letter[0]
        attrs = empty_char
        attrs['ezhuthu'] = letter
        attrs['vagai'] = 'Non Tamil'
        attrs['ucode'] = ord(letter)
        super().__init__(letter, attrs)
