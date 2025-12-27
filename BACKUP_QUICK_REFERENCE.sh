#!/bin/bash

# Quick reference for all backup commands

# ============================================================================
# QUICK START
# ============================================================================

# Make all scripts executable (run once)
chmod +x backup.sh backup-database.sh backup-uploads.sh backup-docker.sh run-daily-backup.sh

# Perform full backup now
./backup.sh full

# ============================================================================
# MAIN BACKUP SCRIPT (backup.sh)
# ============================================================================

./backup.sh full                           # Full backup (everything)
./backup.sh database                       # Database only
./backup.sh uploads                        # Uploads only
./backup.sh volumes                        # Docker volumes only
./backup.sh code                          # Application code only
./backup.sh list                          # List all backups
./backup.sh cleanup                       # Remove old backups
./backup.sh restore-db <file>            # Restore database

# ============================================================================
# DATABASE BACKUP (backup-database.sh)
# ============================================================================

./backup-database.sh full                 # Full SQL backup
./backup-database.sh custom              # Custom format (large DB)
./backup-database.sh table <name>        # Backup specific table
./backup-database.sh list                # List backups
./backup-database.sh restore <file>      # Restore from backup
./backup-database.sh stats               # Database statistics

# Example - Backup specific tables
./backup-database.sh table articles
./backup-database.sh table users
./backup-database.sh table projects

# ============================================================================
# UPLOADS BACKUP (backup-uploads.sh)
# ============================================================================

./backup-uploads.sh full                 # Full uploads backup
./backup-uploads.sh daily                # Daily dated backup
./backup-uploads.sh specific <path>      # Backup specific file/dir
./backup-uploads.sh list                 # List backups
./backup-uploads.sh restore <file>       # Restore uploads
./backup-uploads.sh stats                # Show statistics
./backup-uploads.sh archive              # Create long-term archive
./backup-uploads.sh verify <file>        # Verify backup integrity
./backup-uploads.sh cleanup [DAYS]       # Remove old backups

# Example - Backup specific files
./backup-uploads.sh specific images/
./backup-uploads.sh specific documents/report.pdf

# ============================================================================
# DOCKER BACKUP (backup-docker.sh)
# ============================================================================

./backup-docker.sh full                  # Full Docker backup
./backup-docker.sh postgres              # PostgreSQL only
./backup-docker.sh redis                 # Redis only
./backup-docker.sh backend               # Backend config
./backup-docker.sh images                # Export Docker images
./backup-docker.sh compose               # Docker-compose files
./backup-docker.sh status                # Container status
./backup-docker.sh volumes               # Volume info
./backup-docker.sh list                  # List backups
./backup-docker.sh cleanup               # Remove old backups

# ============================================================================
# AUTOMATED DAILY BACKUP
# ============================================================================

./run-daily-backup.sh                    # Run full automated backup

# Add to crontab for daily at 2 AM
# crontab -e
# 0 2 * * * /home/unique/projects/BIM/run-daily-backup.sh

# ============================================================================
# RESTORE PROCEDURES
# ============================================================================

# Restore database
./backup-database.sh restore backups/database/geobiro_db_20250101_120000.sql.gz

# Restore uploads
./backup-uploads.sh restore backups/uploads/uploads_full_20250101_120000.tar.gz

# Restore Docker volume (PostgreSQL)
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd)/backups/docker/volumes:/backup \
  alpine tar -xzf /backup/postgres_volume_20250101_120000.tar.gz -C /data

# Restore Docker images
docker load -i backups/docker/images/postgres_15-alpine_20250101_120000.tar.gz
docker load -i backups/docker/images/redis_7-alpine_20250101_120000.tar.gz

# ============================================================================
# MONITORING & MAINTENANCE
# ============================================================================

# List all backups
./backup.sh list

# Show backup sizes
du -sh backups/*
du -sh backups/database/*
du -sh backups/uploads/*
du -sh backups/docker/*

# Show latest backups
ls -lt backups/**/* | head -20

