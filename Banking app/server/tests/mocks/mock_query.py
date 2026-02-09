class MockQuery:
    def __init__(self, items) -> None:
        self._items = items
        self.order_by_called = 0
        self.last_order_by_arg = None

    def order_by(self, arg):
        self.order_by_called += 1
        self.last_order_by_arg = arg
        return self

    def all(self):
        return self._items
