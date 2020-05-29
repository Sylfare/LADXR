from locations.items import *


class OR(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "or%s" % (super().__repr__())


class AND(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "and%s" % (super().__repr__())


class COUNT:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def __eq__(self, other):
        return other.item == self.item and other.amount == self.amount

    def __hash__(self):
        return hash((self.item, self.amount))

    def __repr__(self):
        return "<%dx%s>" % (self.amount, self.item)


def hasConsumableRequirement(requirements):
    if isinstance(requirements, list) or isinstance(requirements, tuple):
        return any(map(hasConsumableRequirement, requirements))
    if isinstance(requirements, COUNT):
        return isConsumable(requirements.item)
    return isConsumable(requirements)


def isConsumable(item):
    if item.startswith("RUPEES_"):
        return True
    if item.startswith("KEY") and len(item) == 4:
        return True
    return False


bush = OR(SWORD, MAGIC_POWDER, MAGIC_ROD, POWER_BRACELET)
attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG)
attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG)  # cannot kill skeletons with the fire rod
rear_attack = OR(SWORD, BOMB)
fire = OR(MAGIC_POWDER, MAGIC_ROD)


def flatten(req):
    result = set()
    if isinstance(req, OR):
        for r in req:
            for res in flatten(r):
                result.add(res)
    elif isinstance(req, AND):
        sets = []
        for r in req:
            sets.append(flatten(r))

        def _buildAND(target, r, idx):
            for s in sets[idx]:
                if idx < len(sets) - 1:
                    _buildAND(target, r.union(s), idx + 1)
                else:
                    target.add(frozenset(r.union(s)))
        _buildAND(result, set(), 0)
    else:
        result.add(frozenset((req,)))
    return result


def mergeFlat(req1, req2):
    result = req1.union(req2)
    result = set(filter(lambda s: all(map(lambda s2: not (s > s2), result)), result))
    return result


if __name__ == "__main__":
    req = AND("A", "B", "C")
    req = OR(req, "A")
    req = OR(req, "B")
    for res in mergeFlat(flatten(req), set()):
        print(">", res)
