# Sistema de Tickets de Soporte — v1

**Universidad Católica Boliviana "San Pablo" (UCB)**
**Asignatura:** Estructura de Datos — Proyecto Final (versión v1)
**Dominio seleccionado:**  Sistema de tickets de soporte
**Nombre completo:** Santiago Encinas Jadue

## Descripción

Sistema en consola que gestiona solicitudes de soporte: los tickets se registran,
esperan su turno en orden de llegada, son atendidos, resueltos y finalmente
archivados en un historial. Cualquier ticket puede consultarse al instante por su ID.

## Ficha de análisis del dominio

| # | Necesidad del dominio | Estructura elegida | Operación clave | Complejidad |
|---|---|---|---|---|
| 1 | Atender los tickets pendientes en orden de llegada | **Cola (FIFO)** | `encolar` / `desencolar` | O(1) |
| 2 | Encontrar un ticket directamente por su ID único | **Tabla Hash** | `insertar` / `buscar` | O(1) promedio |
| 3 | Conservar el historial de tickets cerrados/resueltos | **Lista** | `append` / recorrido | O(1) agregar, O(n) recorrer |

## Justificación de las estructuras

- **Cola — "La uso porque..."** los tickets deben atenderse en el mismo orden en que
  llegaron (el primero en entrar es el primero en salir). La cola garantiza ese
  comportamiento justo y sus operaciones principales son O(1). Está implementada con
  nodos enlazados, por lo que no hay desplazamiento de elementos al desencolar.
- **Tabla Hash — "La uso porque..."** necesito consultar el estado de cualquier ticket
  por su ID sin recorrer la cola ni el historial. La tabla hash da acceso directo O(1)
  promedio. Está implementada desde cero con encadenamiento separado para resolver
  colisiones y se redimensiona cuando el factor de carga supera 0.75.
- **Lista — "La uso porque..."** el historial de tickets resueltos solo crece al final
  y se consulta recorriéndolo en orden cronológico de cierre. Una lista es ideal:
  `append` es eficiente, conserva el orden y permite iterar o filtrar fácilmente.

## Flujo del sistema

```
crear_ticket ──► Cola (pendientes) + Tabla Hash (índice por ID)
atender_siguiente ──► sale de la Cola, estado EN_ATENCION
resolver_ticket ──► estado RESUELTO + se agrega a la Lista (historial)
buscar_ticket(id) ──► Tabla Hash, O(1)
```

## Estructura del proyecto

```
proyecto_tickets/
├── README.md
├── src/
│   ├── __init__.py
│   ├── ticket.py               # Clase modelo Ticket
│   ├── cola_soporte.py         # Cola FIFO (nodos enlazados)
│   ├── tabla_hash_tickets.py   # Tabla Hash (encadenamiento)
│   └── sistema_soporte.py      # Gestor principal + demo
└── tests/
    ├── __init__.py
    └── test_sistema.py         # Pruebas unitarias
```

## Ejecución

Requiere Python 3.8 o superior, sin dependencias externas. Desde la raíz del proyecto:

```bash
# Demostración
python -m src.sistema_soporte

# Pruebas unitarias
python -m unittest discover -s tests -t . -v
```

## Ejemplo de uso

```python
from src.sistema_soporte import SistemaSoporte

s = SistemaSoporte()
t = s.crear_ticket("Sin internet", "Laboratorio 3", "María Gómez", "ALTA")
atendido = s.atender_siguiente()
s.resolver_ticket(atendido.id_ticket, "Se reinició el router.")
print(s.buscar_ticket(t.id_ticket))
print(s.estadisticas())
```

## Limitaciones de la v1 (mejoras futuras)

- La prioridad (BAJA/MEDIA/ALTA) se registra, pero la atención es estrictamente FIFO.
- Los datos se guardan solo en memoria (sin persistencia en archivos).
- Interfaz solo por código/consola de demostración.
