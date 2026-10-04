"""Regression cases for links normalized by GitBook's Git export."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_docs


class LinkChecks(unittest.TestCase):
    def check_fixture(self, link, files):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            docs = root / 'docs'
            docs.mkdir()
            (docs / 'README.md').write_text('# Home\n\n' + link + '\n')
            entries = ['* [Home](README.md)']
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                if path.is_relative_to(docs) and path.suffix == '.md':
                    entries.append(f'* [Page]({path.relative_to(docs).as_posix()})')
            (docs / 'SUMMARY.md').write_text('# Summary\n\n' + '\n'.join(entries))
            output = io.StringIO()
            with patch.object(check_docs, 'ROOT', root), \
                 patch.object(check_docs, 'DOCS', docs), \
                 contextlib.redirect_stdout(output):
                result = check_docs.check()
            return result, output.getvalue()

    def test_published_directory_with_spaces(self):
        result, _ = self.check_fixture(
            '[Source](chapter/Part%20II/)',
            {'docs/chapter/Part II/chapter.md': '# Source'})
        self.assertEqual(result, 0)

    def test_missing_source_still_fails(self):
        result, output = self.check_fixture('[Source](../SLAM/missing.md)', {})
        self.assertEqual(result, 1)
        self.assertIn('link leaves docs', output)

    def test_link_cannot_escape_repository(self):
        result, output = self.check_fixture('[Outside](../../outside.md)', {})
        self.assertEqual(result, 1)
        self.assertIn('link leaves docs', output)

    def test_other_repository_directory_stays_rejected(self):
        result, output = self.check_fixture(
            '[Draft](../drafts/example.md)', {'drafts/example.md': '# Draft'})
        self.assertEqual(result, 1)
        self.assertIn('link leaves docs', output)

    def test_source_images_must_be_in_published_content(self):
        for link in ('![Image](../SLAM/diagram.svg)', '<img src="../SLAM/diagram.svg">'):
            with self.subTest(link=link):
                result, output = self.check_fixture(link, {'SLAM/diagram.svg': '<svg/>'})
                self.assertEqual(result, 1)
                self.assertIn('link leaves docs', output)

    def test_directory_link_checks_readme_anchor(self):
        for anchor, expected in [('topic', 0), ('missing', 1)]:
            with self.subTest(anchor=anchor):
                result, output = self.check_fixture(
                    f'[Chapter](chapter/#{anchor})', {'docs/chapter/README.md': '# Topic'})
                self.assertEqual(result, expected)
                if expected:
                    self.assertIn('missing anchor', output)


if __name__ == '__main__':
    unittest.main()
