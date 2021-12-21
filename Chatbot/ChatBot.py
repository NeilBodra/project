import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Kindly please select from this list\n\n1 Saving account\n\n2 Current account', ['Check', 'balance'], required_words=['check', 'balance'])
    response('Kindly provide us with your registered phone number', ['saving', 'account'], required_words=['saving'])
    response('Kindly provide us with your registered mobile number', ['current', 'account'], required_words=['current'])
    response('Kindly please select from this list\n1 New ATM card\n2 Block ATM card', ['atm', 'card'], required_words=['atm', 'card'])
    response('Please provide me with your \'account number\' for verification ', ['new'], required_words=['new'])
    response('Please provide me with your \'account number\' for verification', ['block'], required_words=['block'])
    response('We will be sending it on your registered mobile number', ['Request', 'for', 'passbook'], required_words=['passbook'] )
    response('Goodbye happy helping you', ['bye'], single_response=True)
    response('Our customer care representative will shortly contact you', ['customer', 'care'], required_words=['customer', 'care'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# Testing the response system
print('Bot:','Hello I am Alice')
print('Bot:','How can I help you today?')
print('Bot:','Kindly please select from this list\n\n1 Check account balance\n\n2 Atm Card\n\n3 Request for passbook\n\n4 Talk to customer care representative\n\n5 Type Bye to exit from the conversation')
while True:
    chat = input('You: ')
    try:
        x=int(chat)
        print('Bot: We are sending your requested details on your registered mobile number')
    except:
        print('Bot: ' + get_response(chat))
    if chat == 'bye' or chat == 'Bye':
        break
