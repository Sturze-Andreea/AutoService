import pickle

from Domain.Exceptions import RepositoryError


class GenericFileRepository:
    """
    Generic repository for storing data in a file
    """

    def __init__(self, fileName):
        """
        Creates a repository
        :param fileName: the file name
        """
        self.__storage = []
        self.__fileName = fileName

    def __loadFromFile(self):
        """
        Loads the content from a file
        """
        try:
            with open(self.__fileName, 'rb') as f_read:
                self.__storage = pickle.load(f_read)
        except FileNotFoundError:
            self.__storage.clear()
        except Exception:
            self.__storage.clear()

    def __saveToFile(self):
        """
        Saves the entities in a file
        """
        with open(self.__fileName, 'wb') as f_write:
            pickle.dump(self.__storage, f_write)

    def create(self, entity):
        """
        Adds a new entity.
        :param entity: the given entity
        :return: -
        :raises: RepositoryError if the id already exists
        """
        self.__loadFromFile()
        for e in self.__storage:
            if e.entityId == entity.entityId:
                raise RepositoryError("The entity id already exists!")
        self.__storage.append(entity)
        self.__saveToFile()

    def read(self, entityId=None):
        """
        Gets an entity by id or all the entities
        :param entityId: optional, the entity id
        :return: the list of entities or the entity with the given id
        """
        self.__loadFromFile()
        if entityId is None:
            return self.__storage[:]
        for entity in self.__storage:
            if entity.entityId == entityId:
                return entity
        return None

    def update(self, entity):
        """
        Updates an entity.
        :param entity: the entity to update
        :raises: RepositoryError if the id does not exist
        """
        entityId = entity.entityId
        ok = 0
        for index in range(len(self.__storage)):
            if self.__storage[index].entityId == entityId:
                ok = 1
                self.__storage[index] = entity
                break
        if ok == 0:
            raise RepositoryError("There is no entity with that id!")
        self.__saveToFile()

    def delete(self, entityId):
        """
        Deletes a entity.
        :param entityId: the entity id to delete.
        :raises RepositoryError: if no entity with id_entity
        """
        self.__loadFromFile()
        ok = 0
        for index in range(len(self.__storage)):
            if self.__storage[index].entityId == entityId:
                del self.__storage[index]
                ok = 1
                break
        if ok == 0:
            raise RepositoryError("There is no entity with that id!")
        self.__saveToFile()

    def clear(self):
        """
        Clears the file
        """
        self.__storage.clear()
        self.__saveToFile()
