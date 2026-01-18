from typing import Optional


class Role:
    def __init__(self, id: Optional[int], description: str):
        self.id = id
        self.description = description

    description: str
    id: Optional[int]


class RoleFactory:
    @staticmethod
    def create(description: str, id: Optional[int] = None) -> Role:
        return Role(id=id, description=description)
