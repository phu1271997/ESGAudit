# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class Contract(gl.Contract):
    """
    Sanity check contract to verify GenLayer Studio deployment and basic storage operations.
    """
    counter: u256
    test_map: TreeMap[str, u256]

    def __init__(self):
        # Rule #2: DO NOT reassign TreeMap or DynArray in __init__ (no self.test_map = TreeMap())
        self.counter = u256(0)

    @gl.public.write
    def increment(self) -> None:
        """
        Increments the global counter by 1.
        """
        self.counter += u256(1)

    @gl.public.write
    def set_map_value(self, key: str, value: int) -> None:
        """
        Sets a value in the TreeMap for a given key.
        Rule #3 & #4: Float is prohibited in public method signatures. We use `int`.
        """
        self.test_map[key] = u256(value)

    @gl.public.view
    def get_count(self) -> u256:
        """
        Returns the current global counter value.
        """
        return self.counter

    @gl.public.view
    def get_map_value(self, key: str) -> u256:
        """
        Returns the value in the TreeMap for a given key.
        """
        if key in self.test_map:
            return self.test_map[key]
        return u256(0)
