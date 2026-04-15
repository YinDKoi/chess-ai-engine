# ♟️ Chess AI Engine

A chess AI engine implemented in Python using the **Minimax algorithm with Alpha-Beta pruning**, featuring multiple difficulty levels and an interactive graphical interface.

---

## 🚀 Features

* ♟️ **Minimax Algorithm** for decision-making
* ⚡ **Alpha-Beta Pruning** for performance optimization
* 🧠 Multiple AI difficulty levels:

  * **Poor Agent** (depth = 2)
  * **Average Agent** (depth = 3 + positional evaluation)
  * **Good Agent** (depth = 4 + move ordering)
* 📊 **Heuristic evaluation function** (material + positional scoring)
* 📐 **Piece-Square Tables (PST)** for positional strength
* 🎮 Interactive GUI using **Pygame**
* 🧪 Automated testing (AI vs Random agent)

---

## 🧠 AI Techniques Used

* Game Tree Search (Minimax)
* Alpha-Beta Pruning
* Heuristic Evaluation Function
* Move Ordering Optimization
* Depth-based Search Strategy

---

## 🖥️ Demo

> 📌 Add a screenshot of your game here (recommended)

Example:

```
![Demo](images/demo.png)
```

---

## ⚙️ Installation

Make sure you have Python installed, then install dependencies:

```bash
pip install pygame chess
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🎮 Controls

* Choose AI level: `1 / 2 / 3`
* Choose color: `W / B`
* Start game: `ENTER`
* Back to menu: `ESC`

---

## 📊 Evaluation

You can run automated matches to evaluate performance:

* AI vs Random Agent (10 matches)
* Compare win rate and behavior

---

## 🛠️ Tech Stack

* Python
* Pygame
* python-chess

---

## 📂 Project Structure

```
.
├── engine.py      # AI logic (Minimax, evaluation)
├── main.py        # GUI and game loop
├── images/        # Chess piece assets
└── README.md
```

---

## 👤 Author

**Doãn Anh Khôi**

* GitHub: https://github.com/YinDKoi

---

## 🌟 Future Improvements

* Add opening book
* Implement transposition table
* Improve evaluation function
* Add neural network evaluation

---
