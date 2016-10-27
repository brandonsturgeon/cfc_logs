import re
import pprint
from os import listdir
from random import shuffle
import json
import time
import mmap
import ujson
import cProfile

pp = pprint.PrettyPrinter(indent=4)


class LogLine():
    def __init__(self, line_text, patterns):
        self.text = line_text
        self.player = None
        self.subject = None
        self.patterns = patterns

        self.line_type = self._determine_line_type()
        if self.line_type:
            self.player = self._get_player()
            self.subject = self._get_subject()

        self.regex_match = None

        # regex


    @property
    def is_ent_spawned_line(self):
        return self.line_type == "ent_spawned"

    @property
    def is_tool_used_line(self):
        return self.line_type == "tool_used"

    @property
    def is_chat_line(self):
        return self.line_type == "chat"

    @property
    def is_kill_line(self):
        return self.line_type == "kill"

    @property
    def is_connection_line(self):
        return self.line_type == "connection"

    @property
    def is_suicide_line(self):
        return self.line_type == "suicide"
    
    @property
    def is_kick_line(self):
        return self.line_type == "kick"

    def _get_regex_match(self, text):
        chat_regex        = self.patterns['chat_regex']
        ent_spawned_regex = self.patterns['ent_spawned_regex']
        tool_used_regex   = self.patterns['tool_used_regex']
        kill_regex        = self.patterns['kill_regex']
        killed_by_regex   = self.patterns['killed_by_regex']
        connection_regex  = self.patterns['connection_regex']
        suicide_regex     = self.patterns['suicide_regex']
        kick_regex        = self.patterns['kick_regex']
        ban_regex         = self.patterns['ban_regex']

        chat = re.search(chat_regex, text)
        if chat:
            return {'match': chat, 'line_type': 'chat'}
       
        # Always assume it's chat first, in case someone quotes console
        if not chat:
            if 'spawned' in text:
                ent_spawned = re.search(ent_spawned_regex, text)
                if ent_spawned:
                    return {'match': ent_spawned, 'line_type': 'ent_spawned'}

            if 'used the tool' in text:
                tool_used = re.search(tool_used_regex, text)
                if tool_used:
                    return {'match': tool_used, 'line_type': 'tool_used'}

            if 'killed' in text:
                kill = re.search(kill_regex, text)
                killed_by = re.search(killed_by_regex, text)
                if kill:
                    return {'match': kill, 'line_type': 'kill'}
                elif killed_by:
                    return {'match': killed_by, 'line_type': 'kill'}

            if 'connected' in text:
                connection = re.search(connection_regex, text)
                if connection:
                    return {'match': connection, 'line_type': 'connection'}

            if 'suicided' in text:
                suicide = re.search(suicide_regex, text)
                if suicide:
                    return {'match': suicide, 'line_type': 'suicide'}

            if 'kicked' in text:
                kick = re.search(kick_regex, text)
                if kick:
                    return {'match': kick, 'line_type': 'kick'}

        return {}

    def _determine_line_type(self):
        match = self._get_regex_match(self.text)

        if match == {}:
            # print('')
            # print('NO MATCHES FOUND, RETURNING NONE')
            # print(repr(self.text))
            # print('')
            return None

        self.regex_match = match['match']

        return match['line_type']

    def _get_player(self):
        return self.regex_match.group(1)

    def _get_subject(self):
        line_type = self.line_type
        match = self.regex_match

        if self.is_ent_spawned_line:
            return match.group(3)

        elif self.is_tool_used_line:
            return match.group(3)

        elif self.is_kill_line:
            return match.group(2)

        elif self.is_chat_line:
            return match.group(2)

        elif self.is_connection_line:
            return ''

        elif self.is_suicide_line:
            return match.group(1)

        elif self.is_kick_line:
            return match.group(2)

        return None


