# Diagnose-Firmwares

- `pindiag-config/` – ZMK-Config (west.yml, Shield `pindiag`, Keymap A–P, conf mit RC-Takt + Polling).
  Bauen: `west build -p -s zmk/app -b nice_nano_v2 -- -DSHIELD=pindiag -DZMK_CONFIG=<pfad>/pindiag-config`
  Mit Log: zusätzlich `-S zmk-usb-logging` und `-DCONFIG_ZMK_LOG_LEVEL_DBG=y`.
- `test-tippt-a.keymap` – ersetzt `mute_buzzer.keymap`, Switch tippt einfach „a“.
- `endpoints-diag.patch` – temporärer Patch für ZMK v0.3 `app/src/endpoints.c` (DIAGNOSE-4): loggt bei jedem Report Transport/USB-Status. Nach dem Build wieder zurücksetzen.
