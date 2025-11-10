import tkinter as tk
from tkinter import ttk
import random

# -----------------------------
# Base de données des pilotes
# -----------------------------
f1PilotsDatabase = [
    {"id": 1, "name": "Max Verstappen", "speed": 10, "consistency": 9, "aggression": 8},
    {"id": 2, "name": "Sergio Pérez", "speed": 7, "consistency": 6, "aggression": 7},
    {"id": 3, "name": "Lewis Hamilton", "speed": 9, "consistency": 10, "aggression": 7},
    {"id": 4, "name": "George Russell", "speed": 8, "consistency": 8, "aggression": 7},
    {"id": 5, "name": "Charles Leclerc", "speed": 9, "consistency": 7, "aggression": 9},
    {"id": 6, "name": "Carlos Sainz", "speed": 8, "consistency": 9, "aggression": 6},
    {"id": 7, "name": "Lando Norris", "speed": 9, "consistency": 8, "aggression": 7},
    {"id": 8, "name": "Oscar Piastri", "speed": 8, "consistency": 8, "aggression": 6},
    {"id": 9, "name": "Fernando Alonso", "speed": 8, "consistency": 9, "aggression": 8},
    {"id": 10, "name": "Lance Stroll", "speed": 6, "consistency": 6, "aggression": 5},
    {"id": 11, "name": "Pierre Gasly", "speed": 7, "consistency": 7, "aggression": 7},
    {"id": 12, "name": "Esteban Ocon", "speed": 7, "consistency": 7, "aggression": 6},
    {"id": 13, "name": "Alexander Albon", "speed": 7, "consistency": 7, "aggression": 6},
    {"id": 14, "name": "Logan Sargeant", "speed": 5, "consistency": 5, "aggression": 5},
    {"id": 15, "name": "Yuki Tsunoda", "speed": 7, "consistency": 6, "aggression": 8},
    {"id": 16, "name": "Daniel Ricciardo", "speed": 7, "consistency": 6, "aggression": 7},
    {"id": 17, "name": "Nico Hülkenberg", "speed": 7, "consistency": 8, "aggression": 6},
    {"id": 18, "name": "Kevin Magnussen", "speed": 7, "consistency": 6, "aggression": 8},
    {"id": 19, "name": "Valtteri Bottas", "speed": 7, "consistency": 8, "aggression": 5},
    {"id": 20, "name": "Zhou Guanyu", "speed": 6, "consistency": 6, "aggression": 5},
]

