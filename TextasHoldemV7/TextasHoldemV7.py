try:
    from treys import Card, Deck, Evaluator
except ImportError:
    print("The 'treys' library is not installed. Please install it by running 'pip install treys'")
    exit(1)
import random

# Encapsulation: Player class encapsulates player attributes and methods
class Player:
    def __init__(self, name, stack, hero=False):
        self.name = name
        self.stack = stack
        self.hand = []
        self.hero = hero

    def choose_action(self):
        # Polymorphism: Method behaves differently based on hero attribute
        if self.hero:
            while True:
                action = input(f"Choose action: ").lower()
                if action in ("call", "raise", "check", "all in", "fold"):
                    return action
                else:
                    print("Invalid action. Please choose again.")
        else:
            return random.choice(["call", "raise", "check", "all in", "fold"])

    def print_balance(self):
        print(f"Your balance: {self.stack}$, Opponent's balance: {opponent.stack}$")

# Inheritance: HumanPlayer inherits from Player and overrides choose_action method
class HumanPlayer(Player):
    def choose_action(self):
        while True:
            action = input(f"Choose action: ").lower()
            if action in ("call", "raise", "check", "all in", "fold"):
                return action
            else:
                print("Invalid action. Please choose again.")

class Blinds:
    def __init__(self):
        self.small_blind = 10
        self.big_blind = 20
        self.round_count = 0

    def switch_blinds(self):
        self.round_count += 1
        if self.round_count % 3 == 0:
            self.small_blind *= 2
            self.big_blind *= 2

