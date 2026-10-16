# Generated with an llm from the practice slides
import unittest
import math
import numpy as np

from zpgso_graphics_project.modules.vec4 import Vec4
from zpgso_graphics_project.modules.mat4 import Mat4

from zpgso_graphics_project.modules.transformation_matrices import (
    get_identity_matrix,
    get_rotation_z_axis_matrix,
    get_rotation_y_axis_matrix,
    get_rotation_x_axis_matrix,
    get_translation_matrix,
    get_scaling_matrix,
    get_camera_transformation_matrix,
    get_orthographic_transformation_matrix,
    get_pixel_transformation_matrix,
    combine_transformation_matrices,
)


class TestTransformationMatrices(unittest.TestCase):

    def assertVec4Equal(self, actual, expected):
        """Compare two Vec4 objects with floating-point tolerance."""
        np.testing.assert_allclose(
            actual._vector,
            np.array(expected, dtype=float),
            rtol=1e-7,
            atol=1e-7
        )

    def assertMat4Equal(self, actual, expected):
        """Compare two Mat4 objects with floating-point tolerance."""
        np.testing.assert_allclose(
            actual._matrix,
            np.array(expected, dtype=float),
            rtol=1e-7,
            atol=1e-7
        )

    # ------------------------------------------------------------------
    # 1. T(1,2,3) * S(2)
    # ------------------------------------------------------------------

    def test_translation_times_scaling(self):
        """
        M = T(1,2,3) * S(2)

        Expected:
        [2 0 0 1]
        [0 2 0 2]
        [0 0 2 3]
        [0 0 0 1]
        """
        translation = get_translation_matrix(1, 2, 3)
        scaling = get_scaling_matrix(2, 2, 2)

        result = translation * scaling

        expected = [
            [2, 0, 0, 1],
            [0, 2, 0, 2],
            [0, 0, 2, 3],
            [0, 0, 0, 1],
        ]

        self.assertMat4Equal(result, expected)

    # ------------------------------------------------------------------
    # 1b. I*M and M*I both equal M
    # ------------------------------------------------------------------

    def test_identity_times_matrix(self):
        identity = get_identity_matrix()

        matrix = (
            get_translation_matrix(1, 2, 3)
            * get_scaling_matrix(2, 2, 2)
        )

        result = identity * matrix

        self.assertMat4Equal(result, matrix._matrix)

    def test_matrix_times_identity(self):
        identity = get_identity_matrix()

        matrix = (
            get_translation_matrix(1, 2, 3)
            * get_scaling_matrix(2, 2, 2)
        )

        result = matrix * identity

        self.assertMat4Equal(result, matrix._matrix)

    # ------------------------------------------------------------------
    # 2. T(1,2,3) * (0,0,0,1)
    # ------------------------------------------------------------------

    def test_translation_of_origin(self):
        """
        T(1,2,3) * (0,0,0,1)
        =
        (1,2,3,1)
        """
        translation = get_translation_matrix(1, 2, 3)
        point = Vec4(0, 0, 0, 1)

        result = translation * point

        self.assertVec4Equal(
            result,
            [1, 2, 3, 1]
        )

    # ------------------------------------------------------------------
    # 3. T(1,2,3) * (1,0,0,0)
    # ------------------------------------------------------------------

    def test_translation_does_not_affect_vector_with_w_zero(self):
        """
        A vector with w=0 represents a direction/vector rather than
        a point, so translation must not affect it.

        T(1,2,3) * (1,0,0,0)
        =
        (1,0,0,0)
        """
        translation = get_translation_matrix(1, 2, 3)
        vector = Vec4(1, 0, 0, 0)

        result = translation * vector

        self.assertVec4Equal(
            result,
            [1, 0, 0, 0]
        )

    # ------------------------------------------------------------------
    # 4. S(2) * (1,2,3,1)
    # ------------------------------------------------------------------

    def test_scaling_point(self):
        """
        S(2) * (1,2,3,1)
        =
        (2,4,6,1)
        """
        scaling = get_scaling_matrix(2, 2, 2)
        point = Vec4(1, 2, 3, 1)

        result = scaling * point

        self.assertVec4Equal(
            result,
            [2, 4, 6, 1]
        )

    # ------------------------------------------------------------------
    # 5. Rz(pi/2) * (1,0,0,1)
    # ------------------------------------------------------------------

    def test_rotation_z_axis(self):
        """
        Rz(pi/2) * (1,0,0,1)
        =
        (0,1,0,1)
        """
        rotation = get_rotation_z_axis_matrix(math.pi / 2)
        point = Vec4(1, 0, 0, 1)

        result = rotation * point

        self.assertVec4Equal(
            result,
            [0, 1, 0, 1]
        )

    # ------------------------------------------------------------------
    # 6a. Rx(pi/2) * (0,1,0,1)
    # ------------------------------------------------------------------

    def test_rotation_x_axis(self):
        """
        Rx(pi/2) * (0,1,0,1)
        =
        (0,0,1,1)
        """
        rotation = get_rotation_x_axis_matrix(math.pi / 2)
        point = Vec4(0, 1, 0, 1)

        result = rotation * point

        self.assertVec4Equal(
            result,
            [0, 0, 1, 1]
        )

    # ------------------------------------------------------------------
    # 6b. Ry(pi/2) * (0,0,1,1)
    # ------------------------------------------------------------------

    def test_rotation_y_axis(self):
        """
        Ry(pi/2) * (0,0,1,1)
        =
        (1,0,0,1)
        """
        rotation = get_rotation_y_axis_matrix(math.pi / 2)
        point = Vec4(0, 0, 1, 1)

        result = rotation * point

        self.assertVec4Equal(
            result,
            [1, 0, 0, 1]
        )

    # ------------------------------------------------------------------
    # 7. Translate first:
    # Rz(pi/2) * T(2,0,0) * (0,0,0,1)
    # ------------------------------------------------------------------

    def test_translate_then_rotate(self):
        """
        Translation happens first, then rotation:

        Rz(pi/2) * T(2,0,0) * (0,0,0,1)
        =
        (0,2,0,1)
        """
        rotation = get_rotation_z_axis_matrix(math.pi / 2)
        translation = get_translation_matrix(2, 0, 0)

        point = Vec4(0, 0, 0, 1)

        result = rotation * translation * point

        self.assertVec4Equal(
            result,
            [0, 2, 0, 1]
        )

    # ------------------------------------------------------------------
    # 8. Rotate first:
    # T(2,0,0) * Rz(pi/2) * (1,0,0,1)
    # ------------------------------------------------------------------

    def test_rotate_then_translate(self):
        """
        Rotation happens first, then translation:

        T(2,0,0) * Rz(pi/2) * (1,0,0,1)
        =
        (2,1,0,1)
        """
        translation = get_translation_matrix(2, 0, 0)
        rotation = get_rotation_z_axis_matrix(math.pi / 2)

        point = Vec4(1, 0, 0, 1)

        result = translation * rotation * point

        self.assertVec4Equal(
            result,
            [2, 1, 0, 1]
        )

    # ------------------------------------------------------------------
    # combine_transformation_matrices
    # ------------------------------------------------------------------

    def test_combine_transformation_matrices(self):
        """
        combine_transformation_matrices([R, T])
        should produce R * T.
        """
        rotation = get_rotation_z_axis_matrix(math.pi / 2)
        translation = get_translation_matrix(2, 0, 0)

        result = combine_transformation_matrices([
            rotation,
            translation
        ])

        expected = rotation * translation

        self.assertMat4Equal(
            result,
            expected._matrix
        )

    def test_combine_transformation_matrices_order(self):
        """
        Verify that transformations are applied from right to left.

        [R, T] means:

            R * T * v

        so translation happens before rotation.
        """
        rotation = get_rotation_z_axis_matrix(math.pi / 2)
        translation = get_translation_matrix(2, 0, 0)

        point = Vec4(0, 0, 0, 1)

        matrix = combine_transformation_matrices([
            rotation,
            translation
        ])

        result = matrix * point

        self.assertVec4Equal(
            result,
            [0, 2, 0, 1]
        )


