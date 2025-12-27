# BIM Project - Backup System Installation & Setup Guide

## Installation Summary

You now have a complete backup system for your BIM project! Here's what was installed:

## Files Created

### Main Backup Scripts
1. **backup.sh** (13KB) - Main orchestration script for all backups
2. **backup-database.sh** (7.9KB) - PostgreSQL database backup management
3. **backup-uploads.sh** (9.6KB) - Uploads directory backup management
4. **backup-docker.sh** (11KB) - Docker containers and volumes backup
5. **run-daily-backup.sh** (8.9KB) - Automated daily backup runner with notifications

### Documentation
1. **BACKUP_README.md** (11KB) - Comprehensive backup documentation
2. **BACKUP_QUICK_REFERENCE.sh** (9.4KB) - Quick command reference
3. **BACKUP_INSTALL.md** - This installation guide

## Quick Start (3 Steps)

### Step 1: Verify Scripts Are Executable
```bash
chmod +x backup.sh backup-database.sh backup-uploads.sh backup-docker.sh run-daily-backup.sh
```

### Step 2: Run Your First Backup
```bash
./backup.sh full
```

### Step 3: Verify Backup Success
```bash
./backup.sh list
du -sh backups/
```

## Backup Strategy Recommendations

### Daily Routine
```bash
# Run daily at 2 AM
0 2 * * * /home/unique/projects/BIM/backup.sh full
```

### Hourly Database Backup
```bash
# Critical data protection
0 * * * * /home/unique/projects/BIM/backup-database.sh full
```

### Weekly Full Docker Backup
```bash
# Container and volume snapshots
0 3 * * 0 /home/unique/projects/BIM/backup-docker.sh full
```

### Automatic Cleanup
```bash
# Remove backups older than 30 days
0 4 * * * /home/unique/projects/BIM/backup.sh cleanup
```

## Setup Automated Backups with Cron

### Option 1: Simple Daily Backup (Recommended)

```bash
# Edit crontab
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * /home/unique/projects/BIM/backup.sh full

# Add this for daily cleanup
0 4 * * * /home/unique/projects/BIM/backup.sh cleanup
```

### Option 2: Full Automated Setup (With Notifications)

```bash
# Edit crontab
crontab -e

# Add these lines:

# Daily full backup with email notifications at 2 AM
0 2 * * * SEND_EMAIL=true EMAIL_TO=admin@example.com /home/unique/projects/BIM/run-daily-backup.sh

# Hourly database backup
0 * * * * /home/unique/projects/BIM/backup-database.sh full

# Daily uploads backup at 2:30 AM
30 2 * * * /home/unique/projects/BIM/backup-uploads.sh daily

# Weekly Docker backup (Sunday at 3 AM)
0 3 * * 0 /home/unique/projects/BIM/backup-docker.sh full

# Daily cleanup
0 4 * * * /home/unique/projects/BIM/backup.sh cleanup
```

### Option 3: With Slack Notifications

```bash
# Edit crontab with Slack webhook
crontab -e

# Add this line
0 2 * * * SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL" /home/unique/projects/BIM/run-daily-backup.sh
```

## Usage Examples

### Most Common Commands

```bash
# Full backup
./backup.sh full

# List all backups
./backup.sh list

# Database backup only
./backup-database.sh full

# Uploads backup
./backup-uploads.sh daily

# Restore database
./backup-database.sh restore backups/database/geobiro_db_20250101_120000.sql.gz

# Restore uploads
./backup-uploads.sh restore backups/uploads/uploads_full_20250101_120000.tar.gz
```

## Backup Storage Structure

After first backup run, you'll have:

```
backups/
├── database/              # PostgreSQL dumps (compressed)
│   ├── geobiro_db_*.sql.gz
│   └── MANIFEST_*.txt
├── uploads/              # Uploads directory backups
│   ├── YYYY-MM-DD/
│   └── uploads_*.tar.gz
├── docker/              # Docker backups
│   ├── volumes/        # Volume backups
│   │   ├── postgres_volume_*.tar.gz
│   │   └── redis_volume_*.tar.gz
│   ├── images/        # Docker image exports
│   ├── configs/       # Container configs
│   └── docker-compose*.tar.gz
└── logs/              # Backup logs
    ├── backup_YYYY-MM-DD.log
    └── REPORT_*.txt
```

## Monitoring Your Backups

### Check Latest Backups
```bash
ls -lt backups/**/* | head -10
```

### View Backup Sizes
```bash
du -sh backups/*
du -sh backups/database/*
du -sh backups/uploads/*
```

### Monitor Backup Logs
```bash
# Today's log
tail -50 backups/logs/backup_$(date +%Y-%m-%d).log

# Watch in real-time
tail -f backups/logs/backup_$(date +%Y-%m-%d).log
```

### Check Cron Job Status
```bash
# View scheduled jobs
crontab -l

# Check job history
grep CRON /var/log/syslog | tail -20
```

## Email Notifications Setup

### Enable Email Notifications

1. Ensure `mail` or `sendmail` is installed:
```bash
sudo apt-get install mailutils  # Ubuntu/Debian
brew install postfix           # macOS
```

2. Set environment variables:
```bash
export SEND_EMAIL=true
export EMAIL_TO="your-email@example.com"
```

