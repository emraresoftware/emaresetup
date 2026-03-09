import json
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    RICH = True
except ImportError:
    RICH = False


def check_registry_sync(project_root: Path) -> bool:
    registry_path = project_root / "data" / "registry.json"
    expected_target = (
        Path.home()
        / "Library"
        / "Mobile Documents"
        / "com~apple~CloudDocs"
        / "EmareHubSync"
        / "registry.json"
    )

    if not registry_path.exists():
        print("ℹ️ registry.json bulunamadı (SQLite aktif).")
        return True

    if not registry_path.is_symlink():
        print("⚠️ registry.json iCloud symlink değil.")
        print("   Çalıştır: ./scripts/setup_registry_sync.sh")
        return False

    current_target = registry_path.resolve()
    if current_target != expected_target:
        print("⚠️ registry.json farklı bir hedefe bağlı görünüyor.")
        print(f"   Mevcut hedef: {current_target}")
        print(f"   Beklenen hedef: {expected_target}")
        print("   Çalıştır: ./scripts/setup_registry_sync.sh")
        return False

    print("🔗 iCloud registry senkronu aktif.")
    return True


# ─── CLI Helpers ───────────────────────────────────────────────

BANNER = r"""
╔══════════════════════════════════════════╗
║         🏭 EMARE HUB FABRİKA            ║
║      Yazılım Üretim Komut Merkezi       ║
╚══════════════════════════════════════════╝
"""

MODULE_TYPES = {
    "1": ("analytics_module", "Veri analizi modülü"),
    "2": ("api_service", "REST API servisi"),
    "3": ("worker_agent", "Arka plan işçisi / agent"),
    "4": ("cli_tool", "Komut satırı aracı"),
    "5": ("standard_module", "Genel amaçlı modül"),
}


def cmd_create() -> None:
    """Interaktif yeni modül oluştur."""
    from factory_worker import worker

    print("\n── 🆕 Yeni Modül Oluştur ──")
    name = input("Modül adı (snake_case): ").strip()
    if not name:
        print("❌ Modül adı boş olamaz.")
        return

    print("\nModül tipi seç:")
    for key, (_, desc) in MODULE_TYPES.items():
        print(f"  {key}) {desc}")
    choice = input("Seçim [5]: ").strip() or "5"
    module_type, type_desc = MODULE_TYPES.get(choice, MODULE_TYPES["5"])

    description = input(f"Görev açıklaması [{type_desc}]: ").strip() or type_desc

    print()
    worker.create_module_scaffold(
        module_name=name,
        module_type=module_type,
        description=description,
    )


def cmd_list() -> None:
    """Kayıtlı modülleri listele."""
    from emare_core import hub

    print("\n── 📦 Kayıtlı Modüller ──")
    data = hub._load_registry()
    modules = hub.list_modules()
    if not modules:
        print("  (henüz modül yok)")
        return

    for i, mod in enumerate(modules, 1):
        name = mod.get("name", "?")
        mtype = mod.get("type", "?")
        reg_at = mod.get("registered_at", "?")[:19]
        mod_path = Path("modules") / name / "main.py"
        status = "✅" if mod_path.exists() else "⚠️ dosya yok"
        print(f"  {i}. {name:<30} [{mtype}]  ({reg_at})  {status}")

    print(f"\n  Toplam: {len(modules)} modül")
    print(f"  Son güncelleme: {data.get('updated_at', '?')[:19]}")


def cmd_run_module() -> None:
    """Bir modülün main.py'sini çalıştır."""
    modules_dir = Path("modules")
    available = sorted(
        d.name for d in modules_dir.iterdir()
        if d.is_dir() and (d / "main.py").exists()
    ) if modules_dir.exists() else []

    if not available:
        print("❌ Çalıştırılacak modül bulunamadı.")
        return

    print("\n── ▶️  Modül Çalıştır ──")
    for i, name in enumerate(available, 1):
        print(f"  {i}) {name}")

    choice = input("Seçim: ").strip()
    try:
        idx = int(choice) - 1
        selected = available[idx]
    except (ValueError, IndexError):
        print("❌ Geçersiz seçim.")
        return

    mod_path = modules_dir / selected / "main.py"
    print(f"\n▶️  {selected}/main.py çalıştırılıyor...\n")
    import subprocess
    result = subprocess.run(
        [sys.executable, str(mod_path)],
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"\n⚠️  Modül {result.returncode} koduyla çıktı.")


