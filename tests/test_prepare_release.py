import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import prepare_release  # noqa: E402


class PrepareReleaseTests(unittest.TestCase):
    def setUp(self):
        self.brief = {
            "title": "A Friendly Song",
            "audience": "Families",
            "language": "English",
            "concept": "An original friendship song.",
            "lyrics": "Wave hello, sing along!",
            "visual_direction": "Original watercolor animals.",
            "rights": {"lyrics": "original", "music": "original", "visuals": "original", "samples": "none"},
            "keywords": ["kids song"],
            "hashtags": ["#KidsSongs"],
        }

    def test_prepare_writes_reviewable_package(self):
        with tempfile.TemporaryDirectory() as directory:
            output = prepare_release.prepare(self.brief, Path(directory))
            self.assertTrue((output / "digen-job.json").exists())
            self.assertTrue((output / "youtube-metadata.json").exists())
            self.assertIn("#KidsSongs", (output / "youtube-metadata.json").read_text())

    def test_blocks_reference_channel(self):
        self.brief["concept"] = "Copy SunriseJungleBeat and change the lyrics."
        with self.assertRaisesRegex(ValueError, "Reference-channel"):
            prepare_release.validate(self.brief)


if __name__ == "__main__":
    unittest.main()
