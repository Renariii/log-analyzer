import os
import gzip
import pandas as pd
from datetime import datetime

# =========================
# KONFIGURATSIOON
# =========================

LOG_DIR = "logs"
OUTPUT_FILE = "analysis_results.xlsx"

# Otsitavad sündmused (täpne sõnastus logidest)
EVENT_PATTERNS = {
    "New user registered": "New user registered",
    "Administrator privileges granted": "Administrator privileges granted",
    "Service started": "Service started",
    "Service stopped": "Service stopped",
    "System rebooted": "System rebooted",
    "System reboot initiated": "System reboot initiated",

    "Email sent": "Email sent",
    "Email received": "Email received",
    "Database connection established": "Database connection established",
    "Database connection lost": "Database connection lost",
    "Archive created": "Archive created",
    "Notification sent": "Notification sent",
    "Notification received": "Notification received",
    "File downloaded": "File downloaded",
    "File uploaded": "File uploaded",
}

# Exceli töölehtede nimed (alla 31 tähemärgi)
SHEET_NAMES = {
    "New user registered": "New user registered",
    "Administrator privileges granted": "Admin privileges",
    "Service started": "Service started",
    "Service stopped": "Service stopped",
    "System rebooted": "System rebooted",
    "System reboot initiated": "Reboot initiated",

    "Email sent": "Email sent",
    "Email received": "Email received",
    "Database connection established": "DB connected",
    "Database connection lost": "DB disconnected",
    "Archive created": "Archive created",
    "Notification sent": "Notification sent",
    "Notification received": "Notification received",
    "File downloaded": "File downloaded",
    "File uploaded": "File uploaded",
}


# =========================
# ABIFUNKTSIOONID
# =========================

def check_excel_writable(path: str) -> bool:
    """
    Kontrollib, kas Exceli faili saab kirjutada.
    Kui fail on avatud, antakse kasutajale teada.
    """
    if not os.path.exists(path):
        return True

    try:
        with open(path, "a"):
            pass
        return True
    except PermissionError:
        print("❌ Exceli fail on avatud. Sulge fail ja proovi uuesti.")
        return False


def read_log_file(path: str) -> list[str]:
    """
    Loeb logifaili sisu.
    Toetab nii .log kui ka .gz faile.
    """
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()


def collect_log_lines() -> list[str]:
    """
    Loeb kõik logid logs kaustast kokku.
    """
    lines = []

    if not os.path.isdir(LOG_DIR):
        print(f"❌ Logide kausta ei leitud: {LOG_DIR}")
        return lines

    for file in os.listdir(LOG_DIR):
        if file.endswith(".log") or file.endswith(".gz"):
            full_path = os.path.join(LOG_DIR, file)
            lines.extend(read_log_file(full_path))

    return lines


# =========================
# ANALÜÜS
# =========================

def analyze_logs(lines: list[str]) -> dict:
    """
    Analüüsib logiridu ja jaotab sündmused kategooriate kaupa.
    Uuemad kirjed pannakse nimekirjas ettepoole.
    """
    results = {key: [] for key in EVENT_PATTERNS.keys()}

    for line in lines:
        for event_name, pattern in EVENT_PATTERNS.items():
            if pattern in line:
                results[event_name].insert(0, line.strip())

    return results


# =========================
# SALVESTAMINE
# =========================

def save_results_to_excel(results: dict):
    """
    Salvestab analüüsi tulemused Exceli faili.
    Iga sündmus salvestatakse eraldi töölehele.
    """
    if not check_excel_writable(OUTPUT_FILE):
        return

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        for event_name, values in results.items():
            if not values:
                continue

            sheet_name = SHEET_NAMES.get(event_name, event_name)
            df = pd.DataFrame(values, columns=[event_name])
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("✅ analysis_results.xlsx on edukalt loodud")


# =========================
# PEAFUNKTSIOON
# =========================

def main():
    """
    Programmi käivituspunkt.
    """
    print("📄 Alustan logide analüüsi...")

    lines = collect_log_lines()
    print(f"📊 Leiti kokku {len(lines)} logikirjet")

    results = analyze_logs(lines)
    save_results_to_excel(results)


if __name__ == "__main__":
    main()
