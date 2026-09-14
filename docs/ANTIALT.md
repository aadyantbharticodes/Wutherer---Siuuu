# Anti-Alt & Account Verification Shield

Wutherer includes an automated Anti-Alt subsystem designed to block burner accounts, fresh alternate accounts, and coordinated bot raids.

---

## Verification Criteria

1. **Minimum Account Age Verification**:
   - Compares the member's account registration date (`member.created_at`) against the guild's minimum age requirement (default: 7 days).
   - Accounts younger than the configured threshold trigger automated countermeasures immediately upon joining.

2. **Custom Avatar Enforcement**:
   - Detects whether an account is using a default Discord avatar.
   - When enabled, accounts lacking a custom avatar are flagged as suspicious.

3. **Automated Countermeasures**:
   - `quarantine`: Confines the account to an isolated quarantine role with no channel access until manually vetted.
   - `kick`: Evicts the account immediately with an explanatory reason.
   - `ban`: Permanently bans the account from the server.

---

## Discord Commands

| Command | Arguments | Permission | Description |
| :--- | :--- | :--- | :--- |
| `s!antialt` | *None* | Administrator | Displays Anti-Alt shield status and settings. |
| `s!antialt toggle` | *None* | Administrator | Enables or disables the anti-alt shield. |
| `s!antialt minage` | `<days>` | Administrator | Sets minimum account age threshold (1–365 days). |
| `s!antialt avatar` | `<on/off>` | Administrator | Requires incoming accounts to have a custom avatar. |
| `s!antialt action` | `<quarantine/kick/ban>` | Administrator | Configures the automated enforcement penalty. |
| `s!antialt logs` | *None* | Administrator | Displays recent flagged accounts and actions taken. |
