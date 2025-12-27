# BIM Project - Backup Management Guide

## Overview

This project includes comprehensive backup scripts for Docker containers, database, and uploads. There are three main backup scripts:

- **backup.sh** - Main orchestration script for all backups
- **backup-database.sh** - PostgreSQL database backups
- **backup-uploads.sh** - Uploads directory backups
- **backup-docker.sh** - Docker containers and volumes

## Quick Start

### Make Scripts Executable

```bash
chmod +x backup.sh
chmod +x backup-database.sh
chmod +x backup-uploads.sh
chmod +x backup-docker.sh
```

### Perform Full Backup

```bash
./backup.sh full
```

This will backup:
- PostgreSQL database
- Uploads directory
- Docker volumes (PostgreSQL and Redis)
- Application code

## Backup Scripts Details

### 1. backup.sh - Main Backup Orchestration

**Usage:**
```bash
./backup.sh [COMMAND]
```

**Commands:**
- `full` - Perform complete backup (default)
- `database` - Database backup only
- `uploads` - Uploads backup only
- `volumes` - Docker volumes backup only
- `code` - Application code backup only
- `cleanup` - Remove old backups (older than 30 days)
- `list` - List all available backups
- `restore-db <file>` - Restore database from backup

**Example:**
```bash
./backup.sh full          # Full backup
./backup.sh list          # List backups
./backup.sh cleanup       # Remove old backups
```

### 2. backup-database.sh - PostgreSQL Database

**Usage:**
```bash
./backup-database.sh [COMMAND]
```

**Commands:**
- `full` - Full database backup in SQL format
- `custom` - Custom format backup (better for large databases)
- `table <TABLE_NAME>` - Backup specific table
- `list` - List all database backups
- `restore <FILE>` - Restore from backup
- `stats` - Show database statistics

**Examples:**
```bash
# Create full backup
./backup-database.sh full

# Backup specific table
./backup-database.sh table articles

# Show database statistics
./backup-database.sh stats

# List all backups
./backup-database.sh list

# Restore from backup
./backup-database.sh restore backups/database/geobiro_db_20250101_120000.sql.gz
```

**Backup Format:**
- SQL format (plain text, compressed with gzip)
- Custom format (binary, better for large databases)
- All backups are automatically compressed

**Database Info:**
- Database: `geobiro_db`
- User: `geobiro`
- Host: `localhost` (via Docker)
- Port: `5432`

### 3. backup-uploads.sh - Uploads Management

**Usage:**
```bash
./backup-uploads.sh [COMMAND]
```

**Commands:**
- `full` - Full uploads backup
- `daily` - Create daily uploads backup
- `specific <PATH>` - Backup specific file/directory
- `list` - List all upload backups
- `restore <FILE>` - Restore from backup
- `stats` - Show uploads statistics
- `archive` - Create long-term storage archive
- `verify <FILE>` - Verify backup integrity
- `cleanup [DAYS]` - Remove old backups

**Examples:**
```bash
# Create full uploads backup
./backup-uploads.sh full

# Create daily backup
./backup-uploads.sh daily

# Backup specific files
./backup-uploads.sh specific images/photo.jpg

# Show statistics
./backup-uploads.sh stats

# Verify backup integrity
./backup-uploads.sh verify backups/uploads/uploads_full_20250101_120000.tar.gz

# Restore uploads
./backup-uploads.sh restore backups/uploads/uploads_full_20250101_120000.tar.gz

# Cleanup old backups (older than 30 days)
./backup-uploads.sh cleanup 30
```

### 4. backup-docker.sh - Docker Containers & Volumes

**Usage:**
```bash
./backup-docker.sh [COMMAND]
```

**Commands:**
- `full` - Complete Docker backup
- `postgres` - PostgreSQL container and volume
- `redis` - Redis container and volume
- `backend` - Backend container configuration
- `images` - Export Docker images
- `compose` - Backup docker-compose files
- `status` - Show container status
- `volumes` - Show volume information
- `list` - List all Docker backups
- `cleanup` - Remove old backups

**Examples:**
```bash
# Full Docker backup
./backup-docker.sh full

# Backup specific container
./backup-docker.sh postgres
./backup-docker.sh redis

# Export Docker images
./backup-docker.sh images

# Show container status
./backup-docker.sh status

# List all backups
./backup-docker.sh list
```

## Backup Directory Structure

```
backups/
├── database/              # PostgreSQL backups
│   ├── geobiro_db_*.sql.gz
│   └── MANIFEST_*.txt
├── uploads/              # Uploads directory backups
│   ├── YYYY-MM-DD/
│   └── uploads_*.tar.gz
├── docker/              # Docker backups
│   ├── volumes/         # Volume backups
│   ├── images/          # Exported Docker images
│   └── configs/         # Container configurations
└── logs/               # Backup logs
```

## Backup Configuration

### Default Settings

- **Retention Period:** 30 days (automatically delete older backups)
- **Compression:** All backups are compressed (gzip for SQL, tar.gz for files)
- **Database:** PostgreSQL 15
- **Volumes:** postgres_data, redis_data
- **Uploads Directory:** backend/uploads/

### Modify Configuration

Edit the scripts to change:
- Backup retention days
- Database credentials
- Container/volume names
- Backup directory location

