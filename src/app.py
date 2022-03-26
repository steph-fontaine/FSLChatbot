#!/bin/usr/env python3

from Motbot import Motbot


def load_greetings(file_path):
    """ ... """

    # output = {}

    lines = None
    
    with open(file_path, 'r', encoding='utf8') as input_file:
        lines = input_file.readlines()
    
    # TODO: Create dictionary containing keys (chatbot messages) to values (expected responses from the user).

    # return output

    return lines


def main():
    """ The application entrypoint. """

    # greetings = load_greetings('greetings.yml')
    
    # for greeting in greetings:
    #     print(greeting)

    conversation = [
        "Hello",
        "Hi there!",
        "How are you doing?",
        "I'm doing great.",
        "That is good to hear",
        "Thank you.",
        "You're welcome."
    ]

    perfect_response_map = {}
    motbot = Motbot('Motbot', perfect_response_map)

    motbot.train(conversation)
    motbot.say(f'Hello. My name is {motbot.name}! Let\'s chat! :)')

    print()

    expected_user_message = None
    score = 100

    while True:
        user_message = input('Say: ')

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