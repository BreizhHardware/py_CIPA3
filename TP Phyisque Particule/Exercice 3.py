import matplotlib.pyplot as plt
import numpy as np

# Constantes physiques et paramètres
e = 1.602 * 10 ** (-19)  # C
m = 9.11 * 10 ** (-31)  # kg
V0 = 2 * 10 ** (7)  # m/s
B = 1 * 10 ** (-3)  # T (1 mT)
dt = 10 ** (-9)  # s

# Initialisation des listes pour stocker les valeurs
list_vx = [V0]
list_vy = [0]
list_x = [0]
list_y = [0]

# Calcul des vitesses et positions
for i in range(1000):
    # Mise à jour des vitesses selon la force de Lorentz
    list_vx.append(list_vx[-1] + (e * B / m) * list_vy[-1] * dt)
    list_vy.append(list_vy[-1] - (e * B / m) * list_vx[-1] * dt)

    # Mise à jour des positions
    list_x.append(list_x[-1] + list_vx[-1] * dt)
    list_y.append(list_y[-1] + list_vy[-1] * dt)

# Tracé de la trajectoire
plt.figure(figsize=(10, 6))
plt.plot(list_x, list_y, label="Trajectoire de l'électron", color="blue")
plt.xlabel("Position x (m)")
plt.ylabel("Position y (m)")
plt.title("Trajectoire de l'électron dans un champ magnétique")
plt.legend()
plt.grid(True)
plt.axis("equal")  # Pour garder les mêmes échelles sur les axes x et y
plt.show()

# Affichage des résultats
print("Vx:", list_vx)
print("Vy:", list_vy)
print("X:", list_x)
print("Y:", list_y)
