#!/bin/usr/env python3

import enum
from Motbot import Motbot


def load_conversation_file(file_path):
    """ ... """

    conversation = []

    lines = None
    
    with open(file_path, 'r', encoding='utf8') as input_file:
        lines = input_file.readlines()
    
    for line in lines:
        line = line.replace(' - ', '')
        line = line.lstrip('-')
        line = line.replace('\n', '')
        line = line.strip()

        conversation.append(line)

    return conversation
 

def load_conversation_map(conversation_list):
    """ ... """

    output = {}
    
    key = None
    value = None

    for i, line in enumerate(conversation_list):
        if i % 2 == 0:
            value = line
        else:
            key = line

        if key is not None and value is not None:
            output[key] = value
            key = None
            value = None


    return output


def main():
    """ The application entrypoint. """

    conversation = load_conversation_file('chats.txt')

    perfect_response_map = load_conversation_map(conversation)
    
    #for key in perfect_response_map:
    #    print(key)
    #    print(perfect_response_map[key])
    
    motbot = Motbot('Motbot', perfect_response_map)

    motbot.train(conversation)
    motbot.say(f'Hello. My name is {motbot.name}! Let\'s chat! :)')
    motbot.say('Salut, comment ça va? (Say: "I am good, and you?")')

    print()

    expected_user_message = 'Ça va bien, et toi?'
    score = 100

    while True:
        user_message = input('You: ')

        if user_message.lower().strip() == 'bye':
            motbot.say('Bye!')
            break

        if expected_user_message is not None:
            if user_message == expected_user_message:
                motbot.say('Good job, human!')
            else:
                motbot.say(f'Not quite. I expected you to say:\n"{expected_user_message}".')
                score -= 5
            print()

        motbot_message = motbot.get_response(user_message)
        expected_user_message = motbot.get_expected_response(motbot_message)

        motbot.say(motbot_message)
        print()

    print(f'Score: {score}')

if __name__ == '__main__':
    main()