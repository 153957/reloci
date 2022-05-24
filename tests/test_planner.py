import unittest

from pathlib import Path

from exiftool import ExifTool

from reloci import planner, renamer


class PlannerTestCase(unittest.TestCase):
    def setUp(self):
        self.source = Path(__file__).parent.parent / 'demo/source/'
        self.output = self.source.parent / 'output/'
        self.planner = planner.Planner(self.source, self.output, renamer.Renamer)

    def test_init(self):
        self.assertEqual(self.source, self.planner.input_root)
        self.assertEqual(self.output, self.planner.output_root)
        self.assertIsInstance(self.planner.renamer, renamer.Renamer)

    def test_get_files(self):
        self.assertCountEqual(
            [
                self.source / 'APL_082158.NEF',
                self.source / 'APS_003129.MOV',
                self.source / 'DSC_064662.NEF',
                self.source / 'IMG_6828.JPG',
                self.source / 'IMG_7074.MOV',
                self.source / 'IMG_9895.JPG',
                self.source / 'IMG_9895.MOV',
                self.source / 'IMG_054762.JPG',
                self.source / 'JYBF8578.DNG',
            ],
            self.planner.get_files()
        )

    def test_get_output_path(self):
        combinations = [
            ('APL_082158.NEF', '2021/04/210402/APL_082158.NEF'),
            ('APS_003129.MOV', '2021/05/210501/APS_003129.MOV'),
            ('DSC_064662.NEF', '2009/01/090106/DSC_064662.NEF'),
            ('IMG_6828.JPG', '2019/04/190430/CLK_jv3vijqe.JPG'),
            ('IMG_7074.MOV', '2022/05/220520/TRM_l3evriag.MOV'),
            ('IMG_9895.JPG', '2020/03/200320/CLK_k80cid1l.JPG'),
            ('IMG_9895.MOV', '2020/03/200320/CLK_k80cid1l.MOV'),
            ('IMG_054762.JPG', '2006/10/061025/IMG_054762.JPG'),
            ('JYBF8578.DNG', '2020/10/201018/CLK_kgex8fen.DNG'),
        ]
        with ExifTool() as exiftool:
            for source_file, output_path in combinations:
                with self.subTest(source_path=source_file):
                    self.assertEqual(self.output / output_path, self.planner.get_output_path(self.source / source_file, exiftool))
