import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from score import calculate_score

class FantasyCricketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Cricket Game")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f0f0")
        
        # State Variables
        self.team_name = "None"
        self.total_points = 100
        self.points_used = 0
        
        self.counts = {'BAT': 0, 'BWL': 0, 'AR': 0, 'WK': 0}
        self.selected_players = {} # Name: (Category, Value)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top Frame: Current Allocations
        top_frame = tk.LabelFrame(self.root, text="Your Team Statistics", font=("Arial", 10, "bold"), bg="#e1e1e1", padx=10, pady=10)
        top_frame.pack(fill="x", padx=10,pady=5)
        
        self.lbl_bat = tk.Label(top_frame, text="Batsmen (BAT): 0", bg="#e1e1e1")
        self.lbl_bat.grid(row=0, column=0, padx=15)
        self.lbl_bwl = tk.Label(top_frame, text="Bowlers (BWL): 0", bg="#e1e1e1")
        self.lbl_bwl.grid(row=0, column=1, padx=15)
        self.lbl_ar = tk.Label(top_frame, text="All-Rounders (AR): 0", bg="#e1e1e1")
        self.lbl_ar.grid(row=0, column=2, padx=15)
        self.lbl_wk = tk.Label(top_frame, text="Wicket-Keepers (WK): 0", bg="#e1e1e1")
        self.lbl_wk.grid(row=0, column=3, padx=15)
        
        # Point trackers
        self.lbl_points_avail = tk.Label(top_frame, text="Points Available: 100", font=("Arial", 10, "bold"), fg="green", bg="#e1e1e1")
        self.lbl_points_avail.grid(row=1, column=0, columnspan=2, pady=5)
        self.lbl_points_used = tk.Label(top_frame, text="Points Used: 0", font=("Arial", 10, "bold"), fg="blue", bg="#e1e1e1")
        self.lbl_points_used.grid(row=1, column=2, columnspan=2, pady=5)

        self.lbl_team = tk.Label(self.root, text=f"Team Name: {self.team_name}", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.lbl_team.pack(pady=5)

        # Middle Selection Area
        mid_frame = tk.Frame(self.root, bg="#f0f0f0")
        mid_frame.pack(fill="both", expand=True, padx=10)
        
        # Left: Available Pool
        left_pool = tk.Frame(mid_frame, bg="#f0f0f0")
        left_pool.pack(side="left", fill="both", expand=True, padx=5)
        
        # Category Selectors (Radio buttons)
        self.cat_var = tk.StringVar(value="BAT")
        cat_frame = tk.Frame(left_pool, bg="#f0f0f0")
        cat_frame.pack(anchor="w")
        
        for cat in ['BAT', 'BWL', 'AR', 'WK']:
            tk.Radiobutton(cat_frame, text=cat, variable=self.cat_var, value=cat, command=self.load_category_players, bg="#f0f0f0").pack(side="left", padx=5)
            
        self.box_available = tk.Listbox(left_pool, font=("Arial", 10))
        self.box_available.pack(fill="both", expand=True, pady=5)
        self.box_available.bind("<Double-1>", self.add_player)
        
        # Right: Chosen Selection
        right_pool = tk.Frame(mid_frame, bg="#f0f0f0")
        right_pool.pack(side="right", fill="both", expand=True, padx=5)
        
        tk.Label(right_pool, text="Selected Players (Double click to remove)", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.box_selected = tk.Listbox(right_pool, font=("Arial", 10), fg="darkblue")
        self.box_selected.pack(fill="both", expand=True, pady=5)
        self.box_selected.bind("<Double-1>", self.remove_player)
        
        # Footer Action Control Panel
        btn_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="NEW TEAM", command=self.new_team, width=12, bg="#4CAF50", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="SAVE TEAM", command=self.save_team, width=12, bg="#2196F3", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="OPEN TEAM", command=self.open_team, width=12, bg="#FF9800", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="EVALUATE SCORE", command=self.evaluate_team, width=15, bg="#9C27B0", fg="white").pack(side="right", padx=10)
        
        # Initial Population
        self.load_category_players()

    def update_displays(self):
        self.lbl_team.config(text=f"Team Name: {self.team_name}")
        self.lbl_bat.config(text=f"Batsmen (BAT): {self.counts['BAT']}")
        self.lbl_bwl.config(text=f"Bowlers (BWL): {self.counts['BWL']}")
        self.lbl_ar.config(text=f"All-Rounders (AR): {self.counts['AR']}")
        self.lbl_wk.config(text=f"Wicket-Keepers (WK): {self.counts['WK']}")
        
        self.lbl_points_avail.config(text=f"Points Available: {self.total_points - self.points_used}")
        self.lbl_points_used.config(text=f"Points Used: {self.points_used}")
        
        # Refresh Selection Box UI
        self.box_selected.delete(0, tk.END)
        for name in self.selected_players:
            self.box_selected.insert(tk.END, name)

    def load_category_players(self):
        self.box_available.delete(0, tk.END)
        category = self.cat_var.get()
        try:
            conn = sqlite3.connect('fantasy.db')
            cursor = conn.cursor()
            cursor.execute("SELECT player FROM stats WHERE ctg=?", (category,))
            for row in cursor.fetchall():
                # Avoid showing already chosen players in the selection list
                if row[0] not in self.selected_players:
                    self.box_available.insert(tk.END, row[0])
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Could not read from database: {e}")

    def validate_and_extract_player_stats(self, p_name):
        conn = sqlite3.connect('fantasy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ctg, value FROM stats WHERE player=?", (p_name,))
        res = cursor.fetchone()
        conn.close()
        return res

    def add_player(self, event):
        if self.team_name == "None":
            messagebox.showwarning("Warning", "Please initiate a 'NEW TEAM' first.")
            return
            
        selection = self.box_available.curselection()
        if not selection: return
        
        p_name = self.box_available.get(selection[0])
        ctg, val = self.validate_and_extract_player_stats(p_name)
        
        # Validation Checks
        if len(self.selected_players) >= 11:
            messagebox.showerror("Validation Error", "Maximum of 11 players allowed.")
            return
        if self.points_used + val > self.total_points:
            messagebox.showerror("Validation Error", "Not enough remaining points allocation.")
            return
            
        # Extra safeguards based on positional caps 
        if ctg == 'WK' and self.counts['WK'] >= 1:
            messagebox.showerror("Validation Error", "Only 1 Wicket Keeper is permitted.")
            return

        # Commit logic additions
        self.selected_players[p_name] = (ctg, val)
        self.counts[ctg] += 1
        self.points_used += val
        
        self.update_displays()
        self.load_category_players()

    def remove_player(self, event):
        selection = self.box_selected.curselection()
        if not selection: return
        
        p_name = self.box_selected.get(selection[0])
        ctg, val = self.selected_players[p_name]
        
        del self.selected_players[p_name]
        self.counts[ctg] -= 1
        self.points_used -= val
        
        self.update_displays()
        self.load_category_players()

    def new_team(self):
        name = simpledialog.askstring("Team Identity Setting", "Enter unique team name:")
        if name:
            self.team_name = name
            self.selected_players.clear()
            self.counts = {'BAT': 0, 'BWL': 0, 'AR': 0, 'WK': 0}
            self.points_used = 0
            self.update_displays()
            self.load_category_players()

    def save_team(self):
        if self.team_name == "None" or not self.selected_players:
            messagebox.showerror("Save Error", "Cannot save an empty/non-existent team structure.")
            return
            
        # Core Roster Checklist Rule Constraints
        if len(self.selected_players) != 11:
            messagebox.showerror("Validation Error", "Teams must consist of exactly 11 players.")
            return
        if self.counts['BAT'] < 3 or self.counts['BWL'] < 3 or self.counts['AR'] < 1 or self.counts['WK'] < 1:
            messagebox.showerror("Validation Error", "Criteria incomplete. Required: Minimum 3 BAT, 3 BWL, 1 AR, 1 WK.")
            return
            
        p_string = ",".join(self.selected_players.keys())
        try:
            conn = sqlite3.connect('fantasy.db')
            cursor = conn.cursor()
            
            # Check if team already exists, replace it if it does
            cursor.execute("DELETE FROM teams WHERE name=?", (self.team_name,))
            cursor.execute("INSERT INTO teams (name, players, value) VALUES (?, ?, ?)", 
                           (self.team_name, p_string, self.points_used))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Team '{self.team_name}' successfully saved to database!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")

    def open_team(self):
        try:
            conn = sqlite3.connect('fantasy.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM teams")
            teams = [row[0] for row in cursor.fetchall()]
            
            if not teams:
                messagebox.showinfo("Information", "No saved configurations found in data store.")
                conn.close()
                return
                
            # Ask the user for the team name via simple prompt string match
            team_choice = simpledialog.askstring("Open Team Selector", f"Available Teams:\n{', '.join(teams)}\n\nEnter Team Name:")
            if team_choice not in teams:
                if team_choice: messagebox.showerror("Error", "Selected team setup does not exist.")
                conn.close()
                return
                
            cursor.execute("SELECT players FROM teams WHERE name=?", (team_choice,))
            players_list = cursor.fetchone()[0].split(',')
            
            # Rebuild Team Configuration
            self.team_name = team_choice
            self.selected_players.clear()
            self.counts = {'BAT': 0, 'BWL': 0, 'AR': 0, 'WK': 0}
            self.points_used = 0
            
            for player in players_list:
                cursor.execute("SELECT ctg, value FROM stats WHERE player=?", (player,))
                ctg, val = cursor.fetchone()
                self.selected_players[player] = (ctg, val)
                self.counts[ctg] += 1
                self.points_used += val
                
            conn.close()
            self.update_displays()
            self.load_category_players()
            messagebox.showinfo("Loaded", f"Team configuration '{team_choice}' is active.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Access Error", str(e))

    def evaluate_team(self):
        if not self.selected_players or len(self.selected_players) != 11:
            messagebox.showerror("Evaluation Failed", "Load or fully compile an 11-player setup first.")
            return
            
        try:
            conn = sqlite3.connect('fantasy.db')
            cursor = conn.cursor()
            
            total_team_score = 0
            breakdown_msg = f"Match Summary Performance Breakdown ({self.team_name}):\n" + "-"*50 + "\n"
            
            for player in self.selected_players:
                cursor.execute("SELECT * FROM match WHERE player=?", (player,))
                match_data = cursor.fetchone()
                
                if match_data:
                    p_score = calculate_score(match_data)
                else:
                    p_score = 0 # Player sat out/did not register matching data record
                    
                total_team_score += p_score
                breakdown_msg += f"{player}: {p_score} Points\n"
                
            breakdown_msg += "-"*50 + f"\nAGGREGATED TEAM TOTAL SCORE: {total_team_score} Points"
            
            # Show output inside modular dialog window
            messagebox.showinfo("Performance Metrics Evaluation Grid", breakdown_msg)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Evaluation system fetch failure", str(e))

if __name__ == '__main__':
    # Initialize DB first to guarantee data state safety
    from database import create_database
    create_database()
    
    root = tk.Tk()
    app = FantasyCricketApp(root)
    root.mainloop()