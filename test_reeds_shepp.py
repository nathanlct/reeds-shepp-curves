import unittest
from reeds_shepp import PathElement, Steering, Gear, path_length, timeflip, reflect


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


class TestTimeflip(unittest.TestCase):
    def setUp(self) -> None:
        self.path = [PathElement(1, Steering.LEFT, g) for g in (Gear.FORWARD, Gear.BACKWARD)]
        self.timeflipped = timeflip(self.path)

    def test_it_flips_forward_backward(self):
        self.assertEqual(
            self.timeflipped[0].gear,
            Gear.BACKWARD
        )
        self.assertEqual(
            self.timeflipped[1].gear,
            Gear.FORWARD
        )

    def test_it_does_not_mutate_original_path(self):
        self.assertEqual(
            self.path[0].gear,
            Gear.FORWARD,
        )


class TestReflect(unittest.TestCase):
    def setUp(self) -> None:
        self.path = [PathElement(1, s, Gear.FORWARD) for s in (Steering.LEFT, Steering.STRAIGHT, Steering.RIGHT)]
        self.reflected = reflect(self.path)

    def test_it_reflects_steering(self):
        self.assertEqual(
            self.reflected[0].steering,
            Steering.RIGHT
        )
        self.assertEqual(
            self.reflected[1].steering,
            Steering.STRAIGHT
        )
        self.assertEqual(
            self.reflected[2].steering,
            Steering.LEFT
        )

    def test_it_does_not_mutate_original_path(self):
        self.assertEqual(
            self.path[0].steering,
            Steering.LEFT,
        )



if __name__ == '__main__':
    unittest.main()
