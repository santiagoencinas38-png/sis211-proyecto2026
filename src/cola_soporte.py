
class NodoCola:

    __slots__ = ("dato", "siguiente")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ColaVaciaError(Exception):
    """Se lanza al intentar sacar o ver un elemento de una cola vacía."""


class ColaSoporte:

    def __init__(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def encolar(self, ticket):
    
        nuevo = NodoCola(ticket)
        if self._final is None:
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamanio += 1

    def desencolar(self):
        
        if self.esta_vacia():
            raise ColaVaciaError("No hay tickets pendientes en la cola.")
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1
        return nodo.dato

    def frente(self):
        
        if self.esta_vacia():
            raise ColaVaciaError("No hay tickets pendientes en la cola.")
        return self._frente.dato

    def esta_vacia(self):
        return self._tamanio == 0

    def __len__(self):
        return self._tamanio

    def __iter__(self):
        
        actual = self._frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
