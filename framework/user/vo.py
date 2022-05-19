class WalletVo:
    def __init__(self, address, passphrase):
        self.passphrase = passphrase
        for key in address:
            setattr(self, key, address[key])

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)

        except AttributeError:
            value = "Empty"
            setattr(self, name, value)
            return value
