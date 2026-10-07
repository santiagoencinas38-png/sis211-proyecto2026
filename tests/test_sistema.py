import unittest

from src.cola_soporte import ColaSoporte, ColaVaciaError
from src.sistema_soporte import SistemaSoporte
from src.tabla_hash_tickets import TablaHashTickets
from src.ticket import Ticket, ESTADO_EN_ATENCION, ESTADO_PENDIENTE, ESTADO_RESUELTO


def crear(id_ticket="T1"):
    return Ticket(id_ticket, "Titulo", "Desc", "Usuario", "MEDIA")


class TestTicket(unittest.TestCase):
    def test_estado_inicial_pendiente(self):
        self.assertEqual(crear().estado, ESTADO_PENDIENTE)

    def test_ciclo_de_vida(self):
        t = crear()
        t.iniciar_atencion()
        self.assertEqual(t.estado, ESTADO_EN_ATENCION)
        t.cerrar("Solucionado")
        self.assertEqual(t.estado, ESTADO_RESUELTO)
        self.assertIsNotNone(t.fecha_cierre)

    def test_no_se_cierra_sin_atender(self):
        with self.assertRaises(ValueError):
            crear().cerrar("Solución")

    def test_prioridad_invalida(self):
        with self.assertRaises(ValueError):
            Ticket("T1", "x", "y", "z", "URGENTISIMA")

    def test_titulo_vacio(self):
        with self.assertRaises(ValueError):
            Ticket("T1", "  ", "y", "z")


class TestCola(unittest.TestCase):
    def test_orden_fifo(self):
        cola = ColaSoporte()
        for i in range(1, 4):
            cola.encolar(crear(f"T{i}"))
        self.assertEqual(cola.desencolar().id_ticket, "T1")
        self.assertEqual(cola.desencolar().id_ticket, "T2")
        self.assertEqual(cola.desencolar().id_ticket, "T3")
        self.assertTrue(cola.esta_vacia())

    def test_desencolar_vacia(self):
        with self.assertRaises(ColaVaciaError):
            ColaSoporte().desencolar()

    def test_frente_no_extrae(self):
        cola = ColaSoporte()
        cola.encolar(crear("T1"))
        self.assertEqual(cola.frente().id_ticket, "T1")
        self.assertEqual(len(cola), 1)

    def test_reutilizable_tras_vaciarse(self):
        cola = ColaSoporte()
        cola.encolar(crear("T1"))
        cola.desencolar()
        cola.encolar(crear("T2"))
        self.assertEqual(cola.desencolar().id_ticket, "T2")


class TestTablaHash(unittest.TestCase):
    def test_insertar_y_buscar(self):
        tabla = TablaHashTickets()
        t = crear("T1")
        tabla.insertar("T1", t)
        self.assertIs(tabla.buscar("T1"), t)

    def test_buscar_inexistente(self):
        self.assertIsNone(TablaHashTickets().buscar("NOPE"))

    def test_colisiones(self):
        tabla = TablaHashTickets(capacidad=1)  # fuerza colisiones
        tabla.insertar("A", crear("A"))
        tabla.insertar("B", crear("B"))
        self.assertEqual(tabla.buscar("A").id_ticket, "A")
        self.assertEqual(tabla.buscar("B").id_ticket, "B")

    def test_redimensionamiento(self):
        tabla = TablaHashTickets()
        cap_inicial = tabla.capacidad
        for i in range(50):
            tabla.insertar(f"T{i}", crear(f"T{i}"))
        self.assertGreater(tabla.capacidad, cap_inicial)
        self.assertEqual(len(tabla), 50)
        for i in range(50):
            self.assertTrue(tabla.contiene(f"T{i}"))

    def test_eliminar(self):
        tabla = TablaHashTickets()
        tabla.insertar("T1", crear("T1"))
        self.assertTrue(tabla.eliminar("T1"))
        self.assertFalse(tabla.eliminar("T1"))
        self.assertEqual(len(tabla), 0)


class TestSistema(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaSoporte()

    def test_ids_secuenciales(self):
        t1 = self.sistema.crear_ticket("A", "d", "u")
        t2 = self.sistema.crear_ticket("B", "d", "u")
        self.assertEqual(t1.id_ticket, "TCK-0001")
        self.assertEqual(t2.id_ticket, "TCK-0002")

    def test_atiende_en_orden_de_llegada(self):
        self.sistema.crear_ticket("Primero", "d", "u", "BAJA")
        self.sistema.crear_ticket("Segundo", "d", "u", "ALTA")
        self.assertEqual(self.sistema.atender_siguiente().titulo, "Primero")

    def test_flujo_completo(self):
        t = self.sistema.crear_ticket("Falla", "d", "u")
        atendido = self.sistema.atender_siguiente()
        self.sistema.resolver_ticket(atendido.id_ticket, "Reiniciado")
        self.assertEqual(self.sistema.buscar_ticket(t.id_ticket).estado, ESTADO_RESUELTO)
        self.assertEqual(len(self.sistema.listar_historial()), 1)
        self.assertEqual(self.sistema.estadisticas(),
                         {"total": 1, "pendientes": 0, "resueltos": 1})

    def test_resolver_inexistente(self):
        with self.assertRaises(KeyError):
            self.sistema.resolver_ticket("TCK-9999", "x")

    def test_resolver_ticket_pendiente_falla(self):
        t = self.sistema.crear_ticket("A", "d", "u")
        with self.assertRaises(ValueError):
            self.sistema.resolver_ticket(t.id_ticket, "x")

    def test_atender_sin_pendientes(self):
        with self.assertRaises(ColaVaciaError):
            self.sistema.atender_siguiente()


if __name__ == "__main__":
    unittest.main()
