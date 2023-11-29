import random
import string
import requests
import hashlib
import tkinter as tk 
from tkinter import messagebox


def generate_password():
    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Most of them are letters, then numbers, then special characters
    password_letters = ''.join(random.choice(letters) for _ in range(7))
    password_digits = ''.join(random.choice(digits) for _ in range(random.randint(2, 3)))
    password_symbols = ''.join(random.choice(symbols) for _ in range(12 - len(password_letters) - len(password_digits)))

    # Combine them
    password = password_letters + password_digits + password_symbols

    # Make it random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

# Generate password
generated_password = generate_password()
print("Password is being generated:", generated_password)


#Checking password health part
def check_password_strength(password):
    #Check length
    good_length = len(password) >= 12

    #Check if it contains uppercase and lowercase letters
    uppercase_letters = any(char.isupper() for char in password)
    lowercase_letters = any(char.islower() for char in password)
    good_letters = uppercase_letters and lowercase_letters
    
    #Check if it contains numbers
    good_numbers = any(char.isdigit() for char in password)

    #Check if it contains special characters
    good_symbols = any(char in string.punctuation for char in password)

    #Overall strength 
    is_strong = good_length and good_letters and good_numbers and good_symbols

    #Give comments
    strength_feedback = "Strong" if is_strong else "Weak"

    return strength_feedback

#Test the strength of the generated password
strength_result = check_password_strength(generated_password)
print("Password Generated Health:", strength_result)

#Detecting compromised password part

def check_password_compromised(password):
    #Hash password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    #Send the request to HIBP API
    url = f'https://api.pwnedpasswords.com/range/{sha1_password[:5]}'
    response = requests.get(url)

    #Check if the hash prefix is found in the request
    return sha1_password[5:] in response.text

# GUI setup
root = tk.Tk()
root.title("Password Generator and Checker")

# Password generation
password_label = tk.Label(root, text="Generated Password:")
password_display = tk.Entry(root)
password_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
password_display.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Password strength check
strength_label = tk.Label(root, text="Password Strength:")
strength_display = tk.Entry(root)
strength_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
strength_display.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# User password input
entry_label = tk.Label(root, text="Test your password:")
entry = tk.Entry(root)
entry_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Test password button
def test_password():
    user_password = entry.get()

    # Check if the entry field is empty
    if not user_password:
        messagebox.showwarning("Warning", "Please enter a password.")
        return

    try:
        is_compromised = check_password_compromised(user_password)
        if is_compromised:
            messagebox.showwarning("Warning", "Password has been compromised!")
        else:
            messagebox.showinfo("Password Check", "Your password is secure.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

test_button = tk.Button(root, text="Test Your Password", command=test_password)
test_button.grid(row=3, column=0, columnspan=2, pady=10)

# Generate password button
def generate_new_password():
    generated_password = generate_password()
    password_display.delete(0, tk.END)
    password_display.insert(0, generated_password)

    # Test the strength of the generated password
    strength_result = check_password_strength(generated_password)
    strength_display.delete(0, tk.END)
    strength_display.insert(0, strength_result)

generate_button = tk.Button(root, text="Generate New Password", command=generate_new_password)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()