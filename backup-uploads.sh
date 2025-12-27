#!/bin/bash

#################################################################################
# Uploads Backup Script
# Purpose: Backup and manage uploads directory
#################################################################################

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPLOADS_DIR="${PROJECT_DIR}/backend/uploads"
BACKUP_DIR="${PROJECT_DIR}/backups/uploads"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y-%m-%d)

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

# Check if uploads directory exists
check_uploads_dir() {
    if [ ! -d "${UPLOADS_DIR}" ]; then
        warning "Uploads directory not found: ${UPLOADS_DIR}"
        log "Creating uploads directory..."
        mkdir -p "${UPLOADS_DIR}"
    fi
}

# Create full uploads backup
create_full_backup() {
    check_uploads_dir
    
    if [ ! "$(ls -A ${UPLOADS_DIR})" ]; then
        warning "Uploads directory is empty, nothing to backup"
        return 0
    fi
    
    log "Creating full uploads backup..."
    
    local backup_file="${BACKUP_DIR}/uploads_full_${TIMESTAMP}.tar.gz"
    
    if tar -czf "${backup_file}" -C "${PROJECT_DIR}/backend" uploads \
        --exclude='*.tmp' --exclude='.gitkeep'; then
        
        local size=$(du -h "${backup_file}" | cut -f1)
        local count=$(find "${UPLOADS_DIR}" -type f | wc -l)
        
        success "Uploads backup created: $(basename ${backup_file}) (${size}, ${count} files)"
        
        # Create manifest
        echo "Uploads Backup Manifest
======================
File: $(basename ${backup_file})
Size: ${size}
Files: ${count}
Timestamp: ${TIMESTAMP}
Source: ${UPLOADS_DIR}
Format: tar.gz
" > "${BACKUP_DIR}/MANIFEST_${TIMESTAMP}.txt"
        
    else
        error "Failed to create uploads backup"
        exit 1
    fi
}

# Create daily incremental-like backup
create_daily_backup() {
    check_uploads_dir
    
    log "Creating daily uploads backup..."
    
    local daily_dir="${BACKUP_DIR}/${DATE}"
    mkdir -p "${daily_dir}"
    
    local backup_file="${daily_dir}/uploads_${TIMESTAMP}.tar.gz"
    
    if tar -czf "${backup_file}" -C "${PROJECT_DIR}/backend" uploads \
        --exclude='*.tmp' --exclude='.gitkeep'; then
        
        local size=$(du -h "${backup_file}" | cut -f1)
        success "Daily backup created: $(basename ${backup_file}) (${size})"
        
    else
        error "Failed to create daily backup"
        exit 1
    fi
}

# Backup specific file/directory
backup_specific() {
    local target="$1"
    
    if [ -z "${target}" ]; then
        error "Please specify file or directory"
        exit 1
    fi
    
    local full_path="${UPLOADS_DIR}/${target}"
    
    if [ ! -e "${full_path}" ]; then
        error "File or directory not found: ${full_path}"
        exit 1
    fi
    
    log "Backing up: ${target}..."
    
    local backup_file="${BACKUP_DIR}/backup_${target//\//_}_${TIMESTAMP}.tar.gz"
    
    if tar -czf "${backup_file}" -C "${UPLOADS_DIR}" "${target}"; then
        local size=$(du -h "${backup_file}" | cut -f1)
        success "Backup created: $(basename ${backup_file}) (${size})"
    else
        error "Failed to backup: ${target}"
        exit 1
    fi
}

# List all backups
list_backups() {
    log "Uploads backups in ${BACKUP_DIR}:"
    echo ""
    
    if [ -d "${BACKUP_DIR}" ] && [ "$(ls -A ${BACKUP_DIR})" ]; then
        find "${BACKUP_DIR}" -type f -name "*.tar.gz" -o -name "*.tar" | while read file; do
            local size=$(du -h "${file}" | cut -f1)
            local name=$(basename "${file}")
            echo -e "${size}\t${name}"
        done | sort -k2 | awk '{printf "%-10s %s\n", $1, $2}' | column -t
        
        echo ""
        log "Total backup size: $(du -sh ${BACKUP_DIR} 2>/dev/null | cut -f1)"
    else
        warning "No backups found"
    fi
}

