import random

def adivina(intentos):
    numero_secreto = random.randint(0, 100)
    print(numero_secreto)
    intento_actual = 0

    while intento_actual < intentos:
        entrada = input(f"Intento {intento_actual + 1}/{intentos} - Adiviná el número (0-100): ")
        try:
            numero = int(entrada)
        except ValueError:
            print("Entrada inválida. Por favor, ingresá un número.")
            continue  # NO cuenta como intento

        intento_actual += 1  # Solo se incrementa si la entrada fue válida

        if numero == numero_secreto:
            print(f"¡Adivinaste! El número era {numero_secreto}. Lo lograste en {intento_actual} intentos.")
            return
        elif numero < numero_secreto:
            print("Demasiado bajo.")
        else:
            print("Demasiado alto.")

    print(f"Se terminaron los intentos. El número era {numero_secreto}.")

# Ejecutar el juego
if __name__ == "__main__":
    intentos = 5
    adivina(intentos)
