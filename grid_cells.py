import random

class GridCells:
    #REQUIRED = {"depth", "wind", "waves"}
    REQUIRED = {"navigable"}
    def __init__(self, **kwds):
        self.dict = kwds
        if "name" in kwds:
            self.name = kwds["name"]

        for key in self.REQUIRED:
            if key not in kwds:
                raise ValueError(f"Missing required key: {key}")

    def set(self, key, value):
        self.dict[key] = value

    def get(self, key):
        return self.dict[key]

    def __contains__(self, item):
        return item in self.dict

    def save(self):
        return self.dict


def default():
    return GridCells(navigable=random.choice([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False]), default=True)






