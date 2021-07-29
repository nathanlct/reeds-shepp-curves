import unittest
from reeds_shepp import PathElement, Steering, Gear, path_length


class TestPathElement(unittest.TestCase):
    def setUp(self) -> None:
        self.element = PathElement(13, Steering.LEFT, Gear.FORWARD)

    def test_repr(self):
        self.assertEqual(
            repr(self.element),
            "{ Steering: LEFT	Gear: FORWARD	distance: 13 }"
        )

    def test_reverse_gear(self):
        self.element.reverse_gear()
        self.assertEqual(
            self.element.gear,
            Gear.BACKWARD
        )

    def test_reverse_steering(self):
        self.element.reverse_steering()
        self.assertEqual(
            self.element.steering,
            Steering.RIGHT
        )


class TestPathLength(unittest.TestCase):
    def test_with_positive_path_elements(self):
        path = [PathElement(1, Steering.LEFT, Gear.FORWARD) for _ in range(2)]
        self.assertEqual(
            path_length(path),
            2
        )


if __name__ == '__main__':
    unittest.main()
