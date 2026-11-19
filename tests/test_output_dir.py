import json
import tempfile
import unittest
from pathlib import Path
from Keil2Json import CompileCommandsGenerator


class OutputDirectoryTests(unittest.TestCase):
    def test_output_locations(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            root = Path(temp) / 'project'
            root.mkdir()
            for destination in (None, Path(temp) / 'nested space' / 'out'):
                with self.subTest(destination=destination):
                    generator = CompileCommandsGenerator(path=root, output_dir=destination)
                    generator.project_root = root
                    entries = [{'directory': str(root), 'file': 'main.c'}]
                    output = generator.write_json(entries)
                    self.assertEqual(output, (destination or root) / 'compile_commands.json')
                    self.assertEqual(json.loads(output.read_text()), entries)

    def test_file_as_directory(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            destination = Path(temp) / 'file'
            destination.write_text('existing')
            generator = CompileCommandsGenerator(output_dir=destination)
            with self.assertRaises(FileExistsError):
                generator.write_json([])
            self.assertEqual(destination.read_text(), 'existing')


if __name__ == '__main__':
    unittest.main()
