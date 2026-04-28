# ✈️ GitHub Copilot Demo App

> *Because manually writing code in 2024 is so last century.*

---

## What Is This?

This is a **Streamlit web app** built to showcase the glorious superpowers of [GitHub Copilot](https://github.com/features/copilot) — your AI pair-programmer who never steals your lunch from the office fridge and always shows up to the stand-up (virtually).

Think of it as a love letter to AI-assisted development, written *with* AI-assisted development. Very meta. Much wow.

---

## Features (a.k.a. Things To Click When Your Manager Is Watching)

### 🏠 Home — *Top 10 GitHub Copilot Features*
A beautifully rendered list of the ten reasons you will never remember how to write a for-loop from memory again. Highlights include:

- **Code Completions** — Copilot finishes your sentences. Your partner could never.
- **Agent Mode** — Sit back, sip your coffee, and watch Copilot build the whole feature while you pretend to review it.
- **Test Generation** — Yes, Copilot will write the tests you were definitely going to write *eventually*.

### 🧮 Calculator — *Powered by Human Hubris*
A fully functional on-screen calculator built entirely in Streamlit. Yes, someone wrote a calculator app to demonstrate an AI coding tool. No, we do not see the irony.

Features include addition, subtraction, multiplication, and division — the four horsemen of elementary arithmetic.

### 💡 Code Generation Lab — *Where the Magic Happens (Allegedly)*
A playground for generating code snippets using natural language prompts. Describe what you want in plain English and watch Copilot either nail it perfectly or produce something that *technically* compiles.

---

## Getting Started

### Prerequisites
- Python 3.13+ (because we live dangerously on the cutting edge)
- A sense of humour (not optional)

### Installation

```bash
# Clone this magnificent repository
git clone https://github.com/ajafry/copilot-training-04-28.git
cd copilot-training-04-28

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (there's only one, we're minimalists)
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

Your browser will open automatically. If it doesn't, navigate to `http://localhost:8501` and pretend it was intentional.

---

## Project Structure

```
copilot-training-04-28/
├── app.py              # Entry point — the one file to rule them all
├── requirements.txt    # streamlit. That's it. That's the file.
└── views/
    ├── home.py         # Top-10 Copilot features showcase
    ├── calculator.py   # A calculator because why not
    ├── codegen_lab.py  # Code generation playground
    └── styles.py       # Makes everything look pretty
```

---

## Contributing

Found a bug? Open an issue. Have a feature idea? Open a PR. Want to rewrite it in Rust? Please don't.

---

## License

This project is open source. Use it, fork it, show it off at conferences, or just stare at it lovingly. All equally valid choices.

---

*Built with ❤️, ✈️, and a suspiciously large amount of GitHub Copilot.*
