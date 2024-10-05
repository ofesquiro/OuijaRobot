from ParseStringStrategy import ParseStringStrategy
class UTF_8(ParseStringStrategy):
        
        
    def __init__(self):
        pass
    
    
    def parse(self, string) -> str:
        try:
            return string.decode('utf-8')
        except Exception as e:
            print(e)
            return "Error"
    

class ISO(ParseStringStrategy):
    
    
    def __init__(self):
        pass
    
    
    def parse(self, string) -> str:
        try:
            return string.decode('ISO-8859-1')
        except Exception as e:
            print(e)
            return "Error"
        
        
class UFT_16(ParseStringStrategy):
    
    
    def __init__(self):
        pass
    
    
    def parse(self, string) -> str:
        try:
            return string.decode('utf-16')
        except Exception as e:
            print(e)
            return "Error"
        

class UFT_32(ParseStringStrategy):
    
    
    def __init__(self):
        pass
    
    
    def parse(self, string) -> str:
        try:
            return string.decode('utf-32')
        except Exception as e:
            print(e)
            return "Error"
        
        
class ASCII(ParseStringStrategy):
        
        
        def __init__(self):
            pass
        
        
        def parse(self, string) -> str:
            try:
                return string.decode('ascii')
            except Exception as e:
                print(e)
                return "Error"
            
class Windows_1252(ParseStringStrategy):
        
        
        def __init__(self):
            pass
        
        
        def parse(self, string) -> str:
            try:
                return string.decode('windows-1252')
            except Exception as e:
                print(e)
                return "Error"  
            
