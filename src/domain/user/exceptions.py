class InvalidPasswordLengthException(Exception):
    def __init__(self):
        super().__init__('The provided password is not long enough.')


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__('User not found for given id.')


class UserEmailAlreadyInUseException(Exception):
    def __init__(self):
        super().__init__(
            'The provided email is already in use by another user.'
        )
