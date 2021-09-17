from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def view(self, *args):
        pass


class ViewerInterface(Interface):
    def view(self, *args):
        print(*args)


viewer = ViewerInterface().view


