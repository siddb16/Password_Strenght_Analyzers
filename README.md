<p align="center">
  <img src="https://img.shields.io/badge/Password%20Strength%20Auditor-But%20Smarter-1f6feb?style=for-the-badge&logo=python&logoColor=white" />
</p>

# Password Strength Auditor (But Smarter)

## 🌍 Why This Project Is Needed Today
Weak passwords remain one of the biggest reasons for cyber-attacks globally.  
Most users still rely on predictable patterns like **“P@ssw0rd”**, believing that adding symbols makes a password secure.

Attackers today use:
- Large leaked-password databases  
- Smart brute-forcing tools  
- Pattern recognition (keyboard sequences, substitutions, repetition)  
- Behavioral analysis  

…which makes simple passwords crackable within seconds.

Cybersecurity now demands **real-world password auditing**, not textbook checks.  
This project brings exactly that: a smarter, attacker-like password analyzer.

---

## 🔐 Project Overview
**Password Strength Auditor (But Smarter)** is a Python tool that evaluates passwords using real attacker logic.  
It detects:

- Disguised common passwords (`p@ssw0rd` → "password")
- Keyboard sequences (`qwerty`, `asdf`, `12345`)
- Repeated characters (`aaaa`, `1111`)
- Leetspeak substitutions (`0→o`, `@→a`, `5→s`)
- Similarity to leaked/common passwords
- Low character variety
- Short-length penalties

It returns:

- **Score: 0–100**
- **Rating: Weak / Moderate / Strong / Very Weak**
- **Feedback explaining the weakness**
- **Practical suggestions for improvement**

---

## 🚀 Features
- Smart pattern detection  
- Leetspeak reverse-mapping  
- Leaked-password similarity analysis  
- Modular & readable Python code  
- Clean CLI interface  
- Easily expandable for future development  

---

## 🧠 Project Structure

Password_Strength_Auditor/
│
├── auditor.py # Main script with analysis logic
├── subs.txt # Optional substitution map
├── rockyou.txt # Mini leaked-password sample list
├── README.md # Documentation
└── ARCHITECTURE.md # Internal architecture & design

---

## 🏗 Architecture Summary
The system uses a modular functional architecture:

- **normalize_password()**  
  Handles substitution reversal (leetspeak → plain text)

- **contains_sequence()**  
  Detects keyboard and number patterns

- **has_repeated_chars()**  
  Finds repeated characters

- **similar_to_leaked()**  
  Matches against leaked/common passwords

- **get_password_score()**  
  Main scoring engine

- **get_suggestions()**  
  Generates practical improvement tips

This architecture makes the project easy to extend into web apps, APIs, GUIs, and enterprise systems.

---

## 🔧 Installation
```bash
git clone https://github.com/your-username/password-strength-auditor.git
cd password-strength-auditor
python auditor.py
