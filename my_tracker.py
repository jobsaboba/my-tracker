#!/usr/bin/env python3
import requests, tkinter as tk, re
from bs4 import BeautifulSoup
from tkinter import ttk, messagebox, simpledialog

# Your default trainers
D = ["Carroll", "Appleby", "Evans", "Butler", "Watson", "Fahey", "Boughey", "Brittain", "Loughnane", "Haynes", "Channon", "Carr"]

class App:
    def __init__(self, r):
        self.r = r
        r.title("10p Trainer Tracker")
        r.geometry("850x550")
        self.tr = list(D)
        
        # Header with Buttons
        b = tk.Frame(r); b.pack(pady=10)
        tk.Button(b, text="SCAN TRAINERS", command=self.scan, bg="#27ae60", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(b, text="ADD", command=self.add, bg="#2980b9", fg="white", width=8).grid(row=0, column=1, padx=5)
        tk.Button(b, text="REMOVE", command=self.rem, bg="#c0392b", fg="white", width=8).grid(row=0, column=2, padx=5)
        tk.Button(b, text="LIST", command=self.ls, bg="#7f8c8d", fg="white", width=8).grid(row=0, column=3, padx=5)
        
        # The Table
        self.t = ttk.Treeview(r, columns=(1, 2), show="headings")
        self.t.heading(1, text="Trainer Name"); self.t.heading(2, text="Status")
        self.t.column(1, width=250); self.t.column(2, width=550)
        self.t.pack(fill="both", expand=1, padx=10, pady=10)
        
        self.s = tk.Label(r, text="System Ready", font=('Arial', 10, 'bold')); self.s.pack()

    def ls(self): 
        messagebox.showinfo("Trainers", "\n".join(sorted(self.tr)))

    def add(self):
        n = simpledialog.askstring("Add", "Surname:")
        if n:
            name = n.strip().title()
            if name not in self.tr:
                self.tr.append(name)
                self.s.config(text=f"Added {name}")
                self.scan()
            else:
                messagebox.showinfo("Exists", f"{name} is already in the list.")

    def rem(self):
        sel = self.t.selection()
        if sel:
            name = self.t.item(sel)['values'][0].title()
        else:
            n = simpledialog.askstring("Remove", "Surname to Delete:")
            name = n.strip().title() if n else None

        if name and name in self.tr:
            self.tr.remove(name) # This removes it from the memory list
            self.s.config(text=f"Removed {name}")
            self.scan() # This clears and redraws the table
        elif name:
            messagebox.showwarning("Not Found", f"Could not find {name}")

    def scan(self):
        for i in self.t.get_children(): self.t.delete(i)
        self.s.config(text="Scanning Sporting Life..."); self.r.update()
        seen_today = set()
        try:
            h = {'User-Agent': 'Mozilla/5.0'}
            url = "https://www.sportinglife.com/racing/abc-guide/today/trainers"
            req = requests.get(url, headers=h, timeout=15)
            soup = BeautifulSoup(req.text, 'html.parser')
            f = 0
            for row in soup.find_all('tr'):
                row_text = row.get_text(" ", strip=True).lower()
                if "entries" in row_text:
                    for n in self.tr:
                        n_low = n.lower()
                        if n_low not in seen_today:
                            if re.search(r'\b' + re.escape(n_low) + r'\b', row_text):
                                self.t.insert("", "end", values=(n.upper(), "ACTIVE TODAY"))
                                seen_today.add(n_low)
                                f += 1
                                break
            self.s.config(text=f"Found {f} unique trainers.")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
