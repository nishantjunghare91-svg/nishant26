import re
import random
import json
import datetime
from typing import Dict, List, Optional
import os

class AdvancedRuleBasedChatbot:
    def __init__(self, config_file: str = "chatbot_config.json"):
        self.name = "Alex"
        self.version = "2.0"
        self.context = {}
        self.conversation_history = []
        self.load_config(config_file)
        self.session_start = datetime.datetime.now()
        
    def load_config(self, config_file: str):
        """Load rules and responses from JSON config"""
        default_config = {
            "responses": {
                "greeting": ["Hello! 👋 How can I help you today?", "Hi there! 😊 What's up?"],
                "goodbye": ["Goodbye! 👋 Have a great day!", "See you later! Take care! 😊"],
                "name": ["I'm {name} v{version}! Your AI assistant. 🤖"],
                "help": ["I can help with: time, weather, jokes, math, news, games, and more!\nCommands: /help, /joke, /time, /calc 2+2, /clear"],
                "thanks": ["You're welcome! 😊", "Happy to help!", "Anytime! 👍"],
                "default": ["That's interesting! Tell me more...", "I understand. What else?", "Hmm, can you rephrase that?"],
                "math": ["Let me calculate that for you..."],
                "error": ["Sorry, I didn't understand that. Try /help for commands!"],
                "joke": [
                    "Why don't scientists trust atoms? They make up everything! 😂",
                    "Why did the scarecrow win an award? Outstanding in his field! 🌾",
                    "Parallel lines have so much in common. It's a shame they'll never meet! 📏"
                ],
                "compliment": ["Thank you! You're pretty awesome too! 😎", "Aw, thanks! Right back at you! 💖"]
            },
            "rules": {
                "greeting": r"\b(hello|hi|hey|good morning|good afternoon|good evening|sup|yo)\b",
                "goodbye": r"\b(bye|goodbye|see you|farewell|exit|quit|leave)\b",
                "name": r"\b(who are you|what.?s your name|name|call you)\b",
                "help": r"\b(help|commands|what can you do|menu)\b",
                "time": r"\b(time|clock|hour|what time)\b",
                "weather": r"\b(weather|temperature|rain|sunny|hot|cold|forecast)\b",
                "joke": r"\b(joke|funny|laugh|haha|tell me a joke)\b",
                "math": r"(/calc|calculate|math|add|subtract|multiply|divide)",
                "thanks": r"\b(thank|thanks|appreciate|cheers)\b",
                "compliment": r"\b(great|awesome|amazing|cool|nice|beautiful|smart)\b",
                "how_are_you": r"\b(how are you|how do you do|how.?s it going)\b"
            }
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
        except Exception as e:
            print(f"Config error: {e}. Using defaults.")
            self.config = default_config

    def get_current_time(self) -> str:
        """Get formatted current time"""
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p on %A, %B %d, %Y")

    def calculate(self, expression: str) -> Optional[str]:
        """Simple calculator using eval (SAFE version)"""
        try:
            # Only allow safe operations
            safe_pattern = r'^[\d\s+\-*/().]+$'
            if re.match(safe_pattern, expression.strip()):
                result = eval(expression)
                return f"✅ {expression} = **{result}**"
            return None
        except:
            return None

    def get_response(self, user_input: str) -> str:
        """Main response logic with rule matching"""
        user_input_lower = user_input.lower().strip()
        self.conversation_history.append({"user": user_input, "timestamp": datetime.datetime.now()})
        
        # Command handling
        if user_input.startswith('/'):
            return self.handle_command(user_input)
        
        # Rule matching (priority order)
        for intent, pattern in self.config["rules"].items():
            if re.search(pattern, user_input_lower):
                return self.generate_response(intent)
        
        # Context-aware responses
        if self.context.get('waiting_for_math'):
            math_result = self.calculate(user_input)
            if math_result:
                self.context['waiting_for_math'] = False
                return math_result
            else:
                self.context['waiting_for_math'] = False
                return "❌ Invalid math expression. Try: /calc 2+2"
        
        return self.generate_response('default')

    def handle_command(self, command: str) -> str:
        """Handle slash commands"""
        cmd = command.lower().strip().lstrip('/')
        
        if cmd == 'help':
            return self.config["responses"]['help'][0]
        elif cmd == 'joke':
            return random.choice(self.config["responses"]['joke'])
        elif cmd == 'time':
            return f"🕐 Current time: **{self.get_current_time()}**"
        elif cmd.startswith('calc'):
            expr = cmd[4:].strip()
            if expr:
                result = self.calculate(expr)
                return result or "❌ Invalid calculation"
            self.context['waiting_for_math'] = True
            return "🧮 Enter math expression (e.g., 2+2, 5*3):"
        elif cmd == 'clear':
            self.conversation_history.clear()
            self.context.clear()
            return "🧹 Conversation history cleared!"
        elif cmd == 'stats':
            return f"📊 Session: {len(self.conversation_history)} messages | Started: {self.session_start.strftime('%H:%M')}"
        else:
            return self.config["responses"]['error'][0]

    def generate_response(self, intent: str) -> str:
        """Generate response with context and randomization"""
        responses = self.config["responses"].get(intent, self.config["responses"]['default'])
        response = random.choice(responses)
        
        # Template substitution
        response = response.format(
            name=self.name,
            version=self.version,
            time=self.get_current_time()
        )
        
        # Add emojis randomly
        if random.random() > 0.7:
            emojis = ['😊', '👍', '🎉', '🤖', '✨']
            response += f" {random.choice(emojis)}"
        
        return response

    def save_session(self, filename: str = "chat_sessions.json"):
        """Save conversation history"""
        session_data = {
            "session_start": self.session_start.isoformat(),
            "total_messages": len(self.conversation_history),
            "history": self.conversation_history[-50:]  # Last 50 messages
        }
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
        except:
            pass

def main():
    bot = AdvancedRuleBasedChatbot()
    
    print("🤖" + "="*50)
    print(f"  Welcome to {bot.name} v{bot.version}!")
    print("  Type /help for commands | /quit to exit")
    print("="*50)
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input or user_input.lower() in ['/quit', 'quit', 'exit', 'bye']:
                print(f"\n🤖 {bot.generate_response('goodbye')}")
                bot.save_session()
                break
            
            response = bot.get_response(user_input)
            print(f"🤖 {response}")
            
    except KeyboardInterrupt:
        print(f"\n\n🤖 {bot.generate_response('goodbye')}")
        bot.save_session()

if __name__ == "__main__":
    main()