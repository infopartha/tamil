
class NonTamilLetterException(Exception):
    """Raised when the given character is not a Tamil letter/not in the Tamil aruchuvadi"""
    def __init__(self, letter=None, message=None) -> None:
        self.letter = letter
        if message:
            self.message = message
        elif letter:
            self.message = f'இந்த எழுத்து [{self.letter}] தமிழ் எழுத்தல்ல.\nThis letter [{self.letter}] is not a Tamil letter'
        else:
            self.message = 'இந்த எழுத்து தமிழ் எழுத்தல்ல.\nThis letter is not a Tamil letter'

        super().__init__(self.message)


class InvalidLetterAddition(Exception):
    """Raised when a Letter is added to another Letter object"""
    def __init__(self, letter=None, other=None, message=None) -> None:
        if message:
            self.message = message
        elif letter and other:
            self.message = f"[{letter}] என்ற எழுத்துடன் [{other}]ஐ சேர்த்தால், அது எழுத்தாக அல்லாமல் சொல்லாகி விடும்.\
                \nThe letter [{other}] can not be added with [{letter}]. Instead of adding, try to create a word (Sol)\
                \nEx. Sol('{letter}', '{other}')"
        else:
            self.message = "ஒரு தனி எழுத்துடன் இன்னொரு தனி எழுத்தை சேர்க்க முடியாது. அதற்கு சொல்லைப் பயன்படுத்தவும்.\
                \nTwo Letter objects can not be added. Instead, try to create a word (Sol)\
                \nEx. Sol('<எழுத்து 1>', '<எழுத்து 2>')"
        super().__init__(self.message)
