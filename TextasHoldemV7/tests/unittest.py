import unittest
from unittest.mock import patch
from TextasHoldemV7 import Player, HumanPlayer, Blinds, Game
from treys import Card, Deck, Evaluator
import random

# Assuming the classes Player, HumanPlayer, Blinds, and Game are defined as in your provided code

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer", 1000)

    def test_initialization(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.stack, 1000)
        self.assertEqual(self.player.hand, [])
        self.assertFalse(self.player.hero)

    @patch('random.choice', return_value='call')
    def test_choose_action_non_hero(self, mock_choice):
        self.player.hero = False
        action = self.player.choose_action()
        self.assertEqual(action, 'call')

class TestHumanPlayer(unittest.TestCase):
    def setUp(self):
        self.human_player = HumanPlayer("HumanPlayer", 1000, hero=True)

    def test_initialization(self):
        self.assertEqual(self.human_player.name, "HumanPlayer")
        self.assertEqual(self.human_player.stack, 1000)
        self.assertEqual(self.human_player.hand, [])
        self.assertTrue(self.human_player.hero)

    @patch('builtins.input', return_value='call')
    def test_choose_action_hero(self, mock_input):
        action = self.human_player.choose_action()
        self.assertEqual(action, 'call')

class TestBlinds(unittest.TestCase):
    def setUp(self):
        self.blinds = Blinds()

    def test_initialization(self):
        self.assertEqual(self.blinds.small_blind, 10)
        self.assertEqual(self.blinds.big_blind, 20)
        self.assertEqual(self.blinds.round_count, 0)

    def test_switch_blinds(self):
        self.blinds.switch_blinds()
        self.assertEqual(self.blinds.round_count, 1)
        self.blinds.switch_blinds()
        self.assertEqual(self.blinds.round_count, 2)
        self.blinds.switch_blinds()
        self.assertEqual(self.blinds.round_count, 3)
        self.assertEqual(self.blinds.small_blind, 20)
        self.assertEqual(self.blinds.big_blind, 40)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.player1 = HumanPlayer("Hero", 1000, hero=True)
        self.opponent = Player("Opponent", 1000)
        self.game = Game(self.player1, self.opponent)

    def test_initialization(self):
        self.assertEqual(self.game.player1.name, "Hero")
        self.assertEqual(self.game.opponent.name, "Opponent")
        self.assertEqual(self.game.round_number, 1)
        self.assertTrue(isinstance(self.game.deck, Deck))
        self.assertTrue(isinstance(self.game.blinds, Blinds))
        self.assertTrue(isinstance(self.game.evaluator, Evaluator))

    @patch.object(Deck, 'draw', side_effect=[[Card.new('Ac'), Card.new('Kc')], [Card.new('Qc'), Card.new('Jc')]])
    def test_deal_cards(self, mock_draw):
        self.game.deal_cards()
        self.assertEqual(len(self.player1.hand), 2)
        self.assertEqual(len(self.opponent.hand), 2)

    def test_deal_blinds(self):
        sb, bb = self.game.deal_blinds()
        self.assertEqual(sb.stack, 990)
        self.assertEqual(bb.stack, 980)
        self.assertTrue(sb.hero)
        self.assertFalse(bb.hero)

    @patch.object(Evaluator, 'evaluate', side_effect=[1, 2])
    def test_determine_winner(self, mock_evaluate):
        board = [Card.new('2c'), Card.new('3c'), Card.new('4c'), Card.new('5c'), Card.new('6c')]
        winner, winner_class = self.game.determine_winner(board)
        self.assertEqual(winner, self.opponent)

    @patch('builtins.input', side_effect=['call'])
    def test_player_action_call(self, mock_input):
        action = self.game.player_action(self.player1, 10)
        self.assertEqual(action, 'call')
        self.assertEqual(self.player1.stack, 990)
        self.assertEqual(self.game.pot, 30)

if __name__ == '__main__':
    unittest.main()
