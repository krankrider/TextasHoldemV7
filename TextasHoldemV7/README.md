# TextasHoldemV7

## Introduction:

### Application Description:

The python application is a terminal-based poker game simulation where a human player competes against an NPC opponent, the legendary Tony G. There is a single betting round, after which the round winner is decided. The game implements basic poker rules and mechanics, allowing players to make decisions such as calling, raising, checking, or folding during each hand. The goal of the game is to be the only player left with a positive balance. After the game is over, the results are saved in a .txt file.

### How to Run the Program:

To run the program, ensure that the required `treys` library is installed by running `pip install treys`. Then, execute the Python script in a terminal or command prompt by entering `python poker_game.py`.

### How to Use the Program:

Upon running the program, the user will be prompted to enter their name. The game then proceeds with the player competing against the AI opponent in rounds of poker hands. The player interacts with the game by inputing actions displayed on the screen during their turn. Possible actions include "check", "call", "raise", "fold" and "all in", with safeguards in place to prevent the player from making illegal actions. After the round ends, the player is asked if he wants to move on to the next round.

## Body/Analysis:

### Functional Requirements Implementation:

- **Encapsulation:** Encapsulation is demonstrated in the `Player` class where the player's attributes and methods are bundled together. This ensures that the internal state of the player object is hidden and can only be accessed or modified through defined methods.
- **Abstraction:** The `Game` class abstracts the complexities of the poker game. Users of the `Game` class can start a game by calling the `play_game` method without worrying about the underlying details of how the game is managed.
- **Inheritance:** Inheritance is shown through the `HumanPlayer` class, which inherits from the `Player` class and overrides the `choose_action` method to provide specific behavior for human players.
- **Polymorphism:** Polymorphism is evident in the `choose_action` method of the `Player` class, where the method's behavior varies based on whether the player is a hero or not.

### Singleton Pattern:

The Singleton pattern ensures that a class has only one instance and provides a global point of access to it. This is suitable for managing game state or configuration settings where only one instance should exist throughout the program's lifecycle. In this case, the Singleton pattern is used for the `Game` class to ensure that only one game instance is created and managed.

### Factory Method Pattern:

The Factory Method pattern defines an interface for creating an object but allows subclasses to alter the type of objects that will be created. This is useful for creating different types of players (e.g., `HumanPlayer` vs. `AIPlayer`). The Factory Method pattern is used to create player instances, allowing us to extend the player creation logic easily.

## Results and Summary:

### Results:

- Successfully implemented a functional poker game simulation with one betting round and main mechanics.
- Faced challenges in implementing complex logic for player actions and maintaining an object oriented approach.
- Overcame challenges through refactoring, careful debugging and testing.

### Conclusions:

- The implemented poker game achieves its goal of providing a quick and interactive poker hand experience.
- Future prospects of the program include adding more advanced features such as more betting rounds, multiplayer support, improved AI opponent behavior, and enhanced graphical user interface.

Resources:

- [Treys Library Documentation](https://pypi.org/project/treys/)
