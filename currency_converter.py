import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

API_URL = "https://api.exchangerate-api.com/v4/latest/"
CACHE_FILE = "cached_rates.json"

class CurrencyConverter:
    def __init__(self, base="USD"):
        self.base = base
        self.rates = self.load_rates(base)

    def load_rates(self, base):
        try:
            response = requests.get(API_URL + base)
            data = response.json()
            self.cache_rates(data)
            return data["rates"]
        except:
            print("Using cached data.")
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f)
                    return data["rates"]
            else:
                messagebox.showerror("Error", "No internet and no cached data.")
                return {}

    def cache_rates(self, data):
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)

    def convert(self, amount, from_currency, to_currency):
        if from_currency != self.base:
            amount = amount / self.rates[from_currency]
        return round(amount * self.rates[to_currency], 4)

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("520x500")
        self.is_dark = False
        self.converter = CurrencyConverter()
        self.root.config(bg="#f0f4f7")
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#f0f4f7")
        header_frame.pack(fill='x', pady=(10, 0))
        tk.Label(header_frame, text="Currency Converter", font=("Arial", 26, "bold"), bg="#f0f4f7", fg="#0a4d68").pack(pady=(0, 10))

        self.base_currency = ttk.Combobox(self.root, values=list(self.converter.rates.keys()), state="readonly", width=12, font=("Arial", 13))
        self.base_currency.set("USD")
        self.base_currency.pack(pady=(0, 10))
        self.base_currency.bind("<<ComboboxSelected>>", self.update_base_currency)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(pady=10)

        self.amount_entry = ttk.Entry(frame, width=18, font=("Arial", 13))
        self.amount_entry.grid(row=0, column=0, padx=8, pady=8)
        self.amount_entry.insert(0, "1")

        self.from_currency = ttk.Combobox(frame, values=list(self.converter.rates.keys()), state="readonly", width=12, font=("Arial", 13))
        self.from_currency.grid(row=0, column=1, padx=8, pady=8)
        self.from_currency.set("USD")

        self.to_currency = ttk.Combobox(frame, values=list(self.converter.rates.keys()), state="readonly", width=12, font=("Arial", 13))
        self.to_currency.grid(row=0, column=2, padx=8, pady=8)
        self.to_currency.set("INR")

        swap_button = ttk.Button(frame, text="⇄", command=self.swap_currencies)
        swap_button.grid(row=0, column=3, padx=8, pady=8)

        convert_button = ttk.Button(self.root, text="Convert", command=self.perform_conversion)
        convert_button.pack(pady=12)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="green")
        self.result_label.pack(pady=6)

        self.rate_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f4f7", fg="gray")
        self.rate_label.pack(pady=(0, 8))

        ttk.Button(self.root, text="🌙 Toggle Theme", command=self.toggle_theme).pack(pady=3)
        ttk.Button(self.root, text="🧹 Clear History", command=self.clear_history).pack(pady=3)

        self.history_label = tk.Label(self.root, text="Conversion History:", font=("Arial", 14, "bold"), bg="#f0f4f7")
        self.history_label.pack(pady=(10, 0))

        self.history_text = tk.Text(self.root, height=8, width=60, state="disabled", bg="#eef7f9", font=("Arial", 11))
        self.history_text.pack(pady=8)

        self.root.bind('<Return>', lambda e: self.perform_conversion())

    def update_base_currency(self, event):
        new_base = self.base_currency.get()
        self.converter = CurrencyConverter(base=new_base)
        rates = list(self.converter.rates.keys())
        self.from_currency['values'] = rates
        self.to_currency['values'] = rates

    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            result = self.converter.convert(amount, from_curr, to_curr)
            result_str = f"{amount} {from_curr} = {result} {to_curr}"
            self.result_label.config(text=result_str)
            rate = self.converter.rates[to_curr] / self.converter.rates[from_curr]
            self.rate_label.config(text=f"1 {from_curr} = {rate:.4f} {to_curr}")
            self.log_history(result_str)
            # playsound("success.mp3")  # Uncomment if you have the sound file and playsound installed
        except ValueError:
            messagebox.showwarning("Input error", "Please enter a valid number.")

    def swap_currencies(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)

    def toggle_theme(self):
        if self.is_dark:
            self.root.config(bg="#f0f4f7")
            self.result_label.config(bg="#f0f4f7", fg="green")
            self.history_label.config(bg="#f0f4f7", fg="black")
            self.rate_label.config(bg="#f0f4f7", fg="gray")
            self.history_text.config(bg="#eef7f9", fg="black")
        else:
            self.root.config(bg="#2c2f33")
            self.result_label.config(bg="#2c2f33", fg="white")
            self.history_label.config(bg="#2c2f33", fg="white")
            self.rate_label.config(bg="#2c2f33", fg="lightgray")
            self.history_text.config(bg="#23272a", fg="white")
        self.is_dark = not self.is_dark

    def log_history(self, entry):
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")

    def clear_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
