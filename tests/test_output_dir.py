import json
import tempfile
import unittest
from Keil2Json import keil_cpu_flags
from pathlib import Path
from Keil2Json import CompileCommandsGenerator


class OutputDirectoryTests(unittest.TestCase):
    def test_cpu_flags(self):
        for core, expected in [('Cortex-M0+', 'cortex-m0plus'), ('Cortex-M0plus', 'cortex-m0plus'), ('Cortex-M3', 'cortex-m3'), ('Cortex-M4', 'cortex-m4'), ('Cortex-M7', 'cortex-m7'), ('Cortex-M33', 'cortex-m33')]:
            with self.subTest(core=core):
                self.assertEqual(keil_cpu_flags('CLOCK(48000000) CPUTYPE("' + core + '")'), ['--target=arm-none-eabi', '-mcpu=' + expected, '-mthumb'])
        self.assertEqual(keil_cpu_flags(''), [])
        self.assertEqual(keil_cpu_flags('CPUTYPE("unknown")'), [])

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
            project.write_text('<Project><Cpu>CPUTYPE("Cortex-M0+")</Cpu><TargetArmAds><Cads><VariousControls><IncludePath>../../source</IncludePath></VariousControls></Cads></TargetArmAds><Groups><Group><Files><File><FilePath>../../source/main.c</FilePath></File></Files></Group></Groups></Project>')
            class Config:
                def get(self, *args):
                    return ''
            generator = CompileCommandsGenerator(path=root, config_manager=Config())
            generator.project_root = root
            includes, _, sources = generator.parse_uvprojx(project)
            self.assertEqual(sources, [(root / 'source/main.c').as_posix()])
            self.assertEqual(includes, [(root / 'source').as_posix()])
            self.assertEqual(generator.format_path(sources[0]), 'source/main.c')
            entries = generator.generate_entries(includes, [], sources)
            self.assertIn('-mcpu=cortex-m0plus', entries[0]['arguments'])

    def test_armcc_declspec_and_switching_compilers(self):
        class Config:
            def get(self, *args):
                return ''
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            root = Path(temp).resolve()
            project = root / 'demo.uvprojx'
            generator = CompileCommandsGenerator(path=root, config_manager=Config())
            generator.project_root = root
            for compiler, enabled in [('ARMCC', True), ('ARMCLANG', False), ('ARMCC', True)]:
                project.write_text('<Project><pCCUsed>' + compiler + '</pCCUsed><Cpu>CPUTYPE("Cortex-M3")</Cpu><Groups><Group><Files><File><FilePath>main.c</FilePath></File></Files></Group></Groups></Project>')
                includes, defines, sources = generator.parse_uvprojx(project)
                args = generator.generate_entries(includes, defines, sources)[0]['arguments']
                self.assertEqual(args.count('-fdeclspec'), int(enabled))
                self.assertIn('-mcpu=cortex-m3', args)

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