# -----------------------------
# Classe principale
# -----------------------------
class RacingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur F1")
        self.root.geometry("900x700")
        self.root.configure(bg="#1f1f1f")

        # Pilotes sélectionnés
        self.pilots = [f1PilotsDatabase[0].copy(), f1PilotsDatabase[1].copy()]
        for i, p in enumerate(self.pilots):
            p.update({"position": i+1, "crashes": 0, "overtakes": 0})

        self.totalLaps = 10
        self.currentLap = 0
        self.isRunning = False

        # Style ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 11), background="#1e90ff", foreground="white", padding=5)
        self.style.map("TButton", background=[("active", "#63B8FF")], foreground=[("disabled", "#A9A9A9")])
        self.style.configure("TLabel", font=("Helvetica", 10), foreground="#F0F0F0", background="#1f1f1f")
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        # Frames
        self.frame_top = ttk.Frame(root, padding=10)
        self.frame_top.pack(fill="x")

        self.frame_pilots = ttk.Frame(root, padding=10)
        self.frame_pilots.pack(fill="x")

        self.frame_buttons = ttk.Frame(root, padding=10)
        self.frame_buttons.pack(fill="x")

        self.frame_events = ttk.Frame(root, padding=10)
        self.frame_events.pack(fill="both", expand=True)

        # Widgets
        ttk.Label(self.frame_top, text="Simulateur de Duel Pilote", style="Header.TLabel").pack(pady=5)

        self.create_pilot_selection()
        self.create_control_buttons()

        self.event_text = tk.Text(self.frame_events, height=15, bg="#333333", fg="white", state="disabled")
        self.event_text.pack(fill="both", expand=True)

    # -----------------
    # Sélection des pilotes
    # -----------------
    def create_pilot_selection(self):
        ttk.Label(self.frame_pilots, text="Choisissez vos pilotes:").pack()
        self.pilot_vars = [tk.StringVar(value=self.pilots[0]["name"]),
                           tk.StringVar(value=self.pilots[1]["name"])]

        self.option_menus = []
        for i in range(2):
            frame = ttk.Frame(self.frame_pilots, padding=5)
            frame.pack(side="left", padx=20)
            ttk.Label(frame, text=f"Pilote {i+1}:", style="Header.TLabel").pack()
            menu = ttk.OptionMenu(frame, self.pilot_vars[i],
                                  self.pilot_vars[i].get(),
                                  *[p["name"] for p in f1PilotsDatabase],
                                  command=lambda val, i=i: self.select_pilot(i, val))
            menu.pack(pady=5)
            self.option_menus.append(menu)

    def select_pilot(self, index, name):
        pilot = next(p for p in f1PilotsDatabase if p["name"] == name)
        self.pilots[index] = pilot.copy()
        self.pilots[index].update({"position": index+1, "crashes":0, "overtakes":0})

    # -----------------
    # Contrôles
    # -----------------
    def create_control_buttons(self):
        ttk.Button(self.frame_buttons, text="Lancer la course", command=self.run_simulation).pack(side="left", padx=10)
        ttk.Button(self.frame_buttons, text="Réinitialiser", command=self.reset_simulation).pack(side="left", padx=10)

    # -----------------
    # Simulation
    # -----------------
    def simulate_lap(self):
        events = []
        for pilot in self.pilots:
            noise = (random.random() - 0.5) * (10 - pilot["consistency"])
            aggression_bonus = pilot["aggression"]*0.5 if random.random() < (pilot["aggression"]/10) else 0
            score = pilot["speed"]*0.4 + pilot["consistency"]*0.3 + aggression_bonus*0.3 + noise
            crash_risk = pilot["aggression"]/50 + random.random()*0.1
            if crash_risk > 0.15:
                pilot["crashes"] += 1
                score *= 0.5
                events.append(f"{pilot['name']} a eu un incident !")
            pilot["score"] = score

        # Trier par score
        self.pilots.sort(key=lambda p: p["score"], reverse=True)
        for i, pilot in enumerate(self.pilots):
            old_pos = pilot["position"]
            pilot["position"] = i+1
            if old_pos > pilot["position"]:
                pilot["overtakes"] += 1
                events.append(f"{pilot['name']} dépasse et passe P{pilot['position']} !")
        return events

    # -----------------
    # Lancer la course
    # -----------------
    def run_simulation(self):
        if self.isRunning:
            return
        self.isRunning = True
        self.currentLap = 0
        self.event_text.configure(state="normal")
        self.event_text.delete("1.0", tk.END)
        self.event_text.configure(state="disabled")
        self.root.after(500, self.next_lap)

    def next_lap(self):
        if self.currentLap >= self.totalLaps:
            self.isRunning = False
            winner = self.pilots[0]["name"]
            self.add_event(f"🏁 Course terminée ! Vainqueur: {winner}")
            return
        self.currentLap += 1
        events = self.simulate_lap()
        for e in events:
            self.add_event(f"Tour {self.currentLap}: {e}")
        self.root.after(800, self.next_lap)

    # -----------------
    # Ajouter un événement
    # -----------------
    def add_event(self, message):
        self.event_text.configure(state="normal")
        self.event_text.insert(tk.END, message + "\n")
        self.event_text.see(tk.END)
        self.event_text.configure(state="disabled")

    # -----------------
    # Réinitialiser
    # -----------------
    def reset_simulation(self):
        self.isRunning = False
        self.currentLap = 0
        self.pilots = [f1PilotsDatabase[0].copy(), f1PilotsDatabase[1].copy()]
        for i, p in enumerate(self.pilots):
            p.update({"position": i+1, "crashes": 0, "overtakes": 0})
        self.event_text.configure(state="normal")
        self.event_text.delete("1.0", tk.END)
        self.event_text.configure(state="disabled")
        for i in range(2):
            self.pilot_vars[i].set(self.pilots[i]["name"])

# -----------------------------
# Lancer l'application
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RacingSimulator(root)
    root.mainloop()
