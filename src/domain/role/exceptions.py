class RoleNotFoundException(Exception):
    def __init__(self):
        super().__init__('Role not found for given id')