# Check backup integrity
./backup-uploads.sh verify backups/uploads/uploads_full_*.tar.gz
tar -tzf backups/docker/volumes/*.tar.gz > /dev/null

# Clean up old backups (older than 30 days)
./backup.sh cleanup
./backup-uploads.sh cleanup 30

# Check Docker status
./backup-docker.sh status

# Show database statistics
./backup-database.sh stats

# ============================================================================
# SYSTEM CHECKS
# ============================================================================

# Check available disk space
df -h /

# Check backup directory size
du -sh backups/

# Check Docker containers
docker ps -a

# Check Docker volumes
docker volume ls

# Check PostgreSQL container logs
docker logs postgres

# Check Redis container logs
docker logs redis

# ============================================================================
# SCHEDULING WITH CRON
# ============================================================================

# Edit crontab
crontab -e

# Add these lines for automated backups:

# Daily full backup at 2 AM
0 2 * * * /home/unique/projects/BIM/backup.sh full

# Hourly database backup
0 * * * * /home/unique/projects/BIM/backup-database.sh full

# Daily uploads backup at 2:30 AM
30 2 * * * /home/unique/projects/BIM/backup-uploads.sh daily

# Weekly Docker backup (Sunday at 3 AM)
0 3 * * 0 /home/unique/projects/BIM/backup-docker.sh full

# Daily cleanup (4 AM)
0 4 * * * /home/unique/projects/BIM/backup.sh cleanup

# Automated daily backup with notifications (2 AM)
0 2 * * * /home/unique/projects/BIM/run-daily-backup.sh

# ============================================================================
# COMMON WORKFLOWS
# ============================================================================

# Daily routine
./backup-database.sh full
./backup-uploads.sh daily
./backup-docker.sh postgres

# Weekly full backup
./backup.sh full

# Before major changes
./backup.sh full

# After backup verification
./backup.sh list
tar -tzf backups/uploads/*.tar.gz | head
gunzip -c backups/database/*.sql.gz | head

# ============================================================================
# CONFIGURATION FILES
# ============================================================================

# Edit configuration in scripts:
# - backup.sh: RETENTION_DAYS, DB_USER, DB_PASSWORD, etc.
# - run-daily-backup.sh: SEND_EMAIL, EMAIL_TO, SLACK_WEBHOOK, etc.

# Configuration for automated backup with email
export SEND_EMAIL=true
export EMAIL_TO="admin@example.com"
export SLACK_WEBHOOK="https://hooks.slack.com/..."

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# PostgreSQL not responding
docker exec postgres pg_isready -U geobiro

# Check PostgreSQL logs
docker logs postgres | tail -20

# Check container status
docker ps | grep postgres

# Test database connection
docker exec postgres psql -U geobiro -d geobiro_db -c "SELECT 1"

# Check disk space
df -h / && du -sh backups/

# View backup logs
cat backups/logs/*.log
tail -f backups/logs/backup_$(date +%Y-%m-%d).log

# ============================================================================
# BACKUP DIRECTORY STRUCTURE
# ============================================================================

# backups/
# ├── database/           # SQL backups
# ├── uploads/            # File backups
# ├── docker/             # Container & volume backups
# │   ├── volumes/
# │   ├── images/
# │   └── configs/
# ├── logs/               # Backup logs
# └── BACKUP_SUMMARY_*.txt

# ============================================================================
# IMPORTANT NOTES
# ============================================================================

# 1. Always test restore procedures
# 2. Store backups in multiple locations
# 3. Monitor backup success regularly
# 4. Document any customizations
# 5. Keep credentials secure
# 6. Review logs for errors
# 7. Test before relying on backups
# 8. Update cron jobs as needed

# ============================================================================
# NEED HELP?
# ============================================================================

# Show help for any script
./backup.sh help
./backup-database.sh help
./backup-uploads.sh help
./backup-docker.sh help

# Read full documentation
cat BACKUP_README.md

# ============================================================================
