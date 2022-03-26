from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class Motbot(object):
    """ ... """

    def __init__(self, name, perfect_response_map = {}):
        """ Motbot initializer. """

        self.bot = ChatBot(name)
        self.trainer = ListTrainer(self.bot)
        self.name = name
        self.perfect_response_map = perfect_response_map

    def say(self, message):
        """ Displays `message` from the chatbot. """

        print(f'{self.name}: {message}')

    def train(self, conversation):
        """ ... """

        self.trainer.train(conversation)

    def get_response(self, message):
        """ Returns the chatbot's response to `message`. """

        return self.bot.get_response(message)

    def get_expected_response(self, message):
        """ Returns the response that the bot expects from the user. """

        if message in self.perfect_response_map:
            return self.perfect_response_map[message]