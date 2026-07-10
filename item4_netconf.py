from ncclient import manager
import xml.dom.minidom


HOST = "192.168.56.101"   
PORT = 830
USER = "admin"
PASS = "Cisco12345"


NUEVO_HOSTNAME = "BahamondesSanhuezaHidalgo"


def conectar():
    """Establece la conexión NETCONF con el router y retorna el objeto manager."""
    m = manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,       
        device_params={'name': 'iosxe'},
        allow_agent=False,
        look_for_keys=False,
        timeout=30
    )
    print(">> Conexión NETCONF establecida correctamente.")
    print(">> Capacidades NETCONF soportadas por el router (primeras 3):")
    for i, cap in enumerate(m.server_capabilities):
        if i >= 3:
            break
        print(f"   - {cap}")
    return m


def cambiar_hostname(m, nuevo_nombre):
    """Cambia el hostname del router vía edit-config usando el modelo nativo IOS-XE."""
    config_xml = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{nuevo_nombre}</hostname>
      </native>
    </config>
    """
    m.edit_config(target='running', config=config_xml)
    print(f">> Hostname cambiado a: {nuevo_nombre}")


def crear_loopback11(m):
    """Crea la interfaz Loopback11 con IP 11.11.11.11/32."""
    config_xml = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>11</name>
            <ip>
              <address>
                <primary>
                  <address>11.11.11.11</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """
    m.edit_config(target='running', config=config_xml)
    print(">> Interfaz Loopback11 creada con IP 11.11.11.11/32.")


def verificar_config(m):
    """Obtiene y muestra la configuración actual de interfaces (formato XML)."""
    filtro = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface/>
      </native>
    </filter>
    """
    respuesta = m.get_config(source='running', filter=filtro)
    xml_bonito = xml.dom.minidom.parseString(str(respuesta)).toprettyxml()
    print("\n--- CONFIGURACIÓN DE INTERFACES (XML) ---")
    print(xml_bonito)


def main():
    m = conectar()
    cambiar_hostname(m, NUEVO_HOSTNAME)
    crear_loopback11(m)
    verificar_config(m)
    m.close_session()
    print("\n>> Sesión NETCONF cerrada correctamente.")


if __name__ == "__main__":
    main()