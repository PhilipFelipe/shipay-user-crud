class Role:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    description: str
    id: int


class RoleFactory:
    @staticmethod
    def create(description: str, id: int = 0) -> Role:
        return Role(id=id, description=description)
