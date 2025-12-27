#!/bin/bash

#################################################################################
# Docker Container & Volumes Backup Script
# Purpose: Backup Docker containers and volumes
#################################################################################

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${PROJECT_DIR}/backups/docker"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y-%m-%d)

# Docker configuration
POSTGRES_CONTAINER="postgres"
REDIS_CONTAINER="redis"
BACKEND_CONTAINER="backend"
POSTGRES_VOLUME="postgres_data"
REDIS_VOLUME="redis_data"

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

# Create backup directories
mkdir -p "${BACKUP_DIR}/volumes"
mkdir -p "${BACKUP_DIR}/images"
mkdir -p "${BACKUP_DIR}/configs"

# Check Docker daemon
check_docker() {
    if ! docker ps &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi
    log "Docker is running"
}

# Backup Docker volume
backup_volume() {
    local volume_name="$1"
    local backup_name="$2"
    
    log "Backing up Docker volume: ${volume_name}..."
    
    local backup_file="${BACKUP_DIR}/volumes/${backup_name}_${TIMESTAMP}.tar.gz"
    
    # Create temporary container to access volume
    if docker run --rm \
        -v "${volume_name}":/volume_data \
        -v "${BACKUP_DIR}/volumes":/backup \
        alpine tar -czf /backup/$(basename ${backup_file}) -C /volume_data . 2>&1; then
        
        local size=$(du -h "${backup_file}" | cut -f1)
        success "Volume backup completed: ${backup_name} (${size})"
        
    else
        error "Failed to backup volume: ${volume_name}"
        return 1
    fi
}

# Backup PostgreSQL container and volume
backup_postgres() {
    log "Backing up PostgreSQL container and data..."
    
    # Check if container exists
    if ! docker ps -a | grep -q "${POSTGRES_CONTAINER}"; then
        error "PostgreSQL container not found"
        return 1
    fi
    
    # Export container configuration
    log "Exporting PostgreSQL container configuration..."
    docker inspect ${POSTGRES_CONTAINER} > "${BACKUP_DIR}/configs/postgres_config_${TIMESTAMP}.json"
    
    # Backup volume
    backup_volume "${POSTGRES_VOLUME}" "postgres_volume"
    
    success "PostgreSQL backup completed"
}

# Backup Redis container and volume
backup_redis() {
    log "Backing up Redis container and data..."
    
    if ! docker ps -a | grep -q "${REDIS_CONTAINER}"; then
        error "Redis container not found"
        return 1
    fi
    
    # Export container configuration
    log "Exporting Redis container configuration..."
    docker inspect ${REDIS_CONTAINER} > "${BACKUP_DIR}/configs/redis_config_${TIMESTAMP}.json"
    
    # Backup volume
    backup_volume "${REDIS_VOLUME}" "redis_volume"
    
    success "Redis backup completed"
}

# Backup backend container
backup_backend() {
    log "Backing up backend container..."
    
    if ! docker ps -a | grep -q "${BACKEND_CONTAINER}"; then
        error "Backend container not found"
        return 1
    fi
    
    # Export container configuration
    log "Exporting backend container configuration..."
    docker inspect ${BACKEND_CONTAINER} > "${BACKUP_DIR}/configs/backend_config_${TIMESTAMP}.json"
    
    success "Backend configuration exported"
}

# Export Docker images
export_docker_images() {
    log "Exporting Docker images..."
    
    local images=("postgres:15-alpine" "redis:7-alpine")
    
    for image in "${images[@]}"; do
        log "Exporting image: ${image}..."
        local image_name=$(echo "${image}" | tr ':/' '_-')
        local image_file="${BACKUP_DIR}/images/${image_name}_${TIMESTAMP}.tar.gz"
        
        if docker save "${image}" | gzip > "${image_file}"; then
            local size=$(du -h "${image_file}" | cut -f1)
            success "Image exported: ${image} (${size})"
        else
            warning "Failed to export image: ${image}"
        fi
    done
}

# Backup docker-compose files
backup_compose_files() {
    log "Backing up docker-compose files..."
    
    local compose_backup="${BACKUP_DIR}/configs/docker-compose_${TIMESTAMP}.tar.gz"
    
    if tar -czf "${compose_backup}" \
        -C "${PROJECT_DIR}" docker-compose.yml \
        -C "${PROJECT_DIR}/backend" docker-compose.yml 2>/dev/null; then
        
        local size=$(du -h "${compose_backup}" | cut -f1)
        success "Docker-compose files backed up (${size})"
    else
        warning "Failed to backup docker-compose files"
    fi
}

