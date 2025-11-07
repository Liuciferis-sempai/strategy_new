import datetime

class Logger:
    def __init__(self):
        self.logging_info = []
        self.logging_errors = []

    def get_time(self) -> str:
        time = datetime.datetime.now()
        return f"{time.hour}:{time.minute}:{time.second}.{time.microsecond}"
    
    def time(self, message: str, func: str):
        self.logging_info.append(f"{self.get_time()}: TIME [{func}] -> {message};\n")
    
    def info(self, message: str, func: str):
        self.logging_info.append(f"{self.get_time()}: INFO [{func}] -> {message};\n")
    
    def warning(self, message: str, func: str):
        message_text = f"{self.get_time()}: WARNING [{func}] -> {message};\n"
        self.logging_info.append(message_text)
        self.logging_errors.append(message_text)
    
    def error(self, message: str, func: str):
        message_text = f"{self.get_time()}: ERROR [{func}] -> {message};\n"
        self.logging_info.append(message_text)
        self.logging_errors.append(message_text)

    def write_down(self):
        with open("data/errors.txt", "a", encoding="utf-8") as f:
            for error in self.logging_errors:
                f.write(error)
        self.logging_errors = []
        with open("data/logs.txt", "a", encoding="utf-8") as f:
            for info in self.logging_info:
                f.write(info)
        self.logging_info = []