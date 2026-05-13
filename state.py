import charactor


class State:
    active_charactor: charactor.Charactor
    isActive: bool = False
    target_charactor = charactor.Charactor
    isTargeting: bool = False

    def __init__(self):
        pass
