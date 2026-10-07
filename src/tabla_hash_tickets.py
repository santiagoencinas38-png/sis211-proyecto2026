class NodoHash:

    __slots__ = ("clave", "valor", "siguiente")

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None


class TablaHashTickets:
    
    CAPACIDAD_INICIAL = 8
    FACTOR_CARGA_MAXIMO = 0.75

    def __init__(self, capacidad=CAPACIDAD_INICIAL):
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1.")
        self._capacidad = capacidad
        self._buckets = [None] * capacidad
        self._cantidad = 0

    def _hash(self, clave, capacidad=None):
        """Hash polinómico de una cadena (base 31)."""
        capacidad = capacidad or self._capacidad
        h = 0
        for caracter in str(clave):
            h = (h * 31 + ord(caracter)) % capacidad
        return h

    def insertar(self, clave, valor):
    
        indice = self._hash(clave)
        actual = self._buckets[indice]
        while actual is not None:
            if actual.clave == clave:
                actual.valor = valor
                return
            actual = actual.siguiente

        nuevo = NodoHash(clave, valor)
        nuevo.siguiente = self._buckets[indice]
        self._buckets[indice] = nuevo
        self._cantidad += 1

        if self.factor_carga() > self.FACTOR_CARGA_MAXIMO:
            self._redimensionar()

    def buscar(self, clave):
        
        actual = self._buckets[self._hash(clave)]
        while actual is not None:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        return None

    def contiene(self, clave):
        return self.buscar(clave) is not None

    def eliminar(self, clave):
      
        indice = self._hash(clave)
        actual = self._buckets[indice]
        anterior = None
        while actual is not None:
            if actual.clave == clave:
                if anterior is None:
                    self._buckets[indice] = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._cantidad -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def factor_carga(self):
        return self._cantidad / self._capacidad

    def _redimensionar(self):
        
        nueva_capacidad = self._capacidad * 2
        nuevos = [None] * nueva_capacidad
        for cabeza in self._buckets:
            actual = cabeza
            while actual is not None:
                siguiente = actual.siguiente
                indice = self._hash(actual.clave, nueva_capacidad)
                actual.siguiente = nuevos[indice]
                nuevos[indice] = actual
                actual = siguiente
        self._buckets = nuevos
        self._capacidad = nueva_capacidad

    def valores(self):
      
        resultado = []
        for cabeza in self._buckets:
            actual = cabeza
            while actual is not None:
                resultado.append(actual.valor)
                actual = actual.siguiente
        return resultado

    @property
    def capacidad(self):
        return self._capacidad

    def __len__(self):
        return self._cantidad
