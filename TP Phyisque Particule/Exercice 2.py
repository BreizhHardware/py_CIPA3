import matplotlib.pyplot as plt
import numpy as np

e = 1.602 * 10 ** (-19)  # C
m = 9.11 * 10 ** (-31)  # kg
V0 = 2 * 10 ** (7)  # m.s**(-1)
Ub = 1000  # V
d = 0.3  # m
L = 1  # m
dt = 10 ** (-9)  # s
E = Ub / d

list_vitesse = [0]

list_position = [0]
time_collision = None

list_real_position = [0]

for i in range(0, 1000):
    calcul = list_vitesse[len(list_vitesse) - 1] - (e * E * dt) / m
    new_pos = list_position[len(list_position) - 1] + calcul * dt
    if new_pos <= -0.15 and time_collision is None:
        time_collision = i * dt
    list_vitesse.append(calcul)
    list_position.append(new_pos)
    real_pos_calcul = 1 / 2 * ((e * E) / m) * ((i * dt) ** 2)
    list_real_position.append(-real_pos_calcul)
print(list_vitesse)
plt.plot(list_vitesse, label="E = Ub/d")
plt.title("Vitesse en fonction du temps")
plt.xlabel("Temps (ms)")
plt.ylabel("Vitesse (m/s)")
plt.legend()

plt.grid()
plt.show()

print(list_position)

plt.plot(list_position, label="Euler Method")
plt.title("Position en fonction du temps Y")
plt.xlabel("Temps (ms)")
plt.ylabel("Position (cm)")
plt.grid()
# Changer le label en x pour remplacer les 0 jusqu'à 1000 par 0 à 1000 * dt ( arrondir de 2 unités)
plt.xticks(np.arange(0, 1000, step=100))
plt.xticks(np.arange(0, 1000, step=100), np.arange(0, 1000 * dt, step=100 * dt))
# Arrondir les valeurs de l'axe des x à 2 décimales
plt.xticks(np.round(plt.xticks()[0], 1))
plt.xticks(rotation=45, ha="right")

print("L'électron va toucher la plaque après", time_collision, "s")

print(list_real_position)

plt.plot(list_real_position, label="Real Position")

plt.show()
