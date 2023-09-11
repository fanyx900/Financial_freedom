import os

class ConfigLoader:

    @staticmethod
    def load_config():
        config = {
            "API_KEY": os.environ.get("BINANCE_API_KEY"),
            "API_SECRET": os.environ.get("BINANCE_API_SECRET")
        }
        return config
