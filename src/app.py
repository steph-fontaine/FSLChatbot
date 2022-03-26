#!/bin/usr/env python3


class Chatbot(object):

    def __init__(self, name):
        """ Chatbot initializer. """

        self.name = name

    def say_hello(self):
        """ Displays a greeting from the chatbot. """

        print(f'Hello. My name is {self.name}!')


def main():
    """ The application entrypoint. """

    chatbot = Chatbot('Tuly')
    chatbot.say_hello()


if __name__ == '__main__':
    main()