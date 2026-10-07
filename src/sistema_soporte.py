from src.cola_soporte import ColaSoporte
from src.tabla_hash_tickets import TablaHashTickets
from src.ticket import Ticket


class SistemaSoporte:

    def __init__(self):
        self._pendientes = ColaSoporte()
        self._indice = TablaHashTickets()
        self._historial = []
        self._contador = 0

    def _generar_id(self):
        self._contador += 1
        return f"TCK-{self._contador:04d}"

    def crear_ticket(self, titulo, descripcion, solicitante, prioridad="MEDIA"):
       
        ticket = Ticket(self._generar_id(), titulo, descripcion, solicitante, prioridad)
        self._pendientes.encolar(ticket)
        self._indice.insertar(ticket.id_ticket, ticket)
        return ticket

    def atender_siguiente(self):
      
        ticket = self._pendientes.desencolar()
        ticket.iniciar_atencion()
        return ticket

    def resolver_ticket(self, id_ticket, solucion):
       
        ticket = self._indice.buscar(id_ticket)
        if ticket is None:
            raise KeyError(f"No existe el ticket {id_ticket}.")
        ticket.cerrar(solucion)
        self._historial.append(ticket)
        return ticket

    def buscar_ticket(self, id_ticket):
    
        return self._indice.buscar(id_ticket)

    def ver_proximo(self):
        
        return self._pendientes.frente()

    def listar_pendientes(self):
        return list(self._pendientes)

    def listar_historial(self):
        return list(self._historial)

    def estadisticas(self):
        return {
            "total": len(self._indice),
            "pendientes": len(self._pendientes),
            "resueltos": len(self._historial),
        }


def _demo():
    sistema = SistemaSoporte()
    sistema.crear_ticket("No enciende el PC", "Pantalla negra", "Ana Pérez", "ALTA")
    sistema.crear_ticket("Olvidé mi contraseña", "Correo institucional", "Luis Rojas", "BAJA")
    sistema.crear_ticket("Sin internet", "Laboratorio 3", "María Gómez", "MEDIA")

    print("Pendientes:")
    for t in sistema.listar_pendientes():
        print("  ", t)

    atendido = sistema.atender_siguiente()
    print("\nAtendiendo:", atendido)
    sistema.resolver_ticket(atendido.id_ticket, "Se reemplazó la fuente de poder.")

    print("\nBúsqueda por ID TCK-0002:", sistema.buscar_ticket("TCK-0002"))
    print("\nHistorial:")
    for t in sistema.listar_historial():
        print("  ", t, "->", t.solucion)
    print("\nEstadísticas:", sistema.estadisticas())


if __name__ == "__main__":
    _demo()
