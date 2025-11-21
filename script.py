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
# Temps de base circuits 2024
# -----------------------------
CIRCUITS_2024 = {
    "Bahreïn": 91.0,
    "Djeddah": 88.5,
    "Melbourne": 87.5,
    "Suzuka": 89.0,
    "Shanghai": 95.0,
    "Miami": 92.0,
    "Imola": 88.0,
    "Monaco": 73.5,
    "Barcelone": 80.5,
    "Montréal": 72.5,
    "Red Bull Ring": 65.5,
    "Silverstone": 87.0,
    "Hungaroring": 77.5,
    "Spa": 104.0,
    "Zandvoort": 72.5,
    "Monza": 81.0,
    "Singapour": 100.0,
    "Austin": 97.0,
    "Mexique": 78.0,
    "Interlagos": 71.0,
    "Las Vegas": 95.0,
    "Abu Dhabi": 94.0
}

# -----------------------------
# Incidents
# -----------------------------
F1_INCIDENTS = [
    {"text": "fait une petite erreur au freinage", "penalty": 1.5},
    {"text": "bloque une roue et élargit", "penalty": 2.0},
    {"text": "glisse en sortie de virage", "penalty": 1.2},
    {"text": "sort un peu large", "penalty": 2.5},
    {"text": "fait un tête-à-queue", "penalty": 4.5},
]

