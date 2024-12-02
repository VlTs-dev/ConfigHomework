import unittest
from src.visualizer import DependencyVisualizer



class TestDependencyVisualizer(unittest.TestCase):
    def test_transitive_dependencies(self):
        """Тест транзитивных зависимостей."""
        self.visualizer._build_dependency_graph("package1")
        self.assertIn("package1 --> com.example:lib1", self.visualizer.graph)
        self.assertIn("package1 --> com.example:lib2", self.visualizer.graph)
        self.assertIn("com.example:lib1 --> com.example:lib3", self.visualizer.graph)

    def setUp(self):
        self.visualizer = DependencyVisualizer("config.ini")

    def test_parse_pom(self):
        dependencies = self.visualizer._parse_pom("package1")
        self.assertEqual(dependencies, ["com.example:lib1", "com.example:lib2"])

    def test_build_dependency_graph(self):
        self.visualizer._build_dependency_graph("package1")
        self.assertIn(("package1", "com.example:lib1"), self.visualizer.graph_data)

    def test_generate_mermaid_graph(self):
        self.visualizer.graph_data = [("A", "B"), ("B", "C")]
        graph = self.visualizer._generate_mermaid_graph()
        self.assertIn("A --> B", graph)
        self.assertIn("B --> C", graph)


if __name__ == "__main__":
    unittest.main()
