import json
import operator
import ujson

class GetData():
    def __init__(self):
        self.prompt_enabled = True

        self.global_deaths = None
        self.player_deaths = None

        self.global_kills = None
        self.player_kills = None

        self.global_tools_used = None
        self.player_tools_used = None

        self.global_ents_spawned = None
        self.player_ents_spawned = None

        self.global_words_said = None
        self.player_words_said = None

        self.global_connections = None

        self.global_kicks_given = None
        self.player_kicks_given = None

        self.global_kicks_received = None
        self.player_kicks_received = None

        self.exclude_words = ['the', '!pvp', '!pvpon', 'on', 'off',
                         'i', 'you', 'a', 'to', 'it', 'is', 'I',
                         '!pvpoff', 'Yes', '(', 'that', 'my', 'in',
                         'me', 'and', 'not', 'yes', 'no', 'oh', 'this',
                         'do', 'its', 'of', 'im', 'can', 'what', '', 'be', '??', '??>',
                         'are', 'for', 'your', 'get', 'so', 'have', 'how', 'was', 'but',
                         'he', 'dont', 'if', 'did', 'see', 'will', 'go', 'ok', 'stop', 'why', 'make', 'or',
                         'out', 'up', 'now', 'know', 'k', 'we', 'an', 'there', 'here', 'all', 'just', 'being', 'over',
                         'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only',
                         'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him',
                         'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some',
                         'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't',
                         'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or',
                         'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom',
                         'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than',
                         'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and',
                         'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no',
                         'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i',
                         'yours', 'so', 'the', 'having', 'once', '??', '??>']

        self.load_json_data()

        self.main()

    def load_json_data(self):
        print("Loading Json data...")

        # Deaths
        with open('json_deaths', 'r') as json_deaths:
            print("Loading json_deaths...")
            json_data = json_deaths.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_deaths = data['global_deaths']
            self.player_deaths = data['player_deaths']
            print("Loaded!")
            print("")

        # Kills
        with open('json_kills', 'r') as json_kills:
            print("Loading json_kills...")
            json_data = json_kills.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_kills = data['global_kills']
            self.player_kills = data['player_kills']
            print("Loaded!")
            print("")
        # Tools
        with open('json_tools', 'r') as json_tools:
            print("Loading json_tools...")
            json_data = json_tools.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_tools_used = data['global_tools_used']
            self.player_tools_used = data['player_tools_used']
            print("Loaded!")
            print("")
        # Ents
        with open('json_ents', 'r') as json_kills:
            print("Loading json_ents...")
            json_data = json_kills.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_ents_spawned = data['global_ents_spawned']
            self.player_ents_spawned = data['player_ents_spawned']
            print("Loaded!")
            print("")
        # Words
        with open('json_words', 'r') as json_words:
            print("Loading json_words...")
            json_data = json_words.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            global_data = data['global_words_said']
            player_data = data['player_words_said']

            self.global_words_said = {k:v for k, v in global_data.iteritems() if k not in self.exclude_words}

            self.player_words_said = {}
            for player, words in player_data.iteritems():
                player_words = {word:num for word, num in words.iteritems() if word not in self.exclude_words}
                self.player_words_said[player] = player_words
            print("Loaded!")
            print("")
        # Kicks
        with open('json_kicks', 'r') as json_kicks:
            print("Loading json_kicks...")
            json_data = json_kicks.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_kicks_given = data['global_kicks_given']
            self.player_kicks_given = data['player_kicks_given']

            self.global_kicks_received = data['global_kicks_received']
            self.player_kicks_received = data['player_kicks_received']

            print("Loaded!")
            print("")
        # Connections
        with open('json_connections', 'r') as json_connections:
            print("Loading json_connections...")
            json_data = json_connections.read()
            data = ujson.loads(unicode(json_data, "ISO-8859-1"))

            self.global_connections = data['global_connections']
            print("Loaded!")
            print("")

    def main(self):
        while(self.prompt_enabled):
            command = raw_input("Command: ")
            self.parse_command(command)

    def parse_command(self, user_command):
        if user_command == '':
            print "Please enter a valid command"
            return

        split_command = user_command.split(' ')

        command = split_command[0]

        if len(split_command) == 1:
            if command == 'top_deaths':
                self.get_top_deaths()

            if command == 'top_kills':
                self.get_top_kills()

            if command == 'top_tools':
                self.get_top_tools()

            if command == 'top_ents':
                self.get_top_ents()

            if command == 'top_words':
                self.get_top_words()

            if command == 'top_kicks_given':
                self.get_top_kicks_given()

            if command == 'top_kicks_received':
                self.get_top_kicks_received()

            if command == 'top_connections':
                self.get_top_connections()

        else:
            argument = " ".join(split_command[1:])

            if command == 'deaths':
                self.get_deaths_for(argument)

            if command == 'kills':
                self.get_kills_for(argument)

            if command == 'tools':
                self.get_tools_for(argument)

            if command == 'ents':
                self.get_ents_for(argument)

            if command == 'chat':
                self.get_words_for(argument)

            if command == 'kicks_given':
                self.get_kicks_given_for(argument)

            if command == 'kicks_received':
                self.get_kicks_received_for(argument)

            if command == 'connections':
                self.get_connections_for(argument)

    @staticmethod
    def sort_dict(dictionary):
        return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    def get_top_deaths(self):
        data = self.global_deaths
        sorted_deaths = self.sort_dict(data)

        for index, place in enumerate(sorted_deaths[:10]):
            name = place[0].encode('ascii', 'replace')
            kills = place[1]
            print "{}. {}: {} deaths".format(index+1, name, kills)
            print ''

    def get_top_kills(self):
        data = self.global_kills
        sorted_kills = self.sort_dict(data)

        for index, place in enumerate(sorted_kills[:10]):
            name = place[0].encode('ascii', 'replace')
            kills = place[1]
            print "{}. {}: {} kills".format(index+1, name, kills)
            print ''

    def get_top_tools(self):
        data = self.global_tools_used
        sorted_tools = self.sort_dict(data)

        for index, place in enumerate(sorted_tools[:10]):
            tool = place[0].encode('ascii', 'replace')
            uses = place[1]
            print "{}. {}: {} uses".format(index+1, tool, uses)
            print ''

    def get_top_ents(self):
        data = self.global_ents_spawned
        sorted_ents = self.sort_dict(data)

        for index, place in enumerate(sorted_ents[:10]):
            ent = place[0].encode('ascii', 'replace')
            spawns = place[1]
            print "{}. {}: {} spawns".format(index+1, ent, spawns)
            print ''

    def get_top_words(self):
        data = self.global_words_said
        sorted_words = self.sort_dict(data)

        for index, place in enumerate(sorted_words[:50]):
            word = place[0].encode('ascii', 'replace')
            occurances = place[1]
            print "{}. '{}': {} occurances".format(index+1, word, occurances)
            print ''

    def get_top_kicks_given(self):
        data = self.global_kicks_given
        sorted_kicks = self.sort_dict(data)

        # TODO: total kicks
        for index, place in enumerate(sorted_kicks[:10]):
            admin = place[0].encode('ascii', 'replace')
            kicks = place[1]
            print "{}. {}: {} kicks given".format(index+1, admin, kicks)
            print ''

    def get_top_kicks_received(self):
        data = self.global_kicks_received
        sorted_kicks = self.sort_dict(data)

        for index, place in enumerate(sorted_kicks[:10]):
            minge = place[0].encode('ascii', 'replace')
            kicks = place[1]
            print "{}. {}: {} kicks received".format(index+1, minge, kicks)
            print ''

    def get_top_connections(self):
        data = self.global_connections
        sorted_connections= self.sort_dict(data)

        # TODO: total connections
        for index, place in enumerate(sorted_connections[:10]):
            name = place[0].encode('ascii', 'replace')
            connections = place[1]
            print "{}. {}: {} connections".format(index+1, name, connections)
            print ''

    #### Player
    def get_deaths_for(self, name):
        data = self.player_deaths[name]
        sorted_deaths = self.sort_dict(data)

        for index, place in enumerate(sorted_deaths[:10]):
            killer = place[0].encode('ascii', 'replace')
            deaths = place[1]
            print "{}. {} died to {} {} times".format(index+1, name, killer, deaths)
            print ''

    def get_kills_for(self, name):
        data = self.player_kills[name]
        sorted_kills = self.sort_dict(data)

        for index, place in enumerate(sorted_kills[:10]):
            victim = place[0].encode('ascii', 'replace')
            kills = place[1]
            print "{}. {} killed {} {} times".format(index+1, name, victim, kills)
            print ''

    def get_tools_for(self, name):
        data = self.player_tools_used[name]
        sorted_tools = self.sort_dict(data)

        for index, place in enumerate(sorted_tools[:10]):
            tool = place[0].encode('ascii', 'replace')
            uses = place[1]
            print "{}. {} used {} {} times".format(index+1, name, tool, uses)
            print ''

    def get_ents_for(self, name):
        data = self.player_ents_spawned[name]
        sorted_ents = self.sort_dict(data)

        for index, place in enumerate(sorted_ents[:10]):
            ent = place[0].encode('ascii', 'replace')
            spawns = place[1]
            print "{}. {} spawned '{}' {} times".format(index+1, name, ent, spawns)
            print ''

    def get_words_for(self, name):
        data = self.player_words_said[name]
        sorted_words = self.sort_dict(data)

        for index, place in enumerate(sorted_words[:50]):
            word = place[0].encode('ascii', 'replace').lower().strip()
            occurances = place[1]
            print "{}. {} said '{}' {} times".format(index+1, name, word, occurances)
            print ''

    def get_connections_for(self, name):
        data = self.global_connections[name]
        print "{} has connected {} times total".format(name, data)

    def get_kicks_given_for(self, name):
        data = self.player_kicks_given[name]
        sorted_kicks = self.sort_dict(data)

        total = sum([count[1] for count in sorted_kicks])
        print "{} total kicks given".format(total)
        for index, place in enumerate(sorted_kicks[:10]):
            minge = place[0].encode('ascii', 'replace')
            kicks = place[1]
            print "{}. {} kicked '{}' {} times".format(index+1, name, minge, kicks)
            print ''

    def get_kicks_received_for(self, name):
        data = self.player_kicks_received[name]
        sorted_kicks = self.sort_dict(data)

        total = sum([count[1] for count in sorted_kicks])
        print "{} total kicks received".format(total)
        for index, place in enumerate(sorted_kicks[:10]):
            admin = place[0].encode('ascii', 'replace')
            kicks = place[1]
            print "{}. {} was kicked by '{}' {} times".format(index+1, name, admin, kicks)
            print ''

if __name__ == '__main__':
    GetData()
    raw_input()
