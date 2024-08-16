import json
class Conversation():
    def __init__(self, user_input: str, bot_response: str) -> None:
        self.user_input : str = user_input
        self.bot_response : str = bot_response
        
class DataType():
    def __init__(self, id: int, exchanges : list[Conversation], feedback: bool) -> None:
        self.id : int = id
        self.exchanges: list[str] = exchanges
        self.feedback: bool = feedback
        
    def toJSON(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
    
    

class DataSaver():
    def __init__(self) -> None:
        self.filePath: str = "./data.json"
        self.dataArr : list[DataType]
        
        
    def save(self, data: str) -> bool:
        try:
            with open(self.filePath, 'a') as file:
                json.dump(data, file)
                return True
        except Exception as err:
            print(err)
            return False
            
            
    def load(self) -> DataType:
        with open(self.filePath, 'a') as file:
            value = file.read()
            value.get("data")
            return value

def test():
    testeo = DataSaver()
    data = DataType(3,[Conversation("como te llamas","my peco db")],True)
    if (testeo.save(data.toJSON())):
        print("todo bien")
    else: 
        print("todo mal")

test()