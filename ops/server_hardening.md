# Server Hardening Checklist

## Priority

1. Switch SSH to keys only and disable password login.
2. Keep the repository private.
3. Use an encrypted backup password for database dumps.
4. Enable unattended security updates.
5. Install and configure `fail2ban` for SSH and nginx.
6. Keep the bot bound to `127.0.0.1` behind nginx only.
7. Keep Postgres and Redis private inside Docker, without published ports.

## SSH

```bash
apt install -y fail2ban unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

Edit `/etc/ssh/sshd_config`:

```text
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
```

Then:

```bash
systemctl restart ssh
```

## UFW

Only keep the ports you really need:

- `22/tcp`
- `80/tcp`
- `443/tcp`
- your `3x-ui` ports

## Nginx

- keep HTTPS only
- add request limits
- keep proxy target on `127.0.0.1:8080`

## Backups

- run `ops/backup_to_github.sh` by cron
- keep `BACKUP_REPO_URL` and `BACKUP_ENCRYPTION_PASSWORD` outside Git
- test restore regularly on a separate host
