import sys
import unittest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lexer import ezhuthu, sol

# python -m unittest --verbose
# python -m coverage run -m unittest --verbose
# python -m coverage report -m

class TestingSol(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.s1 = sol.Sol('தமிழ்')
        self.s2 = sol.Sol('மொழி')
        self.e1 = ezhuthu.Ezhuthu('த')
        self.e2 = ezhuthu.Ezhuthu('மி')
        self.e3 = ezhuthu.Ezhuthu('ழ்')

    def test_repr(self):
        assert(repr(self.s1) == 'தமிழ்')

    def test_len(self):
        assert (len(self.s1) == 3)

    def test_iter(self):
        ltrs = [e for e in self.s1]
        assert(ltrs == [self.e1, self.e2, self.e3])

    def test_eq_1(self):
        assert (self.s1 == 'தமிழ்')

    def test_eq_2(self):
        assert (self.s1 == sol.Sol('தமிழ்'))

    def test_eq_3(self):
        assert (sol.Sol('த') == self.e1)

    def test_eq_4(self):
        s3 = sol.Sol('')
        s3 += []
        assert (s3 == [])

    def test_add_1(self):
        assert (self.s1 + self.s2 == 'தமிழ் மொழி')

    def test_add_2(self):
        assert (self.s1 + 'மொழி' == 'தமிழ் மொழி')

    def test_add_3(self):
        assert (self.s1 + ezhuthu.NonTamilEzhuthu('!') == 'தமிழ் !')

    def test_add_4(self):
        assert (self.s1 + [] == 'தமிழ் []')

    def test_iadd_1(self):
        s3 = sol.Sol('தமிழ்')
        s3 += 'நாடு'
        assert (s3 == sol.Sol('தமிழ்நாடு'))

    def test_iadd_2(self):
        s3 = sol.Sol('தமிழ்')
        s3 += ezhuthu.NonTamilEzhuthu('!')
        assert (s3.tokenize() == ['த', 'மி', 'ழ்', '!'])

    def test_get_item(self):
        assert(self.s1[1] == self.e2)

    def test_set_item(self):
        s3 = sol.Sol('தமிழ்')
        s3[0] = 'அ'
        s3.append('து')
        s3[len(s3)] = '.'
        s3.append(ezhuthu.NonTamilEzhuthu('!'))
        s3.letters.insert(0, '"')
        s3.letters.append('"')
        s3._update_from_letters()
        s3[-3] = '!'
        assert(s3.word == '"அமிழ்து!!"')

    def test_get_letters(self):
        assert (self.s1._get_letters('த', []) == [self.e1])

    def test_update_from_word(self):
        s3 = sol.Sol('தமிழ்')
        s3.word = 'தமிழ்நாடு'
        s3._update_from_word()
        assert(s3.letters == sol.Sol('தமிழ்நாடு').letters)

    def test_exception(self):
        with self.assertRaises(IndexError) as err_cntx:
            self.s1[5] = '!'
        assert('The given index [5] is out of range' in str(err_cntx.exception))

    def test_charlength(self):
        assert (self.s1.charlength() == 5)

    def test_tokenize(self):
        assert (self.s1.tokenize() == ['த', 'மி', 'ழ்'])

    def test_seer_vagai_1(self):
        s4 = sol.Sol('ஒன்று')
        s5 = sol.Sol('இரண்டு')
        s6 = sol.Sol('ஐம்பது')
        s7 = sol.Sol('அறுபது')
        assert(s4.seer_vagai() == 'நேர் நேர்')
        assert(s5.seer_vagai() == 'நிரை நேர்')
        assert(s6.seer_vagai() == 'நேர் நிரை')
        assert(s7.seer_vagai() == 'நிரை நிரை')

    def test_seer_vagai_2(self):
        s8 = sol.Sol('பார்த்தசாரதி')
        assert(s8.seer_vagai() == 'நேர் நிரை நிரை')

    def test_seer_vaaipaadu(self):
        s8 = sol.Sol('மல்லைவேந்தன்')
        s9 = sol.Sol('அழகியதமிழ்மொழி')
        assert(s8.seer_vaaipaadu() == 'தேமாந்தண்பூ')
        assert(s9.seer_vaaipaadu() == 'கருவிளநறுநிழல்')

if __name__ == '__main__':
    unittest.main()