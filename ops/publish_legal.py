#!/usr/bin/env python3
"""Публикует miniapp/legal.json на Telegra.ph.

Источник правды для документов — miniapp/legal.json: его же читает Mini App.
Скрипт держит страницы Telegraph в актуальном состоянии, чтобы публичные ссылки
(их проверяет банк) и текст в Mini App не расходились.

Повторный запуск не создаёт дубликаты: токен и адреса страниц лежат в
ops/.telegraph_state.json, и страницы редактируются на месте.

    python3 ops/publish_legal.py            # опубликовать / обновить
    python3 ops/publish_legal.py --dry-run  # только проверки, без сети
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGAL = ROOT / "miniapp" / "legal.json"
STATE = Path(__file__).resolve().parent / ".telegraph_state.json"
API = "https://api.telegra.ph"

sys.path.insert(0, str(ROOT))


def api(method: str, **params) -> dict:
    """Запрос к Telegraph через curl.

    Именно curl, а не urllib: на машине с перехватывающим TLS-прокси проверка
    сертификата в Python падает, а curl берёт корневые сертификаты из системного
    хранилища, где прокси уже доверенный.
    """
    cmd = ["curl", "-sS", "-m", "30", f"{API}/{method}"]
    for key, value in params.items():
        cmd += ["--data-urlencode", f"{key}={value}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{method}: curl — {result.stderr.strip()}")
    payload = json.loads(result.stdout)
    if not payload.get("ok"):
        raise RuntimeError(f"{method}: {payload.get('error')}")
    return payload["result"]


def check_prices(legal: dict) -> None:
    """Цены в тексте документа обязаны совпадать с теми, по которым бот выставляет счёт.

    Сверяемся с дефолтами bot/config.py, а не с загруженным .env: документ и код
    лежат в одном репозитории и выкатываются вместе, а .env у каждой машины свой.
    Если на сервере цена переопределена через .env — правьте и legal.json тоже.
    """
    from bot.config import Settings

    defaults = {name: field.default for name, field in Settings.model_fields.items()}
    settings = type("Defaults", (), defaults)

    terms = legal["docs"]["terms"]["sections"]
    expected = {
        "ru": [
            f"{settings.price_week_rub} ₽", f"{settings.price_month_rub} ₽", f"{settings.price_year_rub} ₽",
            f"{settings.price_week_usd:.2f} $".replace(".", ","),
            f"{settings.price_month_usd:.2f} $".replace(".", ","),
            f"{settings.price_year_usd:.2f} $".replace(".", ","),
            f"{settings.price_week_stars} звёзд", f"{settings.price_month_stars} звёзд", f"{settings.price_year_stars} звёзд",
            f"{settings.price_protection_usd:.2f} $".replace(".", ","),
            f"{settings.price_protection_stars} звёзд",
            f"{settings.price_trial_days} дня",
        ],
        "en": [
            f"RUB {settings.price_week_rub}", f"RUB {settings.price_month_rub}", f"RUB {settings.price_year_rub}",
            f"USD {settings.price_week_usd:.2f}", f"USD {settings.price_month_usd:.2f}", f"USD {settings.price_year_usd:.2f}",
            f"{settings.price_week_stars} Telegram Stars", f"{settings.price_month_stars} Telegram Stars",
            f"{settings.price_year_stars} Telegram Stars",
            f"USD {settings.price_protection_usd:.2f}", f"{settings.price_protection_stars} Telegram Stars",
            f"{settings.price_trial_days} days",
        ],
    }
    for lang, needles in expected.items():
        blob = " ".join(p for s in terms[lang] for p in s["p"])
        missing = [n for n in needles if n not in blob]
        if missing:
            raise SystemExit(
                f"Цены в legal.json ({lang}) разошлись с bot/config.py.\n"
                f"Не найдено в разделе «Тарифы и цены»: {missing}"
            )
    print("✓ цены в документах совпадают с bot/config.py")


def to_nodes(doc: dict, lang: str, updated: str, support: str) -> list:
    nodes: list = [{"tag": "p", "children": [{"tag": "i", "children": [updated]}]}]
    for section in doc["sections"][lang]:
        nodes.append({"tag": "h4", "children": [section["h"]]})
        for paragraph in section["p"]:
            nodes.append({"tag": "p", "children": [paragraph]})
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": ["Поддержка: ", {"tag": "b", "children": [support]}]})
    return nodes


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    legal = json.loads(LEGAL.read_text(encoding="utf-8"))
    check_prices(legal)

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if dry_run:
        for key, doc in legal["docs"].items():
            nodes = to_nodes(doc, "ru", legal["updated"]["ru"], legal["support"])
            print(f"✓ {key}: {len(nodes)} блоков, {sum(len(s['p']) for s in doc['sections']['ru'])} пунктов")
        print("--dry-run: в сеть не ходили, ничего не опубликовано")
        return

    if not state.get("token"):
        account = api(
            "createAccount",
            short_name="Partisans",
            author_name="Partisans",
            author_url=f"https://t.me/{legal['bot'].lstrip('@')}",
        )
        state["token"] = account["access_token"]
        state.setdefault("pages", {})
        print("создан аккаунт Telegraph")

    for key, doc in legal["docs"].items():
        title = f"{doc['title']['ru']} — Partisans"
        content = json.dumps(
            to_nodes(doc, "ru", f"Редакция от {legal['updated']['ru']}", legal["support"]),
            ensure_ascii=False,
        )
        params = dict(
            access_token=state["token"],
            title=title,
            author_name="Partisans",
            author_url=f"https://t.me/{legal['bot'].lstrip('@')}",
            content=content,
        )
        path = state.get("pages", {}).get(key)
        if path:
            page = api(f"editPage/{path}", **params)
            action = "обновлена"
        else:
            page = api("createPage", **params)
            action = "создана"
        state.setdefault("pages", {})[key] = page["path"]
        print(f"✓ {key}: страница {action} — {page['url']}")

    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    STATE.chmod(0o600)
    print(f"\nТокен и адреса страниц сохранены в {STATE} (в git не попадает).")
    print("Ссылки для .env:")
    for key, path in state["pages"].items():
        print(f"  {'PRIVACY_URL' if key == 'privacy' else 'TERMS_URL'}=https://telegra.ph/{path}")


if __name__ == "__main__":
    main()
