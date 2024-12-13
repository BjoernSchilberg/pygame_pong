#!/usr/bin/env python3

import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RestartHandler(FileSystemEventHandler):
    def __init__(self, game_process, game_file):
        self.game_process = game_process
        self.game_file = game_file

    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Überwacht nur Python-Dateien
            print("Änderung entdeckt, starte das Spiel neu...")
            self.game_process.terminate()
            self.game_process = subprocess.Popen(["python", self.game_file])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Bitte den Namen der Python-Datei als Argument übergeben (z. B. `watch_the_dog.py pong.py`)."
        )
        sys.exit(1)

    game_file = sys.argv[1]  # Der Dateiname wird als erstes Argument erwartet

    # Starte das Spiel
    game_process = subprocess.Popen(["python", game_file])

    # Beobachte Änderungen am aktuellen Verzeichnis
    event_handler = RestartHandler(game_process, game_file)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        game_process.wait()
    except KeyboardInterrupt:
        observer.stop()
        game_process.terminate()

    observer.join()
