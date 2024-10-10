class GridValue:

    REQUIRED = {"depth", "value", "wind", "waves"}

    def __init__(self, **kwds):
        self.dict = kwds
        for key in self.REQUIRED:
            if key not in self.dict:
                raise ValueError(f"Missing required key: {key}")







g = GridValue(depth=3, value=5)

[
    [{"Depth": 0, "Value": 0}, {"Depth": 1, "Value": 1}, {"Depth": 2, "Value": 2}],
    [{"Depth": 0, "Value": 3}, {"Depth": 1, "Value": 4}, {"Depth": 2, "Value": 5}],
    [{"Depth": 0, "Value": 6}, {"Depth": 1, "Value": 7}, {"Depth": 2, "Value": 8}],
    [],
    []

]