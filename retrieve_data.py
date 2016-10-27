import json
import operator

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
            data = json.loads(unicode(json_data, "ISO-8859-1"))

            self.global_deaths = data['global_deaths']
            self.player_deaths = data['player_deaths']
            print("Loaded!")
            print("")

        # Kills
        with open('json_kills', 'r') as json_kills:
            print("Loading json_kills...")
            json_data = json_kills.read()
            data = json.loads(unicode(json_data, "ISO-8859-1"))

            self.global_kills = data['global_kills']
            self.player_kills = data['player_kills']
            print("Loaded!")
            print("")
        # Tools
        with open('json_tools', 'r') as json_tools:
            print("Loading json_tools...")
            json_data = json_tools.read()
            data = json.loads(unicode(json_data, "ISO-8859-1"))

            self.global_tools_used = data['global_tools_used']
            self.player_tools_used = data['player_tools_used']
            print("Loaded!")
            print("")
        # Ents
        with open('json_ents', 'r') as json_kills:
            print("Loading json_ents...")
            json_data = json_kills.read()
            data = json.loads(unicode(json_data, "ISO-8859-1"))

            self.global_ents_spawned = data['global_ents_spawned']
            self.player_ents_spawned = data['player_ents_spawned']
            print("Loaded!")
            print("")
        # Words
        with open('json_words', 'r') as json_words:
            print("Loading json_words...")
            json_data = json_words.read()
            data = json.loads(unicode(json_data, "ISO-8859-1"))

            global_data = data['global_words_said']
            player_data = data['player_words_said']

            self.global_words_said = {k:v for k, v in global_data.iteritems() if k not in self.exclude_words}

            self.player_words_said = {}
            for player, words in player_data.iteritems():
                player_words = {word:num for word, num in words.iteritems() if word not in self.exclude_words}
                self.player_words_said[player] = player_words
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
            if command == 'top_deaths_global':
                self.get_top_deaths()

            if command == 'top_kills_global':
                self.get_top_kills()

            if command == 'top_tools_global':
                self.get_top_tools()

            if command == 'top_ents_global':
                self.get_top_ents()

            if command == 'top_words_global':
                self.get_top_words()

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

if __name__ == '__main__':
    GetData()
    raw_input()
