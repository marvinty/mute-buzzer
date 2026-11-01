# Mute-Buzzer

Ein großer 3D-gedruckter Bluetooth-Knopf, der alle Browser-Tabs stummschaltet, die gerade Ton abspielen. Der nächste
Druck macht genau diese Tabs wieder laut. Webseiten lassen sich auf eine Whitelist setzen und werden dann nie gemutet.

## Download der Browser-Erweiterung

- [Chrome/Edge (ZIP)](https://github.com/marvinty/mute-buzzer/releases/latest/download/mute-buzzer-chrome.zip)
- [Firefox (ZIP)](https://github.com/marvinty/mute-buzzer/releases/latest/download/mute-buzzer-firefox.zip)

Die Erweiterung steht in keinem Store. Die Installation beschreibt die [Anleitung](ANLEITUNG.md). Ohne Knopf funktioniert
sie auch: per Klick aufs Icon oder mit `Strg+Shift+9`.

## Inhalt

| Ordner | Inhalt |
|---|---|
| `1-Firmware/` | Fertige Firmware als `.uf2` für nRF52840-Boards im nice!nano-v2-Format, dazu Diagnose-Firmwares |
| `2-Browser-Erweiterung/` | Erweiterung für Chrome/Edge und Firefox |
| `3-Firmware-Quellcode-ZMK/` | ZMK-Konfiguration (v0.3) |
| `4-Gehaeuse/` | STL und STEP, erzeugt aus `quelle/mute_buzzer_case.py` (CadQuery) |

## Stand

Elektronik, Firmware und Erweiterung sind fertig. Das Gehäuse ist modelliert, aber noch nicht gedruckt und nicht anprobiert.

## Lizenz

[MIT](LICENSE), das gilt für den ganzen Inhalt dieses Repos, auch die Gehäusedateien. Die fertigen `.uf2` in `1-Firmware/`
enthalten zusätzlich ZMK und Zephyr, für diese Teile gelten deren eigene Lizenzen.