# Create docker snapshot/backup summary
create_backup_summary() {
    log "Creating backup summary..."
    
    local summary_file="${BACKUP_DIR}/BACKUP_SUMMARY_${TIMESTAMP}.txt"
    
    cat > "${summary_file}" << EOF
================================================================================
Docker Backup Summary Report
================================================================================
Generated: $(date '+%Y-%m-%d %H:%M:%S')
Backup Directory: ${BACKUP_DIR}

Containers and Volumes:
=======================
PostgreSQL Volume: ${POSTGRES_VOLUME}
  Backup: ${BACKUP_DIR}/volumes/postgres_volume_${TIMESTAMP}.tar.gz

Redis Volume: ${REDIS_VOLUME}
  Backup: ${BACKUP_DIR}/volumes/redis_volume_${TIMESTAMP}.tar.gz

Container Configurations:
=========================
PostgreSQL: ${BACKUP_DIR}/configs/postgres_config_${TIMESTAMP}.json
Redis: ${BACKUP_DIR}/configs/redis_config_${TIMESTAMP}.json
Backend: ${BACKUP_DIR}/configs/backend_config_${TIMESTAMP}.json

Docker Images:
==============
EOF
    
    ls -lh "${BACKUP_DIR}/images" 2>/dev/null | tail -n +2 | \
        awk '{print "  " $9 " (" $5 ")"}' >> "${summary_file}" || true
    
    cat >> "${summary_file}" << EOF

Restore Instructions:
====================

1. Restore PostgreSQL Volume:
   docker run --rm \\
     -v postgres_data:/data \\
     -v $(pwd)/backups/docker/volumes:/backup \\
     alpine tar -xzf /backup/postgres_volume_${TIMESTAMP}.tar.gz -C /data

2. Restore Redis Volume:
   docker run --rm \\
     -v redis_data:/data \\
     -v $(pwd)/backups/docker/volumes:/backup \\
     alpine tar -xzf /backup/redis_volume_${TIMESTAMP}.tar.gz -C /data

3. Import Docker Images:
   docker load -i backups/docker/images/postgres_15-alpine_${TIMESTAMP}.tar.gz
   docker load -i backups/docker/images/redis_7-alpine_${TIMESTAMP}.tar.gz

4. Recreate Containers:
   docker-compose -f backups/docker/configs/docker-compose_${TIMESTAMP}.tar.gz up -d

System Information:
===================
Docker Version: $(docker --version)
Docker Daemon: $(docker ps | grep -c . || echo "0") containers running
Host OS: $(uname -s)

Total Backup Size: $(du -sh ${BACKUP_DIR} 2>/dev/null | cut -f1)

================================================================================
EOF
    
    success "Backup summary created"
}

# List all backups
list_backups() {
    log "Docker backups:"
    echo ""
    
    echo "Volumes:"
    ls -lh "${BACKUP_DIR}/volumes" 2>/dev/null | tail -n +2 | \
        awk '{printf "  %-10s %s\n", $5, $9}' || echo "  None"
    
    echo ""
    echo "Images:"
    ls -lh "${BACKUP_DIR}/images" 2>/dev/null | tail -n +2 | \
        awk '{printf "  %-10s %s\n", $5, $9}' || echo "  None"
    
    echo ""
    echo "Configurations:"
    ls -lh "${BACKUP_DIR}/configs" 2>/dev/null | tail -n +2 | \
        awk '{printf "  %-10s %s\n", $5, $9}' || echo "  None"
}

# Cleanup old backups
cleanup_old_backups() {
    local days="${1:-30}"
    
    log "Removing Docker backups older than ${days} days..."
    
    find "${BACKUP_DIR}" -type f -mtime +${days} -delete
    find "${BACKUP_DIR}" -type d -empty -delete
    
    success "Old Docker backups cleaned up"
}

# Show container status
show_container_status() {
    log "Docker Container Status:"
    echo ""
    
    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | \
        grep -E "(${POSTGRES_CONTAINER}|${REDIS_CONTAINER}|${BACKEND_CONTAINER})" || \
        warning "No containers found"
}

# Show volume information
show_volume_info() {
    log "Docker Volumes Information:"
    echo ""
    
    docker volume ls --filter "name=postgres_data|redis_data" --format "table {{.Name}}\t{{.Driver}}" || \
        warning "No volumes found"
}

# Full Docker backup
full_docker_backup() {
    log "=========================================="
    log "Starting Full Docker Backup"
    log "=========================================="
    
    check_docker
    
    backup_postgres
    backup_redis
    backup_backend
    export_docker_images
    backup_compose_files
    
    create_backup_summary
    
    log "=========================================="
    success "Full Docker backup completed!"
    log "Backup location: ${BACKUP_DIR}"
    log "=========================================="
}

# Show help
show_help() {
    cat << EOF
Docker Container & Volumes Backup Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  full          Perform full Docker backup
  postgres      Backup PostgreSQL container and volume
  redis         Backup Redis container and volume
  backend       Backup backend container configuration
  images        Export Docker images
  compose       Backup docker-compose files
  status        Show container status
  volumes       Show volume information
  list          List all Docker backups
  cleanup       Remove old Docker backups
  help          Show this help message

Examples:
  $0 full                    # Full Docker backup
  $0 postgres                # Backup PostgreSQL only
  $0 redis                   # Backup Redis only
  $0 status                  # Show container status
  $0 cleanup 30              # Remove backups older than 30 days

Configuration:
  Backup Directory: ${BACKUP_DIR}
  PostgreSQL Volume: ${POSTGRES_VOLUME}
  Redis Volume: ${REDIS_VOLUME}

EOF
}

# Main script
main() {
    case "${1:-full}" in
        full)
            full_docker_backup
            ;;
        postgres)
            check_docker
            backup_postgres
            ;;
        redis)
            check_docker
            backup_redis
            ;;
        backend)
            check_docker
            backup_backend
            ;;
        images)
            check_docker
            export_docker_images
            ;;
        compose)
            backup_compose_files
            ;;
        status)
            check_docker
            show_container_status
            ;;
        volumes)
            check_docker
            show_volume_info
            ;;
        list)
            list_backups
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
