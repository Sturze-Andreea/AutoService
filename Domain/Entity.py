class Entity:

    def __init__(self, entityId):
        self.__entityId = entityId

    @property
    def entityId(self):
        return self.__entityId

    @entityId.setter
    def entityId(self, idEnt):
        self.__entityId = idEnt
