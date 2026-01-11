import re
import math
import string

# --- Configuration & Common Data ---
# A small sample of "leaked" or common passwords for demonstration.
# In a real app, you might load this from a 'rockyou.txt' file.

COMMON_PASSWORDS =("rockyou.txt","r")

# Common keyboard patterns (English QWERTY)
KEYBOARD_PATTERNS = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "1234567890"
]

def calculate_entropy(password):
    """
    Calculates Shannon Entropy. This measures how 'random' the data is.
    Higher entropy = harder to brute force.
    """
    if not password:
        return 0
    
    entropy = 0
    length = len(password)
    
    # Count frequency of each character
    char_counts = {char: password.count(char) for char in set(password)}
    
    for count in char_counts.values():
        p_x = count / length
        entropy += - p_x * math.log2(p_x)
        
    return entropy

def check_patterns(password):
    """
    Detects common keyboard sequences (like 'qwer' or '1234').
    Returns a list of found patterns.
    """
    found_patterns = []
    lower_pass = password.lower()
    
    # Check for sequences of 3 or more characters
    for pattern in KEYBOARD_PATTERNS:
        # Check forward and reverse patterns
        for i in range(len(lower_pass) - 2):
            chunk = lower_pass[i:i+3]
            if chunk in pattern or chunk in pattern[::-1]:
                found_patterns.append(f"Keyboard sequence found: '{chunk}'")
                break # Stop checking this pattern once found to avoid spam
                
    return found_patterns

def load_substitutions(file_path="subs.txt"):
    subs = {}
    try:
        with open("subs.txt", "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    subs[key] = value
    except FileNotFoundError:
        print("[!] substitution file not found.")
    return subs

def check_substitutions(password):
    """
    Checks if the password is a common word disguised with simple numbers/symbols.
    e.g., 'P@ssw0rd' -> 'password'
    """
    # Simple L33t speak mapping
    subs = load_substitutions()
    
    normalized = password.lower()
    for symbol, letter in subs.items():
        normalized = normalized.replace(symbol, letter)
        
    if normalized in COMMON_PASSWORDS:
        # print("Hello World")
        return True, normalized
    return False, ""

def audit_password(password):
    # Main logic to score the password and generate feedback.
    
    score = 0
    feedback = []
    suggestions = []
    
    # 1. Critical Fail: Common/Leaked Password
    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "rating": "CRITICAL",
            "feedback": ["This is a known leaked password."],
            "suggestions": ["Change this immediately. Never use common words."]
        }

    # 2. Critical Fail: Disguised Common Password
    is_common_sub, original_word = check_substitutions(password)
    if is_common_sub:
         return {
            "score": 10,
            "rating": "VERY WEAK",
            "feedback": [f"This is just the word '{original_word}' with simple substitutions."],
            "suggestions": ["Substitutions like '@' for 'a' are easily guessed by hackers."]
        }

    # --- Scoring Logic ---
    
    # Base Score: Length (up to 40 points)
    length_score = min(len(password) * 4, 40)
    score += length_score
    if len(password) < 8:
        feedback.append("Password is too short.")
        suggestions.append("Make it at least 12 characters long.")
    
    # Complexity: Character Types (up to 30 points)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password))
    
    types_count = sum([has_upper, has_lower, has_digit, has_special])
    score += (types_count * 7.5) # Max 30
    
    if types_count < 3:
        suggestions.append("Mix uppercase, lowercase, numbers, and symbols.")

    # Entropy Bonus (up to 20 points)
    entropy = calculate_entropy(password)
    if entropy > 3.0:
        score += min(entropy * 5, 20)
    else:
        feedback.append("Character variety is low (repetitive).")

    # --- Penalties ---
    
    # Pattern Detection Penalty
    patterns = check_patterns(password)
    if patterns:
        score -= len(patterns) * 10
        feedback.extend(patterns)
        suggestions.append("Avoid keyboard rows like 'qwerty' or 'asdf'.")

    # Repetition Penalty (e.g., 'aaaa')
    if len(set(password)) < len(password) / 2:
        score -= 10
        feedback.append("Too many repeated characters.")

    # Clamp Score 0-100
    score = max(0, min(100, int(score)))

    # Determine Rating
    if score < 40: rating = "WEAK"
    elif score < 70: rating = "MODERATE"
    elif score < 90: rating = "STRONG"
    else: rating = "VERY STRONG"

    return {
        "score": score,
        "rating": rating,
        "feedback": feedback,
        "suggestions": suggestions
    }

# --- CLI Interface ---

def main():
    print("=========================================")
    print(" SmartGuard: Password Strength Auditor")
    print("=========================================")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a password to test: ")
        
        if user_input.lower() == 'exit':
            print("Stay safe! Exiting...")
            break
            
        result = audit_password(user_input)
        
        print("\n--- Analysis Result ---")
        print(f"Score: {result['score']}/100")
        print(f"Rating: {result['rating']}")
        
        if result['feedback']:
            print("\n  Issues Found:")
            for item in result['feedback']:
                print(f"   - {item}")
        
        if result['suggestions']:
            print("\n Suggestions:")
            for item in result['suggestions']:
                print(f"   - {item}")
                
        print("\n" + "-"*30 + "\n")

if __name__ == "__main__":
    main()