import numpy as np

class ElasticModulusAndVelocityCalculator:
    def __init__(self, c11, c12, c44, rho):
        """
        Initialize the class with individual elastic constants and density.
        c11: Individual C11 elastic constant value (GPa)
        c12: Individual C12 elastic constant value (GPa)
        c44: Individual C44 elastic constant value (GPa)
        rho: Individual density value (g/cm³)
        """
        self.c11 = c11
        self.c12 = c12
        self.c44 = c44
        self.rho = rho

    def compute_modulus_and_velocity(self):
        """
        Calculate the elastic moduli and wave velocities for a single data point.
        Returns: B, G, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r
        """
        # 6x6 elastic constant matrix
        C = np.zeros((6, 6))
        C[0:3, 0:3] = np.array([[self.c11, self.c12, self.c12],
                                [self.c12, self.c11, self.c12],
                                [self.c12, self.c12, self.c11]])
        C[3:6, 3:6] = np.identity(3) * self.c44

        # Voigt average
        B_voigt = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
        G_voigt = ((C[0, 0] + C[1, 1] + C[2, 2]) - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15

        # Reuss average
        S = np.linalg.inv(C)  # Calculate the inverse of matrix C
        B_reuss = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
        G_reuss = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))

        # Hill average
        B_hill = 0.5 * (B_voigt + B_reuss)
        G_hill = 0.5 * (G_voigt + G_reuss)

        # Calculate wave velocities (unit: km/s)
        Vp_h = np.sqrt((B_hill + 4 / 3 * G_hill) * 1e9 / (self.rho * 1000)) / 1000  # Voigt-Reuss-Hill average
        Vs_h = np.sqrt(G_hill * 1e9 / (self.rho * 1000)) / 1000
        Vp_v = np.sqrt((B_voigt + 4 / 3 * G_voigt) * 1e9 / (self.rho * 1000)) / 1000  # Voigt average
        Vs_v = np.sqrt(G_voigt * 1e9 / (self.rho * 1000)) / 1000
        Vp_r = np.sqrt((B_reuss + 4 / 3 * G_reuss) * 1e9 / (self.rho * 1000)) / 1000  # Reuss average
        Vs_r = np.sqrt(G_reuss * 1e9 / (self.rho * 1000)) / 1000

        return B_hill, G_hill, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r

