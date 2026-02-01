import unittest

from pathlib import Path

from reloci import cli, renamer


class CLITest(unittest.TestCase):
    def test_get_renamer_class(self) -> None:
        self.assertEqual(
            renamer.DateTimeRenamer,
            cli.get_renamer_class('reloci.renamer.DateTimeRenamer'),
        )
        self.assertEqual(
            renamer.DatePathRenamer,
            cli.get_renamer_class('reloci.renamer.DatePathRenamer'),
        )

    def test_get_parser_reloci(self) -> None:
        parser = cli.get_parser_reloci()

        with self.subTest('Defaults'):
            args = parser.parse_args(['source', 'target'])
            self.assertFalse(args.move)
            self.assertFalse(args.dryrun)
            self.assertEqual(0, args.verbose)
            self.assertEqual(renamer.Renamer, args.renamer)
            self.assertEqual(Path('source'), args.inputpath)
            self.assertEqual(Path('target'), args.outputpath)

        with self.subTest('Enabled move'):
            args = parser.parse_args(['--move', 'source', 'target'])
            self.assertTrue(args.move)

        with self.subTest('Enabled dry run'):
            args = parser.parse_args(['--dryrun', 'source', 'target'])
            self.assertTrue(args.dryrun)

        with self.subTest('Increased verbosity'):
            args = parser.parse_args(['-vvv', 'source', 'target'])
            self.assertEqual(3, args.verbose)

        with self.subTest('Custom Renamer class'):
            args = parser.parse_args(['--renamer', 'reloci.renamer.DateTimeRenamer', 'source', 'target'])
            self.assertEqual(renamer.DateTimeRenamer, args.renamer)

    def test_get_parser_file_info(self) -> None:
        parser = cli.get_parser_file_info()

        args = parser.parse_args(['target'])
        self.assertEqual(Path('target'), args.path)

    def test_get_parser_check_interval(self) -> None:
        parser = cli.get_parser_check_interval()

        with self.subTest('Defaults'):
            args = parser.parse_args([])
            self.assertEqual('*.NEF', args.pattern)
            self.assertEqual(1, args.shots_per_interval)
            self.assertFalse(args.group)

        with self.subTest('Alternative pattern'):
            args = parser.parse_args(['--pattern', '*.tif'])
            self.assertEqual('*.tif', args.pattern)

        with self.subTest('Different number of shot per interval'):
            args = parser.parse_args(['--shots_per_interval', '3'])
            self.assertEqual(3, args.shots_per_interval)

        with self.subTest('Increased verbosity'):
            args = parser.parse_args(['--group'])
            self.assertTrue(args.group)
