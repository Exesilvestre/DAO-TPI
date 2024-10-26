from abc import ABC, abstractmethod


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()


class Observer(ABC):
    @abstractmethod
    def update(self):
        """
        Método abstracto que debe implementar cada observador para recibir notificaciones.
        """
        pass

