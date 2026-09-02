"""
main.py - Graphical User Interface (GUI) for Stone Paper Scissors Game.
Built using Python's standard tkinter and ttk libraries.
Designed with compact, guaranteed-visible controls for all screen resolutions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import (
    STONE, PAPER, SCISSORS, CHOICES, CHOICE_ICONS,
    get_computer_choice, determine_winner, get_result_explanation
)

# Modern Slate / Indigo Color Palette
COLOR_BG = "#0f172a"        # Dark slate background
COLOR_PANEL = "#1e293b"     # Card panel background
COLOR_ACCENT = "#38bdf8"    # Sky blue accent
COLOR_TEXT_MAIN = "#f8fafc" # Light text
COLOR_TEXT_MUTED = "#94a3b8"# Muted text
COLOR_WIN = "#22c55e"       # Green
COLOR_LOSE = "#ef4444"      # Red
COLOR_DRAW = "#f59e0b"      # Amber/Yellow
COLOR_BTN = "#334155"       # Button dark slate
COLOR_BTN_HOVER = "#475569" # Button hover slate


class StonePaperScissorsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stone Paper Scissors - Python GUI Edition")
        
        # Responsive sizing to fit on any screen (including 125%/150% Windows scaling)
        self.root.geometry("560x620")
        self.root.minsize(500, 540)
        self.root.configure(bg=COLOR_BG)

        # Game State
        self.user_score = 0
        self.computer_score = 0
        self.draws = 0
        self.round_number = 0

        # Build UI layout in strict order of visibility
        self._setup_styles()
        self._build_header()
        self._build_scoreboard()
        self._build_battle_arena()
        self._build_choice_menu()
        self._build_control_buttons()   # Guaranteed visible controls
        self._build_history_panel()

        # Keyboard shortcuts
        self.root.bind("1", lambda event: self.play_round(STONE))
        self.root.bind("2", lambda event: self.play_round(PAPER))
        self.root.bind("3", lambda event: self.play_round(SCISSORS))
        self.root.bind("<r>", lambda event: self.restart_game())
        self.root.bind("<Escape>", lambda event: self.exit_and_show_final_score())

    def _setup_styles(self):
        """Configure ttk styles for clean visual appearance."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT_MAIN)

    def _build_header(self):
        """Top title and instructions banner."""
        header_frame = tk.Frame(self.root, bg=COLOR_BG, pady=6)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="STONE  PAPER  SCISSORS",
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_BG,
            fg=COLOR_ACCENT
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Click a move or press keys [1], [2], [3] on your keyboard",
            font=("Segoe UI", 9),
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED
        )
        subtitle_label.pack()

    def _build_scoreboard(self):
        """Card-based scoreboard tracking scores."""
        score_container = tk.Frame(self.root, bg=COLOR_BG)
        score_container.pack(fill=tk.X, padx=16, pady=4)

        # 4 equal stat columns
        for c in range(4):
            score_container.columnconfigure(c, weight=1)

        def create_stat_card(parent, col, title, initial_val, color):
            card = tk.Frame(parent, bg=COLOR_PANEL, bd=1, relief=tk.FLAT, padx=6, pady=6)
            card.grid(row=0, column=col, padx=3, sticky="nsew")
            
            title_lbl = tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
            title_lbl.pack()
            
            val_lbl = tk.Label(card, text=str(initial_val), font=("Segoe UI", 15, "bold"), bg=COLOR_PANEL, fg=color)
            val_lbl.pack(pady=(1, 0))
            return val_lbl

        self.lbl_user_score = create_stat_card(score_container, 0, "YOU (WINS)", self.user_score, COLOR_WIN)
        self.lbl_draws = create_stat_card(score_container, 1, "DRAWS", self.draws, COLOR_DRAW)
        self.lbl_comp_score = create_stat_card(score_container, 2, "COMPUTER", self.computer_score, COLOR_LOSE)
        self.lbl_rounds = create_stat_card(score_container, 3, "ROUND", self.round_number, COLOR_ACCENT)

    def _build_battle_arena(self):
        """Center arena displaying player choice, computer choice, and outcome."""
        arena_frame = tk.Frame(self.root, bg=COLOR_PANEL, padx=12, pady=8)
        arena_frame.pack(fill=tk.X, padx=16, pady=6)

        battle_grid = tk.Frame(arena_frame, bg=COLOR_PANEL)
        battle_grid.pack(fill=tk.X)
        battle_grid.columnconfigure(0, weight=1)
        battle_grid.columnconfigure(1, weight=0)
        battle_grid.columnconfigure(2, weight=1)

        # Player Choice Box
        player_box = tk.Frame(battle_grid, bg=COLOR_BG, padx=8, pady=8)
        player_box.grid(row=0, column=0, sticky="nsew", padx=4)
        
        tk.Label(player_box, text="YOUR MOVE", font=("Segoe UI", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack()
        self.lbl_player_icon = tk.Label(player_box, text="❓", font=("Segoe UI Emoji", 26), bg=COLOR_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_player_icon.pack(pady=2)
        self.lbl_player_text = tk.Label(player_box, text="Waiting...", font=("Segoe UI", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_player_text.pack()

        # VS Label
        vs_lbl = tk.Label(battle_grid, text="VS", font=("Segoe UI", 12, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT)
        vs_lbl.grid(row=0, column=1, padx=8)

        # Computer Choice Box
        comp_box = tk.Frame(battle_grid, bg=COLOR_BG, padx=8, pady=8)
        comp_box.grid(row=0, column=2, sticky="nsew", padx=4)
        
        tk.Label(comp_box, text="COMPUTER", font=("Segoe UI", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack()
        self.lbl_comp_icon = tk.Label(comp_box, text="❓", font=("Segoe UI Emoji", 26), bg=COLOR_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_comp_icon.pack(pady=2)
        self.lbl_comp_text = tk.Label(comp_box, text="Waiting...", font=("Segoe UI", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_comp_text.pack()

        # Result Banner
        self.lbl_result_status = tk.Label(
            arena_frame,
            text="Make your choice below to play!",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_MAIN,
            pady=4
        )
        self.lbl_result_status.pack()

        self.lbl_result_desc = tk.Label(
            arena_frame,
            text="Rules: Stone crushes Scissors | Scissors cut Paper | Paper covers Stone",
            font=("Segoe UI", 8),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_MUTED
        )
        self.lbl_result_desc.pack()

    def _build_choice_menu(self):
        """Menu with interactive buttons for Stone, Paper, Scissors."""
        menu_frame = tk.Frame(self.root, bg=COLOR_BG)
        menu_frame.pack(fill=tk.X, padx=16, pady=4)

        tk.Label(
            menu_frame,
            text="SELECT MOVE:",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_BG,
            fg=COLOR_ACCENT
        ).pack(anchor="w", pady=(0, 3))

        btn_grid = tk.Frame(menu_frame, bg=COLOR_BG)
        btn_grid.pack(fill=tk.X)
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)
        btn_grid.columnconfigure(2, weight=1)

        buttons_info = [
            (STONE, "🪨 Stone (1)", 0),
            (PAPER, "📄 Paper (2)", 1),
            (SCISSORS, "✂️ Scissors (3)", 2),
        ]

        self.choice_buttons = {}
        for choice_key, label_text, col in buttons_info:
            btn = tk.Button(
                btn_grid,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_BTN,
                fg=COLOR_TEXT_MAIN,
                activebackground=COLOR_BTN_HOVER,
                activeforeground=COLOR_TEXT_MAIN,
                relief=tk.FLAT,
                bd=0,
                padx=8,
                pady=8,
                cursor="hand2",
                command=lambda c=choice_key: self.play_round(c)
            )
            btn.grid(row=0, column=col, padx=3, sticky="nsew")
            
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLOR_BTN_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLOR_BTN))
            self.choice_buttons[choice_key] = btn

    def _build_control_buttons(self):
        """
        Guaranteed visible control panel with:
        - 🔄 Restart Game
        - 🛑 Exit Game & Show Final Score
        """
        ctrl_frame = tk.Frame(self.root, bg=COLOR_BG)
        ctrl_frame.pack(fill=tk.X, padx=16, pady=6)

        ctrl_frame.columnconfigure(0, weight=1)
        ctrl_frame.columnconfigure(1, weight=1)

        # Restart Game Button
        btn_restart = tk.Button(
            ctrl_frame,
            text="🔄 Restart Game (R)",
            font=("Segoe UI", 10, "bold"),
            bg="#0369a1",  # Deep Sky Blue
            fg="#ffffff",
            activebackground="#0284c7",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.restart_game
        )
        btn_restart.grid(row=0, column=0, padx=(0, 4), sticky="nsew")

        # Exit Game & Show Final Score Button
        btn_exit = tk.Button(
            ctrl_frame,
            text="🛑 Exit & View Final Score (Esc)",
            font=("Segoe UI", 10, "bold"),
            bg="#b91c1c",  # Prominent Crimson Red
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.exit_and_show_final_score
        )
        btn_exit.grid(row=0, column=1, padx=(4, 0), sticky="nsew")

    def _build_history_panel(self):
        """Scrollable round history list with fixed compact height."""
        history_frame = tk.Frame(self.root, bg=COLOR_BG)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 8))

        tk.Label(
            history_frame,
            text="MATCH HISTORY:",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_BG,
            fg=COLOR_ACCENT
        ).pack(anchor="w", pady=(2, 2))

        list_container = tk.Frame(history_frame, bg=COLOR_PANEL)
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_list = tk.Listbox(
            list_container,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_MAIN,
            font=("Consolas", 9),
            selectbackground=COLOR_BTN_HOVER,
            bd=0,
            height=5,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.config(command=self.history_list.yview)

    def play_round(self, user_choice: str):
        """Executes a game round with the user's choice."""
        if user_choice not in CHOICES:
            messagebox.showerror("Invalid Choice", f"'{user_choice}' is not a valid move!")
            return

        # 1. Computer move
        comp_choice = get_computer_choice()

        # 2. Determine outcome
        winner = determine_winner(user_choice, comp_choice)
        explanation = get_result_explanation(user_choice, comp_choice, winner)

        # 3. Update scores & round counter
        self.round_number += 1
        if winner == "User":
            self.user_score += 1
            status_text = "🎉 YOU WON THIS ROUND!"
            status_color = COLOR_WIN
        elif winner == "Computer":
            self.computer_score += 1
            status_text = "🤖 COMPUTER WON THIS ROUND!"
            status_color = COLOR_LOSE
        else:
            self.draws += 1
            status_text = "🤝 IT'S A DRAW!"
            status_color = COLOR_DRAW

        # 4. Update UI Displays
        self.lbl_user_score.config(text=str(self.user_score))
        self.lbl_comp_score.config(text=str(self.computer_score))
        self.lbl_draws.config(text=str(self.draws))
        self.lbl_rounds.config(text=str(self.round_number))

        self.lbl_player_icon.config(text=CHOICE_ICONS[user_choice])
        self.lbl_player_text.config(text=user_choice)

        self.lbl_comp_icon.config(text=CHOICE_ICONS[comp_choice])
        self.lbl_comp_text.config(text=comp_choice)

        self.lbl_result_status.config(text=status_text, fg=status_color)
        self.lbl_result_desc.config(text=explanation)

        # 5. Append to match history
        history_entry = (
            f"Round {self.round_number:02d}: "
            f"You [{CHOICE_ICONS[user_choice]} {user_choice:<8}] vs "
            f"Computer [{CHOICE_ICONS[comp_choice]} {comp_choice:<8}] -> "
            f"{'WIN' if winner == 'User' else ('LOSE' if winner == 'Computer' else 'DRAW')}"
        )
        self.history_list.insert(0, history_entry)

    def restart_game(self, prompt_confirm: bool = True):
        """Resets all scores, counters, and history to restart the game."""
        if prompt_confirm and self.round_number > 0:
            confirm = messagebox.askyesno("Restart Game", "Are you sure you want to restart and reset all scores to 0?")
            if not confirm:
                return

        self.user_score = 0
        self.computer_score = 0
        self.draws = 0
        self.round_number = 0

        self.lbl_user_score.config(text="0")
        self.lbl_comp_score.config(text="0")
        self.lbl_draws.config(text="0")
        self.lbl_rounds.config(text="0")

        self.lbl_player_icon.config(text="❓")
        self.lbl_player_text.config(text="Waiting...")
        self.lbl_comp_icon.config(text="❓")
        self.lbl_comp_text.config(text="Waiting...")

        self.lbl_result_status.config(text="Game Restarted! Choose a move to play.", fg=COLOR_ACCENT)
        self.lbl_result_desc.config(text="Rules: Stone crushes Scissors | Scissors cut Paper | Paper covers Stone")

        self.history_list.delete(0, tk.END)

    def exit_and_show_final_score(self):
        """
        Completes the game and displays the Final Scores Screen with options
        to Restart a new match, Resume current match, or Quit application.
        """
        exit_win = tk.Toplevel(self.root)
        exit_win.title("Final Match Scores & Exit Menu")
        exit_win.geometry("480x540")
        exit_win.resizable(False, False)
        exit_win.configure(bg=COLOR_BG)
        exit_win.grab_set()  # Focus trap (modal dialog)

        # Match outcome evaluation
        if self.round_number == 0:
            champ_title = "🎮 NO ROUNDS PLAYED YET"
            champ_color = COLOR_TEXT_MUTED
            champ_msg = "Play some rounds first to see match statistics!"
        elif self.user_score > self.computer_score:
            lead = self.user_score - self.computer_score
            champ_title = "🏆 FINAL RESULT: YOU WON THE MATCH!"
            champ_color = COLOR_WIN
            champ_msg = f"Congratulations! You defeated the Computer by {lead} win(s)!"
        elif self.computer_score > self.user_score:
            lead = self.computer_score - self.user_score
            champ_title = "🤖 FINAL RESULT: COMPUTER WON THE MATCH!"
            champ_color = COLOR_LOSE
            champ_msg = f"Computer won this match by {lead} win(s)."
        else:
            champ_title = "🤝 FINAL RESULT: IT'S A TIED MATCH!"
            champ_color = COLOR_DRAW
            champ_msg = "Both you and the computer finished with equal scores!"

        # Title
        hdr = tk.Frame(exit_win, bg=COLOR_BG, pady=12)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="MATCH COMPLETED - FINAL SCORES", font=("Segoe UI", 14, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT).pack()

        # Banner Card
        banner_card = tk.Frame(exit_win, bg=COLOR_PANEL, padx=14, pady=12)
        banner_card.pack(fill=tk.X, padx=20, pady=4)
        tk.Label(banner_card, text=champ_title, font=("Segoe UI", 12, "bold"), bg=COLOR_PANEL, fg=champ_color).pack()
        tk.Label(banner_card, text=champ_msg, font=("Segoe UI", 9), bg=COLOR_PANEL, fg=COLOR_TEXT_MAIN, wraplength=400).pack(pady=(3, 0))

        # Final Scorecard Table
        stats_card = tk.Frame(exit_win, bg=COLOR_PANEL, padx=14, pady=10)
        stats_card.pack(fill=tk.X, padx=20, pady=8)

        tk.Label(stats_card, text="FINAL SCORE SUMMARY", font=("Segoe UI", 10, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 4))

        total_rounds = self.round_number
        user_pct = (self.user_score / total_rounds * 100) if total_rounds > 0 else 0
        comp_pct = (self.computer_score / total_rounds * 100) if total_rounds > 0 else 0
        draw_pct = (self.draws / total_rounds * 100) if total_rounds > 0 else 0

        stats_rows = [
            ("Total Rounds Played:", f"{total_rounds}", COLOR_TEXT_MAIN),
            ("Your Score (Wins):", f"{self.user_score}  ({user_pct:.1f}%)", COLOR_WIN),
            ("Computer Score (Wins):", f"{self.computer_score}  ({comp_pct:.1f}%)", COLOR_LOSE),
            ("Ties / Draws:", f"{self.draws}  ({draw_pct:.1f}%)", COLOR_DRAW),
        ]

        for label_text, val_text, val_color in stats_rows:
            row_frame = tk.Frame(stats_card, bg=COLOR_PANEL)
            row_frame.pack(fill=tk.X, pady=2)
            tk.Label(row_frame, text=label_text, font=("Segoe UI", 9), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(side=tk.LEFT)
            tk.Label(row_frame, text=val_text, font=("Segoe UI", 9, "bold"), bg=COLOR_PANEL, fg=val_color).pack(side=tk.RIGHT)

        # Action Buttons
        actions_frame = tk.Frame(exit_win, bg=COLOR_BG, pady=8)
        actions_frame.pack(fill=tk.X, padx=20)

        # 1. Restart Button
        def on_restart():
            exit_win.destroy()
            self.restart_game(prompt_confirm=False)

        btn_restart = tk.Button(
            actions_frame,
            text="🔄 Restart Game (New Match)",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_WIN,
            fg="#ffffff",
            activebackground="#16a34a",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            pady=8,
            cursor="hand2",
            command=on_restart
        )
        btn_restart.pack(fill=tk.X, pady=3)

        # 2. Return / Resume Button
        def on_resume():
            exit_win.destroy()

        btn_resume = tk.Button(
            actions_frame,
            text="↩️ Return to Current Game",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_BTN,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_BTN_HOVER,
            activeforeground=COLOR_TEXT_MAIN,
            relief=tk.FLAT,
            bd=0,
            pady=7,
            cursor="hand2",
            command=on_resume
        )
        btn_resume.pack(fill=tk.X, pady=3)

        # 3. Quit Button
        def on_quit():
            exit_win.destroy()
            self.root.destroy()

        btn_quit = tk.Button(
            actions_frame,
            text="🚪 Quit & Close Application",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_LOSE,
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            pady=7,
            cursor="hand2",
            command=on_quit
        )
        btn_quit.pack(fill=tk.X, pady=3)


def main():
    root = tk.Tk()
    app = StonePaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
