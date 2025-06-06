class WrapVar[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    async def __call__(self) -> T:
        return self.value
