VALID_MAILING_ROWS: list[list[object]] = [
    ["external_id", "user_id", "email", "subject", "message"],
    ["ext-1", 1, "user1@example.com", "Welcome", "Hello from row 1"],
    ["ext-2", 2, "user2@example.com", "Reminder", "Hello from row 2"],
    ["ext-dup", 3, "dup@example.com", "Duplicate test", "Re-import to get skipped"],
]

INVALID_MAILING_ROWS: list[list[object]] = [
    ["external_id", "user_id", "email", "subject", "message"],
    ["ext-bad-email", 1, "not-an-email", "Bad email", "Invalid email format"],
    ["ext-empty-subject", 2, "ok@example.com", "", "Missing subject"],
    ["ext-bad-user-id", "abc", "ok@example.com", "Bad user_id", "user_id is not integer"],
]

VALID_SAMPLE_FILE = "sample_mailings.xlsx"
INVALID_SAMPLE_FILE = "sample_mailings_invalid.xlsx"

SAMPLE_FILES = {
    "valid": (VALID_SAMPLE_FILE, VALID_MAILING_ROWS),
    "invalid": (INVALID_SAMPLE_FILE, INVALID_MAILING_ROWS),
}
