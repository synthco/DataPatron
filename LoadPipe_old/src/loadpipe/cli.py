
from __future__ import annotations
import sys
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import Config, ConfigError
from .log import get_logger

app = typer.Typer(no_args_is_help=True, help="loadpipe CLI")
console = Console()

@app.command(help="Показати версію")
def version():
    console.print(__version__)

# Sub-app: auth
auth_app = typer.Typer(help="Авторизація Google OAuth (Drive)")
@app.callback()
def _main_callback():
    pass

@auth_app.command("login", help="Ініціювати локальний OAuth-флоу та зберегти токен у .secrets/token.json")
def auth_login(
    config: Optional[str] = typer.Option("configs/config.yaml", "--config", help="Шлях до конфігу"),
):
    cfg = Config.from_file(config)
    # Імпортуємо пізно, щоб не тягнути залежності, доки не потрібно
    try:
        from .auth import oauth
    except Exception as e:
        console.print("[red]Модуль авторизації недоступний:[/red]", e)
        raise typer.Exit(code=1)
    oauth.login(cfg.auth)

@app.command("list", help="Лістинг файлів у папці Drive (id, name, size, modified)")
def list_cmd(
    folder: Optional[str] = typer.Option(None, "--folder", help="ID папки Drive"),
    pattern: Optional[str] = typer.Option(None, "--pattern", help="Напр. '*.zst'"),
    config: Optional[str] = typer.Option("configs/config.yaml", "--config", help="Шлях до конфігу"),
):
    cfg = Config.from_file(config)
    folder_id = folder or cfg.source.folder_id
    if not folder_id:
        console.print("[red]Не задано folder_id (прапор --folder або в configs/config.yaml).[/red]")
        raise typer.Exit(code=2)
    try:
        from .adapters import gdrive
        from .auth import oauth
    except Exception as e:
        console.print("[red]Потрібні залежності Google API (див. extra 'gdrive' у pyproject.toml).[/red]")
        raise typer.Exit(code=1)

    creds = oauth.credentials(cfg.auth)
    service = gdrive.build_service(creds)
    files = gdrive.list_files(service, folder_id, pattern=pattern)
    table = Table(title=f"Files in {folder_id}")
    table.add_column("id")
    table.add_column("name")
    table.add_column("size", justify="right")
    table.add_column("modified")
    for f in files:
        table.add_row(f.id, f.name, str(f.size or "-"), f.modified or "-")
    console.print(table)

@app.command("pull", help="Завантажити файл по ID у stdout або у файл (поки заглушка)")
def pull_cmd(
    file: str = typer.Option(..., "--file", help="ID файлу Drive"),
    chunk_mb: int = typer.Option(64, "--chunk-mb", min=1, help="Розмір чанка у MB"),
    out: Optional[str] = typer.Option(None, "--out", help="Шлях вихідного файлу або '-' для stdout"),
    config: Optional[str] = typer.Option("configs/config.yaml", "--config", help="Шлях до конфігу"),
):
    # Заглушка для M1: лише показує параметри і читає конфіг
    cfg = Config.from_file(config)
    console.print(f"[yellow]pull() ще не реалізовано.[/yellow] file={file} chunk_mb={chunk_mb} out={out}")

@app.command("push", help="Відправити stdin як файл у Drive (поки заглушка)")
def push_cmd(
    folder: Optional[str] = typer.Option(None, "--folder", help="ID папки Drive"),
    name: str = typer.Option("out.bin", "--name", help="Ім'я файлу у Drive"),
    chunk_mb: int = typer.Option(64, "--chunk-mb", min=1, help="Розмір чанка у MB"),
    config: Optional[str] = typer.Option("configs/config.yaml", "--config", help="Шлях до конфігу"),
):
    cfg = Config.from_file(config)
    console.print(f"[yellow]push() ще не реалізовано.[/yellow] folder={folder or cfg.upload.folder_id} name={name} chunk_mb={chunk_mb}")

@app.command("sync", help="Простий конвеєр: list → pull → process(identity) → push (поки заглушка)")
def sync_cmd(
    config: Optional[str] = typer.Option("configs/config.yaml", "--config", help="Шлях до конфігу"),
):
    cfg = Config.from_file(config)
    console.print("[yellow]sync() ще не реалізовано (плейсхолдер).[/yellow] Прочитано конфіг.")
    console.print(cfg)

app.add_typer(auth_app, name="auth")
