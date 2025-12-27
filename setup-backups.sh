#!/bin/bash

#################################################################################
# Backup System Setup - Install Systemd Timers and Configure Automation
# Run this script to set up automatic backups using systemd
#################################################################################

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "This script must be run as root"
        echo "Run with: sudo $0"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v systemctl &> /dev/null; then
        error "Systemd is not available on this system"
        exit 1
    fi
    
    success "All prerequisites met"
}

# Setup using Cron
setup_cron() {
    log "Setting up cron-based backup automation..."
    
    local cron_job="0 2 * * * /home/unique/projects/BIM/backup.sh full"
    local cleanup_job="0 4 * * * /home/unique/projects/BIM/backup.sh cleanup"
    
    # Check if already in crontab
    if (crontab -l 2>/dev/null | grep -q "backup.sh full"); then
        warning "Cron job already exists"
    else
        # Add cron job
        (crontab -l 2>/dev/null || echo "") | \
        (cat; echo "$cron_job") | \
        crontab -
        success "Daily backup cron job added (2 AM)"
    fi
    
    # Add cleanup job
    if (crontab -l 2>/dev/null | grep -q "backup.sh cleanup"); then
        warning "Cleanup cron job already exists"
    else
        (crontab -l 2>/dev/null || echo "") | \
        (cat; echo "$cleanup_job") | \
        crontab -
        success "Cleanup cron job added (4 AM)"
    fi
}

# Setup using Systemd
setup_systemd() {
    log "Setting up systemd timer-based backup automation..."
    
    local service_file="/etc/systemd/system/backup-daily.service"
    local timer_file="/etc/systemd/system/backup-daily.timer"
    local project_dir="/home/unique/projects/BIM"
    
    # Check if systemd files exist
    if [ ! -f "${project_dir}/backup-daily.service" ]; then
        error "backup-daily.service not found in ${project_dir}"
        return 1
    fi
    
    if [ ! -f "${project_dir}/backup-daily.timer" ]; then
        error "backup-daily.timer not found in ${project_dir}"
        return 1
    fi
    
    # Copy systemd files
    log "Installing systemd unit files..."
    cp "${project_dir}/backup-daily.service" "${service_file}"
    cp "${project_dir}/backup-daily.timer" "${timer_file}"
    
    # Set correct permissions
    chmod 644 "${service_file}" "${timer_file}"
    
    # Reload systemd daemon
    log "Reloading systemd daemon..."
    systemctl daemon-reload
    
    # Enable timer
    log "Enabling backup timer..."
    systemctl enable backup-daily.timer
    
    # Start timer
    log "Starting backup timer..."
    systemctl start backup-daily.timer
    
    success "Systemd timer installed and activated"
}

# Verify setup
verify_setup() {
    log "Verifying backup setup..."
    
    echo ""
    echo "Cron jobs:"
    crontab -l 2>/dev/null | grep "backup.sh" || echo "  No cron jobs found"
    
    echo ""
    echo "Systemd timers:"
    systemctl list-timers backup-daily.timer 2>/dev/null || echo "  No systemd timer found"
    
    echo ""
}

# Show configuration
show_configuration() {
    cat << EOF

========================================
Backup System Configuration
========================================

Backup Script Location: /home/unique/projects/BIM/backup.sh
Backup Directory: /home/unique/projects/BIM/backups/
Backup Retention: 30 days (automatic cleanup)

Configured Backups:
  - Database (PostgreSQL)
  - Uploads Directory
  - Docker Volumes
  - Application Code

Database Details:
  - Database: geobiro_db
  - User: geobiro
  - Container: postgres

Docker Containers:
  - PostgreSQL: postgres:15-alpine
  - Redis: redis:7-alpine
  - Backend: Python/FastAPI

Backup Schedule:
  - Full Backup: Daily at 2:00 AM
  - Cleanup: Daily at 4:00 AM
  - Retention: 30 days

========================================

EOF
}

# Show commands
show_commands() {
    cat << EOF

========================================
Quick Commands
========================================

Backup Operations:
  ./backup.sh full              Full backup
  ./backup.sh list              List backups
  ./backup.sh cleanup           Clean old backups

Database:
  ./backup-database.sh full     Database backup
  ./backup-database.sh list     List DB backups
  ./backup-database.sh stats    DB statistics

Uploads:
  ./backup-uploads.sh full      Upload backup
  ./backup-uploads.sh stats     Show statistics

Docker:
  ./backup-docker.sh full       Docker backup
  ./backup-docker.sh status     Container status

Monitoring:
  systemctl status backup-daily.timer    (if using systemd)
  systemctl list-timers                  (if using systemd)
  crontab -l                             (if using cron)
  tail -f backups/logs/backup_*.log      (view logs)

========================================

EOF
}

# Interactive setup
interactive_setup() {
    echo ""
    echo "How would you like to schedule backups?"
    echo ""
    echo "1) Cron (traditional, simple)"
    echo "2) Systemd (modern, better integration)"
    echo "3) Both"
    echo "4) Skip automation setup"
    echo ""
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            setup_cron
            ;;
        2)
            if check_root 2>/dev/null; then
                setup_systemd
            else
                warning "Systemd setup requires root privileges"
            fi
            ;;
        3)
            setup_cron
            if check_root 2>/dev/null; then
                setup_systemd
            else
                warning "Systemd setup requires root privileges"
            fi
            ;;
        4)
            log "Skipping automation setup"
            warning "You'll need to run backups manually"
            ;;
        *)
            error "Invalid choice"
            exit 1
            ;;
    esac
}

# Main setup
main() {
    clear
    
    cat << EOF
╔════════════════════════════════════════════════════════════╗
║      BIM Project - Backup System Setup                    ║
║      Configure Automatic Backups for your Project         ║
╚════════════════════════════════════════════════════════════╝

EOF
    
    log "Starting BIM Backup System Setup..."
    echo ""
    
    # Check prerequisites
    check_prerequisites
    echo ""
    
    # Show current configuration
    show_configuration
    echo ""
    
    # Ask for automation method
    if [ "$1" == "--auto" ]; then
        log "Running in automatic mode..."
        setup_cron
    else
        # Interactive setup
        if [ "$EUID" -eq 0 ]; then
            interactive_setup
        else
            warning "Some features require root. Setting up cron..."
            setup_cron
        fi
    fi
    
    echo ""
    
    # Verify setup
    verify_setup
    
    # Show commands
    show_commands
    
    cat << EOF
========================================
Setup Complete!
========================================

✓ Backup scripts are ready
✓ Automation is configured
✓ Logs will be saved to: backups/logs/

To verify setup:
  systemctl list-timers         (if using systemd)
  crontab -l                    (if using cron)

To test backups:
  ./backup.sh full

For help:
  ./backup.sh help
  less BACKUP_README.md

========================================

EOF
    
    success "BIM Backup System setup complete!"
}

# Run main
main "$@"
