import datetime
import inspect

class MyCustomError(Exception):
    def __init__(self, message, error_code=500, payload=None):
        super().__init__(message)
        self.error_code = error_code
        self.payload = payload
        self.timestamp = datetime.datetime.now()
        self.line_number, self.error_line_content = self._get_error_context()

    def _get_error_context(self):
        stack = inspect.stack()
        if len(stack) > 2:
            frame_info = stack[2]
            line_no = frame_info.lineno
            code_line = frame_info.code_context[0].strip() if frame_info.code_context else "Unknown"
            return line_no, code_line
        return "Unknown", "Unknown"

    def __str__(self):
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        return (f"\n"
                f"--- CUSTOM ERROR REPORT ---\n"
                f"Time:    {time_str}\n"
                f"Code:    {self.error_code}\n"
                f"Message: {self.args[0]}\n"
                f"Line:    {self.line_number} -> `{self.error_line_content}`\n"
                f"Payload: {self.payload}\n"
                f"---------------------------")

    def to_dict(self):
        return {
            "error": self.args[0],
            "code": self.error_code,
            "details": self.payload,
            "line_no": self.line_number,
            "line_content": self.error_line_content
        }