# =====================================================
#              CLASSE PRINCIPALE
# =====================================================
class RacingSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur Duel F1")
        self.root.geometry("1000x700")
        self.root.configure(bg="#101010")

        self.totalLaps = 20
        self.currentLap = 0
        self.isRunning = False

        # Meilleur tour
        self.fastest_lap_time = None
        self.fastest_lap_driver = None

        # Sélection pilotes + circuit
        self.pilot_vars = [tk.StringVar(), tk.StringVar()]
        self.pilot_vars[0].set(f1PilotsDatabase[0]["name"])
        self.pilot_vars[1].set(f1PilotsDatabase[1]["name"])
        self.circuit_var = tk.StringVar(value=list(CIRCUITS_2024.keys())[0])

        # =============================
        # UI
        # =============================
        title = ttk.Label(root, text="SIMULATEUR F1 – DUEL 2 PILOTES",
                          font=("Helvetica", 18, "bold"), background="#101010", foreground="white")
        title.pack(pady=10)

        # Circuit + Pilotes
        top = ttk.Frame(root)
        top.pack()

        # Circuit
        c_frame = ttk.Frame(top)
        c_frame.grid(row=0, column=0, padx=20)
        ttk.Label(c_frame, text="Circuit :", background="#101010", foreground="white").pack()
        ttk.OptionMenu(c_frame, self.circuit_var, self.circuit_var.get(), *CIRCUITS_2024.keys()).pack()

        # Pilotes
        p_frame = ttk.Frame(top)
        p_frame.grid(row=0, column=1, padx=20)

        for i in range(2):
            ttk.Label(p_frame, text=f"Pilote {i+1} :", background="#101010", foreground="white").grid(row=0, column=i)
            ttk.OptionMenu(
                p_frame, self.pilot_vars[i], self.pilot_vars[i].get(),
                *[p["name"] for p in f1PilotsDatabase],
                command=lambda _, idx=i: self.select_pilot(idx)
            ).grid(row=1, column=i, padx=10)

        # Info tour
        self.lap_label = ttk.Label(root, text=f"Tour : 0 / {self.totalLaps}",
                                   background="#101010", foreground="white")
        self.lap_label.pack(pady=5)

        # Tableau style F1 TV
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="x", padx=20)

        self.table = ttk.Treeview(table_frame, columns=("pos", "name", "pit", "inc", "gap"),
                                  show="headings", height=4)
        self.table.pack(fill="x")

        for col, text in zip(("pos", "name", "pit", "inc", "gap"),
                             ("Pos", "Pilote", "Pits", "Inc.", "Écart")):
            self.table.heading(col, text=text)

        # Journal
        ttk.Label(root, text="Journal de course :", background="#101010",
                  foreground="white").pack(anchor="w", padx=20)
        self.event_text = tk.Text(root, height=12, bg="#181818", fg="white", state="disabled")
        self.event_text.pack(fill="both", expand=True, padx=20, pady=5)

        # Tags couleurs
        self.event_text.tag_config("incident", foreground="#ff4c4c")
        self.event_text.tag_config("pit", foreground="#00b7ff")
        self.event_text.tag_config("overtake", foreground="#a020f0")
        self.event_text.tag_config("info", foreground="#ffffff")

        # Boutons
        b_frame = ttk.Frame(root)
        b_frame.pack(pady=10)
        ttk.Button(b_frame, text="🚀 Lancer la course", command=self.run_simulation).grid(row=0, column=0, padx=20)
        ttk.Button(b_frame, text="🔄 Réinitialiser", command=self.reset_simulation).grid(row=0, column=1, padx=20)

        # Init pilotes
        self.init_pilots()

    # =====================================================
    # UTIL : Format temps F1 (m:ss.xxx)
    # =====================================================
    def format_time(self, s):
        m = int(s // 60)
        sec = s % 60
        return f"{m}:{sec:06.3f}"

    # =====================================================
    # Initialisation pilotes
    # =====================================================
    def init_pilots(self):
        self.pilots = []
        for i in range(2):
            data = next(p for p in f1PilotsDatabase if p["name"] == self.pilot_vars[i].get()).copy()
            data.update({
                "position": i+1,
                "incidents": 0,
                "pit_stops": 0,
                "pit_done": False,
                "total_time": 0.0
            })
            self.pilots.append(data)
        self.update_table()

    # Changement pilote depuis menu
    def select_pilot(self, index):
        name = self.pilot_vars[index].get()
        data = next(p for p in f1PilotsDatabase if p["name"] == name).copy()
        data.update({
            "position": index+1,
            "incidents": 0,
            "pit_stops": 0,
            "pit_done": False,
            "total_time": 0.0
        })
        self.pilots[index] = data
        self.update_table()

    # =====================================================
    # TABLEAU
    # =====================================================
    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        ordered = sorted(self.pilots, key=lambda x: x["total_time"])
        leader = ordered[0]["total_time"]

        for p in ordered:
            gap = p["total_time"] - leader
            gap_text = "-" if gap == 0 else f"+{gap:.3f}"
            self.table.insert("", "end",
                              values=(f"P{ordered.index(p)+1}", p["name"],
                                      p["pit_stops"], p["incidents"], gap_text))

    # =====================================================
    # CALCUL TEMPS AU TOUR
    # =====================================================
    def simulate_lap(self):
        events = []
        base = CIRCUITS_2024[self.circuit_var.get()]

        for p in self.pilots:

            # Calcul réaliste
            speed = (10 - p["speed"]) * 0.35
            const = (10 - p["consistency"]) * 0.20
            variance = random.uniform(-0.4, 0.4) * (1.3 - p["consistency"]/10)

            perfect = 0
            if random.random() < (0.02 + p["consistency"]/200):
                perfect = random.uniform(-0.25, -0.10)

            lap = base + speed + const + variance + perfect

            # PIT stop ?
            remaining = self.totalLaps - self.currentLap
            must_pit = False

            if not p["pit_done"]:
                pit_prob = 0.04 + max(0, 10 - remaining) * 0.03
                if random.random() < pit_prob:
                    must_pit = True
                if remaining <= 2:
                    must_pit = True

            if must_pit:
                p["pit_done"] = True
                p["pit_stops"] += 1
                lap += 18
                events.append((f"{p['name']} effectue un arrêt (+18s)", "pit"))

            # INCIDENT
            if p["aggression"]/60 + random.random()*0.05 > 0.16:
                inc = random.choice(F1_INCIDENTS)
                p["incidents"] += 1
                lap += inc["penalty"]
                events.append((f"{p['name']} {inc['text']} (+{inc['penalty']}s)", "incident"))

            # Meilleur tour
            if self.fastest_lap_time is None or lap < self.fastest_lap_time:
                self.fastest_lap_time = lap
                self.fastest_lap_driver = p["name"]
                events.append((f"🔥 Meilleur tour pour {p['name']} : {self.format_time(lap)}", "overtake"))

            # Update temps total
            p["total_time"] += lap

        self.pilots.sort(key=lambda x: x["total_time"])
        return events

    # =====================================================
    # LANCER LA COURSE
    # =====================================================
    def run_simulation(self):
        if self.isRunning:
            return

        self.isRunning = True
        self.currentLap = 0
        self.fastest_lap_time = None
        self.fastest_lap_driver = None

        self.init_pilots()
        self.update_table()

        self.event_text.config(state="normal")
        self.event_text.delete("1.0", tk.END)
        self.event_text.config(state="disabled")

        self.add_event(f"Départ du Grand Prix de {self.circuit_var.get()} !", "info")
        self.root.after(800, self.next_lap)

    # =====================================================
    # PROCHAIN TOUR
    # =====================================================
    def next_lap(self):
        if self.currentLap >= self.totalLaps:

            # PIT manquant
            for p in self.pilots:
                if not p["pit_done"]:
                    p["pit_stops"] += 1
                    p["total_time"] += 20
                    self.add_event(f"⚠️ {p['name']} n'avait pas fait d'arrêt : +20s", "pit")

            # Meilleur tour final
            if self.fastest_lap_time:
                self.add_event(
                    f"⏱️ Meilleur tour : {self.fastest_lap_driver} en {self.format_time(self.fastest_lap_time)}",
                    "info"
                )

            # Classement final
            self.pilots.sort(key=lambda x: x["total_time"])
            winner = self.pilots[0]["name"]
            self.add_event(f"🏁 Vainqueur : {winner}", "info")

            self.update_table()
            self.isRunning = False
            return

        # Sinon on continue
        self.currentLap += 1
        self.lap_label.config(text=f"Tour : {self.currentLap} / {self.totalLaps}")

        events = self.simulate_lap()
        self.update_table()

        for msg, tag in events:
            self.add_event(f"[Tour {self.currentLap}] {msg}", tag)

        self.root.after(800, self.next_lap)

    # =====================================================
    # JOURNAL
    # =====================================================
    def add_event(self, text, tag="info"):
        self.event_text.config(state="normal")
        self.event_text.insert(tk.END, text + "\n", tag)
        self.event_text.see(tk.END)
        self.event_text.config(state="disabled")

    # =====================================================
    # RESET
    # =====================================================
    def reset_simulation(self):
        self.isRunning = False
        self.currentLap = 0
        self.fastest_lap_time = None
        self.fastest_lap_driver = None

        self.lap_label.config(text=f"Tour : 0 / {self.totalLaps}")
        self.init_pilots()

        self.event_text.config(state="normal")
        self.event_text.delete("1.0", tk.END)
        self.event_text.config(state="disabled")


# =====================================================
# LANCER L'APP
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RacingSimulator(root)
    root.mainloop()
