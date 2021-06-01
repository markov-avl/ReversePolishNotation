class Stack(list):
    def push(self, item: any) -> None:
        self.append(item)

    def top(self) -> any:
        return self[-1]

    def pop_top(self) -> any:
        return self.pop(-1)
