class Stack(list):
    def push(self, item: any) -> None:
        self.append(item)

    def top(self) -> any:
        return self[-1] if len(self) else None
