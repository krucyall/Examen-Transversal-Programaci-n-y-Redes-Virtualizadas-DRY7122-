def clasificar_vlan(numero_vlan):
    """Clasifica el número de VLAN según los rangos estándar de Cisco."""
    if 1 <= numero_vlan <= 1005:
        return "RANGO NORMAL"
    elif 1006 <= numero_vlan <= 4094:
        return "RANGO EXTENDIDO"
    else:
        return "FUERA DE RANGO (VLAN inválida, debe ser 1-4094)"

def main():
    print("=" * 50)
    print("CLASIFICADOR DE VLAN - DRY7122")
    print("=" * 50)

    while True:
        entrada = input("Ingrese el número de VLAN (o 's' para salir): ")

        if entrada.lower() == 's':
            print("Saliendo del programa...")
            break

        try:
            vlan = int(entrada)
            resultado = clasificar_vlan(vlan)
            print(f">> VLAN {vlan} corresponde a: {resultado}\n")
        except ValueError:
            print(">> Error: debe ingresar un número entero válido.\n")

if __name__ == "__main__":
    main()