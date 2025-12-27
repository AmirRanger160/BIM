#!/bin/bash

#################################################################################
# BIM Project - Backup Management Script
# Purpose: Centralized backup orchestration for Docker containers, uploads, and database
# Author: System Admin
# Date: 2025
#################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_BASE_DIR="${PROJECT_DIR}/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DATE=$(date +%Y-%m-%d)

# Database configuration from docker-compose
DB_USER="geobiro"
DB_PASSWORD="geobiro_password"
DB_NAME="geobiro_db"
DB_HOST="localhost"
DB_PORT="5432"
DB_CONTAINER="postgres"

# Backup retention (days)
RETENTION_DAYS=30

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Create backup directories
create_backup_dirs() {
    log "Creating backup directories..."
    mkdir -p "${BACKUP_BASE_DIR}/database"
    mkdir -p "${BACKUP_BASE_DIR}/uploads"
    mkdir -p "${BACKUP_BASE_DIR}/docker-volumes"
    mkdir -p "${BACKUP_BASE_DIR}/logs"
    success "Backup directories created"
}

# Backup database
backup_database() {
    log "Starting database backup..."
    
    local backup_file="${BACKUP_BASE_DIR}/database/geobiro_db_${TIMESTAMP}.sql"
    
    # Check if PostgreSQL container is running
    if ! docker ps | grep -q "${DB_CONTAINER}"; then
        error "PostgreSQL container is not running"
        return 1
    fi
    
    # Create database dump
    if docker exec ${DB_CONTAINER} pg_dump \
        -U ${DB_USER} \
        -d ${DB_NAME} \
        --no-password \
        --format=plain \
        --verbose > "${backup_file}"; then
        
        # Compress the backup
        gzip "${backup_file}"
        local compressed_file="${backup_file}.gz"
        
        local size=$(du -h "${compressed_file}" | cut -f1)
        success "Database backup completed: ${compressed_file} (${size})"
        
        # Create backup info file
        echo "Database Backup Info
====================
File: ${compressed_file}
Size: ${size}
Timestamp: ${TIMESTAMP}
Database: ${DB_NAME}
User: ${DB_USER}
Compressed: Yes
" > "${BACKUP_BASE_DIR}/database/BACKUP_${TIMESTAMP}.txt"
        
        return 0
    else
        error "Failed to create database backup"
        return 1
    fi
}

# Backup uploads directory
backup_uploads() {
    log "Starting uploads backup..."
    
    local uploads_dir="${PROJECT_DIR}/backend/uploads"
    local backup_file="${BACKUP_BASE_DIR}/uploads/uploads_${TIMESTAMP}.tar.gz"
    
    if [ ! -d "${uploads_dir}" ]; then
        warning "Uploads directory not found: ${uploads_dir}"
        return 0
    fi
    
    if [ "$(ls -A ${uploads_dir})" ]; then
        if tar -czf "${backup_file}" -C "${PROJECT_DIR}/backend" uploads; then
            local size=$(du -h "${backup_file}" | cut -f1)
            success "Uploads backup completed: ${backup_file} (${size})"
            
            # Create backup info
            echo "Uploads Backup Info
===================
File: ${backup_file}
Size: ${size}
Timestamp: ${TIMESTAMP}
Source: ${uploads_dir}
Compressed: Yes (tar.gz)
" > "${BACKUP_BASE_DIR}/uploads/BACKUP_${TIMESTAMP}.txt"
            return 0
        else
            error "Failed to create uploads backup"
            return 1
        fi
    else
        warning "Uploads directory is empty"
        return 0
    fi
}

# Backup Docker volumes
backup_docker_volumes() {
    log "Starting Docker volumes backup..."
    
    local postgres_volume="postgres_data"
    local redis_volume="redis_data"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    # Create temporary directory for volume backup
    local temp_dir=$(mktemp -d)
    local backup_dir="${BACKUP_BASE_DIR}/docker-volumes/${TIMESTAMP}"
    mkdir -p "${backup_dir}"
    
    # Backup PostgreSQL volume
    log "Backing up PostgreSQL volume..."
    if docker run --rm \
        -v ${postgres_volume}:/data \
        -v "${backup_dir}":/backup \
        alpine tar -czf /backup/postgres_volume_${TIMESTAMP}.tar.gz -C /data .; then
        success "PostgreSQL volume backup completed"
    else
        warning "PostgreSQL volume backup failed"
    fi
    
    # Backup Redis volume
    log "Backing up Redis volume..."
    if docker run --rm \
        -v ${redis_volume}:/data \
        -v "${backup_dir}":/backup \
        alpine tar -czf /backup/redis_volume_${TIMESTAMP}.tar.gz -C /data .; then
        success "Redis volume backup completed"
    else
        warning "Redis volume backup failed"
    fi
    
    # Create backup info
    echo "Docker Volumes Backup Info
===========================
Timestamp: ${TIMESTAMP}
PostgreSQL Volume: postgres_data
Redis Volume: redis_data
" > "${backup_dir}/BACKUP_INFO.txt"
    
    rm -rf "${temp_dir}"
}

# Backup application code
backup_application_code() {
    log "Starting application code backup..."
    
    local backup_file="${BACKUP_BASE_DIR}/docker-volumes/app_code_${TIMESTAMP}.tar.gz"
    
    # Exclude common unnecessary directories
    if tar -czf "${backup_file}" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env' \
        --exclude='dist' \
        --exclude='build' \
        --exclude='.venv' \
        --exclude='venv' \
        -C "${PROJECT_DIR}" . ; then
        
        local size=$(du -h "${backup_file}" | cut -f1)
        success "Application code backup completed: ${backup_file} (${size})"
        return 0
    else
        error "Failed to backup application code"
        return 1
    fi
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
    
    find "${BACKUP_BASE_DIR}" -type f -mtime +${RETENTION_DAYS} -delete
    find "${BACKUP_BASE_DIR}" -type d -empty -delete
    
    success "Old backups cleaned up"
}

