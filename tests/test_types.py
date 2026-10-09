
import unittest
import numpy as np

from modules.vec4 import Vec4
from modules.mat4 import Mat4


class TestVec4(unittest.TestCase):

    def test_constructor_and_indexing(self):
        v = Vec4(1, 2, 3, 4)

        for i, expected in enumerate([1, 2, 3, 4]):
            self.assertEqual(v[i], expected)

    def test_default_w(self):
        v = Vec4(1, 2, 3)

        self.assertEqual(v[3], 1.0)

    def test_negative_indexing(self):
        v = Vec4(1, 2, 3, 4)

        self.assertEqual(v[-1], 4)
        self.assertEqual(v[-2], 3)

    def test_values_are_floats(self):
        v = Vec4(1, 2, 3, 4)

        for i in range(4):
            self.assertIsInstance(v[i], (float, np.floating))

    def test_out_of_range_index(self):
        v = Vec4(1, 2, 3, 4)

        with self.assertRaises(IndexError):
            _ = v[4]

    def test_repr(self):
        v = Vec4(1, 2, 3, 4)

        self.assertEqual(repr(v), "Vec4(1.00, 2.00, 3.00, 4.00)")


class TestMat4(unittest.TestCase):

    def setUp(self):
        self.matrix = Mat4(
            Vec4(1, 2, 3, 4),
            Vec4(5, 6, 7, 8),
            Vec4(9, 10, 11, 12),
            Vec4(13, 14, 15, 16),
        )

    def test_constructor(self):
        expected = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ], dtype=float)

        np.testing.assert_array_equal(
            self.matrix._matrix, expected
        )

        self.assertEqual(self.matrix._matrix.shape, (4, 4))

    def test_matrix_vector_multiplication(self):
        v = Vec4(1, 2, 3, 4)

        result = self.matrix * v

        self.assertIsInstance(result, Vec4)
        np.testing.assert_allclose(
            result._vector,
            np.array([30, 70, 110, 150])
        )

    def test_identity_matrix(self):
        identity = Mat4(
            Vec4(1, 0, 0, 0),
            Vec4(0, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )
        v = Vec4(2, 3, 4, 1)

        result = identity * v

        np.testing.assert_allclose(
            result._vector, v._vector
        )

    def test_zero_matrix(self):
        zero = Mat4(
            Vec4(0, 0, 0, 0),
            Vec4(0, 0, 0, 0),
            Vec4(0, 0, 0, 0),
            Vec4(0, 0, 0, 0),
        )

        result = zero * Vec4(2, 3, 4, 1)

        np.testing.assert_allclose(
            result._vector, np.zeros(4)
        )

    def test_matrix_matrix_multiplication(self):
        identity = Mat4(
            Vec4(1, 0, 0, 0),
            Vec4(0, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )

        result = identity * self.matrix

        self.assertIsInstance(result, Mat4)
        np.testing.assert_allclose(
            result._matrix, self.matrix._matrix
        )

    def test_matrix_multiplication_is_not_commutative(self):
        a = Mat4(
            Vec4(1, 2, 0, 0),
            Vec4(0, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )

        b = Mat4(
            Vec4(1, 0, 0, 0),
            Vec4(3, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )

        ab = (a * b)._matrix
        ba = (b * a)._matrix

        self.assertFalse(np.allclose(ab, ba))

    def test_matrix_multiplication_known_result(self):
        a = Mat4(
            Vec4(1, 2, 0, 0),
            Vec4(0, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )

        b = Mat4(
            Vec4(1, 0, 0, 0),
            Vec4(3, 1, 0, 0),
            Vec4(0, 0, 1, 0),
            Vec4(0, 0, 0, 1),
        )

        result = a * b

        expected = np.array([
            [7, 2, 0, 0],
            [3, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype=float)

        np.testing.assert_allclose(
            result._matrix, expected
        )


if __name__ == "__main__":
    unittest.main()

