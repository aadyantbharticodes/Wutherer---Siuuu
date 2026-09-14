from discord.ext import commands


class SentinelError(commands.CommandError):
    pass


class NotConfigured(SentinelError):

    def __init__(self, feature: str):
        self.feature = feature
        super().__init__(f"{feature} is not configured for this server.")


class MissingSetup(SentinelError):

    def __init__(self, what: str):
        self.what = what
        super().__init__(f"Setup required: {what}")


class Forbidden(SentinelError):

    def __init__(self, reason: str = "You don't have permission to do this."):
        self.reason = reason
        super().__init__(reason)


class RateLimited(SentinelError):

    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Try again in {retry_after:.0f}s.")


class AIUnavailable(SentinelError):

    def __init__(self):
        super().__init__("AI features are not available. Ask an administrator to configure the API key.")


class ExternalAPIError(SentinelError):

    def __init__(self, service: str, detail: str = ""):
        self.service = service
        msg = f"The {service} API is currently unavailable."
        if detail:
            msg += f" ({detail})"
        super().__init__(msg)


class HierarchyError(SentinelError):

    def __init__(self, target: str = "that user"):
        super().__init__(f"Cannot perform this action on {target} due to role hierarchy.")

