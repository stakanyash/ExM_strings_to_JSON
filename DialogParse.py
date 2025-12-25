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
    dialogues_by_character = {}

    for string in root.iter("string"):
        value = string.get("value")
        if not value or "|" not in value:
            continue

        name, text = value.split("|", 1)
        name = name.strip()
        text = text.strip()

        if string.get("numButtons"):
            name = "УВЕДОМЛЕНИЕ"

        dialogues.append({
            "name": name,
            "text": text
        })

        if name not in dialogues_by_character:
            dialogues_by_character[name] = []
        
        dialogues_by_character[name].append(text)

    return dialogues, dialogues_by_character


def calculate_stats(dialogues_by_character):
    stats = {}

    for name, replicas in dialogues_by_character.items():
        total_words = 0
        total_chars = 0

        for text in replicas:
            total_words += len(text.split())
            total_chars += len(text)

        stats[name] = {
            "replicas": len(replicas),
            "words": total_words,
            "characters": total_chars
        }

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

    print("\nНужна ли сортировка реплик по персонажам?")
    print("y - Да")
    print("n - Нет")
    
    choice = input("Введите y или n: ").strip()
    
    dialogues, dialogues_by_character = extract_dialogues(xml_file)
    stats = calculate_stats(dialogues_by_character)

    if choice == "y":
        output_data = {
            "dialogues": dialogues_by_character,
            "statistics": stats
        }
    else:
        output_data = {
            "dialogues": dialogues,
            "statistics": stats
        }

    output_path = os.path.splitext(xml_file)[0] + "_dialogues.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"\nГотово! Файл сохранён:\n{output_path}\n")

    print("Статистика по персонажам:")
    for name, s in sorted(stats.items()):
        print(
            f"- {name}: "
            f"реплик = {s['replicas']}, "
            f"слов = {s['words']}, "
            f"символов = {s['characters']}"
        )


if __name__ == "__main__":
    main()