# --- 1. Define the Color Codes ---
# Every code starts with \033[ and ends with m

# Text Colors (Foreground)
RED_TEXT = "\033[31m"
GREEN_TEXT = "\033[32m"
CYAN_TEXT = "\033[36m"

# Background Colors (\033[30m makes the text color black so it's readable)
GREEN_BG = "\033[42m\033[30m"
YELLOW_BG = "\033[43m\033[30m"
GREY_BG = "\033[100m\033[37m"

# The Reset Code (CRITICAL: If you don't use this, the color leaks forever!)
RESET = "\033[0m"


# --- 2. Test the Colors ---

print("--- Testing Text Colors ---")
print(f"{RED_TEXT}This text is red!")
print(f"{GREEN_TEXT}This text is green!{RESET}")
print(f"{CYAN_TEXT}This text is cyan!{RESET}")
print("Back to normal terminal text.\n")


print("--- Testing Wordle-style Background Tiles ---")
# Using end=" " keeps them all on the same line
print(f"{GREEN_BG} W {RESET}", end=" ")
print(f"{YELLOW_BG} O {RESET}", end=" ")
print(f"{GREY_BG} R {RESET}", end=" ")
print(f"{GREY_BG} D {RESET}", end=" ")
print(f"{GREEN_BG} S {RESET}", end="")

# A blank print at the end to move to a new line safely
print()