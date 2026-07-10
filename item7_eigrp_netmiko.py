from netmiko import ConnectHandler

dispositivo = {
    "device_type": "cisco_ios",
    "host": "192.168.56.101",
    "username": "admin",
    "password": "Cisco12345",
    "secret": "Cisco12345",
}

AS_NUMBER = 100
PROCESO_NOMBRE = "EXAMEN-DRY7122"


def configurar_eigrp(conn):
    """Configura EIGRP Nombrado IPv4 e IPv6 con interfaz pasiva (sintaxis corregida)."""


    print(">> Habilitando ipv6 unicast-routing...")
    salida0 = conn.send_config_set(["ipv6 unicast-routing"])
    print(salida0)


    comandos_ipv4 = [
        f"router eigrp {PROCESO_NOMBRE}",
        f" address-family ipv4 unicast autonomous-system {AS_NUMBER}",
        "  network 192.168.56.0 0.0.0.255",
        "  network 22.22.22.22 0.0.0.0",
        "  af-interface GigabitEthernet1",
        "   passive-interface",
        "  exit-af-interface",
        "  exit-address-family",
    ]
    print(">> Configurando EIGRP IPv4 (Named Mode)...")
    salida1 = conn.send_config_set(comandos_ipv4)
    print(salida1)

    comandos_ipv6 = [
        f"router eigrp {PROCESO_NOMBRE}",
        f" address-family ipv6 unicast autonomous-system {AS_NUMBER}",
        "  eigrp router-id 1.1.1.1",
        "  af-interface GigabitEthernet1",
        "   passive-interface",
        "  exit-af-interface",
        "  exit-address-family",
    ]
    print(">> Configurando EIGRP IPv6 (Named Mode)...")
    salida2 = conn.send_config_set(comandos_ipv6)
    print(salida2)

    comandos_loopback33 = [
        f"router eigrp {PROCESO_NOMBRE}",
        f" address-family ipv6 unicast autonomous-system {AS_NUMBER}",
        "  af-interface Loopback33",
        "   no passive-interface",
        "  exit-af-interface",
        "  exit-address-family",
    ]
    print(">> Agregando Loopback33 al dominio EIGRP IPv6...")
    salida3 = conn.send_config_set(comandos_loopback33)
    print(salida3)


def verificar_eigrp(conn):
    """Muestra la seccion EIGRP de la configuracion."""
    salida = conn.send_command("show running-config | section eigrp")
    print("\n--- SHOW RUNNING-CONFIG | SECTION EIGRP ---")
    print(salida)
    return salida


def obtener_interfaces(conn):
    """Obtiene IP y estado de las interfaces (IPv4 e IPv6)."""
    salida_v4 = conn.send_command("show ip interface brief")
    print("\n--- SHOW IP INTERFACE BRIEF ---")
    print(salida_v4)

    salida_v6 = conn.send_command("show ipv6 interface brief")
    print("\n--- SHOW IPV6 INTERFACE BRIEF ---")
    print(salida_v6)

    return salida_v4, salida_v6


def obtener_running_config(conn):
    """Obtiene el running-config completo."""
    salida = conn.send_command("show running-config")
    print("\n--- SHOW RUNNING-CONFIG (primeras lineas) ---")
    print("\n".join(salida.splitlines()[:15]))
    print("... (config completa capturada en variable) ...")
    return salida


def obtener_version(conn):
    """Obtiene el show version."""
    salida = conn.send_command("show version")
    print("\n--- SHOW VERSION ---")
    print(salida)
    return salida


def main():
    print(">> Conectando al router via SSH (Netmiko)...")
    conn = ConnectHandler(**dispositivo)
    conn.enable()
    print(">> Conexion establecida correctamente.\n")

    configurar_eigrp(conn)
    verificar_eigrp(conn)
    obtener_interfaces(conn)
    obtener_running_config(conn)
    obtener_version(conn)

    conn.disconnect()
    print("\n>> Sesion Netmiko cerrada correctamente.")


if __name__ == "__main__":
    main()