# Create backup summary
create_backup_summary() {
    local summary_file="${BACKUP_BASE_DIR}/BACKUP_SUMMARY_${TIMESTAMP}.txt"
    
    cat > "${summary_file}" << EOF
================================================================================
BIM Project - Backup Summary Report
================================================================================
Generated: $(date '+%Y-%m-%d %H:%M:%S')
Backup Directory: ${BACKUP_BASE_DIR}

Backup Contents:
================

1. Database Backups (${BACKUP_BASE_DIR}/database/)
   - Format: PostgreSQL dump (compressed with gzip)
   - Database: ${DB_NAME}
   - Retention: ${RETENTION_DAYS} days

2. Uploads Backups (${BACKUP_BASE_DIR}/uploads/)
   - Format: TAR.GZ
   - Source: ${PROJECT_DIR}/backend/uploads/
   - Retention: ${RETENTION_DAYS} days

3. Docker Volumes (${BACKUP_BASE_DIR}/docker-volumes/)
   - PostgreSQL data volume
   - Redis data volume
   - Application code

Backup Statistics:
==================
Total Backup Size: $(du -sh "${BACKUP_BASE_DIR}" 2>/dev/null | cut -f1)
Number of Database Backups: $(ls -1 "${BACKUP_BASE_DIR}/database"/*.gz 2>/dev/null | wc -l)
Number of Upload Backups: $(ls -1 "${BACKUP_BASE_DIR}/uploads"/*.gz 2>/dev/null | wc -l)

Restore Instructions:
====================

1. Restore Database:
   gunzip -c backups/database/geobiro_db_TIMESTAMP.sql.gz | docker exec -i postgres psql -U geobiro -d geobiro_db

2. Restore Uploads:
   tar -xzf backups/uploads/uploads_TIMESTAMP.tar.gz -C backend/

3. Restore Docker Volumes:
   docker volume rm postgres_data
   docker run --rm -v postgres_data:/data -v $(pwd)/backups/docker-volumes:/backup alpine tar -xzf /backup/postgres_volume_TIMESTAMP.tar.gz -C /data

System Information:
===================
Hostname: $(hostname)
OS: $(uname -s)
Docker Version: $(docker --version 2>/dev/null || echo "N/A")
PostgreSQL Container: ${DB_CONTAINER}

Notes:
======
- Backups are compressed to save space
- Old backups are automatically deleted after ${RETENTION_DAYS} days
- Always test restore procedures regularly
- Store critical backups in multiple locations

================================================================================
EOF
    
    log "Backup summary created: ${summary_file}"
}

# Main backup function
perform_full_backup() {
    log "=========================================="
    log "Starting Full Backup Suite"
    log "=========================================="
    
    create_backup_dirs
    
    local backup_failed=0
    
    # Run backups
    backup_database || ((backup_failed++))
    backup_uploads || ((backup_failed++))
    backup_docker_volumes || ((backup_failed++))
    backup_application_code || ((backup_failed++))
    
    # Cleanup
    cleanup_old_backups
    
    # Create summary
    create_backup_summary
    
    log "=========================================="
    if [ $backup_failed -eq 0 ]; then
        success "Full backup completed successfully!"
        log "Backup location: ${BACKUP_BASE_DIR}"
    else
        warning "Backup completed with ${backup_failed} warning(s)"
    fi
    log "=========================================="
}

# Show help
show_help() {
    cat << EOF
BIM Project Backup Management Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  full              Perform full backup (default)
  database          Backup only database
  uploads           Backup only uploads
  volumes           Backup only Docker volumes
  code              Backup only application code
  cleanup           Remove old backups
  list              List all backups
  restore-db        Restore database backup (requires file path)
  help              Show this help message

Options:
  --dry-run         Show what would be backed up without actually doing it
  --retention DAYS  Override default retention period (default: ${RETENTION_DAYS})
  --verbose         Show detailed output

Examples:
  $0                                # Perform full backup
  $0 database                       # Backup only database
  $0 restore-db backups/database/geobiro_db_20250101_120000.sql.gz
  $0 cleanup                        # Remove old backups

EOF
}

# List all backups
list_backups() {
    log "Available backups:"
    echo ""
    
    if [ -d "${BACKUP_BASE_DIR}" ]; then
        find "${BACKUP_BASE_DIR}" -type f \( -name "*.gz" -o -name "*.sql" -o -name "*.txt" \) -printf "%T+ %s %p\n" | sort -r | awk '{printf "%-25s %10s %s\n", $1, $2, substr($3, length(ENVIRON["BACKUP_BASE_DIR"])+2)}'
    else
        warning "No backups found"
    fi
}

# Main script logic
main() {
    case "${1:-full}" in
        full)
            perform_full_backup
            ;;
        database)
            create_backup_dirs
            backup_database
            ;;
        uploads)
            create_backup_dirs
            backup_uploads
            ;;
        volumes)
            create_backup_dirs
            backup_docker_volumes
            ;;
        code)
            create_backup_dirs
            backup_application_code
            ;;
        cleanup)
            cleanup_old_backups
            ;;
        list)
            list_backups
            ;;
        restore-db)
            if [ -z "$2" ]; then
                error "Please provide backup file path"
                show_help
                exit 1
            fi
            # Restore database logic
            log "Restoring database from: $2"
            if [ -f "$2" ]; then
                if [[ "$2" == *.gz ]]; then
                    gunzip -c "$2" | docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME}
                else
                    docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME} < "$2"
                fi
                success "Database restored successfully"
            else
                error "Backup file not found: $2"
                exit 1
            fi
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
