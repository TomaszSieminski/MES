class ShapeFunctionDerivatives:
    @staticmethod
    def dN1_dKsi(eta):
        return -1 / 4 * (1 - eta)

    @staticmethod
    def dN2_dKsi(eta):
        return 1 / 4 * (1 - eta)

    @staticmethod
    def dN3_dKsi(eta):
        return 1 / 4 * (1 + eta)

    @staticmethod
    def dN4_dKsi(eta):
        return -1 / 4 * (1 + eta)

    @staticmethod
    def dN1_dEta(ksi):
        return -1 / 4 * (1 - ksi)

    @staticmethod
    def dN2_dEta(ksi):
        return -1 / 4 * (1 + ksi)

    @staticmethod
    def dN3_dEta(ksi):
        return 1 / 4 * (1 + ksi)

    @staticmethod
    def dN4_dEta(ksi):
        return 1 / 4 * (1 - ksi)