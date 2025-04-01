# Eq en régime permanent
# d2T / dx2 = 0
# T(x =0) = T0
# T(x = 1) = T1
# T(i)i E [0, N+1]
# x(i+1) - x(i) = deltaX = 1/N
# d2T/dx2 = (T(i-1) - 2*T(i) + T(i+1))/deltaX**2

# Question 1: Résoudre cette équation pour les conditions aux bord
# d2T / dx2 => dT / dx = A => T(x) = Ax + b
# Ici b = T0 d'où T(x) = Ax + T0
# T1 - T0 / 1 - 0 = A = T1 - T0 donc T(x) = (T1 - T0)x + T0
# Question 2: Ecrire l'équation de la chaleur discrétisée pour i E [1, N-2], puis pour i = 0 et i = N
# d2T/dx2 = 0
# T(i+1) - 2*T(i) + T(i-1) = 0
# Pour i = 0
# -2T0 + T(1) = -T0-
# Pour i = N
