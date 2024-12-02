# import configparser
# import os
# import subprocess
# import xml.etree.ElementTree as ET
# from pathlib import Path
# import sys
# sys.stdout.reconfigure(encoding='utf-8')
#
#
# class DependencyVisualizer:
#     def __init__(self, config_path: str):
#         # Загружаем конфигурацию из файла
#         self.config = self._load_config(config_path)
#         self.vis_tool_path = self.config['Paths']['visualization_tool']
#         self.output_path = self.config['Paths']['output_image']
#         self.package_name = self.config['Analysis']['package_name']
#         self.pom_root = Path(self.config['Analysis']['pom_root'])
#         self.graph_data = []  # Хранилище для графа зависимостей
#
#     def _load_config(self, config_path: str):
#         config = configparser.ConfigParser()
#         with open(config_path, 'r', encoding='utf-8') as f:
#             config.read_file(f)
#         # Отладочный вывод содержимого конфигурации
#
#         return config
#
#     def _parse_pom(self, package_name: str):
#         """Парсинг POM файла для извлечения зависимостей."""
#         pom_path = self.pom_root / package_name / "pom.xml"
#
#
#         if not pom_path.exists():
#             print(f"Предупреждение: POM файл не найден для {package_name}. Пропускаем...")
#             return []  # Возвращаем пустой список зависимостей
#
#         tree = ET.parse(pom_path)
#         root = tree.getroot()
#         namespace = {'m': 'http://maven.apache.org/POM/4.0.0'}
#         dependencies = root.findall('.//m:dependency', namespace)
#
#         result = []
#         for dep in dependencies:
#             group_id = dep.find('m:groupId', namespace).text
#             artifact_id = dep.find('m:artifactId', namespace).text
#             result.append(f"{group_id}:{artifact_id}")
#         return result
#
#     def _build_dependency_graph(self, package_name: str, visited=None):
#         """Рекурсивное построение графа зависимостей."""
#         if visited is None:
#             visited = set()
#         if package_name in visited:
#             return
#         visited.add(package_name)
#
#         dependencies = self._parse_pom(package_name)
#         for dependency in dependencies:
#             self.graph_data.append((package_name, dependency))
#             self._build_dependency_graph(dependency, visited)
#
#     def _generate_mermaid_graph(self):
#         """Генерация графа Mermaid."""
#         lines = ["graph TD"]
#         for parent, child in self.graph_data:
#             lines.append(f"  {parent} --> {child}")
#         return "\n".join(lines)
#
#     import os
#     import subprocess
#
#     def _save_graph_to_file(self, mermaid_data):
#         """Сохранение графа в PNG с помощью mmdc."""
#         mermaid_file = "graph.mmd"
#         with open(mermaid_file, "w") as file:
#             file.write(mermaid_data)
#
#         # Создать выходную папку, если её нет
#         os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
#
#         # Отладочный вывод
#         print(f"Использую инструмент визуализации: {self.vis_tool_path}")
#         print(f"Команда: {[self.vis_tool_path, '-i', mermaid_file, '-o', self.output_path]}")
#
#         # Выполнение команды
#         subprocess.run([self.vis_tool_path, "-i", mermaid_file, "-o", self.output_path], check=True)
#
#     def visualize(self):
#         """Основной процесс визуализации."""
#         self._build_dependency_graph(self.package_name)
#         mermaid_graph = self._generate_mermaid_graph()
#         self._save_graph_to_file(mermaid_graph)
#         print("Граф зависимостей успешно сохранён.")
#
#
# if __name__ == "__main__":
#     visualizer = DependencyVisualizer("config.ini")
#     visualizer.visualize()
import os
import subprocess
import configparser

class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.vis_tool_path = self.config.get("Paths", "visualization_tool")
        self.package_name = self.config.get("Analysis", "package_name")
        self.output_path = self.config.get("Paths", "output_path")
        self.graph = []

    def _load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        print("Содержимое config.ini:", dict(config))
        return config

    def _parse_pom(self, package_name):
        """Парсинг POM-файла для получения зависимостей."""
        # Заменяем ":" на "/" и "." на "_", чтобы найти путь к POM-файлу
        pom_path = os.path.join("pom_data", package_name.replace(":", os.sep).replace(".", "_"), "pom.xml")
        print(f"Ищу POM файл по пути: {pom_path}")

        if not os.path.exists(pom_path):
            print(f"Предупреждение: POM файл не найден для {package_name}. Пропускаем...")
            return []

        dependencies = []
        with open(pom_path, "r") as f:
            for line in f:
                if "<dependency>" in line:
                    dep = line.strip().replace("<dependency>", "").replace("</dependency>", "")
                    dependencies.append(dep)

        return dependencies

    def _build_dependency_graph(self, package_name, visited=None):
        """Рекурсивное построение графа зависимостей, включая транзитивные."""
        if visited is None:
            visited = set()  # Множество для отслеживания посещённых пакетов

        if package_name in visited:
            return  # Избегаем циклов в зависимостях

        visited.add(package_name)  # Помечаем пакет как посещённый

        # Получаем зависимости из POM-файла
        dependencies = self._parse_pom(package_name)

        # Добавляем связи в граф
        for dependency in dependencies:
            self.graph.append(f"{package_name} --> {dependency}")
            self._build_dependency_graph(dependency, visited)  # Рекурсивно обрабатываем зависимости

    def _save_graph_to_file(self, mermaid_data):
        """Сохранение графа в PNG с помощью Mermaid CLI."""
        mermaid_file = "graph.mmd"
        with open(mermaid_file, "w") as file:
            file.write(mermaid_data)

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        print(f"Использую инструмент визуализации: {self.vis_tool_path}")
        subprocess.run([self.vis_tool_path, "-i", mermaid_file, "-o", self.output_path], check=True)

    def visualize(self):
        """Основной метод визуализации."""
        self._build_dependency_graph(self.package_name)

        mermaid_graph = "graph TD\n  " + "\n  ".join(self.graph)
        self._save_graph_to_file(mermaid_graph)
        print(f"Граф зависимостей успешно сохранён в {self.output_path}")

if __name__ == "__main__":
    visualizer = DependencyVisualizer("config.ini")
    visualizer.visualize()
