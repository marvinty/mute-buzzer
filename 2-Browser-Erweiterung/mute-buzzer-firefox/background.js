// Mute-Buzzer – mutet alle Tabs, die gerade Ton abspielen, und entmutet genau diese wieder.
const api = globalThis.browser ?? globalThis.chrome;
const KEY = "mutedByBuzzer";
// Whitelist: Seiten, die nie gemutet werden (URL-Anfang), z. B. ["https://example.com/"]
const EXCLUDED_URLS = [];
// Optional: weitere Einträge in einer lokalen Datei außerhalb von Git (nur Chrome/Edge, Firefox hat kein importScripts)
try {
  importScripts("whitelist.local.js");
} catch {}

function isExcluded(tab) {
  return EXCLUDED_URLS.some((prefix) => tab.url?.startsWith(prefix));
}

async function getList() {
  const data = await api.storage.session.get(KEY);
  return data[KEY] ?? [];
}

async function setList(ids) {
  await api.storage.session.set({ [KEY]: ids });
  await updateBadge(ids.length > 0);
}

async function updateBadge(active) {
  await api.action.setBadgeText({ text: active ? "AUS" : "" });
  await api.action.setBadgeBackgroundColor({ color: "#d32f2f" });
  await api.action.setTitle({
    title: active ? "Mute-Buzzer: stumm – drücken zum Entmuten" : "Mute-Buzzer: drücken zum Muten",
  });
}

async function toggle() {
  const list = await getList();

  // 2. Druck: genau die Tabs wieder laut machen, die wir gemutet haben
  if (list.length > 0) {
    await setList([]); // zuerst leeren, damit der onUpdated-Listener nichts zurückschreibt
    await Promise.all(list.map((id) => api.tabs.update(id, { muted: false }).catch(() => {})));
    return;
  }

  // 1. Druck: alle Tabs muten, die gerade hörbar Ton abspielen (außer Ausnahmen)
  const tabs = await api.tabs.query({});
  const playing = tabs.filter((t) => t.audible && !t.mutedInfo?.muted && !isExcluded(t));

  if (playing.length > 0) {
    await Promise.all(playing.map((t) => api.tabs.update(t.id, { muted: true })));
    await setList(playing.map((t) => t.id));
    return;
  }

  // Nichts spielt: falls der Browser zwischendurch neu gestartet wurde,
  // alle Tabs entmuten, die noch von dieser Erweiterung stumm geschaltet sind.
  const ours = tabs.filter((t) => t.mutedInfo?.muted && t.mutedInfo?.extensionId === api.runtime.id);
  await Promise.all(ours.map((t) => api.tabs.update(t.id, { muted: false }).catch(() => {})));
}

// Merkliste aufräumen, wenn ein Tab geschlossen oder von Hand entmutet wird
api.tabs.onRemoved.addListener(async (id) => {
  const list = await getList();
  if (list.includes(id)) await setList(list.filter((x) => x !== id));
});
api.tabs.onUpdated.addListener(async (id, change) => {
  if (change.mutedInfo && !change.mutedInfo.muted) {
    const list = await getList();
    if (list.includes(id)) await setList(list.filter((x) => x !== id));
  }
});

api.commands.onCommand.addListener((cmd) => {
  if (cmd === "toggle-mute") toggle();
});
api.action.onClicked.addListener(() => toggle());

getList().then((l) => updateBadge(l.length > 0));
