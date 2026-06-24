import time
import threading
from src.acp.bus import ACPBus, ACPMessage

class JARVISAgent:
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.bus = ACPBus()
        self.name = "JARVIS"
        self.running = True

        if not self.use_mock:
            try:
                import speech_recognition as sr
                import pyttsx3
                self.recognizer = sr.Recognizer()
                self.engine = pyttsx3.init()
            except ImportError:
                print("Speech libraries not found. Falling back to mock mode.")
                self.use_mock = True

    def speak(self, text: str):
        print(f"JARVIS (Voice): {text}")
        if not self.use_mock:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self) -> str:
        if self.use_mock:
            # In a real system, this might block until user input in a CLI
            # For this agent, we'll listen for "voice_command" messages on the bus as well
            return ""

        import speech_recognition as sr
        with sr.Microphone() as source:
            print("JARVIS is listening...")
            audio = self.recognizer.listen(source)
            try:
                return self.recognizer.recognize_google(audio)
            except Exception:
                return ""

    def process_voice_command(self, text: str):
        if not text:
            return

        self.speak(f"Processing command: {text}")
        # Simple parser for the clone
        if "list files" in text.lower():
            self.bus.send(ACPMessage(self.name, "OpenCode", "file_list", {"path": "."}))
        elif "hello" in text.lower():
            self.speak("Hello! I am JARVIS. How can I assist you today?")
        else:
            self.speak("I'm not sure how to handle that command yet.")

    def run(self):
        print("JARVIS Agent started...")
        while self.running:
            # 1. Listen for bus messages (e.g., from AI Engine to JARVIS)
            messages = self.bus.receive(self.name)
            for msg in messages:
                if msg.topic == "speak":
                    self.speak(msg.payload.get("text", ""))
                elif msg.topic == "voice_command":
                    self.process_voice_command(msg.payload.get("text", ""))

            # 2. In mock mode, we don't block on microphone.
            # In real mode, you might have a separate thread for continuous listening.
            time.sleep(1)

if __name__ == "__main__":
    agent = JARVISAgent(use_mock=True)
    agent.run()