# Restore uploads backup
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
    
    # Warning
    echo ""
    warning "CAUTION: This will restore uploads from backup!"
    warning "Existing files will be overwritten."
    echo ""
    read -p "Type 'yes' to confirm: " confirm
    
    if [ "${confirm}" != "yes" ]; then
        log "Restore cancelled"
        exit 0
    fi
    
    log "Restoring uploads from: $(basename ${backup_file})..."
    
    # Create backup of current uploads
    if [ "$(ls -A ${UPLOADS_DIR})" ]; then
        log "Creating safety backup of current uploads..."
        tar -czf "${BACKUP_DIR}/uploads_before_restore_${TIMESTAMP}.tar.gz" \
            -C "${PROJECT_DIR}/backend" uploads 2>/dev/null || true
        success "Safety backup created"
    fi
    
    # Restore
    if tar -xzf "${backup_file}" -C "${PROJECT_DIR}/backend"; then
        success "Uploads restored successfully"
        log "Restored to: ${UPLOADS_DIR}"
    else
        error "Failed to restore uploads"
        exit 1
    fi
}

# Show uploads statistics
show_stats() {
    check_uploads_dir
    
    log "Uploads Directory Statistics:"
    echo ""
    
    if [ "$(ls -A ${UPLOADS_DIR})" ]; then
        echo "Total Size: $(du -sh ${UPLOADS_DIR} | cut -f1)"
        echo "Total Files: $(find ${UPLOADS_DIR} -type f | wc -l)"
        echo "Total Directories: $(find ${UPLOADS_DIR} -type d | wc -l)"
        echo ""
        echo "Breakdown by type:"
        find "${UPLOADS_DIR}" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | \
            awk '{printf "  %-10s: %5d files\n", $2, $1}'
        echo ""
        echo "Largest files:"
        find "${UPLOADS_DIR}" -type f -exec du -h {} + | sort -rh | head -10 | \
            awk '{printf "  %s\n", $0}'
    else
        warning "Uploads directory is empty"
    fi
}

# Cleanup old backups
cleanup_old_backups() {
    local days="${1:-30}"
    
    log "Removing backups older than ${days} days..."
    
    find "${BACKUP_DIR}" -type f -mtime +${days} -delete
    find "${BACKUP_DIR}" -type d -empty -delete
    
    success "Old backups cleaned up"
}

# Compress uploads for archival
archive_uploads() {
    local archive_name="uploads_archive_${TIMESTAMP}.tar.gz"
    local archive_file="${BACKUP_DIR}/${archive_name}"
    
    log "Creating archive: ${archive_name}..."
    
    if tar -czf "${archive_file}" -C "${PROJECT_DIR}/backend" uploads; then
        local size=$(du -h "${archive_file}" | cut -f1)
        success "Archive created: ${archive_name} (${size})"
        
        # Create archive info
        echo "Uploads Archive
===============
File: ${archive_name}
Size: ${size}
Timestamp: ${TIMESTAMP}
Files: $(find ${UPLOADS_DIR} -type f | wc -l)
Directories: $(find ${UPLOADS_DIR} -type d | wc -l)
" > "${BACKUP_DIR}/${archive_name}.info"
        
    else
        error "Failed to create archive"
        exit 1
    fi
}

# Verify backup integrity
verify_backup() {
    local backup_file="$1"
    
    if [ -z "${backup_file}" ]; then
        error "Please specify backup file"
        exit 1
    fi
    
    if [ ! -f "${backup_file}" ]; then
        error "Backup file not found: ${backup_file}"
        exit 1
    fi
    
    log "Verifying backup: $(basename ${backup_file})..."
    
    if tar -tzf "${backup_file}" > /dev/null 2>&1; then
        local file_count=$(tar -tzf "${backup_file}" | wc -l)
        success "Backup is valid and contains ${file_count} entries"
    else
        error "Backup is corrupted or invalid"
        exit 1
    fi
}

# Show help
show_help() {
    cat << EOF
Uploads Backup Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  full              Create full uploads backup
  daily             Create daily uploads backup
  specific FILE     Backup specific file/directory
  list              List all backups
  restore FILE      Restore from backup
  stats             Show uploads statistics
  archive           Create archive for long-term storage
  verify FILE       Verify backup integrity
  cleanup [DAYS]    Remove old backups (default: 30 days)
  help              Show this help message

Examples:
  $0 full                              # Create full backup
  $0 daily                             # Create daily backup
  $0 specific images/photo.jpg        # Backup specific file
  $0 restore backups/uploads/...      # Restore backup
  $0 stats                             # Show statistics
  $0 cleanup 30                        # Remove backups older than 30 days

Configuration:
  Uploads Directory: ${UPLOADS_DIR}
  Backup Directory: ${BACKUP_DIR}

EOF
}

# Main script
main() {
    case "${1:-full}" in
        full)
            create_full_backup
            ;;
        daily)
            create_daily_backup
            ;;
        specific)
            backup_specific "$2"
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
        archive)
            archive_uploads
            ;;
        verify)
            verify_backup "$2"
            ;;
        cleanup)
            cleanup_old_backups "$2"
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
