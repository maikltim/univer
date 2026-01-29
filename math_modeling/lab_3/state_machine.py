class FridgeStateMachine:
    def __init__(self):
        self.state = "NORMAL"
        
    def update(self, data):
        if not data["power_on"]:
            self.state = "NO_POWER"

        elif data["power_on"] and not data["cooling"]:
            self.state = "NO_COOLING"

        elif data["noise"]:
            self.state = "NOISE"

        elif data["ice"]:
            self.state = "ICE_BUILDUP"

        else:
            self.state = "NORMAL"

        return self.state
        