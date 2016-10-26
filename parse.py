import re


class LogLine():
    def __init__(self, line_text):
        self.text = line_text
        self.line_type = self._determine_line_type()
        self.player = self._get_player()

    def is_ent_spawned_line(self):
        return self.line_type == "ent_spawned"

    def is_tool_used_line(self):
        return self.line_type == "tool_used"

    def is_chat_line(self):
        return self.line_type == "chat"

    def is_kill_line(self):
        return self.line_type == "kill"

    def _determine_line_type(self):
        pass

    def _get_player(self):
        pass


class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.parse_file()

        self.words_said_global = {}
        self.words_said_people = {}

        self.tools_used_global = {}
        self.tools_used_people = {}

        self.ents_spawned_global = {}
        self.ents_spawned_people = {}

    def parse_file(self):
        with open(self.filename) as log:
            log_text = log.read()
            lines = log_text.split("\n")

            # Main parsing loop
            for line in lines:
                self.parse_line(line)

    def parse_line(line_text):
        line = LogLine(line_text)
        print(line)

if __name__ == '__main__':
    Parser('ulx_logs/01-18-16.txt')
