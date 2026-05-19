
## 5. Пример тестов (`tests/test_training.py`)

```python
import unittest
import json
import os
from datetime import datetime

class TestTrainingPlanner(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_file = "test_trainings.json"
        self.test_data = [
            {"date": "2024-12-20", "type": "Бег", "duration": 30},
            {"date": "2024-12-21", "type": "Плавание", "duration": 45}
        ]
    
    def test_date_validation(self):
        """Тест проверки формата даты"""
        def validate_date(date_string):
            try:
                datetime.strptime(date_string, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_date("2024-12-25"))
        self.assertFalse(validate_date("25.12.2024"))
        self.assertFalse(validate_date("2024-13-45"))
    
    def test_duration_validation(self):
        """Тест проверки длительности"""
        def validate_duration(duration):
            try:
                d = int(duration)
                return d > 0
            except:
                return False
        
        self.assertTrue(validate_duration("30"))
        self.assertFalse(validate_duration("-10"))
        self.assertFalse(validate_duration("0"))
        self.assertFalse(validate_duration("abc"))
    
    def test_filter_by_type(self):
        """Тест фильтрации по типу"""
        filter_type = "Бег"
        filtered = [t for t in self.test_data if t["type"] == filter_type]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
    
    def test_filter_by_date(self):
        """Тест фильтрации по дате"""
        filter_date = "2024-12-20"
        filtered = [t for t in self.test_data if t["date"] == filter_date]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["date"], "2024-12-20")
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки JSON"""
        # Сохранение
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f, indent=4, ensure_ascii=False)
        
        # Загрузка
        with open(self.test_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, self.test_data)
        
        # Очистка
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()


