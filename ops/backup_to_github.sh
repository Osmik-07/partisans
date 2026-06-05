#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/root/partisans}"
BACKUP_BRANCH="${BACKUP_BRANCH:-backup-data}"
BACKUP_REPO_URL="${BACKUP_REPO_URL:-}"
BACKUP_ENCRYPTION_PASSWORD="${BACKUP_ENCRYPTION_PASSWORD:-}"
BACKUP_SERVER_NAME="${BACKUP_SERVER_NAME:-$(hostname)}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"

if [[ -z "$BACKUP_REPO_URL" ]]; then
  echo "BACKUP_REPO_URL is required"
  exit 1
fi

if [[ -z "$BACKUP_ENCRYPTION_PASSWORD" ]]; then
  echo "BACKUP_ENCRYPTION_PASSWORD is required"
  exit 1
fi

TMP_DIR="$(mktemp -d)"
BACKUP_DIR="$TMP_DIR/backup"
REPO_DIR="$TMP_DIR/repo"
mkdir -p "$BACKUP_DIR"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cd "$ROOT_DIR"

docker compose exec -T db sh -lc 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$BACKUP_DIR/postgres.dump"
openssl enc -aes-256-cbc -pbkdf2 -salt \
  -in "$BACKUP_DIR/postgres.dump" \
  -out "$BACKUP_DIR/postgres.dump.enc" \
  -pass env:BACKUP_ENCRYPTION_PASSWORD
rm -f "$BACKUP_DIR/postgres.dump"

mkdir -p "$BACKUP_DIR/nginx"
cp docker-compose.yml "$BACKUP_DIR/docker-compose.yml"
if [[ -f /etc/nginx/nginx.conf ]]; then
  cp /etc/nginx/nginx.conf "$BACKUP_DIR/nginx/nginx.conf"
fi
if [[ -f /etc/nginx/sites-available/traceapp.ru ]]; then
  cp /etc/nginx/sites-available/traceapp.ru "$BACKUP_DIR/nginx/traceapp.ru"
fi
if [[ -f /etc/nginx/sites-enabled/traceapp.ru ]]; then
  cp /etc/nginx/sites-enabled/traceapp.ru "$BACKUP_DIR/nginx/traceapp.ru.enabled"
fi

docker compose exec -T db sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "select version_num from alembic_version;"' > "$BACKUP_DIR/alembic_version.txt"

cat > "$BACKUP_DIR/manifest.txt" <<EOF
server=${BACKUP_SERVER_NAME}
created_at_utc=${TIMESTAMP}
root_dir=${ROOT_DIR}
EOF

git clone --quiet "$BACKUP_REPO_URL" "$REPO_DIR"
cd "$REPO_DIR"
git checkout --orphan "$BACKUP_BRANCH"
git rm -rf . >/dev/null 2>&1 || true
mkdir -p backups/current
cp -R "$BACKUP_DIR"/. backups/current/
cat > .gitignore <<'EOF'
.DS_Store
EOF
git add .
git -c user.name="Partisans Backup" -c user.email="backup@partisans.local" commit -m "Backup ${TIMESTAMP}"
git push --force origin "$BACKUP_BRANCH"
