import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Constantes et paramètres
N = 1000
delta_x = 1 / N
delta_x2 = delta_x**2
D = 1
delta_t = 0.9 * (delta_x2 / 2 * D)
T0 = 0
T1 = 0

if delta_t < (delta_x2 / 2 * D):
    M = np.zeros((N + 1, N + 1))

    # Remplissage de la matrice M
    for i in range(N + 1):
        if i == 0:
            M[i, i] = 1 - 2 * delta_t * D / delta_x2
            M[i, i + 1] = delta_t * D / delta_x2
        elif i == N:
            M[i, i - 1] = delta_t * D / delta_x2
            M[i, i] = 1 - 2 * delta_t * D / delta_x2
        else:
            M[i, i - 1] = delta_t * D / delta_x2
            M[i, i] = 1 - 2 * delta_t * D / delta_x2
            M[i, i + 1] = delta_t * D / delta_x2

    # Vecteur spatial pour tracer
    x = np.linspace(0, 1, N + 1)

    # Condition initiale T₀(x) = sin(πx)
    T = np.sin(np.pi * x)
    T[0] = T0
    T[N] = T1

    # Temps de simulation
    temps_final = 0.1
    nb_iterations = int(temps_final / delta_t)

    # Nombre de courbes souhaité
    nb_courbes = 100000

    # Sauvegarder plus de profils à différents temps
    profils = [T.copy()]
    iterations_sauvegarde = np.linspace(0, nb_iterations, nb_courbes, dtype=int)
    temps_sauvegarde = [0] + [i * delta_t for i in iterations_sauvegarde[1:]]

    # Simulation de l'évolution temporelle
    for n in range(nb_iterations):
        T = M @ T
        if n in iterations_sauvegarde:
            profils.append(T.copy())

    # Tracer les profils de température avec un dégradé de couleurs
    plt.figure(figsize=(12, 8))
    colormap = cm.viridis

    # Affichage des courbes avec un dégradé de couleurs
    for i, t in enumerate(temps_sauvegarde):
        if i < len(profils):
            couleur = colormap(i / len(temps_sauvegarde))
            plt.plot(x, profils[i], color=couleur, alpha=0.7)

    # Afficher seulement quelques légendes pour éviter l'encombrement
    indices_legende = np.linspace(0, len(temps_sauvegarde) - 1, 10, dtype=int)
    for i in indices_legende:
        if i < len(profils):
            couleur = colormap(i / len(temps_sauvegarde))
            plt.plot([], [], color=couleur, label=f"t = {temps_sauvegarde[i]:.4f}s")

    plt.xlabel("Position x")
    plt.ylabel("Température T")
    plt.title("Évolution de la température au cours du temps (50 courbes)")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.colorbar(plt.cm.ScalarMappable(cmap=colormap), label="Temps (s)", ax=plt.gca())
    plt.show()
else:
    print("Constante incorrect")
    print(f"delta_t = {delta_t}")
    print(f"(delta_x2 / 2 * D) = {(delta_x2 / 2 * D)}")
