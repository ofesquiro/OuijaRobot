import json
        
class Analyzer():
    def __init__(self):
        self.data = self.load_conversation_log()


    def load_conversation_log(file_path) -> list:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['chat_log']

        
    def generate_response(user_input):
        # Placeholder for a response generation mechanism
        return "Sample response based on: " + user_input


    def save_conversation(self, user_input, bot_response, successful) -> None:
        self.data.append({"user": user_input, "bot": bot_response, "successful": successful})
        with open("chat_log.json", "w") as log_file:
            json.dump(self.data, log_file["chat_log"], indent=4)


def main():
    analyzer : Analyzer = Analyzer()
    analyzer.save_conversation("Hola", "Hola, ¿en qué puedo ayudarte?", True)
    analyzer.save_conversation("¿Cómo estás?", "ayer", False)

main()