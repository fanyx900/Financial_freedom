class LeverageManager:
    def __init__(self, algo, default_leverage=1.0):
        """
        Inițializează managerul de levier.

        :param algo: Instanța algoritmului QCAlgorithm.
        :param default_leverage: Levierul implicit.
        """
        self.algo = algo
        self.default_leverage = default_leverage

    def set_leverage(self, symbol, leverage=None):
        """
        Setează levierul pentru un anumit simbol.

        :param symbol: Simbolul pentru care se setează levierul.
        :param leverage: Valoarea levierului. Dacă nu este specificat, se va folosi levierul implicit.
        """
        if leverage is None:
            leverage = self.default_leverage

        self.algo.Securities[symbol].SetLeverage(leverage)

    def get_leverage(self, symbol):
        """
        Obține levierul curent pentru un anumit simbol.

        :param symbol: Simbolul pentru care se obține levierul.
        :return: Valoarea levierului.
        """
        return self.algo.Securities[symbol].Leverage

    def reset_leverage(self, symbol):
        """
        Resetează levierul pentru un anumit simbol la valoarea implicită.

        :param symbol: Simbolul pentru care se resetează levierul.
        """
        self.set_leverage(symbol, self.default_leverage)
