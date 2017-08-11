from abc import ABCMeta, abstractmethod


class CreationBase(metaclass=ABCMeta):

    def __call__(self, *args, **kwargs):
        return self.create(*args, **kwargs)

    @abstractmethod
    def create(self):
        pass
