class MockId:
    def __init__(self, desc_value="__DESC__") -> None:
        self.desc_value = desc_value
        self.desc_called = 0

    def desc(self):
        self.desc_called += 1
        return self.desc_value