Example (in backup.sh):
```bash
RETENTION_DAYS=30        # Change backup retention
DB_USER="geobiro"        # PostgreSQL user
DB_PASSWORD="..."        # PostgreSQL password
DB_NAME="geobiro_db"     # Database name
```

## Scheduling Backups

### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/unique/projects/BIM/backup.sh full

# Add hourly database backup
0 * * * * /home/unique/projects/BIM/backup-database.sh full

# Add daily uploads backup
30 2 * * * /home/unique/projects/BIM/backup-uploads.sh daily

# Weekly Docker backup (Sunday at 3 AM)
0 3 * * 0 /home/unique/projects/BIM/backup-docker.sh full

# Daily cleanup (remove backups older than 30 days)
0 4 * * * /home/unique/projects/BIM/backup.sh cleanup
```

### Using Docker Cron Container

Create a `docker-compose-backup.yml`:

```yaml
version: '3.8'

services:
  backup-scheduler:
    image: mcuadros/ofelia:latest
    container_name: backup-scheduler
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: daemon --docker
    environment:
      - SCHEDULER_DOCKER=true
```

## Restore Instructions

### Restore Database

```bash
# From backup.sh
./backup.sh restore-db backups/database/geobiro_db_20250101_120000.sql.gz

# From backup-database.sh
./backup-database.sh restore backups/database/geobiro_db_20250101_120000.sql.gz
```

### Restore Uploads

```bash
./backup-uploads.sh restore backups/uploads/uploads_full_20250101_120000.tar.gz
```

### Restore Docker Volumes

```bash
# PostgreSQL
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd)/backups/docker/volumes:/backup \
  alpine tar -xzf /backup/postgres_volume_20250101_120000.tar.gz -C /data

# Redis
docker run --rm \
  -v redis_data:/data \
  -v $(pwd)/backups/docker/volumes:/backup \
  alpine tar -xzf /backup/redis_volume_20250101_120000.tar.gz -C /data
```

### Restore Docker Images

```bash
docker load -i backups/docker/images/postgres_15-alpine_20250101_120000.tar.gz
docker load -i backups/docker/images/redis_7-alpine_20250101_120000.tar.gz
```

## Backup Verification

### Verify Database Backup

```bash
# List tables in backup
gunzip -c backups/database/geobiro_db_*.sql.gz | head -100
```

### Verify Upload Backup

```bash
# List contents
./backup-uploads.sh verify backups/uploads/uploads_full_*.tar.gz

# Or manually
tar -tzf backups/uploads/uploads_full_*.tar.gz | head
```

### Verify Docker Volume Backup

```bash
# List contents
tar -tzf backups/docker/volumes/postgres_volume_*.tar.gz | head
```

## Best Practices

### 1. **Regular Testing**
- Test restore procedures regularly
- Keep a test environment for restore verification
- Document any issues found

### 2. **Backup Storage**
- Store backups in multiple locations
- Use external storage for critical backups
- Consider cloud storage for disaster recovery

### 3. **Backup Monitoring**
- Check backup logs regularly
- Set up alerts for failed backups
- Monitor available disk space

### 4. **Documentation**
- Keep backup schedules documented
- Document any customizations made
- Maintain restore procedure documentation

### 5. **Security**
- Protect backup files with appropriate permissions
- Encrypt sensitive backups
- Limit access to backup storage

## Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs postgres

# Test connection
docker exec postgres pg_isready -U geobiro
```

### Docker Daemon Issues

```bash
# Check Docker status
docker ps

# Restart Docker daemon
sudo systemctl restart docker
```

### Permission Issues

```bash
# Make scripts executable
chmod +x backup*.sh

# Check backup directory permissions
ls -la backups/
```

### Disk Space Issues

```bash
# Check disk usage
du -sh backups/

# Show largest files
du -sh backups/* | sort -rh

# Cleanup old backups
./backup.sh cleanup
```

## Backup Size Estimation

- **Database:** 10-100 MB (compressed)
- **Uploads:** Varies (typically 100 MB - 1 GB)
- **Docker Volumes:** 50-200 MB (compressed)
- **Application Code:** 10-50 MB (compressed)
- **Total:** ~200 MB - 1.5 GB per full backup

## Support and Maintenance

### Log Files

Backup logs are stored in `backups/logs/`

### Backup Summaries

Each backup includes a summary file with:
- Backup timestamp
- File sizes
- Backup method used
- Restore instructions

### Monitoring Backups

```bash
# List recent backups
./backup.sh list

# Check backup sizes
du -sh backups/database/*
du -sh backups/uploads/*
du -sh backups/docker/volumes/*
```

## Advanced Usage

### Backup with Custom Retention

```bash
# Cleanup backups older than 14 days
./backup.sh cleanup
```

### Incremental-like Backups

```bash
# Create daily dated backups
./backup-uploads.sh daily
```

### Archive Old Backups

```bash
# Create archive for long-term storage
./backup-uploads.sh archive
```

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Backup Best Practices](https://en.wikipedia.org/wiki/Backup)

## Notes

- All backup scripts are idempotent and safe to run multiple times
- Backups are automatically compressed to save space
- Old backups are automatically deleted based on retention policy
- Always test restore procedures before relying on backups
- Keep backups in multiple locations for disaster recovery
