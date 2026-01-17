class InvalidPasswordLengthException(Exception):
    def __init__(self):
        super().__init__('The provided password is not long enough.')
