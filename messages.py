# All messages that bot will send to the users

WELCOME_MESSAGE = "Hello\nIt is a chat bot, which help to analyze the user's mental state\n" \
                  "This chat bot will scan all user’s posts on Instagram to detect user’s mental problems." \
                  "\nIt will analyze post descriptions, photos.\nWe won’t use your personal data only " \
                  "those that you post yourself\n\n\nTo register please type:\n\n/register name surname inst_account "
SEND_CODE = 'Successfully sent a code\nTo verify your email type:\n/check_code code'
REGISTER = 'Alright, now you have to verify your email\n\nPlease type:\n\n/send_code your email address\n\n\n' \
           'If you continue, it means, you agree with our private policy, if you you want to see it, ' \
           'type: /send_private_policy'
SIGN_WORDS = ['afraid', 'end', 'away', 'dead', 'kill', 'hate', 'alone', 'suicide', 'fuck',
              'fail', 'debt', 'last', 'help']

SEND_BAD_RESULT = ["Please, ask about her/his problems", 'Please, try talk to him']
SEND_GOOD_RESULT = ['She/He is funny', 'Everything is OK']
WRONG_CODE = 'You wrote a wrong code, please try again'
