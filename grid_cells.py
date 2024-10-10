class GridCells:
    REQUIRED = {"depth", "value", "wind", "waves"}

    def __init__(self, **kwds):
        self.dict = kwds
        if "name" in kwds:
            self.name = kwds["name"]
        for key in self.REQUIRED:
            if key not in self.dict:
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
    return GridCells(depth=-1, value=-1, wind=-1, waves=-1, default=True)





