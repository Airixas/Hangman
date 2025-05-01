import unittest
from unittest.mock import patch, MagicMock
from hangman import HangmanGame, BasicHangman, AdvancedHangman

class TestHangmanGame(unittest.TestCase):
    
    def test_load_words_from_file_valid(self):
        """Testuoja, ar žodžiai teisingai įkeliami iš failo"""
        game = BasicHangman(1000, 600)
        
        # Mock failo atidarymą
        with patch("builtins.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = ["apple\n", "banana\n"]
            words = game.load_words_from_file("mockfile.txt")
            self.assertEqual(words, ["apple", "banana"])

    def test_load_words_from_file_invalid(self):
        """Testuoja, ką daro load_words_from_file, kai failas neegzistuoja"""
        game = BasicHangman(1000, 600)
        
        # Patikriname, ar klaida bus sugauta
        with patch("builtins.open", side_effect=FileNotFoundError):
            words = game.load_words_from_file("non_existent_file.txt")
            self.assertEqual(words, [])  # Turėtų grąžinti tuščią sąrašą

    def test_guessing_letter_correct(self):
        """Testuoja, ar teisingai spėjama raidė yra pridedama į spėjimų sąrašą"""
        game = BasicHangman(1000, 600)
        game.word = "apple"
        game.guessed = []
        
        # Spėjame raidę 'a'
        game.guess_letter('a')
        
        self.assertIn('a', game.guessed)  # Patikriname, ar raidė buvo pridėta į spėjimų sąrašą

    def test_guessing_letter_incorrect(self):
        """Testuoja, ar neteisingas spėjimas didina hangman statusą"""
        game = BasicHangman(1000, 600)
        game.word = "apple"
        game.guessed = []
        
        # Spėjame neteisingą raidę 'z'
        game.guess_letter('z')
        
        self.assertEqual(game.hangman_status, 1)  # Neteisingo spėjimo atveju hangman statusas turėtų padidėti

    @patch('pygame.display.set_mode')  # Mocking Pygame display
    def test_draw(self, mock_set_mode):
        """Testuoja, ar draw metodas užtikrina, kad ekranas užpildomas"""
        game = BasicHangman(1000, 600)
        
        # Imituojame, kad ekranas buvo nustatytas
        game.draw()
        mock_set_mode.assert_called_once()  # Patikriname, ar buvo iškviesta pygame.display.set_mode

if __name__ == "__main__":
    unittest.main()