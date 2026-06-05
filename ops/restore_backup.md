# Restore Backup

1. Checkout the backup branch:

```bash
git fetch origin backup-data
git checkout backup-data
```

2. Decrypt the database dump:

```bash
export BACKUP_ENCRYPTION_PASSWORD='your-password'
openssl enc -d -aes-256-cbc -pbkdf2 \
  -in backups/current/postgres.dump.enc \
  -out postgres.dump \
  -pass env:BACKUP_ENCRYPTION_PASSWORD
```

3. Restore Postgres:

```bash
cat postgres.dump | docker compose exec -T db pg_restore -U notspybot -d notspybot --clean --if-exists --no-owner --no-privileges
```

4. Restore nginx files manually from `backups/current/nginx/`.
