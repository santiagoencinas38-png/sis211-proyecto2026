from datetime import datetime

PRIORIDADES_VALIDAS = ("BAJA", "MEDIA", "ALTA")

ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_EN_ATENCION = "EN_ATENCION"
ESTADO_RESUELTO = "RESUELTO"


class Ticket:

    def __init__(self, id_ticket, titulo, descripcion, solicitante, prioridad="MEDIA"):
        if not id_ticket or not str(id_ticket).strip():
            raise ValueError("El ID del ticket no puede estar vacío.")
        if not titulo or not titulo.strip():
            raise ValueError("El título del ticket no puede estar vacío.")
        if not solicitante or not solicitante.strip():
            raise ValueError("El solicitante no puede estar vacío.")
        prioridad = prioridad.upper()
        if prioridad not in PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridad inválida. Use una de: {PRIORIDADES_VALIDAS}")

        self.id_ticket = str(id_ticket)
        self.titulo = titulo.strip()
        self.descripcion = descripcion
        self.solicitante = solicitante.strip()
        self.prioridad = prioridad
        self.estado = ESTADO_PENDIENTE
        self.fecha_creacion = datetime.now()
        self.fecha_cierre = None
        self.solucion = None

    def iniciar_atencion(self):
        """Marca el ticket como en atención (sale de la cola)."""
        if self.estado != ESTADO_PENDIENTE:
            raise ValueError(
                f"El ticket {self.id_ticket} no está pendiente (estado: {self.estado})."
            )
        self.estado = ESTADO_EN_ATENCION

    def cerrar(self, solucion):
        """Cierra el ticket registrando la solución aplicada."""
        if self.estado != ESTADO_EN_ATENCION:
            raise ValueError(
                f"El ticket {self.id_ticket} debe estar EN_ATENCION para cerrarse "
                f"(estado actual: {self.estado})."
            )
        if not solucion or not solucion.strip():
            raise ValueError("Debe indicar la solución aplicada.")
        self.solucion = solucion.strip()
        self.fecha_cierre = datetime.now()
        self.estado = ESTADO_RESUELTO

    def esta_resuelto(self):
        return self.estado == ESTADO_RESUELTO

    def __str__(self):
        return (
            f"[{self.id_ticket}] {self.titulo} | {self.solicitante} | "
            f"Prioridad: {self.prioridad} | Estado: {self.estado}"
        )

    def __repr__(self):
        return f"Ticket(id={self.id_ticket!r}, estado={self.estado!r})"
