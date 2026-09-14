# Background Daemon Workers

Wutherer runs asynchronous worker daemons in the background to handle periodic polling, real-time security auditing, data aggregation, and queued task dispatching.

---

## Active Daemons

### 1. AntiNukeWatchdogWorker (`bot/workers/antinuke_watchdog.py`)
- **Interval**: 15 seconds
- **Function**: Continuously audits recent guild audit log entries across all connected shards.
- **Responsibilities**:
  - Intercepts unauthorized bot additions by un-whitelisted administrative accounts.
  - Automatically bans or demotes compromised accounts and triggers security alerts.

### 2. OnboardingDispatcherWorker (`bot/workers/onboarding_dispatcher.py`)
- **Interval**: 30 seconds
- **Function**: Processes asynchronous delayed autoroles and retry queues.
- **Responsibilities**:
  - Automatically assigns member roles after a user completes the probationary delay duration.
  - Eliminates synchronous event loop blocking during heavy raid arrivals.

### 3. AnalyticsAggregatorWorker (`bot/workers/analytics_aggregator.py`)
- **Interval**: 60 seconds
- **Function**: Aggregates guild telemetries into hourly records.
- **Responsibilities**:
  - Logs active voice minutes, active channel chatters, and message frequencies into SQLite for dashboard charts.

### 4. YouTubeMonitorWorker (`bot/workers/youtube_monitor.py`)
- **Interval**: 120 seconds
- **Function**: Polls YouTube RSS feeds for creator channel uploads and dispatches announcement embeds.

### 5. MinecraftStatusUpdaterWorker (`bot/workers/mc_status_updater.py`)
- **Interval**: 60 seconds
- **Function**: Pings registered Java/Bedrock Minecraft servers to update status embeds and voice channel player counters.

### 6. GiveawayCheckerWorker (`bot/workers/giveaway_checker.py`)
- **Interval**: 15 seconds
- **Function**: Checks active giveaway timestamps, rolls random winners, and dispatches victory notifications.

### 7. ReminderDispatcherWorker (`bot/workers/reminder_dispatcher.py`)
- **Interval**: 10 seconds
- **Function**: Checks user reminders and delivers scheduled DM alerts.
