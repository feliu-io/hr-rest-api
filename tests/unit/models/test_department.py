from unittest import TestCase

from models.department import DepartmentModel


class TestDepartment(TestCase):
    """Unit tests for the DepartmentModel."""

    def test_init(self):
        """Test the __init__ method of the DepartmentModel class."""
        self.d = DepartmentModel('test_d', 1, True)

        self.assertEqual(self.d.department_name, 'test_d')
        self.assertEqual(self.d.organization_id, 1)
