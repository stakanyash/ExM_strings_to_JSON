import xml.etree.ElementTree as ET
import json
import os
import tkinter as tk
from tkinter import filedialog


def extract_dialogues(xml_path):
    with open(xml_path, "r", encoding="windows-1251") as f:
        xml_data = f.read()

    root = ET.fromstring(xml_data)

    dialogues = []

    for string in root.iter("string"):
        value = string.get("value")
        if not value or "|" not in value:
            continue

        name, text = value.split("|", 1)

        dialogues.append({
            "name": name.strip(),
            "text": text.strip()
        })

    return dialogues


def calculate_stats(dialogues):
    stats = {}

    for d in dialogues:
        name = d["name"]
        text = d["text"]

        if name not in stats:
            stats[name] = {
                "replicas": 0,
                "words": 0,
                "characters": 0
            }

        stats[name]["replicas"] += 1
        stats[name]["words"] += len(text.split())
        stats[name]["characters"] += len(text)

    return stats


def main():
    root = tk.Tk()
    root.withdraw()

    xml_file = filedialog.askopenfilename(
        title="Выберите XML файл",
        filetypes=[("XML files", "*.xml")]
    )

    if not xml_file:
        print("Файл не выбран.")
        return

    dialogues = extract_dialogues(xml_file)
    stats = calculate_stats(dialogues)

    output_data = {
        "dialogues": dialogues,
        "statistics": stats
    }

    output_path = os.path.splitext(xml_file)[0] + "_dialogues.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Готово! Файл сохранён:\n{output_path}\n")

    print("Статистика по персонажам:")
    for name, s in stats.items():
        print(
            f"- {name}: "
            f"реплик = {s['replicas']}, "
            f"слов = {s['words']}, "
            f"символов = {s['characters']}"
        )


if __name__ == "__main__":
    main()
