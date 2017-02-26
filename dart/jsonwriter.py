import json
import os

"""
Writes json file of server specific data:
    > Servers name
    > Servers Id
    > Command Prefix
    > List of global commands
    > List of server specific commands

"""

PATH = os.path.dirname(os.path.realpath(__file__))
GLOBAL_PREFIX = "!"
GLOBAL_CMD = ["add",
              "disconnect",
              "emodelete",
              "emolist",
              "emomake",
              "hello",
              "joinvoice",
              "leave",
              "pause",
              "play",
              "playing",
              "purge",
              "skip",
              "summon",
              "volume"]

class JsonInterp:

    @staticmethod
    def write_server_cmd_file(server_id,
                              name,
                              prefix=GLOBAL_PREFIX,
                              default_cmd_aliases=GLOBAL_CMD,
                              server_specific_cmd_aliases=[]):
        """
        Write server specific json file of server commands, command prefixes, and server specific prefix and commands
        :param server_id: Server id
        :param name: Servers name
        :param prefix: command prefix
        :param default_cmd_aliases: Default commands for each server
        :param server_specific_cmd_aliases: Server specific commands
        :return:
        """

        server_cmd = {"name": name,
                      "server_id": server_id,
                      "command_prefix": prefix,
                      "command_list": default_cmd_aliases,
                      "server_specific_commands": server_specific_cmd_aliases}

        file_name = PATH + "\\" + r"data\{}.json".format(name)

        with open(file_name, 'w')as json_file:
            json.dump(server_cmd, json_file, sort_keys=True, indent=4)

    @staticmethod
    def load_server_cmd_file(server_name):
        """
        Loads server data to a dictionary and returns it
        :param server_name: Servers name / file name
        :return: Dictionary of server data
        """
        with open(PATH + "\\" + r"data\{}.json".format(server_name), 'r')as server_file:
            cmd_data = json.load(server_file)
        return cmd_data

    @staticmethod
    def unpack_cmd_data(server_data):
        """
        Unpacks server data dictionary
        :param server_data: Dictionary object of server data from a json file
        :return: returns each keys value unpacked
        """
        return server_data["name"], server_data["server_id"], server_data["command_prefix"], server_data["command_list"], server_data["server_specific_commands"]

    @staticmethod
    def create_cmd_list_with_prefix(data):
        """
        return a list of pre concatenated commands with their respective prefixes
        :param data: Servers json data
        :return: list of commands with prefix
        """
        defaults = data["command_list"]
        customs = data["server_specific_commands"]
        prefix = data["prefix"]
        concat_cmds = []

        for item in defaults:
            concat_cmds.append(prefix + item)

        if len(customs) != 0:
            for item in customs:
                concat_cmds.append(prefix + item)

        return concat_cmds

    @staticmethod
    def update_server_cmd_file(name,
                               server_id=None,
                               prefix=GLOBAL_PREFIX,
                               default_cmd_aliases=[],
                               server_specific_cmd_aliases=[]):

        """
        Updates server json file with updated info, re-saves the file and returns the updated dictionary object
        :param server_id: Server id
        :param name: Servers name
        :param prefix: command prefix
        :param default_cmd_aliases: Default commands for each server
        :param server_specific_cmd_aliases: Server specific commands
        :return: returns new dictionary of server data
        """

        new_server_file_data = {"name": name,
                                "server_id": server_id,
                                "command_prefix": prefix,
                                "command_list": default_cmd_aliases,
                                "server_specific_commands": server_specific_cmd_aliases}

        file_name = PATH + "\\" + r"data\{}.json".format(name)

        with open(file_name, 'w')as json_file:
            json.dump(new_server_file_data, json_file, sort_keys=True, indent=4)

        return new_server_file_data