def cmd_health() -> None:
    """Sağlık kontrolü çalıştır."""
    import subprocess
    subprocess.run(["bash", "scripts/fleet_health_check.sh"])


def cmd_delete() -> None:
    """Modülü sil."""
    from emare_core import hub

    modules_dir = Path("modules")
    available = sorted(
        d.name for d in modules_dir.iterdir()
        if d.is_dir()
    ) if modules_dir.exists() else []

    if not available:
        print("❌ Silinecek modül bulunamadı.")
        return

    print("\n── 🗑️  Modül Sil ──")
    for i, name in enumerate(available, 1):
        print(f"  {i}) {name}")

    choice = input("Seçim: ").strip()
    try:
        idx = int(choice) - 1
        selected = available[idx]
    except (ValueError, IndexError):
        print("❌ Geçersiz seçim.")
        return

    confirm = input(f"'{selected}' silinecek. Emin misiniz? (e/h): ").strip().lower()
    if confirm != "e":
        print("İptal edildi.")
        return

    shutil.rmtree(modules_dir / selected, ignore_errors=True)

    # SQLite registry'den kaldır
    hub.remove_module(selected)

    print(f"✅ '{selected}' silindi.")


def cmd_export() -> None:
    """Tüm modülleri ZIP olarak dışa aktar."""
    modules_dir = Path("modules")
    if not modules_dir.exists():
        print("❌ Modül dizini bulunamadı.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"emare_modules_{timestamp}.zip"
    zip_path = Path("data") / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in modules_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(modules_dir.parent))

    size_kb = zip_path.stat().st_size / 1024
    print(f"✅ Dışa aktarıldı: {zip_path} ({size_kb:.1f} KB)")


def cmd_stats() -> None:
    """Proje istatistikleri."""
    from emare_core import hub
    from provider_router import router

    data = hub._load_registry()
    modules = hub.list_modules()
    modules_dir = Path("modules")

    total_lines = 0
    total_tests = 0
    for mod in modules:
        name = mod.get("name", "")
        code_path = modules_dir / name / "main.py"
        test_path = modules_dir / name / "tests" / "test_main.py"
        if code_path.exists():
            total_lines += len(code_path.read_text(encoding="utf-8").splitlines())
        if test_path.exists():
            total_tests += 1

    available = [p.name for p in router.available_providers]

    if RICH:
        console = Console()
        table = Table(title="📊 Emare Hub İstatistikleri")
        table.add_column("Metrik", style="cyan")
        table.add_column("Değer", style="green")
        table.add_row("Toplam Modül", str(len(modules)))
        table.add_row("Toplam Kod Satırı", str(total_lines))
        table.add_row("Test Dosyası", str(total_tests))
        table.add_row("AI Sağlayıcılar", ", ".join(available) or "yok")
        table.add_row("Son Güncelleme", data.get("updated_at", "?")[:19])
        console.print(table)
    else:
        print(f"\n📊 İstatistikler")
        print(f"  Modül sayısı:     {len(modules)}")
        print(f"  Kod satırı:       {total_lines}")
        print(f"  Test dosyası:     {total_tests}")
        print(f"  AI sağlayıcılar:  {', '.join(available) or 'yok'}")
        print(f"  Son güncelleme:   {data.get('updated_at', '?')[:19]}")


def cmd_test() -> None:
    """Modül testlerini çalıştır."""
    from test_generator import create_test_file, run_module_tests

    modules_dir = Path("modules")
    available = sorted(
        d.name for d in modules_dir.iterdir()
        if d.is_dir() and (d / "main.py").exists()
    ) if modules_dir.exists() else []

    if not available:
        print("❌ Test edilecek modül yok.")
        return

    print("\n── 🧪 Modül Test ──")
    print("  0) Tüm modülleri test et")
    for i, name in enumerate(available, 1):
        has_test = "✅" if (modules_dir / name / "tests" / "test_main.py").exists() else "⚠️ test yok"
        print(f"  {i}) {name}  {has_test}")

    choice = input("Seçim [0]: ").strip() or "0"

    if choice == "0":
        targets = available
    else:
        try:
            idx = int(choice) - 1
            targets = [available[idx]]
        except (ValueError, IndexError):
            print("❌ Geçersiz seçim.")
            return

    for name in targets:
        test_dir = modules_dir / name / "tests"
        if not (test_dir / "test_main.py").exists():
            print(f"\n  📝 '{name}' için test üretiliyor...")
            create_test_file(name)

        print(f"\n  🧪 '{name}' test ediliyor...")
        result = run_module_tests(name)
        status = "✅ PASSED" if result["status"] == "passed" else "❌ FAILED"
        print(f"  {status}")
        if result["status"] == "failed":
            for line in result["output"].splitlines()[-10:]:
                print(f"    {line}")


