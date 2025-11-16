from utils import validar_entero_menu
from auth import registro_usuario, inicio_sesion
from game import jugar


def menu_principal():
    menu = (
        "\n--- CulturaMundo ---\n"
        "1. Registrar nuevo usuario\n"
        "2. Iniciar sesión\n"
        "3. Salir\n"
    )
    return validar_entero_menu(menu, "Seleccione una opción (1-3): ", 1, 3)


def main():
    main_iniciado = True
    sesion = False
    
    while main_iniciado:
        opcion = menu_principal()
        
        match opcion:
            case 1:
                registro_usuario()
            case 2:
                sesion = inicio_sesion()
                if sesion:
                    main_iniciado = False
            case 3:
                main_iniciado = False
        
        if sesion:
            jugar()
        else:
            print("Fin del juego. ¡Vuelve pronto!")


if __name__ == "__main__":
    main()