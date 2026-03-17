"""Unit tests for Logic Engine."""
import unittest
import os
import tempfile
from task import TaskDatabase, Task


class TestTaskDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
    
    def tearDown(self):
        os.unlink(self.db_path)
    
    def test_add_task(self):
        with TaskDatabase(self.db_path) as db:
            task = db.add_task("Test Task", "Test description")
            self.assertIsNotNone(task.id)
            self.assertEqual(task.title, "Test Task")
            self.assertEqual(task.status, "pending")
    
    def test_get_all_tasks(self):
        with TaskDatabase(self.db_path) as db:
            db.add_task("Task 1")
            db.add_task("Task 2")
            tasks = db.get_all_tasks()
            self.assertEqual(len(tasks), 2)
    
    def test_update_status(self):
        with TaskDatabase(self.db_path) as db:
            task = db.add_task("Task")
            self.assertTrue(db.update_status(task.id, "completed"))
            tasks = db.get_all_tasks()
            self.assertEqual(tasks[0].status, "completed")
    
    def test_delete_task(self):
        with TaskDatabase(self.db_path) as db:
            task = db.add_task("Task")
            self.assertTrue(db.delete_task(task.id))
            tasks = db.get_all_tasks()
            self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()