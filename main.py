import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import string
import json
import os
from datetime import datetime
import hashlib
import re
import threading
import time

# Try to import pyperclip, fallback to tkinter clipboard
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

class ModernPasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✨ Amazing Password Generator ✨")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Initialize variables
        self.dark_mode = tk.BooleanVar(value=True)
        self.password_history = []
        self.load_history()
        
        # Configure styles
        self.setup_styles()
        
        # Create main interface
        self.create_interface()
        
        # Load initial theme
        self.toggle_theme()
    
    def setup_styles(self):
        """Setup custom styles for modern look"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define color schemes
        self.themes = {
            'dark': {
                'bg': '#1a1a2e',
                'secondary_bg': '#16213e',
                'accent': '#e94560',
                'text': '#ffffff',
                'secondary_text': '#a0a0a0',
                'success': '#0f3460',
                'button_bg': '#0f3460',
                'button_hover': '#e94560'
            },
            'light': {
                'bg': '#f8f9fa',
                'secondary_bg': '#ffffff',
                'accent': '#e94560',
                'text': '#2c3e50',
                'secondary_text': '#6c757d',
                'success': '#28a745',
                'button_bg': '#007bff',
                'button_hover': '#0056b3'
            }
        }
        
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="normal")
        self.button_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.password_font = font.Font(family="Courier", size=14, weight="bold")
    
    def create_interface(self):
        """Create the beautiful main interface"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.root['bg'])
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Password options section
        self.create_options_section(main_frame)
        
        # Password length section
        self.create_length_section(main_frame)
        
        # Generated password section
        self.create_password_section(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
        
        # Password strength indicator
        self.create_strength_indicator(main_frame)
        
        # History section
        self.create_history_section(main_frame)
    
    def create_header(self, parent):
        """Create beautiful header with title and theme toggle"""
        header_frame = tk.Frame(parent, bg=parent['bg'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🔐 Amazing Password Generator",
            font=self.title_font,
            bg=parent['bg'],
            fg='#ffffff'
        )
        title_label.pack(side='left')
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            header_frame,
            text="🌙" if self.dark_mode.get() else "☀️",
            font=("Helvetica", 16),
            bg='#e94560',
            fg='white',
            border=0,
            pady=8,
            padx=15,
            cursor='hand2',
            command=self.toggle_theme
        )
        self.theme_btn.pack(side='right')
        
        # Subtitle
        subtitle_label = tk.Label(
            parent,
            text="Generate secure, customizable passwords with beautiful design",
            font=self.subtitle_font,
            bg=parent['bg'],
            fg='#a0a0a0'
        )
        subtitle_label.pack(anchor='w', pady=(0, 20))
    
    def create_options_section(self, parent):
        """Create password options with beautiful checkboxes"""
        options_frame = tk.LabelFrame(
            parent,
            text="Password Options",
            font=self.subtitle_font,
            bg=parent['bg'],
            fg='#ffffff',
            bd=2,
            relief='groove'
        )
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Create a grid for options
        options_grid = tk.Frame(options_frame, bg=options_frame['bg'])
        options_grid.pack(padx=20, pady=15)
        
        # Initialize option variables
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        self.pronounceable = tk.BooleanVar(value=False)
        
        # Create styled checkboxes
        options = [
            ("🔤 Lowercase Letters", self.include_lowercase),
            ("🔠 Uppercase Letters", self.include_uppercase),
            ("🔢 Numbers", self.include_numbers),
            ("🔣 Symbols", self.include_symbols),
            ("❌ Exclude Ambiguous (0,O,l,1)", self.exclude_ambiguous),
            ("🗣️ Pronounceable", self.pronounceable)
        ]
        
        for i, (text, var) in enumerate(options):
            cb = tk.Checkbutton(
                options_grid,
                text=text,
                variable=var,
                font=("Helvetica", 10),
                bg=options_grid['bg'],
                fg='#ffffff',
                selectcolor='#e94560',
                activebackground=options_grid['bg'],
                activeforeground='#ffffff',
                cursor='hand2'
            )
            cb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
    
    def create_length_section(self, parent):
        """Create password length section with slider"""
        length_frame = tk.LabelFrame(
            parent,
            text="Password Length",
            font=self.subtitle_font,
            bg=parent['bg'],
            fg='#ffffff',
            bd=2,
            relief='groove'
        )
        length_frame.pack(fill='x', pady=(0, 20))
        
        length_container = tk.Frame(length_frame, bg=length_frame['bg'])
        length_container.pack(padx=20, pady=15)
        
        # Length slider
        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(
            length_container,
            text=f"Length: {self.length_var.get()} characters",
            font=("Helvetica", 11),
            bg=length_container['bg'],
            fg='#ffffff'
        )
        self.length_label.pack(anchor='w')
        
        self.length_scale = tk.Scale(
            length_container,
            from_=4,
            to=128,
            orient='horizontal',
            variable=self.length_var,
            bg='#0f3460',
            fg='#ffffff',
            troughcolor='#16213e',
            activebackground='#e94560',
            highlightthickness=0,
            command=self.update_length_label
        )
        self.length_scale.pack(fill='x', pady=(5, 0))
    
    def create_password_section(self, parent):
        """Create generated password display section"""
        password_frame = tk.LabelFrame(
            parent,
            text="Generated Password",
            font=self.subtitle_font,
            bg=parent['bg'],
            fg='#ffffff',
            bd=2,
            relief='groove'
        )
        password_frame.pack(fill='x', pady=(0, 20))
        
        password_container = tk.Frame(password_frame, bg=password_frame['bg'])
        password_container.pack(padx=20, pady=15, fill='x')
        
        # Password display with copy button
        password_display_frame = tk.Frame(password_container, bg=password_container['bg'])
        password_display_frame.pack(fill='x')
        
        self.password_var = tk.StringVar(value="Click 'Generate' to create a password")
        self.password_entry = tk.Entry(
            password_display_frame,
            textvariable=self.password_var,
            font=self.password_font,
            bg='#16213e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=10,
            state='readonly'
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.copy_btn = tk.Button(
            password_display_frame,
            text="📋 Copy",
            font=self.button_font,
            bg='#e94560',
            fg='white',
            border=0,
            pady=10,
            padx=20,
            cursor='hand2',
            command=self.copy_password
        )
        self.copy_btn.pack(side='right')
    
    def create_action_buttons(self, parent):
        """Create main action buttons"""
        button_frame = tk.Frame(parent, bg=parent['bg'])
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Generate button (main CTA)
        self.generate_btn = tk.Button(
            button_frame,
            text="✨ Generate Amazing Password",
            font=("Helvetica", 14, "bold"),
            bg='#e94560',
            fg='white',
            border=0,
            pady=15,
            cursor='hand2',
            command=self.generate_password
        )
        self.generate_btn.pack(fill='x', pady=(0, 10))
        
        # Secondary buttons row
        secondary_frame = tk.Frame(button_frame, bg=button_frame['bg'])
        secondary_frame.pack(fill='x')
        
        self.clear_btn = tk.Button(
            secondary_frame,
            text="🗑️ Clear",
            font=self.button_font,
            bg='#6c757d',
            fg='white',
            border=0,
            pady=8,
            padx=20,
            cursor='hand2',
            command=self.clear_password
        )
        self.clear_btn.pack(side='left', padx=(0, 10))
        
        self.save_btn = tk.Button(
            secondary_frame,
            text="💾 Save to History",
            font=self.button_font,
            bg='#28a745',
            fg='white',
            border=0,
            pady=8,
            padx=20,
            cursor='hand2',
            command=self.save_to_history
        )
        self.save_btn.pack(side='left')
    
    def create_strength_indicator(self, parent):
        """Create password strength indicator"""
        strength_frame = tk.Frame(parent, bg=parent['bg'])
        strength_frame.pack(fill='x', pady=(0, 20))
        
        strength_label = tk.Label(
            strength_frame,
            text="Password Strength:",
            font=("Helvetica", 10),
            bg=parent['bg'],
            fg='#ffffff'
        )
        strength_label.pack(anchor='w')
        
        # Strength indicator bars
        self.strength_bars_frame = tk.Frame(strength_frame, bg=parent['bg'])
        self.strength_bars_frame.pack(fill='x', pady=(5, 0))
        
        self.strength_bars = []
        for i in range(5):
            bar = tk.Frame(
                self.strength_bars_frame,
                bg='#16213e',
                height=8,
                width=100
            )
            bar.pack(side='left', fill='x', expand=True, padx=(0, 2 if i < 4 else 0))
            self.strength_bars.append(bar)
        
        self.strength_text = tk.Label(
            strength_frame,
            text="",
            font=("Helvetica", 9),
            bg=parent['bg'],
            fg='#a0a0a0'
        )
        self.strength_text.pack(anchor='w', pady=(5, 0))
    
    def create_history_section(self, parent):
        """Create password history section"""
        history_frame = tk.LabelFrame(
            parent,
            text="Password History",
            font=self.subtitle_font,
            bg=parent['bg'],
            fg='#ffffff',
            bd=2,
            relief='groove'
        )
        history_frame.pack(fill='both', expand=True)
        
        # History listbox with scrollbar
        history_container = tk.Frame(history_frame, bg=history_frame['bg'])
        history_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.history_listbox = tk.Listbox(
            history_container,
            bg='#16213e',
            fg='#ffffff',
            selectbackground='#e94560',
            font=("Courier", 10),
            relief='flat',
            bd=5
        )
        self.history_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(history_container, bg='#0f3460')
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Bind double-click to copy
        self.history_listbox.bind('<Double-1>', self.copy_from_history)
        
        self.load_history_display()
    
    def generate_password(self):
        """Generate a new password with selected options"""
        # Build character set
        chars = ""
        
        if self.include_lowercase.get():
            chars += string.ascii_lowercase
        if self.include_uppercase.get():
            chars += string.ascii_uppercase
        if self.include_numbers.get():
            chars += string.digits
        if self.include_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if self.exclude_ambiguous.get():
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        if not chars:
            messagebox.showerror("Error", "Please select at least one character type!")
            return
        
        length = self.length_var.get()
        
        if self.pronounceable.get():
            password = self.generate_pronounceable_password(length)
        else:
            password = ''.join(random.choice(chars) for _ in range(length))
        
        self.password_var.set(password)
        self.update_strength_indicator(password)
        self.animate_generation()
    
    def generate_pronounceable_password(self, length):
        """Generate a pronounceable password"""
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        numbers = "0123456789"
        symbols = "!@#$%"
        
        password = ""
        i = 0
        
        while len(password) < length:
            if i % 2 == 0:  # Consonant
                password += random.choice(consonants)
            else:  # Vowel
                password += random.choice(vowels)
            i += 1
        
        # Add some numbers and symbols randomly
        if self.include_numbers.get() and length > 4:
            pos = random.randint(0, len(password)-1)
            password = password[:pos] + random.choice(numbers) + password[pos+1:]
        
        if self.include_symbols.get() and length > 6:
            pos = random.randint(0, len(password)-1)
            password = password[:pos] + random.choice(symbols) + password[pos+1:]
        
        # Capitalize some letters
        if self.include_uppercase.get():
            password = ''.join(c.upper() if random.random() < 0.3 else c for c in password)
        
        return password[:length]
    
    def update_strength_indicator(self, password):
        """Update password strength indicator"""
        score = self.calculate_password_strength(password)
        
        # Reset all bars
        for bar in self.strength_bars:
            bar.config(bg='#16213e')
        
        # Color bars based on strength
        colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997']
        strength_texts = ['Very Weak', 'Weak', 'Fair', 'Good', 'Excellent']
        
        for i in range(min(score, 5)):
            self.strength_bars[i].config(bg=colors[i])
        
        self.strength_text.config(
            text=f"{strength_texts[min(score-1, 4)] if score > 0 else 'Very Weak'} "
                 f"({len(password)} characters)"
        )
    
    def calculate_password_strength(self, password):
        """Calculate password strength score (1-5)"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        
        return min(score, 5)
    
    def animate_generation(self):
        """Add a subtle animation effect when generating"""
        original_text = self.generate_btn['text']
        self.generate_btn.config(text="✨ Generating...", bg='#28a745')
        self.root.after(500, lambda: self.generate_btn.config(
            text=original_text, bg='#e94560'
        ))
    
    def copy_password(self):
        """Copy password to clipboard with feedback"""
        password = self.password_var.get()
        if password and password != "Click 'Generate' to create a password":
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(password)
            else:
                # Fallback to tkinter clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()  # Required for clipboard to work
            
            original_text = self.copy_btn['text']
            self.copy_btn.config(text="✅ Copied!", bg='#28a745')
            self.root.after(1500, lambda: self.copy_btn.config(
                text=original_text, bg='#e94560'
            ))
    
    def clear_password(self):
        """Clear the generated password"""
        self.password_var.set("Click 'Generate' to create a password")
        for bar in self.strength_bars:
            bar.config(bg='#16213e')
        self.strength_text.config(text="")
    
    def save_to_history(self):
        """Save current password to history"""
        password = self.password_var.get()
        if password and password != "Click 'Generate' to create a password":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                'password': password,
                'timestamp': timestamp,
                'length': len(password),
                'strength': self.calculate_password_strength(password)
            }
            self.password_history.append(entry)
            self.save_history()
            self.load_history_display()
            
            # Show feedback
            original_text = self.save_btn['text']
            self.save_btn.config(text="✅ Saved!", bg='#28a745')
            self.root.after(1500, lambda: self.save_btn.config(
                text=original_text, bg='#28a745'
            ))
    
    def copy_from_history(self, event):
        """Copy selected password from history"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            password = self.password_history[-(index+1)]['password']
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(password)
            else:
                # Fallback to tkinter clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def load_history(self):
        """Load password history from file"""
        try:
            if os.path.exists('password_history.json'):
                with open('password_history.json', 'r') as f:
                    self.password_history = json.load(f)
        except:
            self.password_history = []
    
    def save_history(self):
        """Save password history to file"""
        try:
            # Keep only last 50 entries
            self.password_history = self.password_history[-50:]
            with open('password_history.json', 'w') as f:
                json.dump(self.password_history, f)
        except:
            pass
    
    def load_history_display(self):
        """Load history into the listbox"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.password_history[-10:]):  # Show last 10
            display_text = f"{entry['timestamp']} | {entry['password'][:20]}{'...' if len(entry['password']) > 20 else ''}"
            self.history_listbox.insert(0, display_text)
    
    def update_length_label(self, value):
        """Update length label when slider moves"""
        self.length_label.config(text=f"Length: {value} characters")
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        current_theme = 'light' if self.dark_mode.get() else 'dark'
        colors = self.themes[current_theme]
        
        # Update main window
        self.root.configure(bg=colors['bg'])
        
        # Update theme button
        self.theme_btn.config(text="☀️" if current_theme == 'dark' else "🌙")
        
        # Toggle the variable
        self.dark_mode.set(not self.dark_mode.get())
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernPasswordGenerator()
    app.run()