#!/bin/bash

#################################################################################
# Database Backup Script for PostgreSQL
# Purpose: Create and manage PostgreSQL database backups
#################################################################################

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${PROJECT_DIR}/backups/database"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y-%m-%d)

# Database credentials (from docker-compose.yml)
DB_USER="geobiro"
DB_PASSWORD="geobiro_password"
DB_NAME="geobiro_db"
DB_HOST="localhost"
DB_PORT="5432"
DB_CONTAINER="postgres"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
error() { echo -e "${RED}✗ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠ $1${NC}"; }

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Check if PostgreSQL container is running
check_postgres() {
    if ! docker ps | grep -q "${DB_CONTAINER}"; then
        error "PostgreSQL container '${DB_CONTAINER}' is not running"
        error "Start it with: docker-compose up -d postgres"
        exit 1
    fi
}

# Create full backup
create_full_backup() {
    log "Creating full database backup for '${DB_NAME}'..."
    
    local backup_file="${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.sql"
    
    PGPASSWORD="${DB_PASSWORD}" docker exec -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
        pg_dump -U ${DB_USER} -d ${DB_NAME} --no-password --format=plain \
        --verbose > "${backup_file}" 2>&1
    
    if [ $? -eq 0 ]; then
        # Compress backup
        gzip -9 "${backup_file}"
        local compressed="${backup_file}.gz"
        local size=$(du -h "${compressed}" | cut -f1)
        
        success "Full backup created: ${compressed} (${size})"
        
        # Create manifest
        echo "Full Database Backup
====================
File: $(basename "${compressed}")
Size: ${size}
Timestamp: ${TIMESTAMP}
Database: ${DB_NAME}
Backup Type: FULL
Format: SQL (compressed)
" > "${BACKUP_DIR}/MANIFEST_${TIMESTAMP}.txt"
        
    else
        error "Failed to create database backup"
        exit 1
    fi
}

# Create custom format backup (better for large databases)
create_custom_backup() {
    log "Creating custom format database backup..."
    
    local backup_file="${BACKUP_DIR}/${DB_NAME}_custom_${TIMESTAMP}.dump"
    
    PGPASSWORD="${DB_PASSWORD}" docker exec -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
        pg_dump -U ${DB_USER} -d ${DB_NAME} --no-password --format=custom \
        --file "${backup_file}" -v
    
    if [ $? -eq 0 ]; then
        # Compress
        gzip -9 "${backup_file}"
        local compressed="${backup_file}.gz"
        local size=$(du -h "${compressed}" | cut -f1)
        
        success "Custom format backup created: ${compressed} (${size})"
    else
        error "Failed to create custom format backup"
        exit 1
    fi
}

# Create backup with specific table
backup_specific_table() {
    local table="$1"
    
    if [ -z "${table}" ]; then
        error "Please specify table name"
        exit 1
    fi
    
    log "Creating backup for table '${table}'..."
    
    local backup_file="${BACKUP_DIR}/${DB_NAME}_${table}_${TIMESTAMP}.sql"
    
    PGPASSWORD="${DB_PASSWORD}" docker exec -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
        pg_dump -U ${DB_USER} -d ${DB_NAME} --no-password \
        --table "${table}" > "${backup_file}"
    
    if [ $? -eq 0 ]; then
        gzip "${backup_file}"
        local size=$(du -h "${backup_file}.gz" | cut -f1)
        success "Table backup created: ${backup_file}.gz (${size})"
    else
        error "Failed to backup table '${table}'"
        exit 1
    fi
}

# List all backups
list_backups() {
    log "Database backups in ${BACKUP_DIR}:"
    echo ""
    
    if [ -d "${BACKUP_DIR}" ] && [ "$(ls -A ${BACKUP_DIR})" ]; then
        ls -lh "${BACKUP_DIR}" | grep -E '\.(sql|dump|gz)' | awk '{printf "%-12s %s\n", $5, $9}' | column -t
        echo ""
        log "Total backup size: $(du -sh ${BACKUP_DIR} | cut -f1)"
    else
        warning "No backups found"
    fi
}

# Restore from backup
restore_backup() {
    local backup_file="$1"
    
    if [ -z "${backup_file}" ]; then
        error "Please specify backup file"
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "${backup_file}" ]; then
        error "Backup file not found: ${backup_file}"
        exit 1
    fi
    
    # Warning before restore
    echo ""
    warning "CAUTION: This will restore the database from backup!"
    warning "Current database will be overwritten."
    echo ""
    read -p "Type 'yes' to confirm restore: " confirm
    
    if [ "${confirm}" != "yes" ]; then
        log "Restore cancelled"
        exit 0
    fi
    
    log "Restoring database from: ${backup_file}..."
    
    # Handle compressed files
    if [[ "${backup_file}" == *.gz ]]; then
        gunzip -c "${backup_file}" | PGPASSWORD="${DB_PASSWORD}" docker exec -i \
            -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
            psql -U ${DB_USER} -d ${DB_NAME} --no-password
    else
        PGPASSWORD="${DB_PASSWORD}" docker exec -i \
            -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
            psql -U ${DB_USER} -d ${DB_NAME} --no-password < "${backup_file}"
    fi
    
    if [ $? -eq 0 ]; then
        success "Database restored successfully"
    else
        error "Failed to restore database"
        exit 1
    fi
}

# Get database statistics
show_stats() {
    log "Database Statistics for '${DB_NAME}':"
    echo ""
    
    docker exec -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
        psql -U ${DB_USER} -d ${DB_NAME} --no-password -c "
        SELECT 
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
        FROM pg_tables 
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;" || true
    
    echo ""
    log "Total database size:"
    docker exec -e PGPASSWORD="${DB_PASSWORD}" ${DB_CONTAINER} \
        psql -U ${DB_USER} -d ${DB_NAME} --no-password -c \
        "SELECT pg_size_pretty(pg_database_size('${DB_NAME}'));" || true
}

# Show help
show_help() {
    cat << EOF
PostgreSQL Database Backup Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  full              Create full database backup (SQL format)
  custom            Create custom format backup (for large databases)
  table TABLE       Backup specific table
  list              List all backups
  restore FILE      Restore from backup file
  stats             Show database statistics
  help              Show this help message

Examples:
  $0 full                           # Create full backup
  $0 custom                         # Create custom format backup
  $0 table articles                 # Backup only articles table
  $0 list                           # List all backups
  $0 restore backups/database/...   # Restore from backup
  $0 stats                          # Show database statistics

Configuration:
  Database: ${DB_NAME}
  User: ${DB_USER}
  Host: ${DB_HOST}
  Port: ${DB_PORT}
  Container: ${DB_CONTAINER}
  Backup Directory: ${BACKUP_DIR}

EOF
}

# Main script
main() {
    check_postgres
    
    case "${1:-full}" in
        full)
            create_full_backup
            ;;
        custom)
            create_custom_backup
            ;;
        table)
            backup_specific_table "$2"
            ;;
        list)
            list_backups
            ;;
        restore)
            restore_backup "$2"
            ;;
        stats)
            show_stats
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

main "$@"
