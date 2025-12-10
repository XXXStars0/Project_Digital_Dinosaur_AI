class GameStateService:
    def __init__(self):
        """
        Initialize the game state.
        Now includes logic for 'Time Consumption' and 'Neglect Penalties'.
        """
        self.state = {
            "hunger": 50,          # 0-100
            "mood": 50,            # 0-100
            "affinity": 10,        # 0-100
            "day": 1,
            "time_phase": "Morning" # Morning -> Afternoon -> Night
        }
        
        self.time_cycle = ["Morning", "Afternoon", "Night"]

    def _advance_time(self):
        current_index = self.time_cycle.index(self.state["time_phase"])
        if current_index < len(self.time_cycle) - 1:
            self.state["time_phase"] = self.time_cycle[current_index + 1]
            self.state["hunger"] = max(0, self.state["hunger"] - 10) 
            return True
        return False

    def handle_action(self, action_type):
        system_event_desc = ""
        current_time = self.state["time_phase"]
        
        # --- LOGIC 1: Night Penalty ---
        # If it is Night, and the user does ANYTHING other than sleep, prompt a penalty.
        if current_time == "Night" and action_type != "sleep":
            self.state["affinity"] = max(0, self.state["affinity"] - 5)
            self.state["mood"] = max(0, self.state["mood"] - 10)
            system_event_desc = (
                "(System: It is late night. You woke the pet up. "
                "It is very grumpy and tired. Affinity decreased.)"
            )
            if action_type == "chat":
                 return self.state, system_event_desc

        # --- LOGIC 2: Action Processing ---
        
        if action_type == "sleep":
            # [Neglect Penalty Check] Before resetting, check if stats were bad
            penalty_desc = ""
            if self.state["hunger"] <= 0:
                self.state["affinity"] = max(0, self.state["affinity"] - 20)
                self.state["mood"] = 0
                penalty_desc = " Because it starved last night, it hates you now."
            
            # New day
            self.state["day"] += 1
            self.state["time_phase"] = "Morning"
            self.state["hunger"] = max(0, self.state["hunger"] - 20) 
            
            system_event_desc = (
                f"(System: You turned off the lights. Day {self.state['day']} begins. "
                f"{penalty_desc})"
            )

        elif action_type == "feed":
            self.state["hunger"] = min(100, self.state["hunger"] + 30)
            self.state["affinity"] = min(100, self.state["affinity"] + 2)
            system_event_desc = "(System: You fed the pet. It looks satisfied.)"
            if self._advance_time():
                 system_event_desc += f" (Time passed: It is now {self.state['time_phase']}.)"

        elif action_type == "pet":
            self.state["mood"] = min(100, self.state["mood"] + 15)
            self.state["affinity"] = min(100, self.state["affinity"] + 3)
            system_event_desc = "(System: You played with the pet.)"
            if self._advance_time():
                 system_event_desc += f" (Time passed: It is now {self.state['time_phase']}.)"

        elif action_type == "chat":
            # Chatting does NOT advance time.
            # But it builds small affinity (unless it's night, handled above).
            if current_time != "Night":
                self.state["affinity"] = min(100, self.state["affinity"] + 1)
                system_event_desc = f"(System: User is chatting with you. Time: {current_time}.)"

        return self.state, system_event_desc
    
    def get_state(self):
        return self.state

current_game_state = GameStateService()