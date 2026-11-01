# Mute-Buzzer – Anleitung

Kurz drücken: alle Tabs, die gerade Ton abspielen, werden stumm. Nochmal drücken: genau diese Tabs werden wieder laut.
5 Sekunden gedrückt halten: Bluetooth-Kopplung löschen (zum Umkoppeln auf einen anderen Rechner).

## 1. Firmware flashen
1. Board per USB-C anstecken, RST zweimal schnell mit GND verbinden → Laufwerk „NICENANO“ erscheint.
2. `1-Firmware/mute_buzzer-nice_nano_v2-zmk.uf2` auf das Laufwerk ziehen.
   Das Laufwerk verschwindet von selbst (macOS meldet evtl. „nicht korrekt ausgeworfen“ – ignorieren).

Hinweis: Das Board ist ein nice!nano-Klon ohne 32-kHz-Quarz. Die Firmware nutzt deshalb den internen
Taktgeber (`CONFIG_CLOCK_CONTROL_NRF_K32SRC_RC=y`). Ohne diese Einstellung erkennt das Board keine Tastendrücke.

## 2. Verdrahtung
- Switch: ein Beinchen → **017**, anderes → **GND**
- Akku: Plus → Schiebeschalter → **B+**, Minus → **B−** (Polarität vorher messen!)

## 3. Koppeln
- Per Kabel: funktioniert sofort als USB-Tastatur (solange USB steckt, wird über USB gesendet).
- Per Bluetooth: Kabel ab, Akku an, am Rechner mit **Mute-Buzzer** koppeln.
- Mac: Den Tastatur-Assistenten („Tastatur identifizieren“) einfach schließen.

## 4. Browser-Erweiterung installieren
Download: [Chrome/Edge](https://github.com/marvinty/mute-buzzer/releases/latest/download/mute-buzzer-chrome.zip) ·
[Firefox](https://github.com/marvinty/mute-buzzer/releases/latest/download/mute-buzzer-firefox.zip)

**Chrome / Edge / Brave / Opera**
1. `chrome://extensions` (bzw. `edge://extensions`) → **Entwicklermodus** an.
2. **Entpackte Erweiterung laden** → den entpackten Download-Ordner (oder `2-Browser-Erweiterung/mute-buzzer-chrome`) wählen.
   Den Ordner danach nicht löschen oder verschieben.
3. Windows: Nichts weiter einstellen. Der Knopf wirkt auch, wenn der Browser im Hintergrund ist. Zur Kontrolle steht unter
   `chrome://extensions/shortcuts` bei „Mute-Buzzer“ `Strg+Umschalt+9` mit **Global**.
   Mac: Der Knopf wirkt nur, wenn Chrome im Vordergrund ist.

**Firefox**
- Testen: `about:debugging` → „Dieser Firefox“ → **Temporäres Add-on laden** → `manifest.json` im entpackten Download-Ordner
  (oder in `mute-buzzer-firefox`). Das hält nur bis zum nächsten Neustart von Firefox.
- Dauerhaft: Ordner zippen, auf addons.mozilla.org als „nicht gelistet“ signieren lassen, .xpi installieren.
- Firefox reagiert nur, wenn das Firefox-Fenster im Vordergrund ist.

Rotes „AUS“ am Erweiterungs-Icon = gerade stumm. Klick aufs Icon macht dasselbe wie der Knopf.

**Whitelist**
Seiten, die nie stummgeschaltet werden sollen, in `background.js` in die Liste `EXCLUDED_URLS` eintragen (URL-Anfang,
z. B. `["https://example.com/"]`) und die Erweiterung neu laden.

## 5. Auf einen anderen Rechner umziehen
Knopf 5 s halten → Kopplung gelöscht. Am alten Rechner das Gerät entfernen, am neuen Rechner neu koppeln.
Notfalls `settings_reset-nice_nano_v2-zmk.uf2` flashen (löscht alles), danach wieder die normale Firmware.

## Firmware ändern (optional)
Änderung in `3-Firmware-Quellcode-ZMK/config` auf GitHub pushen → unter „Actions“ werden die .uf2 automatisch gebaut.
Kürzel ändern: `config/mute_buzzer.keymap`. Pin ändern: `config/boards/shields/mute_buzzer/mute_buzzer.overlay`.
