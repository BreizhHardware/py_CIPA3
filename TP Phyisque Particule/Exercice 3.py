import matplotlib.pyplot as plt
import numpy as np

# Constantes physiques et paramètres
e = 1.602 * 10 ** (-19)  # C
m = 9.11 * 10 ** (-31)  # kg
V0x = 2 * 10**7  # m/s
V0y = 0  # m/s
B = 1 * 10 ** (-3)  # T (1 mT)
Dt = 10 ** (-9)  # s
q = 1.602 * 10 ** (-19)  # C

# Initialisation des listes pour stocker les valeurs
vitesse_y = [V0y]
vitesse_x = [V0x]
temps = [0]
position_x = [0]
position_y = [0]

n = 30

# Calcul des vitesses et positions
for j in range(1, n):
    vitesse_y_var = vitesse_y[j - 1] - Dt * ((q * B) / m) * vitesse_x[j - 1]
    vitesse_x_var = vitesse_x[j - 1] + Dt * ((q * B) / m) * vitesse_y[j - 1]
    nv_temps = Dt * j
    temps.append(nv_temps)
    vitesse_x.append(vitesse_x_var)
    vitesse_y.append(vitesse_y_var)

    position_x_var = position_x[j - 1] + Dt * vitesse_x[j - 1]
    position_y_var = position_y[j - 1] + Dt * vitesse_y[j - 1]
    position_x.append(position_x_var)
    position_y.append(position_y_var)

# Calcul des positions exactes
omega = q * B / m
R = m * V0x / (q * B)
position_x_exact = [R * np.sin(omega * t) for t in temps]
position_y_exact = [R * (1 - np.cos(omega * t)) for t in temps]

# Tracé de la trajectoire
plt.figure(figsize=(10, 6))
plt.plot(position_x, position_y, label="Trajectoire numérique", color="blue")
plt.plot(
    position_x_exact,
    position_y_exact,
    label="Trajectoire exacte",
    color="red",
    linestyle="--",
)
plt.xlabel("Position x (m)")
plt.ylabel("Position y (m)")
plt.title("Trajectoire de l'électron dans un champ magnétique")
plt.legend()
plt.grid(True)
plt.axis("equal")  # Pour garder les mêmes échelles sur les axes x et y
plt.show()

# Affichage des résultats
print("Vitesse y:", vitesse_y)
print("Vitesse x:", vitesse_x)
print("Position x:", position_x)
print("Position y:", position_y)
