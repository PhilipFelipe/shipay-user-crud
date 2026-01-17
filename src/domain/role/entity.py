class Role:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    id: int
    description: str


class RoleFactory:
    @staticmethod
    def create_role(id: int, description: str) -> Role:
        return Role(id=id, description=description)