3. Or add to crontab:
```bash
0 2 * * * SEND_EMAIL=true EMAIL_TO=admin@example.com /home/unique/projects/BIM/backup.sh full
```

## Slack Integration Setup

### Configure Slack Webhook

1. Go to https://api.slack.com/apps
2. Create new app or select existing
3. Go to "Incoming Webhooks"
4. Create new webhook for your channel
5. Copy the webhook URL

### Use Slack Webhook

```bash
# In crontab
0 2 * * * SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL" /home/unique/projects/BIM/run-daily-backup.sh
```

Or set as environment variable:
```bash
export SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

## Backup Retention Policy

### Default Settings
- **Database Backups:** Kept for 30 days
- **Uploads Backups:** Kept for 30 days
- **Docker Backups:** Kept for 30 days
- **Application Code:** Kept for 30 days

### Modify Retention Period

Edit the backup script and change `RETENTION_DAYS`:
```bash
# In backup.sh, around line 30
RETENTION_DAYS=30        # Change this value
```

Or use cleanup command:
```bash
# Cleanup files older than 14 days
./backup-uploads.sh cleanup 14
```

## Security Best Practices

### 1. Protect Backup Directory
```bash
# Set proper permissions
chmod 700 backups/
chmod 600 backups/database/*.gz
chmod 600 backups/uploads/*.tar.gz
```

### 2. Store Backups Externally
```bash
# Sync to external drive or cloud storage
rsync -av backups/ /mnt/external-drive/bim-backups/
```

### 3. Encrypt Sensitive Backups
```bash
# Encrypt database backup
gpg --symmetric backups/database/geobiro_db_*.sql.gz

# Decrypt when needed
gpg --decrypt backups/database/geobiro_db_*.sql.gz.gpg > backup.sql
```

### 4. Secure Credentials
```bash
# Create .env file for sensitive variables
echo "DB_PASSWORD=geobiro_password" > .env.backup
chmod 600 .env.backup

# Use in scripts
source .env.backup
```

## Troubleshooting

### PostgreSQL Connection Error
```bash
# Check if container is running
docker ps | grep postgres

# Test connection
docker exec postgres pg_isready -U geobiro

# View logs
docker logs postgres
```

### Docker Daemon Not Running
```bash
# Restart Docker
sudo systemctl restart docker

# Or on macOS
open -a Docker
```

### Permission Denied Error
```bash
# Make scripts executable
chmod +x backup*.sh run-daily-backup.sh
```

### Disk Space Issues
```bash
# Check available space
df -h /

# Show largest backups
du -sh backups/* | sort -rh

# Cleanup immediately
./backup.sh cleanup
```

### Cron Job Not Running
```bash
# Check cron logs
grep CRON /var/log/syslog
sudo journalctl -u cron

# Verify crontab syntax
crontab -l

# Check cron is running
sudo systemctl status cron
```

## Testing Restores

### It's Critical to Test Backups!

**Test Database Restore:**
```bash
# Create test database
docker exec postgres psql -U geobiro -c "CREATE DATABASE test_db;"

# Restore to test database
./backup-database.sh restore backups/database/geobiro_db_*.sql.gz
```

**Test Uploads Restore:**
```bash
# Create test directory
mkdir -p backend/uploads-test/

# Extract backup there
tar -xzf backups/uploads/uploads_*.tar.gz -C backend/uploads-test/
```

## Advanced Usage

### Backup Specific Tables Only
```bash
./backup-database.sh table articles
./backup-database.sh table users
./backup-database.sh table projects
```

### Create Archive for Long-term Storage
```bash
./backup-uploads.sh archive
```

### Verify Backup Integrity
```bash
./backup-uploads.sh verify backups/uploads/uploads_*.tar.gz
```

### Monitor Database Size
```bash
./backup-database.sh stats
```

## Support Resources

- Full documentation: `BACKUP_README.md`
- Quick reference: `BACKUP_QUICK_REFERENCE.sh`
- Script help: `./backup.sh help` (for any script)

## Next Steps

1. ✅ Review all scripts (read the help output)
2. ✅ Run a full backup test
3. ✅ Test a restore procedure
4. ✅ Set up automated cron jobs
5. ✅ Configure notifications (email/Slack)
6. ✅ Store backups externally
7. ✅ Monitor backup logs regularly
8. ✅ Document your backup procedures

## Support & Maintenance

### Regular Maintenance Tasks

- **Daily:** Monitor backup logs for errors
- **Weekly:** Verify backup integrity
- **Monthly:** Test restore procedures
- **Quarterly:** Review and update backup strategy
- **Yearly:** Audit backup storage and retention

### Getting Help

```bash
# View help for any script
./backup.sh help
./backup-database.sh help
./backup-uploads.sh help
./backup-docker.sh help

# Read full documentation
less BACKUP_README.md

# Check logs for errors
cat backups/logs/backup_$(date +%Y-%m-%d).log
```

## Summary

You now have:
- ✅ 5 comprehensive backup scripts
- ✅ Automated backup orchestration
- ✅ Multiple backup types (database, uploads, Docker)
- ✅ Automatic retention and cleanup
- ✅ Notification support (email, Slack)
- ✅ Recovery procedures
- ✅ Monitoring and logging
- ✅ Complete documentation

**Your backups are ready to use!** 🎉

Start with: `./backup.sh full`
