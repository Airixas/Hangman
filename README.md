# 🎮 Hangman Game – Factory Method Design Pattern

## 1. 📘 Introduction

### What is your application?
The Hangman Game is a fun, interactive word-guessing game built with Python and Pygame. Players can choose between Basic and Advanced game modes, each offering its own set of words and visual style. Behind the scenes, the game uses object-oriented programming principles and the Factory Method design pattern to neatly manage how each game mode is created and runs.

### How to run the program?
1. Make sure `Python` and `Pygame` are installed.
2. Files required:
   - `hangman.py`
   - `words.txt`, `advancedwords.txt`
   - `basic0.png` to `basic6.png`, `hangman0.png` to `hangman6.png`
3. Run from terminal:

```bash
python hangman.py
```

### How to use the program?
Once the program launches:
- Select "Basic" or "Advanced" game mode via the game mode menu.
- Guess letters by clicking on them with the mouse.
- The game ends when you either guess the word, run out of tries (6), or time runs out (60 seconds).
- Message shows if you win or lose, and reveals the correct word.

## 2. 🧠 Body / Analysis

### ✔️ Functional Requirements Implementation

#### Project Hosting and Version Control
The project is fully managed using Git and hosted on GitHub, where all source code, assets, and documentation are committed regularly. This setup ensures code backups, easier collaboration, and version tracking throughout the development process.

#### 🧱 Object-Oriented Design
The game is structured using core object-oriented programming (OOP) principles to ensure modular, extendable code:

**Abstraction**
A central abstract class, `HangmanGame`, defines the shared game mechanics such as drawing elements, managing guessed letters, and tracking the game timer. This allows developers to focus on differences between game modes rather than rewriting base logic.

**Inheritance**
`BasicHangman` and `AdvancedHangman` both inherit from `HangmanGame`. These subclasses override only what's specific to their gameplay — like loading different word sets or image assets — keeping code clean and maintainable.

**Polymorphism**
The main game loop uses the base class interface but can run any subclass transparently. Whether it's a basic or advanced game mode, the logic calls methods like `load_images()` without needing to know the specific type.

**Encapsulation**
Key data like guessed letters, the word list, and game status are handled internally by each instance, preventing accidental modification and keeping game state controlled.

#### 🏭 Factory Method Pattern in Use
To cleanly separate user interaction from game logic, a Factory Method pattern is used when choosing game modes. Instead of hardcoding which mode starts, the user selects via a graphical interface, and the program dynamically instantiates the correct class.

This pattern was ideal here because:
- It makes the game easy to extend with future modes.
- The logic for how each mode behaves is kept isolated.
- The code that launches the game doesn’t need to change — it just requests a mode from the factory logic.

A simplified version of the factory logic:
```python
if basic_btn.collidepoint(m_x, m_y):
    game = BasicHangman(1000, 600)
elif adv_btn.collidepoint(m_x, m_y):
    game = AdvancedHangman(1000, 600)

game.main()
```

---

## 3. 📌 Results and Summary

### ✅ Results
- Game logic and interface run as expected using OOP principles.
- Successfully implemented Factory Method pattern to support multiple game modes.
- User interaction with mouse events is intuitive and responsive.
- Added word and image customization based on selected mode.
- Pygame's event loop and drawing operations tested and functional.

### 📈 Challenges Faced
- Handling slow performance due to font and Pygame initialization (solved by profiling and reducing redundancy).
- Ensuring asset files existed and were not missing.
- Structuring the Factory class to be extensible and maintainable.

### ✅ Conclusions
 The project resulted in a functional and engaging Hangman game with selectable modes and a clean structure using OOP and the Factory Method. 
 It’s easy to maintain and extend, with room to grow by adding better visuals or new features.

### 💡 Possible Extensions
- Add new game modes (e.g., "Hardcore") via Factory pattern.
- Save/load game state to JSON for persistent sessions.
- Add keyboard input support for improved accessibility.
- Create a GUI menu using buttons instead of ellipses.
- Replace static hangman images with dynamic background scenes that visually reflect the player's progress.

---

## 4. 🔗 References
- [Chat GPT] - Used for design suggestions, code simplification ideas, and improving overall structure clarity.
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Factory Method Pattern – Refactoring Guru](https://refactoring.guru/design-patterns/factory-method)
