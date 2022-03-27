#!/bin/usr/env python3

import enum
import os
import sys
from Motbot import Motbot
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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

def read_user_score_file(file_path):
	with open(file_path, 'rb') as input_file:
		value_bytes = input_file.read(4)
		return int.from_bytes(value_bytes, byteorder='little')

def write_user_Score_file(file_path, value):
	with open(file_path, 'wb') as output_file:
		value_bytes = value.to_bytes(length=4, byteorder='little')
		output_file.write(value_bytes)        


def main():
    """ The application entrypoint. """

    perfect_response_map = {}
    motbot = Motbot('Motbot', perfect_response_map)

    user_name = input('What is your name? ')
    user_file_name = f'{user_name}.bin'

    if os.path.isfile(user_file_name):
        previous_score = read_user_score_file(user_file_name)
    else:
        previous_score = 0

    motbot.say(f'Hello. My name is {motbot.name}! Let\'s chat! :) You can type "Bye" anytime during our conversation to stop chatting.')
    motbot.say('What do you want to work on today? Please choose from this list: sports, hobbies, greetings, present-verbs and passe-compose: ')

    user_choice = input().lower().strip()
    available_topics = ['sports', 'hobbies', 'greetings', 'present-verbs', 'passe-compose']
    valid_choice = False
    attempt_counter = 0
    
    while not valid_choice:
        if user_choice in available_topics:
            conversation = load_conversation_file(f'{user_choice}.txt')
            valid_choice = True
        else:
            if attempt_counter > 1:
                print('Invalid choice. Aborting program. ')
                sys.exit(1)
            else:
                if attempt_counter == 0:
                    print('Invalid option. Please choose again. You have 2 more attempts: ')
                elif attempt_counter == 1:
                    print('Invalid option. Please choose again. This is your last attempt: ')

                user_choice = input().lower().strip()
                attempt_counter += 1

    perfect_response_map = load_conversation_map(conversation)
    motbot = Motbot('Motbot', perfect_response_map)

    motbot.train(conversation)

    print()

    expected_user_message = None
    current_score = 100

    print(f'Current Score: {current_score}')
    motbot.say('Let\'s start! Remember that accents matter! If you don\'t know the answer, type "Skip"')
    print()

    for key in perfect_response_map:
        matching_ratio = 0
        motbot_message = perfect_response_map[key]
        motbot.say(motbot_message)
        expected_user_message = key
        user_message = input('You: ')

        if user_message.lower().strip() == 'bye' or user_message.lower().strip() == 'bye!' :
            motbot.say('Bye!')
            break

        if expected_user_message is not None:
            if user_message.lower().strip() == 'skip':
                motbot.say(f'I expected you to say:\n"{expected_user_message}".\n You lost 5 points :(')
                current_score -= 5
                print()
                continue

            matching_ratio = fuzz.ratio(user_message.lower().strip('!'), expected_user_message.lower())
            if matching_ratio >= 95:
                motbot.say(f'Good job, {user_name}!')
            else:
                motbot.say(f'Not quite. I expected you to say:\n"{expected_user_message}".\n You lost 5 points :(')
                current_score -= 5
            print()

        print()
    print()

    print(f'Final Score: {current_score}')
    print()
    print()

    if current_score > previous_score:
        print('Congratulations! You did better than last time. Keep it up! ')
        print()
    elif current_score == previous_score:
        print('No change in your score.')
        print()
    else:
        print('Aww you didn\'t do as great as last time. Try again!')
        print()

    write_user_Score_file(user_file_name, current_score)

if __name__ == '__main__':
    main()