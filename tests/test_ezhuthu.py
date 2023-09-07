import sys
import unittest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lexer import ezhuthu
from lexer.exceptions import NonTamilLetterException, InvalidLetterAddition


class TestingEzhuthu(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.e1 = ezhuthu.Ezhuthu('த')
        self.e2 = ezhuthu.Ezhuthu('மி')
        self.e3 = ezhuthu.Ezhuthu('ழ்')

    def test_eq_1(self):
        assert(self.e1 == 'த')

    def test_eq_2(self):
        assert(self.e2 == ezhuthu.Ezhuthu('மி'))
    
    def test_get_name_1(self):
        assert(self.e2.get_name() == 'மிகரம்')

    def test_get_name_2(self):
        assert(self.e3.get_name() == 'ழகர ஒற்று')

    def test_get_name_3(self):
        assert(ezhuthu.Ezhuthu('ஆ').get_name() == 'ஆகாரம்')

    def test_get_name_4(self):
        assert(ezhuthu.Ezhuthu('ஃ').get_name() == 'அஃகேனம்')

    def test_get_name_5(self):
        assert(ezhuthu.Ezhuthu('௬').get_name() == 'ஆறு')

    def test_add_1(self):
        assert(self.e1 + 'ீ' == 'தீ')

    def test_add_2(self):
        assert(self.e1 + ezhuthu.Ezhuthu('ா') == 'தா')

    def test_iadd_1(self):
        e4 = ezhuthu.Ezhuthu('த')
        e4 += 'ீ'
        assert(e4 == 'தீ')

    def test_iadd_2(self):
        e4 = ezhuthu.Ezhuthu('த')
        e4 += ezhuthu.Ezhuthu('ா')
        assert(e4 == 'தா')

    def test_iadd_3(self):
        e4 = ezhuthu.Ezhuthu('த')
        with self.assertRaises(InvalidLetterAddition) as err_cntx:
            e4 += None
        assert("The letter of type [<class 'NoneType'>] can not be added" in str(err_cntx.exception))

    def test_iadd_4(self):
        e4 = ezhuthu.Ezhuthu('தா')
        with self.assertRaises(InvalidLetterAddition) as err_cntx:
            e4 += 'தி'
        assert("அது எழுத்தாக அல்லாமல் சொல்லாகி விடும்" in str(err_cntx.exception))

    def test_strict_1(self):
        with self.assertRaises(ValueError) as err_cntx:
            e5 = ezhuthu.Ezhuthu('த', 'ம', strict=True)
        assert("இரண்டாம் எழுத்து [ம] துணையெழுத்தல்ல" in str(err_cntx.exception))

    def test_strict_2(self):
        e5 = ezhuthu.Ezhuthu('த', 'ி', strict=True)
        assert(e5 == 'தி')

    def test_strict_3(self):
        with self.assertRaises(ValueError) as err_cntx:
            e5 = ezhuthu.Ezhuthu('ஃ', 'ி', strict=True)
        assert("ஆய்த எழுத்து துணையெழுத்துடன் சேராது" in str(err_cntx.exception))

    def test_letter_repr(self):
        ltr1 = ezhuthu.Letter('A')
        assert(repr(ltr1) == 'A')

if __name__ == '__main__':
    unittest.main()