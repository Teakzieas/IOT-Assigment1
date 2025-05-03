class Data:
    def __init__(self, temperature=0, humidity=0, light_in=0, light_out=0, curtain_pos=0,human_presence=False):
        self.temperature = temperature
        self.humidity = humidity
        self.light_in = light_in
        self.light_out = light_out
        self.curtain_pos = curtain_pos
        self.human_presence = human_presence

        
    def __str__(self):
        return f"Temperature: {self.temperature}°C, Humidity: {self.humidity}%, Light In: {self.light_in}, Light Out: {self.light_out}, Curtain Position: {self.curtain_pos}%, Human Presence: {self.human_presence}"
