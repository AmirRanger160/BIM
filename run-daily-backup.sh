#!/bin/bash

#################################################################################
# Automated Daily Backup Runner
# Purpose: Run all backups and send notification
# Usage: Schedule this with cron or systemd timer
#################################################################################

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_LOG_DIR="${PROJECT_DIR}/backups/logs"
BACKUP_LOG="${BACKUP_LOG_DIR}/backup_$(date +%Y-%m-%d).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Email configuration (optional)
SEND_EMAIL=${SEND_EMAIL:-false}
EMAIL_TO="${EMAIL_TO:-admin@example.com}"
EMAIL_SUBJECT="BIM Backup Report - $(date +%Y-%m-%d)"

# Slack webhook (optional)
SLACK_WEBHOOK=${SLACK_WEBHOOK:-""}

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create log directory
mkdir -p "${BACKUP_LOG_DIR}"

# Log function
log_message() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1" | tee -a "${BACKUP_LOG}"
}

success_message() {
    echo -e "${GREEN}✓ $1${NC}" | tee -a "${BACKUP_LOG}"
}

error_message() {
    echo -e "${RED}✗ $1${NC}" | tee -a "${BACKUP_LOG}"
}

warning_message() {
    echo -e "${YELLOW}⚠ $1${NC}" | tee -a "${BACKUP_LOG}"
}

# Send Slack notification
send_slack_notification() {
    local status="$1"
    local message="$2"
    
    if [ -z "${SLACK_WEBHOOK}" ]; then
        return
    fi
    
    local color="good"
    if [ "${status}" = "error" ]; then
        color="danger"
    elif [ "${status}" = "warning" ]; then
        color="warning"
    fi
    
    local payload=$(cat <<EOF
{
  "attachments": [
    {
      "fallback": "BIM Backup Report",
      "title": "BIM Backup Report - $(date +%Y-%m-%d)",
      "text": "${message}",
      "color": "${color}",
      "footer": "BIM Project Backup System",
      "ts": $(date +%s)
    }
  ]
}
EOF
)
    
    curl -X POST -H 'Content-type: application/json' \
        --data "${payload}" \
        "${SLACK_WEBHOOK}" 2>/dev/null || true
}

# Send email notification
send_email_notification() {
    local subject="$1"
    local body="$2"
    
    if [ "${SEND_EMAIL}" != "true" ]; then
        return
    fi
    
    if command -v mail &> /dev/null; then
        echo "${body}" | mail -s "${subject}" "${EMAIL_TO}"
    elif command -v sendmail &> /dev/null; then
        {
            echo "To: ${EMAIL_TO}"
            echo "Subject: ${subject}"
            echo ""
            echo "${body}"
        } | sendmail -t
    else
        warning_message "Mail command not found, skipping email notification"
    fi
}

# Get backup statistics
get_backup_stats() {
    local backup_dir="$1"
    local count=$(find "${backup_dir}" -type f -mtime -1 | wc -l)
    local size=$(du -sh "${backup_dir}" 2>/dev/null | cut -f1)
    
    echo "Count: ${count}, Size: ${size}"
}

