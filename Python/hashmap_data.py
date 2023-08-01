import json

class Hashmap:
    def __init__(self, length):
        self.datas = []
        for i in range(length):
            self.datas.append({})

    def append(self, key, value):
        index = key % len(self.datas)
        data_dict = self.datas[index]
        if key not in data_dict:
            data_dict[key] = [value]
        else:
            data_dict[key].append(value)

    def get(self, key):
        index = key % len(self.datas)
        data_dict = self.datas[index]
        if key in data_dict:
            return data_dict[key]
        return None
    
    def get_all_commands(self):
        commands = []
        for data_dict in self.datas:
            for user_commands in data_dict.values():
                commands.extend(user_commands)
        return commands
    
    def sauvegarder_donnees(self, filename):
        data = {}
        for data_dict in self.datas:
            for key, user_commands in data_dict.items():
                if key not in data:
                    data[key] = []
                data[key].extend(user_commands)

        with open(filename, 'w') as file:
            json.dump(data, file)

    def charger_donnees(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)

            for key, user_commands in data.items():
                key = int(key)  # Convertir la clé en entier
                for command in user_commands:
                    self.append(key, command)
