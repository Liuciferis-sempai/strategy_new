import datetime

class Logger:
    def __init__(self):
        self.logging_info = {
            "time": "",
            "info": "",
            "warning": "",
            "error": ""
        }

    def get_time(self) -> str:
        time = datetime.datetime.now()
        return f"{time.hour}:{time.minute}:{time.second}.{time.microsecond}"
    
    def time(self, message: str, func: str):
        self.logging_info["time"] += f"{self.get_time()}: TIME [{func}] -> {message};\n"
    
    def info(self, message: str, func: str):
        self.logging_info["info"] += f"{self.get_time()}: INFO [{func}] -> {message};\n"
    
    def warning(self, message: str, func: str):
        self.logging_info["warning"] += f"{self.get_time()}: WARNING [{func}] -> {message};\n"
    
    def error(self, message: str, func: str):
        self.logging_info["error"] += f"{self.get_time()}: ERROR [{func}] -> {message};\n"

    def write_down(self):
        if self.logging_info["error"] != "":
            with open("data/errors.txt", "a", encoding="utf-8") as f:
                f.write(self.logging_info["error"])
        with open("data/logs.txt", "a", encoding="utf-8") as f:
            for log_type in self.logging_info:
                f.write(self.logging_info[log_type])
                self.logging_info[log_type] = ""