import re
import pprint
pp = pprint.PrettyPrinter(indent=4)


class LogLine():
    def __init__(self, line_text):
        self.text = line_text
        self.player = None
        self.subject = None

        self.line_type = self._determine_line_type()
        if self.line_type:
            self.player = self._get_player()
            self.subject = self._get_subject()

        self.regex_match = None

    def is_ent_spawned_line(self):
        return self.line_type == "ent_spawned"

    def is_tool_used_line(self):
        return self.line_type == "tool_used"

    def is_chat_line(self):
        return self.line_type == "chat"

    def is_kill_line(self):
        return self.line_type == "kill"

    def _determine_line_type(self):
        ent_spawned_regex = r'\[\d\d:\d\d:\d\d] (.*)<(.*)> spawned (?:vehicle|model|sent) (.*)\r'
        chat_regex = r'\[\d\d:\d\d:\d\d] (.*): (.*)\r'
        tool_used_regex = r'\[\d\d:\d\d:\d\d] (.*)<(.*)> used the tool (\w*) on (.*)\r'
        kill_regex = r'\[\d\d:\d\d:\d\d] (.*) killed (.*) using (.*)\r'

        matches = []

        # TODO: reorder these in order of most frequently found lines
        ent_spawned = re.search(ent_spawned_regex, self.text)
        if ent_spawned:
            matches.append({'match': ent_spawned, 'line_type': 'ent_spawned'})

        tool_used = re.search(tool_used_regex, self.text)
        if tool_used:
            matches.append({'match': tool_used, 'line_type': 'tool_used'})

        chat = re.search(chat_regex, self.text)
        if chat:
            matches.append({'match': chat, 'line_type': 'chat'})

        kill = re.search(kill_regex, self.text)
        if kill:
            matches.append({'match': kill, 'line_type': 'kill'})

        if len(matches) > 1:
            print('')
            print('MULTIPLE MATCHES FOUND, CHOOSING FIRST')
            print(matches)
            print(self.text)
            print('')

        if len(matches) == 0:
            #print('')
            #print('NO MATCHES FOUND, RETURNING NONE')
            #print(self.text)
            #print('')
            return None

        match = matches[0]
        self.regex_match = match['match']

        return match['line_type']


    def _get_player(self):
        return self.regex_match.group(1)

    def _get_subject(self):
        line_type = self.line_type
        match = self.regex_match

        if line_type == 'ent_spawned':
            return match.group(3)
        elif line_type == 'tool_used':
            return match.group(3)
        elif line_type == 'kill':
            return match.group(2)
            # return {'victim': match.group(2),
            #         'weapon': match.group(3)}

        return None


class Parser():
    def __init__(self, filename):
        self.filename = filename

        self.words_said_global = {}
        self.words_said_people = {}

        self.tools_used_global = {}
        self.tools_used_people = {}

        self.kills_global = {}
        self.kills_people = {}
        self.deaths_global = {}
        self.deaths_people = {}

        self.ents_spawned_global = {}
        self.ents_spawned_people = {}

        self.parse_file()

    def parse_file(self):
        with open(self.filename) as log:
            log_text = log.read()
            lines = log_text.split("\n")

            # Main parsing loop
            for line in lines:
                self.parse_line(line)

            pp.pprint(self.deaths_people)

    def parse_line(self, line_text):
        line = LogLine(line_text)

        line_type = line.line_type

        if line_type:
            player = line.player
            subject = line.subject

            if line_type == 'ent_spawned':
                self.add_spawned_ent(player, subject)

            elif line_type == 'tool_used':
                self.add_tool_used(player, subject)

            elif line_type == 'kill':
                self.add_kill(player, subject)
                self.add_death(subject, player)

            elif line_type == 'chat':
                self.add_words(player, subject)

    def add_spawned_ent(self, player, ent):
        global_data = self.ents_spawned_global
        player_data = self.ents_spawned_people.get(player, {})

        global_data[ent] = global_data.get(ent, 0) + 1

        player_data[ent] = player_data.get(ent, 0) + 1
        self.ents_spawned_people[player] = player_data

    def add_tool_used(self, player, tool):
        global_data = self.tools_used_global
        player_data = self.tools_used_people.get(player, {})

        global_data[tool] = global_data.get(tool, 0) + 1

        player_data[tool] = player_data.get(tool, 0) + 1
        self.tools_used_people[player] = player_data

    def add_kill(self, player, victim):
        global_data = self.kills_global
        player_data = self.kills_people.get(player, {})

        global_data[player] = global_data.get(player, 0) + 1

        player_data[victim] = player_data.get(victim, 0) + 1
        self.kills_people[player] = player_data

    def add_death(self, player, killer):
        global_data = self.deaths_global
        player_data = self.deaths_people.get(player, {})

        global_data[player] = global_data.get(player, 0) + 1

        player_data[killer] = player_data.get(killer, 0) + 1
        self.deaths_people[player] = player_data


if __name__ == '__main__':
    Parser('ulx_logs/01-18-16.txt')