# Abstraction: Game class provides an abstraction for playing the poker game
class Game:
    def __init__(self, player1, opponent):
        self.player1 = player1
        self.opponent = opponent
        self.deck = Deck()
        self.blinds = Blinds()
        self.round_number = 1
        self.evaluator = Evaluator()
        self.raise_flag = True
        self.call_amount = self.blinds.big_blind - self.blinds.small_blind
        self.minraise = 2*self.blinds.big_blind
        self.pot = self.blinds.big_blind + self.blinds.small_blind
        self.game_over = False

    def deal_cards(self):
        self.deck.shuffle()
        self.player1.hand = self.deck.draw(2)
        self.opponent.hand = self.deck.draw(2)

    def deal_blinds(self):
        if self.round_number % 2 == 0:
            sb = self.opponent
            bb = self.player1
            sb.hero = False
            bb.hero = True
        else:
            sb = self.player1
            bb = self.opponent
            sb.hero = True
            bb.hero = False
        sb.stack -= self.blinds.small_blind
        bb.stack -= self.blinds.big_blind
        return sb, bb

    def display_info(self, sb, bb):
        print(f"\nRound {self.round_number}")
        self.player1.print_balance()
        print(f"Small blind: {self.blinds.small_blind}$, Big blind: {self.blinds.big_blind}$")
        print(f"Your hand:")
        Card.print_pretty_cards(self.player1.hand)
        if sb == self.player1:
            print(f"You are the Small Blind.")
        else:
            print(f"You are the Big Blind.")

    def determine_winner(self, board):
        player1_score = self.evaluator.evaluate(board, self.player1.hand)
        player1_class = self.evaluator.get_rank_class(player1_score)

        opponent_score = self.evaluator.evaluate(board, self.opponent.hand)
        opponent_class = self.evaluator.get_rank_class(opponent_score)

        if player1_score < opponent_score:
            return self.player1, player1_class
        elif player1_score > opponent_score:
            return self.opponent, opponent_class
        return None, player1_class  # Tie

    def player_action(self, player, call_amount):
        action = player.choose_action()
        if action == "fold":
            if self.raise_flag:
                print(f"{player.name} folds.")
                return action
            else:
                if player.hero:
                    print(f"There is no need to fold. You check instead.")
                    return "check"
                else:
                    print(f"{player.name} checks.")
                    return "check"
        elif action == "call":
            if self.raise_flag:
                if player.stack <= self.call_amount:
                    print(f"{player.name} is all-in with {player.stack}$.")
                    raise_amount = player.stack
                    player.stack = 0
                    self.pot += raise_amount
                    self.raise_flag = False
                    return "all in"
                else:
                    print(f"{player.name} calls {self.call_amount}$.")
                    player.stack -= self.call_amount
                    self.pot += self.call_amount
                    self.raise_flag = False
                    return action
            else:
                if player.hero:
                    print("There is no bet to call.")
                return self.player_action(player, call_amount)
        elif action == "raise":
            if player.hero:
                while True:
                    try:
                        raise_amount = int(input(f"Enter the amount you want to raise (minimum raise: {self.minraise}$): "))
                        if raise_amount < self.minraise:
                            print(f"Minimum raise amount is {self.minraise}$.")
                        elif raise_amount >= player.stack:
                            print(f"{player.name} is all in with {player.stack}$!")
                            self.pot += player.stack
                            player.stack = 0
                            self.raise_flag = True
                            self.minraise = 2*raise_amount
                            self.call_amount = raise_amount
                            return "all in"
                        else:
                            print(f"{player.name} raises by {raise_amount}$")
                            player.stack -= raise_amount
                            self.pot += raise_amount
                            raise_flag = True
                            minraise = 2*raise_amount
                            call_amount = raise_amount
                            return action
                    except ValueError:
                        print("Invalid input. Please enter a valid integer value.")
            else:
                if self.minraise > player.stack:
                    print(f"{player.name} is all in with {player.stack}$!")
                    raise_amount = player.stack
                    self.pot += raise_amount
                    player.stack = 0
                    self.raise_flag = True
                    self.minraise = 2*raise_amount
                    self.call_amount = raise_amount
                    return "all in"
                else:
                    raise_amount = random.randint(self.minraise, player.stack)
                    if raise_amount == player.stack:
                        print(f"{player.name} is all in with {player.stack}$!")
                        raise_amount = player.stack
                        self.pot += raise_amount
                        player.stack = 0
                        self.raise_flag = True
                        self.minraise = 2*raise_amount
                        self.call_amount = raise_amount
                        return "all in"
                    else:
                        print(f"{player.name} raises by {raise_amount}$")
                        player.stack -= raise_amount
                        self.pot += raise_amount
                        self.raise_flag = True
                        self.minraise = 2*raise_amount
                        self.call_amount = raise_amount
                        return action
        elif action == "check":
            if self.raise_flag == False:
                print(f"{player.name} checks.")
                return action
            else:
                if player.hero:
                    print("You can not check now.")
                return self.player_action(player, call_amount)
        elif action == "all in":
            print(f"{player.name} is all in with {player.stack}$!")
            raise_amount = player.stack
            self.pot += raise_amount
            self.call_amount = raise_amount
            player.stack = 0
            self.raise_flag = True
            self.minraise = 2*raise_amount
        return action

    def play_hand(self):
        self.deal_cards()
        sb, bb = self.deal_blinds()
        self.display_info(sb, bb)
        call_amount = self.call_amount

        players = [sb, bb]
        current_player = players[0]

        actions = [self.player_action(sb, call_amount)]

        while sb.stack + bb.stack > 0:
            last_action = actions[-1]
            if last_action == "check":
                break

            if last_action == "fold":
                winner = players[0] if current_player == players[1] else players[1]
                print(f"{winner.name} wins a pot of {self.pot}$!")
                return winner, None

            current_player = players[0] if current_player == players[1] else players[1]
            next_action = self.player_action(current_player, call_amount)
            actions.append(next_action)

            if next_action == "call":
                        break

        board = self.deck.draw(5)
        winner, winner_class = self.determine_winner(board)
        self.show_board(board)
        print(f"Opponent's hand:")
        Card.print_pretty_cards(self.opponent.hand)
        print(f"Pot size: {self.pot}$")
        if self.player1.stack <= 0 or self.opponent.stack <= 0:
                self.game_over = True
        return winner, winner_class

    def show_board(self, board):
        print("Board:")
        Card.print_pretty_cards(board)

    def play_again(self):
        yes = ["yes", "y", "ya", "yup", "ye"]
        play_again_input = input("Next round? (yes/no): ").lower()
        return play_again_input in yes

    def export_results(self, winner, winner_class):
        with open('game_results.txt', 'a') as file:
            file.write(f"Player: {player1.name}\n")
            file.write(f"Winner: {winner.name}\n")
            file.write(f"Winning Hand: {self.evaluator.class_to_string(winner_class) if winner_class else 'N/A'}\n")
            file.write(f"Round Number Reached: {self.round_number}\n")
            file.write(f"{player1.name} Stack: {self.player1.stack}$\n")
            file.write(f"Tony G's Stack: {self.opponent.stack}$\n")
            file.write(f"Final Pot Size: {self.pot}$\n")
            file.write("-" * 40 + "\n")

    def play_game(self):
        while True:
            winner, winner_class = self.play_hand()
            if self.game_over == True:
                if winner == self.opponent:
                    self.opponent.stack += self.pot
                    if winner_class is not None:
                        print(f"{self.evaluator.class_to_string(winner_class)}! {self.opponent.name} wins the game!")
                    else:
                        print(f"{self.opponent.name} wins the game!")
                    self.export_results(winner, winner_class)
                    break
                elif winner == self.player1:
                    self.player1.stack += self.pot
                    if winner_class is not None:
                        print(f"{self.evaluator.class_to_string(winner_class)}! {self.player1.name} wins the game!")
                    else:
                        print(f"{self.player1.name} wins the game!")
                    self.export_results(winner, winner_class)
                    break
            elif winner == self.player1:
                self.player1.stack += self.pot
                if winner_class is not None:
                    print(f"{self.evaluator.class_to_string(winner_class)}! {self.player1.name} wins a pot of {self.pot}$!")
            elif winner == self.opponent:
                self.opponent.stack += self.pot
                if winner_class is not None:
                    print(f"{self.evaluator.class_to_string(winner_class)}! {self.opponent.name} wins a pot of {self.pot}$!")
            else:
                self.player1.stack += self.pot // 2
                self.opponent.stack += self.pot // 2
                print("It's a tie!")

            self.round_number += 1
            self.pot = self.blinds.big_blind + self.blinds.small_blind
            self.blinds.switch_blinds()
            self.raise_flag = True
            self.call_amount = self.blinds.big_blind - self.blinds.small_blind
            self.minraise = 2*self.blinds.big_blind

            if not self.play_again():
                self.export_results(winner, winner_class)
                break

hero_name = input("Enter your name: ")
player1 = HumanPlayer(hero_name, 1000, hero=True)
opponent = Player("Tony G", 1000)

game = Game(player1, opponent)
game.play_game()