class Parser():
    def __init__(self, file_paths):
        self.file_paths = file_paths

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

        self.connections_global = {}

        self.kicks_received_global = {}
        self.kicks_received_people = {}

        self.kicks_given_global = {}
        self.kicks_given_people = {}

        self.regex_patterns = {
            'chat_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*): (.*)\r'),
            'ent_spawned_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*)<(.*)> spawned(?:/gave himself)? (?:vehicle|model|sent|ragdoll|swep) (.*)\r'),
            'tool_used_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*)<(.*)> used the tool (\w*) on (.*)\r'),
            'kill_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*) killed (.*) using (.*)\r'),
            'killed_by_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*) was killed by (.*)\r'),
            'connection_regex': re.compile(r'^\[\d\d:\d\d:\d\d] Client \"(.*)\" connected.\r'),
            'suicide_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*) suicided!\r'),
            'kick_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*) kicked (.*) \((.*)\)\r'),
            'ban_regex': re.compile(r'^\[\d\d:\d\d:\d\d] (.*) banned (.*) (?:for \d* (?:minutes|hours|days)|permanently)(?: \(.*\))?\r')
        }

        self.parse_file()

    def parse_file(self):
        num_files = len(self.file_paths)
        for index, data_file in enumerate(self.file_paths):
            filename = "ulx_logs/"+data_file

            print('Processing: {} ...'.format(filename))
            with open(filename, 'r+b') as log:
                map = mmap.mmap(log.fileno(), 0, prot=mmap.PROT_READ)

                # Main parsing loop
                for line in iter(map.readline, ""):
                    self.parse_line(line)

            print('Finished processing [{}]. {}/{}'.format(filename, index+1, num_files))
            print('')

        self.save_data_to_files()

    def save_data_to_files(self):

        # After parsing
        timestamp = int(time.time())
        json_deaths = ujson.dumps({'global_deaths': self.deaths_global, 'player_deaths': self.deaths_people}, ensure_ascii=False)
        json_kills = ujson.dumps({'global_kills': self.kills_global, 'player_kills': self.kills_people}, ensure_ascii=False)
        json_tools = ujson.dumps({'global_tools_used': self.tools_used_global, 'player_tools_used': self.tools_used_people}, ensure_ascii=False)
        json_ents = ujson.dumps({'global_ents_spawned': self.ents_spawned_global, 'player_ents_spawned': self.ents_spawned_people}, ensure_ascii=False)
        json_words = ujson.dumps({'global_words_said': self.words_said_global, 'player_words_said': self.words_said_people}, ensure_ascii=False)
        json_connections = ujson.dumps({'global_connections': self.connections_global}, ensure_ascii=False)
        json_kicks = ujson.dumps({'global_kicks_given': self.kicks_given_global,
                               'global_kicks_received': self.kicks_received_global,
                               'player_kicks_given': self.kicks_given_people,
                               'player_kicks_received': self.kicks_received_people})

        with open('json_deaths', 'w') as save_file:
            print "Saving json_deaths.."
            save_file.write(json_deaths)
            print "Saved!"

        with open('json_kills', 'w') as save_file:
            print "Saving json_kills.."
            save_file.write(json_kills)
            print "Saved!"

        with open('json_tools', 'w') as save_file:
            print "Saving json_tools.."
            save_file.write(json_tools)
            print "Saved!"

        with open('json_ents', 'w') as save_file:
            print "Saving json_ents.."
            save_file.write(json_ents)
            print "Saved!"

        with open('json_words', 'w') as save_file:
            print "Saving json_words.."
            save_file.write(json_words)
            print "Saved!"

        with open('json_connections', 'w') as save_file:
            print "Saving json_connections.."
            save_file.write(json_connections)
            print "Saved!"

        with open('json_kicks', 'w') as save_file:
            print "Saving json_kicks.."
            save_file.write(json_kicks)
            print "Saved!"

    def parse_line(self, line_text):
        line = LogLine(line_text, self.regex_patterns)

        if line.line_type:
            player = line.player.strip()
            subject = line.subject.strip()

            if line.is_ent_spawned_line:
                self.add_spawned_ent(player, subject)

            if line.is_tool_used_line:
                self.add_tool_used(player, subject)

            elif line.is_kill_line:
                self.add_kill(player, subject)

                if subject != 'prop_physics':
                    self.add_death(subject, player)

            elif line.is_chat_line:
                self.add_words(player, subject)

            elif line.is_connection_line:
                self.add_connection(player)

            elif line.is_suicide_line:
                self.add_death(player, player)
                self.add_kill(player, player)

            elif line.is_kick_line:
                self.add_kick(player, subject)

    def add_spawned_ent(self, player, ent):
        global_data = self.ents_spawned_global
        player_data = self.ents_spawned_people.get(player, {})

        # player = player.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        player = player.strip()

        global_data[ent] = global_data.get(ent, 0) + 1

        player_data[ent] = player_data.get(ent, 0) + 1
        self.ents_spawned_people[player] = player_data

    def add_tool_used(self, player, tool):
        global_data = self.tools_used_global
        player_data = self.tools_used_people.get(player, {})

        # player = player.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        player = player.strip()

        global_data[tool] = global_data.get(tool, 0) + 1

        player_data[tool] = player_data.get(tool, 0) + 1
        self.tools_used_people[player] = player_data

    def add_kill(self, player, victim):
        global_data = self.kills_global
        player_data = self.kills_people.get(player, {})

        #player = player.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        #victim = victim.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        player = player.strip()
        victim = victim.strip()

        global_data[player] = global_data.get(player, 0) + 1

        player_data[victim] = player_data.get(victim, 0) + 1
        self.kills_people[player] = player_data

    def add_death(self, player, killer):
        global_data = self.deaths_global
        player_data = self.deaths_people.get(player, {})

        #player = player.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        #killer = killer.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        player = player.strip()
        killer = killer.strip()

        global_data[player] = global_data.get(player, 0) + 1

        player_data[killer] = player_data.get(killer, 0) + 1
        self.deaths_people[player] = player_data

    def add_words(self, player, text):
        global_data = self.words_said_global
        player_data = self.words_said_people.get(player, {})

        _clean_text = text.decode('utf-8', 'replace').encode('utf-8', 'replace').lower().strip()
        split_text = _clean_text.split(' ')
        for word in split_text:
            global_data[word] = global_data.get(word, 0) + 1
            player_data[word] = player_data.get(word, 0) + 1

        self.words_said_people[player] = player_data

    def add_connection(self, player):
        global_data = self.connections_global

        #player = player.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        player = player.strip()

        self.connections_global[player] = global_data.get(player, 0) + 1

    def add_kick(self, admin, minge):
        #admin = admin.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        #minge = minge.decode('utf-8', 'replace').encode('utf-8', 'replace').strip()
        admin = admin.strip()
        minge = minge.strip()

        # Given
        given_global_data = self.kicks_given_global  # { admin1: 25, admin2: 50, admin3: 12, phatso: 727 }
        given_player_data = self.kicks_given_people.get(admin, {}) #  { minge1: 15, minge2: 10, minge3: 20 }

        given_global_data[admin] = given_global_data.get(admin, 0) + 1
        given_player_data[minge] = given_player_data.get(minge, 0) + 1
        self.kicks_given_people[admin] = given_player_data

        # Received
        received_global_data = self.kicks_received_global # { minge1: 15, minge2: 25, minge3: 16, Thanatos: 9001, }
        received_player_data = self.kicks_received_people.get(minge, {}) #  { admin1: 13, admin2: 1, admin3: 11 }

        received_global_data[minge] = received_global_data.get(minge, 0) + 1
        received_player_data[admin] = received_player_data.get(admin, 0) + 1
        self.kicks_received_people[minge] = received_player_data


if __name__ == '__main__':
    files = listdir('ulx_logs/')
    shuffle(files)
    cProfile.run('Parser(files[:50])')