def cmd_upgrade() -> None:
    """Modülü yeni versiyona yükselt."""
    from factory_worker import worker

    modules_dir = Path("modules")
    available = sorted(
        d.name for d in modules_dir.iterdir()
        if d.is_dir() and (d / "manifest.json").exists()
    ) if modules_dir.exists() else []

    if not available:
        print("❌ Yükseltilecek modül yok.")
        return

    print("\n── ⬆️  Modül Yükselt ──")
    for i, name in enumerate(available, 1):
        manifest_path = modules_dir / name / "manifest.json"
        version = "?"
        if manifest_path.exists():
            try:
                m = json.loads(manifest_path.read_text(encoding="utf-8"))
                version = m.get("version", "?")
            except json.JSONDecodeError:
                pass
        print(f"  {i}) {name}  (v{version})")

    choice = input("Seçim: ").strip()
    try:
        idx = int(choice) - 1
        selected = available[idx]
    except (ValueError, IndexError):
        print("❌ Geçersiz seçim.")
        return

    worker.upgrade_module(selected)


def cmd_smart_build() -> None:
    """Doğal dil ile çoklu modül üret (Akıllı Fabrika)."""
    from smart_factory import smart_factory

    print("\n── 🧠 Akıllı Fabrika ──")
    print("Ne yapmak istediğinizi doğal dille anlatın:")
    request = input("> ").strip()

    if not request:
        print("❌ Boş istek.")
        return

    smart_factory.build_from_request(request)


def cmd_fleet() -> None:
    """Filo yönetim menüsü."""
    from fleet_manager import fleet_manager

    print("\n── 🌐 Filo Yönetimi ──")
    print("  1) Tüm cihazları listele")
    print("  2) Filo özeti")
    print("  3) Bu cihazı kaydet")

    choice = input("Seçim: ").strip()

    if choice == "1":
        devices = fleet_manager.list_devices()
        if not devices:
            print("  (kayıtlı cihaz yok)")
            return
        for d in devices:
            emoji = "🟢" if d.status == "healthy" else "🟡" if d.status == "degraded" else "🔴"
            print(f"  {emoji} {d.device_id:<30} [{d.status}] modüller: {len(d.modules)}")

    elif choice == "2":
        summary = fleet_manager.get_fleet_summary()
        print(f"  Toplam cihaz:    {summary['total_devices']}")
        print(f"  🟢 Sağlıklı:     {summary['healthy']}")
        print(f"  🟡 Düşük:        {summary['degraded']}")
        print(f"  🔴 Sorunlu:      {summary['unhealthy']}")
        print(f"  Benzersiz modül: {summary['unique_modules']}")

    elif choice == "3":
        import os, platform, subprocess
        from fleet_manager import DeviceHeartbeat
        from emare_core import hub

        modules = [m.get("name", "") for m in hub.list_modules()]

        hb = DeviceHeartbeat(
            device_id=f"{platform.node()}-{os.getlogin()}",
            hostname=platform.node(),
            platform=sys.platform,
            modules=modules,
            python_version=platform.python_version(),
        )

        try:
            result = subprocess.run(
                ["bash", "scripts/fleet_health_check.sh"],
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.splitlines():
                if "PASS:" in line:
                    hb.health_pass = int(line.split("PASS:")[1].strip())
                elif "WARN:" in line:
                    hb.health_warn = int(line.split("WARN:")[1].strip())
                elif "FAIL:" in line:
                    hb.health_fail = int(line.split("FAIL:")[1].strip())
        except Exception:
            pass

        record = fleet_manager.process_heartbeat(hb)
        print(f"  ✅ Kayıt: {record.device_id} [{record.status}]")


def cmd_api() -> None:
    """Web API sunucusunu başlat."""
    print("\n── 🌐 Web API Başlatılıyor ──")
    print("Swagger UI: http://localhost:8000/docs")
    print("Durdurmak için Ctrl+C\n")
    import subprocess
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.server:app", "--reload", "--port", "8000",
    ])


