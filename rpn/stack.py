class Stack(list):
    def push(self, item: any) -> None:
        self.append(item)

    def top(self) -> any:
        return self[-1] if len(self) > 0 else None

    def pop_top(self) -> any:
        return self.pop(-1)