class TestSpecialTransformationMatrices(unittest.TestCase):

    def assertMat4Equal(self, actual, expected):
        np.testing.assert_allclose(
            actual._matrix,
            np.array(expected, dtype=float),
            rtol=1e-7,
            atol=1e-7
        )

    def assertVec4Equal(self, actual, expected):
        np.testing.assert_allclose(
            actual._vector,
            np.array(expected, dtype=float),
            rtol=1e-7,
            atol=1e-7
        )

    # ------------------------------------------------------------------
    # Camera transformation
    # ------------------------------------------------------------------

    def test_camera_transformation(self):
        camera = Vec4(1, 2, 3, 1)

        result = get_camera_transformation_matrix(camera)

        expected = [
            [1, 0, 0, -1],
            [0, 1, 0, -2],
            [0, 0, 1, -3],
            [0, 0, 0, 1],
        ]

        self.assertMat4Equal(result, expected)

    def test_camera_transformation_moves_point_to_camera_origin(self):
        camera = Vec4(1, 2, 3, 1)

        matrix = get_camera_transformation_matrix(camera)

        result = matrix * camera

        self.assertVec4Equal(
            result,
            [0, 0, 0, 1]
        )

    # ------------------------------------------------------------------
    # Orthographic transformation
    # ------------------------------------------------------------------

    def test_orthographic_transformation(self):
        result = get_orthographic_transformation_matrix(
            -1, 1, 1, -1
        )

        expected = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ]

        self.assertMat4Equal(result, expected)

    # ------------------------------------------------------------------
    # Pixel transformation
    # ------------------------------------------------------------------

    def test_pixel_transformation(self):
        result = get_pixel_transformation_matrix(800, 600)

        expected = [
            [400, 0, 0, 400],
            [0, -300, 0, 300],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]

        self.assertMat4Equal(result, expected)

    def test_pixel_transformation_origin(self):
        """
        The normalized coordinate (0,0,0,1) maps to the center
        of an 800x600 pixel viewport.
        """
        matrix = get_pixel_transformation_matrix(800, 600)

        result = matrix * Vec4(0, 0, 0, 1)

        self.assertVec4Equal(
            result,
            [400, 300, 0, 1]
        )


if __name__ == "__main__":
    unittest.main()
