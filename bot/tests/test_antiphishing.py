import unittest
from bot.services.antiphishing import AntiPhishingService


class TestAntiPhishingService(unittest.TestCase):
    def test_extract_urls(self):
        text = "Check out this link https://discord.gg/test and http://google.com/search?q=hi"
        urls = AntiPhishingService.extract_urls(text)
        self.assertEqual(len(urls), 2)
        self.assertIn("https://discord.gg/test", urls)

    def test_domain_extraction(self):
        domain = AntiPhishingService.extract_domain("https://sub.discord.com/channels/123/456")
        self.assertEqual(domain, "sub.discord.com")

        domain2 = AntiPhishingService.extract_domain("discorcl.com/nitro-gift")
        self.assertEqual(domain2, "discorcl.com")

    def test_typosquatting_detection(self):
        is_typo, target = AntiPhishingService.is_typosquatting("discorcl.com")
        self.assertTrue(is_typo)

        is_typo2, target2 = AntiPhishingService.is_typosquatting("discord.com")
        self.assertFalse(is_typo2)

    def test_evaluate_url_phishing(self):
        is_malicious, reason = AntiPhishingService.evaluate_url("https://discorcl.com/free-nitro")
        self.assertTrue(is_malicious)

        is_malicious_safe, _ = AntiPhishingService.evaluate_url(
            "https://discord.com/channels/1/2",
            whitelisted_domains=["discord.com"]
        )
        self.assertFalse(is_malicious_safe)


if __name__ == "__main__":
    unittest.main()

