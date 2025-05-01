import unittest
import pygame
from unittest.mock import patch, MagicMock
from hangman import BasicHangman

class TestHangmanGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicializuoja pygame prieš vykdant testus"""
        pygame.display.init()  # Inicijuojame tik 'display' modulį
        pygame.font.init()     # Inicijuojame 'font' modulį

    @classmethod
    def tearDownClass(cls):
        """Uždaro pygame po visų testų"""
        pygame.font.quit()     # Uždaro 'font' modulį
        pygame.display.quit()  # Uždaro 'display' modulį

    def test_load_words_from_file_valid(self):
        """Testuoja, ar žodžiai teisingai įkeliami iš failo"""
        game = BasicHangman(1000, 600)
        with patch("builtins.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = ["apple\n", "banana\n"]
            words = game.load_words_from_file("mockfile.txt")
            self.assertEqual(words, ["apple", "banana"])

    def test_load_words_from_file_invalid(self):
        """Testuoja, ką daro load_words_from_file, kai failas neegzistuoja"""
        game = BasicHangman(1000, 600)
        with patch("builtins.open", side_effect=FileNotFoundError):
            words = game.load_words_from_file("non_existent_file.txt")
            self.assertEqual(words, [])  # Turėtų grąžinti tuščią sąrašą

    def test_guessing_letter_correct(self):
        """Testuoja, ar teisingai spėjama raidė yra pridedama į spėjimų sąrašą"""
        game = BasicHangman(1000, 600)
        game.word = "apple"
        game.guessed = []
        game.guess_letter('a')
        self.assertIn('a', game.guessed)  # Patikriname, ar raidė buvo pridėta į spėjimų sąrašą

    def test_guessing_letter_incorrect(self):
        """Testuoja, ar neteisingas spėjimas didina hangman statusą"""
        game = BasicHangman(1000, 600)
        game.word = "apple"
        game.guessed = []
        game.guess_letter('z')
        self.assertEqual(game.hangman_status, 1)  # Neteisingo spėjimo atveju hangman statusas turėtų padidėti

    def test_draw(self):
        """Testuoja, ar draw metodas užtikrina, kad ekranas užpildomas"""
        # Sukuriame žaidimo objektą
        game = BasicHangman(1000, 600)
        
        # Inicializuojame pygame ekraną
        game.win = pygame.display.set_mode((1000, 600))

        # Vykdome testuojamą metodą
        try:
            game.draw()
            pygame.display.update()  # Bandome atnaujinti ekraną
        except Exception as e:
            self.fail(f"Draw metodas nepavyko: {e}")

if __name__ == "__main__":
    unittest.main()