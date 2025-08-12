import random
import string

def generate_username():
    return 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
