from __future__ import annotations

import re
import urllib.parse
from typing import List, Optional, Set, Tuple


SUSPICIOUS_TLDS: Set[str] = {
    ".ru", ".tk", ".ml", ".ga", ".cf", ".gq", ".top", ".xyz", ".buzz", ".monster", ".click", ".link"
}

TARGET_DOMAINS: List[str] = [
    "discord.com",
    "discord.gg",
    "discordapp.com",
    "steamcommunity.com",
    "roblox.com",
    "twitch.tv",
    "youtube.com",
]

PHISHING_KEYWORDS: List[str] = [
    "nitro", "free-nitro", "airdrop", "gift", "steam-promo", "claim",
    "drop", "giveaway", "discorcl", "dlscord", "boost", "premium-nitro"
]

URL_REGEX = re.compile(
    r"(?:https?://)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s]*)?",
    re.IGNORECASE
)


class AntiPhishingService:

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        return URL_REGEX.findall(text)

    @staticmethod
    def extract_domain(url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.hostname or ""
            return domain.lower().strip()
        except Exception:
            return ""

    @classmethod
    def levenshtein_distance(cls, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return cls.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @classmethod
    def is_typosquatting(cls, domain: str) -> Tuple[bool, Optional[str]]:
        clean_domain = domain.split(":")[0]

        if clean_domain.startswith("www."):
            clean_domain = clean_domain[4:]

        for target in TARGET_DOMAINS:
            if clean_domain == target:
                return False, None


            parts = clean_domain.split(".")
            if len(parts) >= 2:
                root_and_tld = ".".join(parts[-2:])
                target_parts = target.split(".")
                target_root = target_parts[0]
                root_candidate = parts[-2]


                dist = cls.levenshtein_distance(root_candidate, target_root)
                if 1 <= dist <= 2 and root_candidate != target_root:
                    return True, target


                if any(kw in root_candidate for kw in ["discorcl", "dlscord", "disscord", "steamcommunityy"]):
                    return True, target

        return False, None

    @classmethod
    def evaluate_url(
        cls,
        url: str,
        whitelisted_domains: Optional[List[str]] = None,
        custom_blacklist: Optional[List[str]] = None,
    ) -> Tuple[bool, str]:
        domain = cls.extract_domain(url)
        if not domain:
            return False, "Invalid or empty domain"


        if whitelisted_domains:
            for w in whitelisted_domains:
                if domain == w.lower() or domain.endswith("." + w.lower()):
                    return False, "Whitelisted domain"


        if custom_blacklist:
            for b in custom_blacklist:
                if domain == b.lower() or domain.endswith("." + b.lower()):
                    return True, f"Blacklisted domain: {domain}"


        is_typo, target = cls.is_typosquatting(domain)
        if is_typo:
            return True, f"Suspicious lookalike / typosquatting domain imitating {target}"


        for kw in PHISHING_KEYWORDS:
            if kw in domain and not any(safe in domain for safe in ["discord.com", "discord.gg"]):

                if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS) or "-" in domain:
                    return True, f"Phishing keyword pattern detected ({kw}) on suspicious host"


        if "discord.com/api/webhooks/" in url and ("token=" in url or "auth" in url):
            return True, "Potential webhook credential harvest vector"

        return False, "Safe"

