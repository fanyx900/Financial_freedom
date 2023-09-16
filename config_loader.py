import os

class ConfigLoader:

    @staticmethod
    def load_config():
        api_key = os.environ.get("BINANCE_API_KEY")
        api_secret = os.environ.get("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise EnvironmentError("Variabilele de mediu BINANCE_API_KEY și BINANCE_API_SECRET trebuie să fie setate.")

        config = {
            "API_KEY": api_key,
            "API_SECRET": api_secret
        }
        return config