def cmd_info() -> None:
    """Modül detayını göster."""
    modules_dir = Path("modules")
    available = sorted(
        d.name for d in modules_dir.iterdir()
        if d.is_dir() and (d / "manifest.json").exists()
    ) if modules_dir.exists() else []

    if not available:
        print("❌ Modül bulunamadı.")
        return

    print("\n── 🔍 Modül Detayı ──")
    for i, name in enumerate(available, 1):
        print(f"  {i}) {name}")

    choice = input("Seçim: ").strip()
    try:
        idx = int(choice) - 1
        selected = available[idx]
    except (ValueError, IndexError):
        print("❌ Geçersiz seçim.")
        return

    manifest_path = modules_dir / selected / "manifest.json"
    code_path = modules_dir / selected / "main.py"

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"\n📋 {selected}")
    print(f"   Tip:        {manifest.get('type', '?')}")
    print(f"   Açıklama:   {manifest.get('description', '?')}")
    print(f"   Hub uyumlu: {manifest.get('emare_hub_compatible', False)}")

    if code_path.exists():
        lines = code_path.read_text(encoding="utf-8").splitlines()
        print(f"   Kod satırı: {len(lines)}")
        print(f"\n   ── İlk 15 satır ──")
        for line in lines[:15]:
            print(f"   {line}")
        if len(lines) > 15:
            print(f"   ... (+{len(lines) - 15} satır)")


# ─── Main Menu ─────────────────────────────────────────────────

COMMANDS = {
    "1": ("🆕  Yeni modül oluştur", cmd_create),
    "2": ("📦  Modül listele", cmd_list),
    "3": ("▶️   Modül çalıştır", cmd_run_module),
    "4": ("🔍  Modül detayı", cmd_info),
    "5": ("�  Modül test et", cmd_test),
    "6": ("⬆️   Modül yükselt", cmd_upgrade),
    "7": ("🗑️   Modül sil", cmd_delete),
    "8": ("📊  İstatistikler", cmd_stats),
    "9": ("📤  Dışa aktar (ZIP)", cmd_export),
    "10": ("🧠 Akıllı fabrika (doğal dil)", cmd_smart_build),
    "11": ("🌐 Filo yönetimi", cmd_fleet),
    "12": ("🩺 Sağlık kontrolü", cmd_health),
    "13": ("🚀 Web API başlat", cmd_api),
    "q": ("🚪  Çıkış", None),
}


def main() -> int:
    project_root = Path(__file__).resolve().parent
    check_registry_sync(project_root)

    # Doğrudan komut desteği: python main.py list | health | create
    if len(sys.argv) > 1:
        subcmd = sys.argv[1].lower()
        dispatch = {
            "list": cmd_list,
            "health": cmd_health,
            "create": cmd_create,
            "info": cmd_info,
            "run": cmd_run_module,
            "delete": cmd_delete,
            "export": cmd_export,
            "stats": cmd_stats,
            "test": cmd_test,
            "upgrade": cmd_upgrade,
            "smart": cmd_smart_build,
            "fleet": cmd_fleet,
            "api": cmd_api,
        }
        handler = dispatch.get(subcmd)
        if handler:
            handler()
            return 0
        print(f"❌ Bilinmeyen komut: {subcmd}")
        print(f"   Kullanım: python main.py [{' | '.join(dispatch)}]")
        return 1

    print(BANNER)

    while True:
        print("\n── Ana Menü ──")
        for key, (label, _) in COMMANDS.items():
            print(f"  {key}) {label}")

        choice = input("\nSeçim: ").strip().lower()

        if choice == "q":
            print("👋 Görüşmek üzere!")
            return 0

        entry = COMMANDS.get(choice)
        if not entry:
            print("❌ Geçersiz seçim, tekrar dene.")
            continue

        _, handler = entry
        if handler:
            try:
                handler()
            except KeyboardInterrupt:
                print("\n⏹️  İptal edildi.")
            except Exception as exc:
                print(f"\n❌ Hata: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# === Emare Feedback ===
from feedback_router import router as feedback_router
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
# ======================