# Main backup routine
run_backups() {
    log_message "=========================================="
    log_message "Starting Automated Backup Suite"
    log_message "=========================================="
    log_message "Timestamp: ${TIMESTAMP}"
    
    local backup_failed=0
    local backup_warnings=0
    
    # Change to project directory
    cd "${PROJECT_DIR}"
    
    # Run database backup
    log_message ""
    log_message "1. Database Backup"
    log_message "==================="
    if ./backup-database.sh full >> "${BACKUP_LOG}" 2>&1; then
        success_message "Database backup completed"
        local db_stats=$(get_backup_stats "${PROJECT_DIR}/backups/database")
        log_message "Database Statistics: ${db_stats}"
    else
        error_message "Database backup failed"
        ((backup_failed++))
    fi
    
    # Run uploads backup
    log_message ""
    log_message "2. Uploads Backup"
    log_message "================="
    if ./backup-uploads.sh daily >> "${BACKUP_LOG}" 2>&1; then
        success_message "Uploads backup completed"
        local uploads_stats=$(get_backup_stats "${PROJECT_DIR}/backups/uploads")
        log_message "Uploads Statistics: ${uploads_stats}"
    else
        warning_message "Uploads backup failed or directory is empty"
        ((backup_warnings++))
    fi
    
    # Run Docker backup
    log_message ""
    log_message "3. Docker Backup"
    log_message "================"
    if ./backup-docker.sh full >> "${BACKUP_LOG}" 2>&1; then
        success_message "Docker backup completed"
        local docker_stats=$(get_backup_stats "${PROJECT_DIR}/backups/docker")
        log_message "Docker Statistics: ${docker_stats}"
    else
        error_message "Docker backup failed"
        ((backup_failed++))
    fi
    
    # Cleanup old backups
    log_message ""
    log_message "4. Cleanup Old Backups"
    log_message "======================"
    if ./backup.sh cleanup >> "${BACKUP_LOG}" 2>&1; then
        success_message "Old backups cleaned up"
    else
        warning_message "Cleanup failed"
        ((backup_warnings++))
    fi
    
    # Generate summary
    log_message ""
    log_message "=========================================="
    log_message "Backup Summary"
    log_message "=========================================="
    
    local total_size=$(du -sh "${PROJECT_DIR}/backups" 2>/dev/null | cut -f1)
    log_message "Total Backup Size: ${total_size}"
    log_message "Backup Location: ${PROJECT_DIR}/backups"
    log_message "Log File: ${BACKUP_LOG}"
    
    log_message ""
    log_message "System Information:"
    log_message "  Hostname: $(hostname)"
    log_message "  Disk Usage: $(df -h / | tail -1 | awk '{print $5 " of " $2}')"
    log_message "  Docker Status: $(docker ps | wc -l) containers running"
    
    log_message ""
    if [ ${backup_failed} -eq 0 ] && [ ${backup_warnings} -eq 0 ]; then
        log_message "=========================================="
        success_message "All backups completed successfully!"
        log_message "=========================================="
        return 0
    elif [ ${backup_failed} -eq 0 ]; then
        log_message "=========================================="
        warning_message "Backups completed with ${backup_warnings} warning(s)"
        log_message "=========================================="
        return 1
    else
        log_message "=========================================="
        error_message "Backups failed with ${backup_failed} error(s)"
        log_message "=========================================="
        return 2
    fi
}

# Create report file
create_report() {
    local report_file="${BACKUP_LOG_DIR}/REPORT_$(date +%Y-%m-%d_%H%M%S).txt"
    
    cat > "${report_file}" << EOF
BIM Project - Backup Report
===========================
Generated: $(date '+%Y-%m-%d %H:%M:%S')
Hostname: $(hostname)
OS: $(uname -s)

Backup Statistics:
==================
Total Backups: $(find "${PROJECT_DIR}/backups" -type f | wc -l)
Total Size: $(du -sh "${PROJECT_DIR}/backups" 2>/dev/null | cut -f1)

Database Backups:
  Count: $(ls -1 "${PROJECT_DIR}/backups/database" 2>/dev/null | wc -l)
  Size: $(du -sh "${PROJECT_DIR}/backups/database" 2>/dev/null | cut -f1)

Uploads Backups:
  Count: $(find "${PROJECT_DIR}/backups/uploads" -type f 2>/dev/null | wc -l)
  Size: $(du -sh "${PROJECT_DIR}/backups/uploads" 2>/dev/null | cut -f1)

Docker Backups:
  Count: $(find "${PROJECT_DIR}/backups/docker" -type f 2>/dev/null | wc -l)
  Size: $(du -sh "${PROJECT_DIR}/backups/docker" 2>/dev/null | cut -f1)

System Information:
===================
Disk Space: $(df -h / | tail -1)
Memory Usage: $(free -h | grep Mem)
Load Average: $(uptime | awk -F'load average:' '{print $2}')
Docker Version: $(docker --version 2>/dev/null || echo "N/A")
PostgreSQL Status: $(docker ps | grep postgres | wc -l) running
Redis Status: $(docker ps | grep redis | wc -l) running

Backup Log:
===========
$(tail -50 "${BACKUP_LOG}")

End of Report
=============
EOF
    
    echo "${report_file}"
}

# Main execution
main() {
    log_message "Backup automation started"
    
    # Run backups
    run_backups
    local backup_status=$?
    
    # Create report
    local report_file=$(create_report)
    log_message "Report created: ${report_file}"
    
    # Send notifications
    if [ ${backup_status} -eq 0 ]; then
        send_slack_notification "success" "✓ All backups completed successfully"
        send_email_notification "${EMAIL_SUBJECT}" "All backups completed successfully. Check ${report_file} for details."
    elif [ ${backup_status} -eq 1 ]; then
        send_slack_notification "warning" "⚠ Backups completed with warnings. Check ${report_file}"
        send_email_notification "${EMAIL_SUBJECT} - WITH WARNINGS" "Backups completed with warnings. Check ${report_file} for details."
    else
        send_slack_notification "error" "✗ Backup failed! Check ${report_file}"
        send_email_notification "${EMAIL_SUBJECT} - FAILED" "Backup failed! Check ${report_file} for details."
    fi
    
    log_message "Backup automation completed with status code: ${backup_status}"
    return ${backup_status}
}

# Execute
main "$@"
