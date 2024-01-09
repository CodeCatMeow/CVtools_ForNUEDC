"跳变检测"


class Hop:
    def __init__(self, beginning=False) -> None:
        self.old = beginning

    def ifRise(self, this: bool) -> bool:
        "检测是否产生上升沿"
        if this ^ self.old:
            self.old = this
            if this:
                return True
            else:
                return False
        else:
            return False

    def ifFall(self, this: bool) -> bool:
        "检测是否产生上升沿"
        if this ^ self.old:
            self.old = this
            if this:
                return False
            else:
                return True
        else:
            return False
