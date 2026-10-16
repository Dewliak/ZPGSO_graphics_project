#Generated vy llm from excercise slides
import unittest
import tempfile
import os
import numpy as np

from zpgso_graphics_project.modules.vec4 import Vec4
from zpgso_graphics_project.modules.loader import load_obj_file


class TestObjLoader(unittest.TestCase):

    def create_obj_file(self, content):
        file = tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".obj"
        )
        file.write(content)
        file.close()
        return file.name

    def test_load_triangle(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            f 1 2 3
            """
        )

        try:
            vertices, faces = load_obj_file(filename)

            self.assertEqual(len(vertices), 3)
            self.assertEqual(len(faces), 1)

            self.assertEqual(faces[0], (0, 1, 2))

            np.testing.assert_allclose(
                vertices[0]._vector,
                [0, 0, 0, 1]
            )

            np.testing.assert_allclose(
                vertices[1]._vector,
                [1, 0, 0, 1]
            )

            np.testing.assert_allclose(
                vertices[2]._vector,
                [0, 1, 0, 1]
            )

        finally:
            os.unlink(filename)

    def test_ignore_comments_empty_lines_vt_and_vn(self):
        filename = self.create_obj_file(
            """
            # this is a comment

            v 0 0 0
            vt 0 0
            vn 0 0 1

            v 1 0 0
            v 0 1 0

            # another comment
            f 1 2 3
            """
        )

        try:
            vertices, faces = load_obj_file(filename)

            self.assertEqual(len(vertices), 3)
            self.assertEqual(len(faces), 1)
            self.assertEqual(faces[0], (0, 1, 2))

        finally:
            os.unlink(filename)

    def test_vertex_has_w_equal_to_one(self):
        filename = self.create_obj_file(
            "v 1.5 2.5 3.5\n"
        )

        try:
            vertices, faces = load_obj_file(filename)

            self.assertEqual(len(vertices), 1)

            np.testing.assert_allclose(
                vertices[0]._vector,
                [1.5, 2.5, 3.5, 1]
            )

        finally:
            os.unlink(filename)

    def test_face_indices_are_zero_based(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            f 1 2 3
            """
        )

        try:
            vertices, faces = load_obj_file(filename)

            self.assertEqual(
                faces,
                [(0, 1, 2)]
            )

        finally:
            os.unlink(filename)

  
    def test_face_uses_first_three_indices(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            v 1 1 0
            f 1 2 3 4
            """
        )

        try:
            vertices, faces = load_obj_file(filename)

            self.assertEqual(
                faces,
                [(0, 1, 2)]
            )

        finally:
            os.unlink(filename)

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            load_obj_file("this_file_does_not_exist.obj")

    def test_invalid_vertex_number(self):
        filename = self.create_obj_file(
            """
            v 0 hello 0
            """
        )

        try:
            with self.assertRaises(ValueError):
                load_obj_file(filename)

        finally:
            os.unlink(filename)

    def test_invalid_face_number(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            f 1 hello 3
            """
        )

        try:
            with self.assertRaises(ValueError):
                load_obj_file(filename)

        finally:
            os.unlink(filename)

    def test_face_index_out_of_range(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            f 1 2 10
            """
        )

        try:
            with self.assertRaises(ValueError):
                load_obj_file(filename)

        finally:
            os.unlink(filename)

    def test_zero_face_index(self):
        filename = self.create_obj_file(
            """
            v 0 0 0
            v 1 0 0
            v 0 1 0
            f 0 2 3
            """
        )

        try:
            with self.assertRaises(ValueError):
                load_obj_file(filename)

        finally:
            os.unlink(filename)


if __name__ == "__main__":
    unittest.main()
