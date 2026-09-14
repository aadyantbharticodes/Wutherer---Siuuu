from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.captcha import CaptchaService


class TestVerificationCaptcha(unittest.TestCase):
    def test_text_captcha_generation(self):
        code, buffer = CaptchaService.generate_text_captcha(length=5)
        self.assertEqual(len(code), 5)
        self.assertGreater(buffer.getbuffer().nbytes, 0)

    def test_math_captcha_generation(self):
        question, answer, buffer = CaptchaService.generate_math_captcha()
        self.assertTrue("?" in question)
        self.assertTrue(answer.isdigit() or (answer.startswith("-") and answer[1:].isdigit()))
        self.assertGreater(buffer.getbuffer().nbytes, 0)


if __name__ == "__main__":
    unittest.main()

