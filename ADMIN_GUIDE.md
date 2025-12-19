# MOOdBBS Admin Tool Guide

The admin tool (`admin.py`) provides a shell-based interface for managing your MOOdBBS database and viewing statistics.

## Running the Admin Tool

```bash
python admin.py
```

## Features

### 1. Database Status

Shows comprehensive database information:
- Database file location and size
- Record counts for all tables (moodlets, quests, completions, etc.)
- Number of applied migrations
- Overall database health

**Use when:** You want to check if the database exists and see how much data you have.

### 2. Reset Database (Safe)

Safely resets the database with automatic backup:

**What it does:**
1. Shows what data will be lost (active quests, moodlets, completions)
2. Asks for confirmation (requires explicit "yes")
3. Creates automatic backup with timestamp (`moodbbs.db.backup.20231126_143000`)
4. Deletes current database
5. Creates fresh database from schema
6. Applies all migrations

**Use when:**
- You want to start completely fresh
- Database is corrupted
- Testing from clean state

**Safety features:**
- Automatic backup before deletion
- Requires confirmation
- Shows exactly what will be lost

### 3. Backup Database

Creates a timestamped backup of your current database.

**Format:** `moodbbs.db.backup.YYYYMMDD_HHMMSS`

**Use when:**
- Before making major changes
- Before upgrading
- Creating restore points

### 4. View User Profile

Displays all fields in the user profile:
- Zipcode
- Transportation preferences
- Memberships
- Location data (if set)
- Setup completion status

**Use when:** Checking what profile data exists.

### 5. Clear Active Moodlets

Removes all currently active moodlets (does NOT delete moodlet templates).

**What it clears:**
- Active mood buffs/debuffs
- Moodlets in backoff phase
- Temporary mood state

**What it preserves:**
- Moodlet templates (the 61 pre-configured moodlets)
- Historical data (quest completions still reference past moodlets)

**Use when:**
- Resetting mood state without losing other data
- Testing moodlet application
- Fixing stuck moodlets

### 6. Clear Active Quests

Marks all active quests as "cancelled" (does NOT delete them).

**What it does:**
- Changes quest status from "active" to "cancelled"
- Removes quests from active quest list
- Preserves quest history

**Use when:**
- Clearing out old/irrelevant quests
- Starting fresh with new quests
- Testing quest system

### 7. View Moodlet Statistics

Comprehensive moodlet analytics:

**Shows:**
- Moodlets by category (quest-based vs event-based breakdown)
- Total counts per category
- Most applied moodlets of all time
- Application frequency

**Use when:**
- Understanding which moodlets are used most
- Analyzing user behavior patterns
- Planning new moodlets

### 8. View Quest Statistics

Quest system analytics:

**Shows:**
- Quest status breakdown (active, completed, cancelled)
- Total completions
- Total XP earned
- Average XP per quest

**Use when:**
- Tracking progress over time
- Understanding quest difficulty balance
- Viewing achievement metrics

### 9. Run Migrations

Manually runs database migrations.

**What it does:**
- Checks for unapplied migrations in `src/database/migrations/`
- Applies them in order (001, 002, 003, etc.)
- Updates migration tracking table

**Use when:**
- After pulling new code with migrations
- Database schema is outdated
- Migrations failed during setup

## Common Workflows

### Starting Fresh
```
1. Run admin tool: python admin.py
2. Select option 2 (Reset Database)
3. Confirm when prompted
4. Exit admin tool
5. Run TUI: python tui.py
6. Complete setup wizard
```

### Before Major Changes
```
1. Run admin tool
2. Select option 3 (Backup Database)
3. Note the backup filename
4. Make your changes
5. If something breaks, restore from backup
```

### Viewing Your Data
```
1. Option 1: Database status (overview)
2. Option 4: User profile (settings)
3. Option 7: Moodlet stats (usage patterns)
4. Option 8: Quest stats (progress)
```

### Quick Reset (Keep Profile)
```
1. Option 5: Clear active moodlets
2. Option 6: Clear active quests
3. (Profile and settings remain)
```

## Backup Management

Backups are stored in the `data/` directory with timestamp format:
```
data/moodbbs.db.backup.20231126_143000
```

### Manual Restore from Backup
```bash
# List available backups
ls -lh data/*.backup.*

# Restore from specific backup
cp data/moodbbs.db.backup.20231126_143000 data/moodbbs.db
```

### Cleaning Old Backups
```bash
# Remove backups older than 7 days
find data/ -name "*.backup.*" -mtime +7 -delete
```

## Safety Features

The admin tool is designed to be safe:

1. **Automatic Backups**: Reset operation creates backup before deletion
2. **Confirmation Prompts**: Destructive operations require explicit confirmation
3. **Data Preservation**: Clear operations mark as cancelled/inactive rather than deleting
4. **Read-Only Views**: Statistics views never modify data
5. **Timestamped Backups**: Never overwrites previous backups

## Troubleshooting

### "Database does not exist"
- Run option 2 (Reset Database) to create a fresh database
- Or run `python tui.py` to trigger automatic setup

### "Migration errors occurred"
- Check that all migration files exist in `src/database/migrations/`
- Ensure database wasn't corrupted
- Try reset database (option 2) for clean slate

### "Error querying database"
- Database may be locked by running TUI
- Close TUI before running admin commands
- Database may be corrupted - consider reset

### Backup restore didn't work
- Ensure you copied to `data/moodbbs.db` exactly
- Check file permissions (should be readable/writable)
- Verify backup isn't corrupted: `sqlite3 data/moodbbs.db.backup.XXX "SELECT COUNT(*) FROM moodlets"`

## Advanced Usage

### Direct Database Access

For advanced users, you can query the database directly:

```bash
sqlite3 data/moodbbs.db

# Example queries:
sqlite> SELECT * FROM moodlets WHERE category = 'social';
sqlite> SELECT * FROM active_moodlets;
sqlite> SELECT * FROM quests WHERE status = 'active';
sqlite> .schema moodlets
sqlite> .exit
```

### Manual Migration Creation

To create a new migration:

1. Create file: `src/database/migrations/008_your_migration_name.sql`
2. Write SQL (use `IF NOT EXISTS` for safety)
3. Run option 9 in admin tool to apply

### Exporting Data

```bash
# Export entire database to SQL
sqlite3 data/moodbbs.db .dump > moodbbs_export.sql

# Export specific table to CSV
sqlite3 data/moodbbs.db <<EOF
.headers on
.mode csv
.output quest_completions.csv
SELECT * FROM quest_completions;
EOF
```

## Tips

- **Backup before experiments**: Always backup before trying new features
- **Check stats regularly**: Moodlet/quest stats help understand usage patterns
- **Keep old backups**: Disk space is cheap, your data isn't
- **Use reset sparingly**: Only reset when truly needed - clearing is often enough
- **Profile first**: Check database status before making changes

## Exit Commands

- Press `q` at any menu to quit
- Press `Ctrl+C` to emergency exit (works anywhere)
- Press `Enter` to continue after viewing information screens
