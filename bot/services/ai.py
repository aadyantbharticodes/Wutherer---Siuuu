from __future__ import annotations
import asyncio
import io
import logging
import time
from collections import defaultdict
from typing import Optional

from config import GEMINI_API_KEY, AI_ENABLED, AI_MODEL, AI_MAX_TOKENS, AI_RATE_LIMIT

log = logging.getLogger("wutherer.ai")

try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None


class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self._calls: dict[str, list[float]] = defaultdict(list)

    def is_limited(self, key: str) -> bool:
        now = time.time()
        self._calls[key] = [t for t in self._calls[key] if now - t < self.period]
        return len(self._calls[key]) >= self.max_calls

    def record(self, key: str):
        self._calls[key].append(time.time())

    def remaining(self, key: str) -> int:
        now = time.time()
        self._calls[key] = [t for t in self._calls[key] if now - t < self.period]
        return max(0, self.max_calls - len(self._calls[key]))

    def retry_after(self, key: str) -> float:
        if not self._calls[key]:
            return 0
        oldest = min(self._calls[key])
        return max(0, self.period - (time.time() - oldest))


_rate_limiter = RateLimiter(AI_RATE_LIMIT, 60.0)


class AIService:
    def __init__(self):
        self.available = AI_ENABLED and GEMINI_AVAILABLE
        self._model = None
        self._vision_model = None
        if self.available:
            self._model = genai.GenerativeModel(AI_MODEL)
            self._vision_model = genai.GenerativeModel(AI_MODEL)

    async def chat(self, prompt: str, history: list[dict] = None,
                   system_prompt: str = None, user_id: int = None,
                   max_tokens: int = None) -> str:
                       pass
        if not self.available:
            return "AI features are not configured. Ask a server administrator to set up the API key."

        rate_key = f"user:{user_id}" if user_id else "global"
        if _rate_limiter.is_limited(rate_key):
            wait = _rate_limiter.retry_after(rate_key)
            return f"You're sending messages too quickly. Please wait {wait:.0f} seconds."

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "user", "parts": [f"System instruction: {system_prompt}"]})
                messages.append({"role": "model", "parts": ["Understood. I will follow these instructions."]})
            if history:
                for msg in history:
                    role = "user" if msg["role"] == "user" else "model"
                    messages.append({"role": role, "parts": [msg["content"]]})
            messages.append({"role": "user", "parts": [prompt]})

            response = await asyncio.to_thread(
                self._model.generate_content,
                messages,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens or AI_MAX_TOKENS,
                    temperature=0.7,
                ),
            )
            _rate_limiter.record(rate_key)

            if response.text:
                return self._truncate(response.text, 2000)
            return "I couldn't generate a response. Please try again."
        except Exception as e:
            log.error("AI chat error: %s", e)
            return "Something went wrong with the AI service. Please try again later."

    async def summarize(self, text: str, style: str = "concise") -> str:
        prompt = f"Summarize the following text in a {style} manner. Keep it under 500 words:\n\n{text}"
        return await self.chat(prompt)

    async def rewrite(self, text: str, tone: str = "professional") -> str:
        prompt = f"Rewrite the following text in a {tone} tone while preserving the meaning:\n\n{text}"
        return await self.chat(prompt)

    async def translate(self, text: str, target_language: str) -> str:
        prompt = f"Translate the following text to {target_language}. Only output the translation:\n\n{text}"
        return await self.chat(prompt)

    async def check_grammar(self, text: str) -> str:
        prompt = f"Check this text for grammar and spelling errors. Show corrections:\n\n{text}"
        return await self.chat(prompt)

    async def classify_content(self, text: str) -> dict:
        prompt = (
            "Analyze this message and classify it. Respond ONLY with a JSON object containing:\n"
            '- "toxic": true/false\n'
            '- "spam": true/false\n'
            '- "category": one of "normal", "toxic", "spam", "self_promotion"\n'
            '- "confidence": 0.0 to 1.0\n'
            f"\nMessage: {text}"
        )
        import json
        result = await self.chat(prompt)
        try:
            clean = result.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(clean)
        except (json.JSONDecodeError, IndexError):
            return {"toxic": False, "spam": False, "category": "normal", "confidence": 0.5}

    async def generate_announcement(self, topic: str, tone: str = "friendly",
                                     guild_name: str = "") -> str:
                                         pass
        prompt = (
            f"Write a Discord server announcement for {guild_name or 'our server'} about: {topic}\n"
            f"Tone: {tone}. Keep it under 300 words. Use Discord markdown formatting. "
            "Make it engaging and include a call to action."
        )
        return await self.chat(prompt)

    async def analyze_image(self, image_bytes: bytes, prompt: str = "Describe this image.") -> str:
        if not self.available:
            return "AI features are not configured."
        try:
            import PIL.Image
            img = PIL.Image.open(io.BytesIO(image_bytes))
            response = await asyncio.to_thread(
                self._vision_model.generate_content,
                [prompt, img],
                generation_config=genai.GenerationConfig(max_output_tokens=AI_MAX_TOKENS),
            )
            if response.text:
                return self._truncate(response.text, 2000)
            return "I couldn't analyze this image."
        except Exception as e:
            log.error("AI image analysis error: %s", e)
            return "Failed to analyze the image. Please try again."

    async def minecraft_help(self, query: str) -> str:
        prompt = (
            "You are a Minecraft expert. Answer this Minecraft-related question concisely. "
            "Include crafting recipes, game mechanics, or tips as relevant. "
            f"Keep your answer under 400 words.\n\nQuestion: {query}"
        )
        return await self.chat(prompt, system_prompt="You are a Minecraft game expert and assistant.")

    async def gaming_tip(self, game: str, topic: str = "") -> str:
        prompt = f"Give a helpful gaming tip or strategy for {game}"
        if topic:
            prompt += f" about {topic}"
        prompt += ". Keep it concise (under 200 words)."
        return await self.chat(prompt, system_prompt="You are a knowledgeable gaming assistant.")

    async def youtube_ideas(self, niche: str, count: int = 5) -> str:
        prompt = (
            f"Generate {count} creative YouTube video ideas for the '{niche}' niche. "
            "For each idea, provide a title and a brief 1-sentence description. "
            "Format as a numbered list."
        )
        return await self.chat(prompt, system_prompt="You are a YouTube content strategy expert.")

    async def study_help(self, topic: str, question: str = "") -> str:
        prompt = f"Help me study {topic}."
        if question:
            prompt += f" Specifically: {question}"
        prompt += " Explain clearly with examples where helpful. Keep it under 500 words."
        return await self.chat(prompt, system_prompt="You are a patient and clear educational tutor.")

    async def code_help(self, language: str, question: str) -> str:
        prompt = f"Help with this {language} coding question: {question}\nProvide a clear explanation with code examples."
        return await self.chat(prompt, system_prompt="You are a senior software developer and teacher.")

    async def suggest_welcome_message(self, guild_name: str, style: str = "friendly") -> str:
        prompt = (
            f"Write a Discord welcome message for new members joining '{guild_name}'. "
            f"Tone: {style}. Use Discord markdown. Include placeholders like {{user}} and {{server}}. "
            "Keep it under 150 words."
        )
        return await self.chat(prompt)

    async def ticket_summary(self, messages: list[str]) -> str:
        text = "\n".join(messages[-50:])
        prompt = f"Summarize this support ticket conversation concisely:\n\n{text}"
        return await self.chat(prompt, system_prompt="You are a support ticket analyst.")

    async def moderation_analysis(self, message: str, context: str = "") -> str:
        prompt = (
            "Analyze this message for potential rule violations. "
            "Provide your assessment but do NOT recommend automatic action. "
            "Only flag issues for human moderator review.\n\n"
            f"Message: {message}"
        )
        if context:
            prompt += f"\n\nAdditional context: {context}"
        return await self.chat(prompt, system_prompt="You are a community moderation assistant.")

    async def server_setup_advice(self, description: str) -> str:
        prompt = (
            f"A Discord server owner describes their server as: {description}\n"
            "Suggest channel structure, role hierarchy, bot features to enable, "
            "and moderation settings. Be specific and actionable."
        )
        return await self.chat(prompt, system_prompt="You are a Discord server organization expert.")

    @staticmethod
    def _truncate(text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[:limit - 3] + "..."


ai_service = AIService()

