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

    def test_nested_keil_project_paths(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            root = Path(temp).resolve()
            project_dir = root / 'ide' / 'keil'
            project_dir.mkdir(parents=True)
            project = project_dir / 'demo.uvprojx'
            project.write_text('<Project><TargetArmAds><Cads><VariousControls><IncludePath>../../source</IncludePath></VariousControls></Cads></TargetArmAds><Groups><Group><Files><File><FilePath>../../source/main.c</FilePath></File></Files></Group></Groups></Project>')
            class Config:
                def get(self, *args):
                    return ''
            generator = CompileCommandsGenerator(path=root, config_manager=Config())
            generator.project_root = root
            includes, _, sources = generator.parse_uvprojx(project)
            self.assertEqual(sources, [(root / 'source/main.c').as_posix()])
            self.assertEqual(includes, [(root / 'source').as_posix()])
            self.assertEqual(generator.format_path(sources[0]), 'source/main.c')

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
