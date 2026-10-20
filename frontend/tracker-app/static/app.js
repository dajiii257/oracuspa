"use strict";

const tg = window.Telegram && window.Telegram.WebApp;

/* icons: drawn for this app, 24x24, stroke */
const I = {
  radar:
    '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12 18.4 5.6"/><circle cx="12" cy="12" r="1.3" fill="currentColor" stroke="none"/>',
  sliders:
    '<path d="M4 7h9.5M18.5 7H20M4 17h3.5M12.5 17H20"/><circle cx="16" cy="7" r="2.4"/><circle cx="10" cy="17" r="2.4"/>',
  person:
    '<circle cx="12" cy="8.2" r="3.8"/><path d="M4.5 20c1.2-3.8 4.2-5.6 7.5-5.6s6.3 1.8 7.5 5.6"/>',
  cart: '<path d="M3 4h2.2l2.1 10.2a1.6 1.6 0 0 0 1.6 1.3h7.9a1.6 1.6 0 0 0 1.6-1.2L20 8H6.2"/><circle cx="9.5" cy="19.5" r="1.3"/><circle cx="16.5" cy="19.5" r="1.3"/>',
  gem: '<path d="M6.5 4h11L21 9l-9 11L3 9z"/><path d="M3 9h18M9.5 4 8 9l4 11 4-11-1.5-5"/>',
  pen: '<path d="M14.5 4.5 19.5 9.5 9 20H4v-5z"/><path d="M12.5 6.5l5 5"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  coin: '<ellipse cx="12" cy="7" rx="7" ry="3"/><path d="M5 7v5c0 1.7 3.1 3 7 3s7-1.3 7-3V7"/><path d="M5 12v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/>',
  spark:
    '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/>',
  ton: '<path d="M5.4 5h13.2c1.1 0 1.8 1.2 1.2 2.1L13 18.9a1.2 1.2 0 0 1-2 0L4.2 7.1C3.6 6.2 4.3 5 5.4 5z"/><path d="M12 5v14.6"/>',
  star: '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z" fill="currentColor" stroke="none"/>',
  up: '<path d="M7 17 17 7M9 7h8v8"/>',
  copy: '<rect x="8.5" y="8.5" width="11" height="11" rx="2.5"/><path d="M15.5 8.5V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7.5a2 2 0 0 0 2 2h2.5"/>',
  left: '<path d="M15 5l-7 7 7 7"/>',
  right: '<path d="M9 5l7 7-7 7"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  chat: '<path d="M20 11.5c0 4.1-3.6 7.5-8 7.5-1.3 0-2.5-.3-3.6-.8L4 19.5l1.2-3.7A7.2 7.2 0 0 1 4 11.5C4 7.4 7.6 4 12 4s8 3.4 8 7.5z"/>',
  flag: '<path d="M5 21V4"/><path d="M5 4.6c4-2 7 2 11 0 1-.5 2.5-.6 3 .2v8.8c-.5-.8-2-.7-3-.2-4 2-7-2-11 0"/>',
  clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
  lock: '<rect x="5" y="10.5" width="14" height="10" rx="3"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
  refresh: '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v4.5h-4.5"/>',
  grid: '<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><rect x="13" y="13" width="7" height="7" rx="2"/>',
  crown: '<path d="M4 8l4 3.5L12 5l4 6.5L20 8l-1.5 10h-13z"/>',
  hex: '<path d="M12 3l7.8 4.5v9L12 21l-7.8-4.5v-9z"/><path d="M8.6 12.4l2.2 2.2 4.6-4.6"/>',
  shield:
    '<path d="M12 3l7 3v5.5c0 4.4-3 7.7-7 9.5-4-1.8-7-5.1-7-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
  minus: '<path d="M6 12h12"/>',
  plus: '<path d="M12 6v12M6 12h12"/>',
  target:
    '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1.2" fill="currentColor" stroke="none"/>',
  send: '<path d="M20.5 3.5 3.5 10.6l6.6 2.4 2.4 6.6z"/><path d="M10.1 13l4.6-4.6"/>',
  at: '<circle cx="12" cy="12" r="3.6"/><path d="M15.6 12v1.4a2.6 2.6 0 0 0 5.2 0V12a8.8 8.8 0 1 0-3.5 7"/>',
  warn: '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17.2v.1"/>',
};
const ic = (name, cls = "") =>
  `<svg class="ic ${cls}" viewBox="0 0 24 24" aria-hidden="true">${
    I[name] || I.spark
  }</svg>`;

const S = {
  tab: "tracker",
  view: "picker",
  me: null,
  prefs: null,
  sections: [],
  sel: null,
  count: 5,
  batch: null,
  idx: 0,
  anim: "",
  sig: "",
  profile: null,
  sheet: null,
  pollT: null,
  saveT: null,
  pending: {},
  paywall: false, // no access: only the shop
  preview: false, // an admin looks at the shop
  shop: null,
  pay: null, // the invoice he is paying
  pick: null, // a tariff with several ways to pay
  step: "intro", // the shop: intro screen or the list of terms
  cdraft: null, // his own section while he edits it
  cpick: null, // collections | backdrops: the picker sheet is open
  catalog: null,
  payT: null,
};

/* helpers */
const esc = (v) =>
  String(v == null ? "" : v).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[
        c
      ])
  );
const $ = (sel) => document.querySelector(sel);
const plain = (n) => String(Number((+n).toFixed(2)));
function fmtTon(n) {
  if (n == null) return "—";
  const v = +n;
  if (v >= 1000) return Math.round(v).toLocaleString("ru-RU");
  return plain(v);
}
const fmtInt = (n) =>
  n == null ? "—" : Math.round(+n).toLocaleString("ru-RU");
/* a lot is sold for TON or for stars, its card and {price} go in that: 30g or 1500⭐ */
const inTon = (card) => card.currency !== "stars";
const native = (card) => (inTon(card) ? +card.price : +card.stars);
const money = (card, v) => (inTon(card) ? `${fmtTon(v)}g` : `${fmtInt(v)}⭐`);
function ago(ts) {
  const s = Math.max(0, Math.floor(Date.now() / 1000 - ts));
  if (s < 60) return `${s} с`;
  if (s < 3600) return `${Math.floor(s / 60)} мин`;
  if (s < 86400) return `${Math.floor(s / 3600)} ч`;
  return `${Math.floor(s / 86400)} д`;
}
function hap(kind) {
  if (!tg || (S.prefs && S.prefs.haptics === false)) return;
  try {
    const h = tg.HapticFeedback;
    if (kind === "ok") h.notificationOccurred("success");
    else if (kind === "err") h.notificationOccurred("error");
    else if (kind === "sel") h.selectionChanged();
    else h.impactOccurred(kind || "light");
  } catch (e) {
    /* old client */
  }
}
function toast(text, kind = "ok") {
  const el = document.createElement("div");
  el.className = `toast ${kind}`;
  el.innerHTML = `${ic(kind === "ok" ? "check" : "warn", "ic-s")}<span>${esc(
    text
  )}</span>`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2200);
}
function openTg(url) {
  try {
    tg.openTelegramLink(url);
  } catch (e) {
    window.open(url, "_blank");
  }
}
function copySync(text) {
  // works inside the tap on every phone, the async clipboard api goes after it
  const t = document.createElement("textarea");
  t.value = text;
  t.setAttribute("readonly", "");
  t.style.position = "fixed";
  t.style.top = "0";
  t.style.opacity = "0";
  document.body.appendChild(t);
  t.select();
  t.setSelectionRange(0, text.length);
  let ok = false;
  try {
    ok = document.execCommand("copy");
  } catch (e) {
    /* the api below */
  }
  t.remove();
  return ok;
}
async function copyText(text, quiet) {
  const ok = copySync(text);
  try {
    await navigator.clipboard.writeText(text);
  } catch (e) {
    if (!ok && !quiet) {
      toast("Скопировать не вышло", "err");
      return;
    }
  }
  if (!quiet) {
    hap("ok");
    toast("Скопировал");
  }
}

/* fullscreen: Telegram 8.0+ can give the app the whole screen */
const canFull = () =>
  !!(
    tg &&
    tg.requestFullscreen &&
    tg.isVersionAtLeast &&
    tg.isVersionAtLeast("8.0")
  );
function applyFullscreen(on) {
  if (!canFull()) return;
  try {
    if (on && !tg.isFullscreen) tg.requestFullscreen();
    if (!on && tg.isFullscreen) tg.exitFullscreen();
  } catch (e) {
    /* old client */
  }
}

async function api(path, body) {
  const headers = { Authorization: `tma ${(tg && tg.initData) || ""}` };
  if (body) headers["Content-Type"] = "application/json";
  const r = await fetch(`api/${path}`, {
    method: body ? "POST" : "GET",
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  let data = {};
  try {
    data = await r.json();
  } catch (e) {
    /* not json */
  }
  if (!r.ok) {
    const err = new Error(data.error || "Нет связи с сервером");
    err.status = r.status;
    // the subscription ran out while he was in the app
    if (r.status === 402) toPaywall();
    throw err;
  }
  return data;
}

/* template */
const SAMPLE = {
  seller: { id: 5012345678, username: "seller", name: "Иван" },
  url: "https://t.me/nft/PlushPepe-1234",
  currency: "ton",
  price: 100,
  stars: 10000,
  title: "Plush Pepe #1234",
};
function priceFor(card) {
  const p = S.prefs;
  let v = native(card);
  if (p.price_on)
    v =
      p.price_mode === "pct"
        ? v * (1 - p.price_value / 100)
        : v - p.price_value;
  v = Math.max(v, 0);
  return inTon(card) ? `${plain(v)}g` : `${Math.round(v)}s`;
}
function fill(tpl, card) {
  const s = card.seller || {};
  const map = {
    id: s.id != null ? String(s.id) : "",
    user: s.username ? `@${s.username}` : "",
    nft: card.url,
    price: priceFor(card),
    gift: card.title,
  };
  return tpl.replace(/\{(id|user|nft|price|gift)\}/g, (_, k) => map[k]);
}

/* paywall: no subscription (or not in the channel) and the app sells itself, nothing else is shown */
function paywallView() {
  const sh = S.shop;
  const close = S.preview
    ? '<div class="pw-top"><button class="chip" data-a="preview-close">Закрыть превью</button></div>'
    : "";
  if (S.pay)
    return `${close}<div class="pw-head small"><h1>Оплата</h1></div>${payView()}`;
  if (sh && S.step === "tariffs") {
    const rows = sh.tariffs
      .map(
        (t) => `
      <button class="row plain" data-a="tariff" data-c="${esc(t.code)}">
        <div class="grow"><div class="title">${esc(
          t.title
        )}</div><div class="hint">${t.options
          .map((o) => esc(o.price))
          .filter((v, i, a) => a.indexOf(v) === i)
          .join(" · ")}</div></div>
        ${ic("right", "ic-s")}
      </button>`
      )
      .join("");
    return `${close}
      <div class="bar"><div class="grow"><b>Выберите срок</b><small>оплата прямо тут</small></div>
        <button class="chip" data-a="step-back">${ic(
          "left",
          "ic-xs"
        )} Назад</button></div>
      <div class="glass list">${
        rows ||
        '<div class="empty-note">Оплата пока не настроена, загляните чуть позже</div>'
      }</div>
      <div class="group-foot">Продлите заранее, время добавится к остатку</div>`;
  }
  const ch = (sh && sh.channel) || {};
  const channel = ch.need
    ? `
    <div class="glass pw-box">
      <b>Сначала подпишитесь на канал${
        ch.title ? ` «${esc(ch.title)}»` : ""
      }</b>
      <div class="btns mt-s">
        <button class="btn secondary small" data-a="chan-open" ${
          ch.url ? "" : "disabled"
        }>${ic("up", "ic-s")} Подписаться</button>
        <button class="btn secondary small" data-a="chan-check">${ic(
          "check",
          "ic-s"
        )} Я подписался</button>
      </div>
    </div>`
    : "";
  const trial =
    sh && sh.trial && !ch.need
      ? `
        <button class="btn green mt-s" data-a="trial">🤑 Попробовать бесплатно 🤤</button>
        <div class="pw-note">${esc(sh.trial)} без оплаты, один раз</div>`
      : "";
  const help =
    sh && sh.support
      ? `<button class="pw-help" data-a="support">Помощь с оплатой</button>`
      : "";
  const promo = S.promoOpen
    ? `<div class="promo-box glass"><input id="promoIn" class="input" maxlength="32" placeholder="Промокод" autocapitalize="characters" autocomplete="off" spellcheck="false"><button class="btn primary small" data-a="promo">Активировать</button></div>`
    : '<button class="pw-help" data-a="promo-open">Есть промокод?</button>';
  return `${close}
    <div class="pw-full">
      <div class="pw-head">
        <div class="pw-logo">${ic("lock")}</div>
        <h1>${
          sh && sh.ended ? "Подписка закончилась" : "У вас нет подписки"
        }</h1>
        <p>Трекер открывается после покупки подписки</p>
      </div>
      <div class="pw-actions">
        ${channel}
        <button class="btn primary" data-a="step-tariffs" ${
          !sh || ch.need || sh.forever ? "disabled" : ""
        }>🦶 Приобрести 🥺</button>
        ${trial}
        ${promo}
        ${help}
      </div>
    </div>`;
}
function payView() {
  const p = S.pay;
  const ton = p.method === "ton";
  const rows = ton
    ? `
      <div class="pay-rows">
        <button class="pay-row" data-a="copy-text" data-v="${esc(
          p.wallet
        )}"><small>Кошелек</small><span>${esc(p.wallet)}</span>${ic(
        "copy",
        "ic-s"
      )}</button>
        <button class="pay-row" data-a="copy-text" data-v="${esc(
          p.memo
        )}"><small>Комментарий</small><span>${esc(p.memo)}</span>${ic(
        "copy",
        "ic-s"
      )}</button>
      </div>
      <div class="pay-warn">${ic(
        "warn",
        "ic-s"
      )} Без комментария платеж не найдется</div>`
    : "";
  const open = ton
    ? `${ic("up", "ic-s")} Оплатить в Tonkeeper`
    : p.method === "stars"
    ? `${ic("star", "ic-s")} Оплатить звездами`
    : `${ic("up", "ic-s")} Оплатить в CryptoBot`;
  return `
    <div class="glass pay">
      <small>${esc(p.title)}</small>
      <div class="pay-sum">${ton ? ic("ton") : ""}${esc(p.amount)}</div>
      <button class="btn primary" data-a="pay-open">${open}</button>
      ${rows}
    </div>
    <div class="pay-wait"><div class="loader sm"></div><span>Жду оплату, трекер откроется сам</span></div>
    <div class="btns mt-s">
      <button class="btn secondary small" data-a="pay-check">${ic(
        "refresh",
        "ic-s"
      )} Проверить</button>
      <button class="btn secondary small" data-a="pay-cancel">${ic(
        "left",
        "ic-s"
      )} Назад</button>
    </div>`;
}
function optionsSheet() {
  const t = S.pick;
  return `<div class="sheet-bg" data-a="pick-close"></div><div class="sheet"><div class="grabber"></div>
    <div class="group-title" style="margin-top:6px">${esc(
      t.title
    )}: чем платишь</div>
    <div class="glass list">${t.options
      .map(
        (o) => `
      <button class="row plain" data-a="option" data-k="${esc(o.key)}">
        <div class="grow"><div class="title" style="font-size:16px">${esc(
          o.name
        )}</div></div><span class="val">${esc(o.price)}</span>${ic(
          "right",
          "ic-s"
        )}
      </button>`
      )
      .join("")}</div></div>`;
}
async function loadShop() {
  try {
    S.shop = await api("shop");
  } catch (e) {
    toast(e.message, "err");
  }
  if (S.paywall || S.preview) render();
}
function toPaywall() {
  if (S.paywall) return;
  S.paywall = true;
  S.shop = null;
  clearTimeout(S.pollT);
  render();
  loadShop();
}
async function unlocked() {
  // paid or trial: the shop goes away, the tracker opens
  clearTimeout(S.payT);
  S.pay = null;
  try {
    const me = await api("me");
    if (!me.access) {
      toast("Доступ еще не пришел, подожди немного", "err");
      return;
    }
    hap("ok");
    toast("Трекер открыт");
    S.paywall = false;
    S.preview = false;
    applyMe(me);
    S.tab = "tracker";
    S.view = "picker";
    render();
  } catch (e) {
    toast(e.message, "err");
  }
}
function payPoll() {
  clearTimeout(S.payT);
  if (!S.pay) return;
  S.payT = setTimeout(async () => {
    if (!S.pay) return;
    try {
      const d = await api("pay", { id: S.pay.id, action: "check" });
      if (d.status === "paid") {
        unlocked();
        return;
      }
      if (d.status === "expired" || d.status === "cancelled") {
        toast("Счет закрыт, выбери срок еще раз", "err");
        S.pay = null;
        render();
        return;
      }
    } catch (e) {
      /* next round */
    }
    payPoll();
  }, 5000);
}
async function buy(tariff, option) {
  hap("medium");
  try {
    const d = await api("buy", { tariff: tariff.code, option: option.key });
    S.pick = null;
    S.pay = d.payment;
    render();
    payOpen();
    payPoll();
  } catch (e) {
    hap("err");
    toast(e.message, "err");
  }
}
function payOpen() {
  const p = S.pay;
  if (!p) return;
  if (p.method === "stars" && p.invoice && tg && tg.openInvoice) {
    tg.openInvoice(p.invoice, (status) => {
      if (status === "paid") unlocked();
    });
  } else if (p.method === "ton" && p.link) {
    try {
      tg.openLink(p.link);
    } catch (e) {
      window.open(p.link, "_blank");
    }
  } else if (p.url) {
    openTg(p.url);
  }
}

/* his own section: a filter of his own */
const EMPTY_CUSTOM = {
  min_ton: null,
  max_ton: null,
  collections: [],
  backdrops: [],
  models: [],
  patterns: [],
  events: "all",
  level_max: null,
  nft_max: null,
  premium: "any",
  max_lots: null,
  free_dm: false,
  one_username: false,
  no_anon: false,
  no_trader: false,
  fancy: false,
  poor: false,
  girl: false,
  anime: false,
};
// the Нищуки topic as separate fields, one tap fills them and he can change any
const POOR_PRESET = {
  free_dm: true,
  one_username: true,
  no_anon: true,
  no_trader: true,
  nft_max: 5,
  level_max: 2,
  max_lots: 2,
};
const PICK_NAMES = {
  collections: "Коллекции",
  backdrops: "Фоны",
  models: "Модели",
  patterns: "Узоры",
};
const many = (n, one, few, lots) =>
  n % 10 === 1 && n % 100 !== 11
    ? one
    : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)
    ? few
    : lots;
function draftOf(saved) {
  const c = JSON.parse(JSON.stringify({ ...EMPTY_CUSTOM, ...(saved || {}) }));
  if (c.poor) {
    // old prefs had one "нищуки" switch
    Object.assign(c, POOR_PRESET, { poor: false });
  }
  return c;
}
function customSummary(c) {
  if (!c) return "";
  c = draftOf(c);
  const parts = [];
  if (c.min_ton != null && c.max_ton != null)
    parts.push(`${plain(c.min_ton)}–${plain(c.max_ton)} TON`);
  else if (c.min_ton != null) parts.push(`от ${plain(c.min_ton)} TON`);
  else if (c.max_ton != null) parts.push(`до ${plain(c.max_ton)} TON`);
  const list = (arr, one, few, lots, single) => {
    if (arr.length)
      parts.push(
        arr.length === 1
          ? `${single}${arr[0]}`
          : `${arr.length} ${many(arr.length, one, few, lots)}`
      );
  };
  list(c.collections, "коллекция", "коллекции", "коллекций", "");
  list(c.models, "модель", "модели", "моделей", "");
  list(c.backdrops, "фон", "фона", "фонов", "фон ");
  list(c.patterns, "узор", "узора", "узоров", "узор ");
  if (c.events === "new") parts.push("только новые");
  if (c.events === "drop") parts.push("только снижения");
  if (c.level_max != null) parts.push(`рейт до ${c.level_max}`);
  if (c.nft_max != null) parts.push(`NFT до ${c.nft_max}`);
  if (c.premium === "no") parts.push("без Premium");
  if (c.premium === "only") parts.push("с Premium");
  if (c.max_lots != null) parts.push(`лотов до ${c.max_lots}`);
  if (c.free_dm) parts.push("ЛС бесплатно");
  if (c.fancy) parts.push("имя шрифтом");
  if (c.girl && c.anime) parts.push("девочка или аниме");
  else if (c.girl) parts.push("девочка");
  else if (c.anime) parts.push("аниме на аве");
  return parts.join(" · ");
}
function chipsOf(kind) {
  const list = S.cdraft[kind];
  const sel = list
    .map(
      (v) =>
        `<button class="chip sel" data-a="c-del" data-k="${kind}" data-v="${esc(
          v
        )}">${esc(v)} <span>×</span></button>`
    )
    .join("");
  return `${sel}<button class="chip add" data-a="c-add" data-k="${kind}">${ic(
    "plus",
    "ic-xs"
  )} Добавить</button>`;
}
function choice(key, options) {
  const v = S.cdraft[key];
  return `<div class="chips flat">${options
    .map(
      ([val, label]) =>
        `<button class="chip ${
          v === val ? "on" : ""
        }" data-a="c-set" data-k="${key}" data-v="${
          val === null ? "" : val
        }">${label}</button>`
    )
    .join("")}</div>`;
}
function toggle(id, title, hint, on) {
  return `
      <label class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">${title}</div>${
    hint ? `<div class="hint">${hint}</div>` : ""
  }</div>
        <span class="switch"><input type="checkbox" data-c="${id}" ${
    on ? "checked" : ""
  }><span></span></span>
      </label>`;
}
function customView() {
  const c = S.cdraft;
  return `
    <div class="bar"><div class="grow"><b>Свой раздел</b><small>фильтр только для вас</small></div>
      <button class="chip" data-a="c-back">${ic(
        "left",
        "ic-xs"
      )} Назад</button></div>
    <div class="group-title">Цена лота, TON</div>
    <div class="glass range">
      <input id="cMin" type="number" inputmode="decimal" min="0" step="0.1" placeholder="от" value="${
        c.min_ton != null ? plain(c.min_ton) : ""
      }">
      <span>—</span>
      <input id="cMax" type="number" inputmode="decimal" min="0" step="0.1" placeholder="до" value="${
        c.max_ton != null ? plain(c.max_ton) : ""
      }">
    </div>
    <div class="group-title">Что ловить</div>
    ${choice("events", [
      ["all", "Все"],
      ["new", "Только новые"],
      ["drop", "Только снижения"],
    ])}
    ${["collections", "models", "backdrops", "patterns"]
      .map(
        (k) => `
    <div class="group-title">${PICK_NAMES[k]}</div>
    <div class="glass pick">${chipsOf(k)}</div>`
      )
      .join("")}
    <div class="group-foot">Пусто: любые</div>

    <div class="group-title">Кто продавец</div>
    <div class="glass list">
      ${toggle(
        "girl",
        "Девочка",
        "По имени, а если по имени не понять, по био профиля",
        c.girl
      )}
      ${toggle(
        "anime",
        "Аниме на аве",
        "Нейросеть смотрит аватарку продавца",
        c.anime
      )}
    </div>
    <div class="group-foot">Включены оба: подходит любой из двух. Трекер проверяет заранее, выдает только тех, кто прошел</div>

    <div class="group-title">Продавец</div>
    <button class="link-chip" data-a="c-poor">${ic(
      "coin",
      "ic-s"
    )}<span class="grow">Как у нищуков</span><small>заполнить все разом</small></button>
    <div class="group-title">Рейтинг не выше</div>
    ${choice("level_max", [
      [null, "Любой"],
      [0, "0"],
      [1, "1"],
      [2, "2"],
      [3, "3"],
      [5, "5"],
    ])}
    <div class="group-title">NFT в профиле не больше</div>
    ${choice("nft_max", [
      [null, "Сколько угодно"],
      [0, "0"],
      [3, "3"],
      [5, "5"],
      [10, "10"],
      [20, "20"],
    ])}
    <div class="group-title">Premium</div>
    ${choice("premium", [
      ["any", "Неважно"],
      ["no", "Без Premium"],
      ["only", "Только с Premium"],
    ])}
    <div class="group-title">Лотов на продаже не больше</div>
    ${choice("max_lots", [
      [null, "Сколько угодно"],
      [1, "1"],
      [2, "2"],
      [5, "5"],
      [10, "10"],
    ])}
    <div class="glass list mt">
      ${toggle(
        "free_dm",
        "ЛС бесплатно",
        "Написать можно без звезд",
        c.free_dm
      )}
      ${toggle(
        "one_username",
        "Один юз",
        "Без коллекционных юзов",
        c.one_username
      )}
      ${toggle("no_anon", "Без номера +888", "", c.no_anon)}
      ${toggle(
        "no_trader",
        "Не трейдер по имени",
        "Без nft, gift, garant, otc, shop в юзе и имени",
        c.no_trader
      )}
      ${toggle(
        "fancy",
        "Имя шрифтом",
        "Продавцы с именем вроде 𝗮𝗹𝗶𝗰𝗮, ɢᴀɪᴀ",
        c.fancy
      )}
    </div>
    <div class="group-foot">Рейтинг и NFT берутся из профиля продавца, трекер проверяет их заранее</div>
    <button class="btn primary mt" data-a="c-save">${ic(
      "check"
    )} Сохранить</button>
    <button class="btn secondary mt-s" data-a="c-clear">Сбросить фильтр</button>`;
}
function pickSheet() {
  const kind = S.cpick;
  const all = (S.catalog && S.catalog[kind]) || [];
  return `<div class="sheet-bg" data-a="c-done"></div><div class="sheet"><div class="grabber"></div>
    <div class="sheet-head"><b>${
      PICK_NAMES[kind] || ""
    }</b><button class="chip on" data-a="c-done">Готово</button></div>
    <input class="search" id="cSearch" placeholder="Поиск" autocomplete="off" autocapitalize="off" spellcheck="false">
    <div class="glass list" id="cList">${pickRows(kind, all, "")}</div></div>`;
}
function pickRows(kind, all, q) {
  const sel = new Set(S.cdraft[kind]);
  const found = all
    .filter((v) => v.toLowerCase().includes(q.toLowerCase()))
    .slice(0, 200);
  if (!S.catalog) return '<div class="empty-note">Загружаю…</div>';
  if (!found.length) return '<div class="empty-note">Ничего не нашлось</div>';
  return found
    .map(
      (v) => `
    <button class="row plain" data-a="c-toggle" data-k="${kind}" data-v="${esc(
        v
      )}">
      <div class="grow"><div class="title" style="font-size:16px;font-weight:500">${esc(
        v
      )}</div></div>
      <div class="radio ${sel.has(v) ? "on" : ""}">${
        sel.has(v) ? ic("check") : ""
      }</div>
    </button>`
    )
    .join("");
}

/* render */
function render() {
  const app = $("#app");
  if (S.paywall || S.preview) {
    app.innerHTML = paywallView();
    $("#tabbar").classList.add("hidden");
    $("#layer").innerHTML = S.pick ? optionsSheet() : "";
    syncBack();
    return;
  }
  if (S.tab === "tracker") {
    if (S.view === "custom" && S.cdraft) app.innerHTML = customView();
    else
      app.innerHTML =
        S.view === "batch" && S.batch ? batchView() : pickerView();
  } else if (S.tab === "settings") app.innerHTML = settingsView();
  else app.innerHTML = profileView();
  S.anim = "";
  renderTabbar();
  renderLayer();
  syncBack();
}
function renderTabbar() {
  const bar = $("#tabbar");
  bar.classList.remove("hidden");
  const tabs = [
    ["tracker", "radar", "Трекер"],
    ["settings", "sliders", "Настройки"],
    ["profile", "person", "Профиль"],
  ];
  bar.innerHTML = tabs
    .map(
      ([id, icon, label]) =>
        `<button class="tab ${
          S.tab === id ? "on" : ""
        }" data-a="tab" data-t="${id}">${ic(
          icon
        )}<span>${label}</span></button>`
    )
    .join("");
}
function syncBack() {
  if (!tg) return;
  const show =
    !!S.sheet ||
    !!S.pick ||
    !!S.pay ||
    S.preview ||
    !!S.cpick ||
    (S.tab === "tracker" && S.view === "custom") ||
    ((S.paywall || S.preview) && S.step === "tariffs") ||
    (!S.paywall && S.tab === "tracker" && S.view === "batch");
  try {
    show ? tg.BackButton.show() : tg.BackButton.hide();
  } catch (e) {
    /* old client */
  }
}
function onBack() {
  if (S.cpick) {
    S.cpick = null;
    renderLayer();
    syncBack();
    return;
  }
  if (S.tab === "tracker" && S.view === "custom") {
    S.view = "picker";
    render();
    return;
  }
  if (S.pick) {
    S.pick = null;
    render();
    return;
  }
  if (S.pay) {
    clearTimeout(S.payT);
    S.pay = null;
    render();
    return;
  }
  if ((S.paywall || S.preview) && S.step === "tariffs") {
    S.step = "intro";
    render();
    return;
  }
  if (S.preview) {
    S.preview = false;
    render();
    return;
  }
  if (S.sheet) {
    S.sheet = null;
    renderLayer();
    syncBack();
    return;
  }
  if (S.tab === "tracker" && S.view === "batch") toPicker();
}

/* tracker: picker */
function readyBadge(s) {
  if (s.ready > 0)
    return `<span class="badge green">${
      s.ready >= 99 ? "99+" : s.ready
    }</span>`;
  return `<span class="badge dim">${s.rare ? "копим" : "ждем"}</span>`;
}
function pickerView() {
  const b = S.batch;
  const resume =
    b && b.cards.length
      ? `
    <button class="glass resume" data-a="resume">
      <div class="tile g-spark">${ic("radar")}</div>
      <div class="grow"><b>Вернуться к пачке</b><span>${esc(
        b.section_name
      )} · ${b.cards.length} из ${b.want}${
          b.done ? "" : " · еще ищу"
        }</span></div>
      ${ic("right", "ic-s")}
    </button>`
      : "";
  const rows = S.sections
    .map((s) => {
      const own = s.custom;
      const hint = own
        ? s.set
          ? customSummary(S.prefs.custom)
          : "Настройте под себя: цена, коллекции, фоны"
        : s.hint;
      const right =
        own && !s.set
          ? `<span class="badge">${ic("sliders", "ic-xs")} Настроить</span>`
          : `${
              own
                ? `<span class="badge dim" data-a="c-edit">${ic(
                    "sliders",
                    "ic-xs"
                  )}</span>`
                : ""
            }${readyBadge(s)}
      <div class="radio ${S.sel === s.id ? "on" : ""}">${
              S.sel === s.id ? ic("check") : ""
            }</div>`;
      return `
    <button class="row" data-a="${
      own && !s.set ? "c-edit" : "pick"
    }" data-id="${s.id}">
      <div class="tile g-${esc(s.icon)}">${ic(s.icon)}</div>
      <div class="grow"><div class="title">${esc(
        s.name
      )}</div><div class="hint">${esc(hint)}</div></div>
      ${right}
    </button>`;
    })
    .join("");
  const max = (S.me && S.me.batch_max) || 10;
  return `
    <div class="top"><h1 class="large">Трекер</h1>${
      S.me && S.me.beta ? '<span class="badge">β · админы</span>' : ""
    }</div>
    <p class="sub">Занял продавца, и он только твой. Выберите раздел</p>
    ${resume}
    <div class="group-title">Что ищем</div>
    <div class="glass list">${
      rows || '<div class="empty-note">Разделов пока нет</div>'
    }</div>
    <div class="group-foot">Справа: сколько продавцов готово прямо сейчас. Редкие разделы трекер копит в фоне до 3 часов</div>
    <div class="group-title">Сколько выдать за раз</div>
    <div class="glass">
      <div class="stepper">
        <button class="round" data-a="count" data-d="-1" ${
          S.count <= 1 ? "disabled" : ""
        }>${ic("minus")}</button>
        <div class="num">${S.count}</div>
        <button class="round" data-a="count" data-d="1" ${
          S.count >= max ? "disabled" : ""
        }>${ic("plus")}</button>
      </div>
      <div class="chips">${[3, 5, 10]
        .map(
          (n) =>
            `<button class="chip ${
              S.count === n ? "on" : ""
            }" data-a="countset" data-n="${n}">${n}</button>`
        )
        .join("")}</div>
    </div>
    <button class="btn primary mt" data-a="start" ${
      S.sel != null ? "" : "disabled"
    }>${ic("radar")} Найти продавцов</button>`;
}

/* tracker: batch */
function attrBox(label, a, card) {
  if (!a)
    return `<div class="attr"><small>${label}</small><b>—</b><span>&nbsp;</span><span>&nbsp;</span></div>`;
  const rare = a.rarity != null ? `${plain(a.rarity)}%` : a.tier || "";
  const floor =
    a.floor != null
      ? `флор ${
          card && !inTon(card) && a.floor_stars != null
            ? `${fmtInt(a.floor_stars)}⭐`
            : `${fmtTon(a.floor)}g`
        }`
      : "";
  return `<div class="attr"><small>${label}</small><b>${esc(a.name)}</b><span>${
    esc(rare) || "&nbsp;"
  }</span><span>${esc(floor) || "&nbsp;"}</span></div>`;
}
function facts(card) {
  const s = card.seller;
  const out = s.loading
    ? ['<span class="shimmer">рейт и nft</span>']
    : [
        `<span>${ic("crown", "ic-xs")} Рейт <b>${
          s.level != null ? s.level : "—"
        }</b></span>`,
        `<span>${ic("hex", "ic-xs")} NFT <b>${
          s.nft != null ? s.nft : "—"
        }</b></span>`,
      ];
  out.push(
    s.paid > 0
      ? `<span class="warn">${ic("chat", "ic-xs")} ЛС ${fmtInt(
          s.paid
        )}⭐</span>`
      : `<span class="good">${ic("chat", "ic-xs")} ЛС бесплатно</span>`
  );
  return out.join("");
}
/* nav: arrows sit in the button row, the whole card is on the screen without scrolling */
function cardView(card, anim = "", readonly = false, nav = false) {
  const s = card.seller;
  const ton = inTon(card);
  const old =
    card.drop && card.old_price
      ? ` · <s>${
          ton ? `${fmtTon(card.old_price)}g` : `${fmtInt(card.old_stars)}⭐`
        }</s>`
      : "";
  // Написать only after Занять: the first one to claim has the seller, nobody else gets him again
  const main = card.claimed
    ? `<button class="btn primary" data-a="write" data-l="${card.listing}">${ic(
        "send"
      )} Написать</button>`
    : card.taken
    ? `<button class="btn done" disabled>${ic("flag")} Занял другой</button>`
    : readonly
    ? ""
    : `<button class="btn green" data-a="claim" data-l="${card.listing}">${ic(
        "flag"
      )} Занять</button>`;
  return `
    <div class="glass lot ${anim}">
      <div class="top-row">
        <div class="art" data-a="nft" data-l="${card.listing}">
          <img src="${esc(
            card.img
          )}" alt="" onerror="this.onerror=null;this.src='${esc(
    card.img_alt
  )}'">
          <span class="go">${ic("up", "ic-xs")}</span>
        </div>
        <div class="meta">
          <div class="title" data-a="nft" data-l="${card.listing}">${esc(
    card.title
  )}</div>
          <div>
            <div class="ton ${ton ? "" : "st"}">${ic(ton ? "ton" : "star")}${
    ton ? fmtTon(card.price) : fmtInt(card.stars)
  }</div>
            <div class="approx">≈ ${
              ton ? `${fmtInt(card.stars)}⭐` : `${fmtTon(card.price)} TON`
            }${old}</div>
          </div>
          <div class="tags">
            <span class="tag">${ic("clock", "ic-xs")} ${ago(card.caught)}</span>
          </div>
        </div>
      </div>
      <div class="attrs">${attrBox("Модель", card.model, card)}${attrBox(
    "Фон",
    card.backdrop,
    card
  )}${attrBox("Узор", card.pattern, card)}</div>
      <div class="seller">
        <div class="ava"><span>${esc(
          (s.username || s.name || "?").trim().charAt(0).toUpperCase()
        )}</span>${
    s.avatar
      ? `<img src="${esc(s.avatar)}" alt="" onerror="this.remove()">`
      : ""
  }</div>
        <div class="who">
          <b data-a="user" data-u="${esc(s.username)}">@${esc(s.username)}${
    s.premium ? ic("star", "ic-xs") : ""
  }</b>
          <div class="mini">${facts(card)}</div>
        </div>
      </div>
      <div class="actions ${nav ? "nav3" : "one"}">
        ${
          nav
            ? `<button class="round" data-a="prev" ${
                S.idx === 0 ? "disabled" : ""
              }>${ic("left")}</button>`
            : ""
        }
        ${main}
        ${
          nav
            ? `<button class="round" data-a="next">${ic("right")}</button>`
            : ""
        }
      </div>
    </div>`;
}
function tplView(card) {
  const tpl = (S.prefs && S.prefs.template) || "";
  const link =
    S.prefs && S.prefs.link
      ? `
    <button class="link-chip" data-a="link">${ic(
      "person",
      "ic-s"
    )}<span class="grow">@${esc(
          S.prefs.link
        )}</span><small>быстрая ссылка</small>${ic("up", "ic-xs")}</button>`
      : "";
  const box = tpl
    ? `<button class="glass tpl" data-a="copy" data-l="${
        card.listing
      }"><span class="text">${esc(
        fill(tpl, card)
      )}</span><span class="copy-ic">${ic("copy", "ic-s")}</span></button>`
    : `<button class="glass tpl" data-a="tab" data-t="settings"><span class="text empty">Шаблона нет, его можно задать в Настройках</span><span class="copy-ic">${ic(
        "sliders",
        "ic-s"
      )}</span></button>`;
  return box + link;
}
function navView(b) {
  const dots = Array.from({ length: b.want }, (_, i) => {
    const c = b.cards[i];
    return `<i class="${
      i === S.idx ? "on" : c && c.claimed ? "taken" : ""
    }"></i>`;
  }).join("");
  const atEnd = S.idx >= b.cards.length;
  return `
    <div class="nav">
      <button class="round" data-a="prev" ${S.idx === 0 ? "disabled" : ""}>${ic(
    "left"
  )}</button>
      <div class="dots">${dots}</div>
      <button class="round" data-a="next" ${atEnd ? "disabled" : ""}>${ic(
    "right"
  )}</button>
    </div>
    <div class="counter">${
      atEnd
        ? b.done
          ? "конец пачки"
          : "ищу следующего"
        : `${S.idx + 1} из ${b.want}`
    }</div>`;
}
function batchView() {
  const b = S.batch;
  const n = b.cards.length;
  const where =
    S.idx < n ? `${S.idx + 1} из ${b.want}` : `найдено ${n} из ${b.want}`;
  const head = `
    <div class="bar">
      <div class="grow"><b>${esc(b.section_name)}</b><small>${where}${
    !b.done && n < b.want ? " · ищу еще" : ""
  }</small></div>
      <button class="chip" data-a="picker">${ic(
        "grid",
        "ic-xs"
      )} Разделы</button>
    </div>
    <div class="progress"><i style="width:${Math.round(
      (n / b.want) * 100
    )}%"></i></div>`;
  if (S.idx < n) {
    const card = b.cards[S.idx];
    return head + cardView(card, S.anim, false, true) + tplView(card);
  }
  if (!b.done) {
    return `${head}
      <div class="glass search">
        <div class="radar"><i></i><i></i><i></i><div class="sweep"></div><div class="core">${ic(
          "radar"
        )}</div></div>
        <h2>Ищу продавцов…</h2>
        <p>${
          n
            ? `Нашел ${n} из ${b.want}. Новые появятся тут сами`
            : "Беру свежие лоты, кроме тех, кого вам уже выдавали за последний час"
        }</p>
      </div>${n ? navView(b) : ""}`;
  }
  const taken = b.cards.filter((c) => c.claimed).length;
  return `${head}
    <div class="glass end">
      <div class="big">${ic(n ? "check" : "radar")}</div>
      <h2>${n ? "Пачка закончилась" : "Никого не нашлось"}</h2>
      <p>${esc(
        b.note ||
          (n ? `Занято ${taken} из ${n}` : "Свежих продавцов в разделе нет")
      )}</p>
      <div class="btns">
        <button class="btn primary small" data-a="more">${ic(
          "refresh",
          "ic-s"
        )} Еще ${b.want}</button>
        <button class="btn secondary small" data-a="other">${ic(
          "grid",
          "ic-s"
        )} Другой раздел</button>
      </div>
    </div>${n ? navView(b) : ""}`;
}

/* settings */
function settingsView() {
  const p = S.prefs;
  const pct = p.price_mode === "pct";
  return `
    <div class="top"><h1 class="large">Настройки</h1></div>
    <div class="group-title">Шаблон сообщения</div>
    <div class="glass list">
      <div class="field"><textarea class="input" id="tpl" maxlength="600" placeholder="Твой текст продавцу, вставки ниже">${esc(
        p.template
      )}</textarea></div>
      <div class="ph-row">${["{id}", "{user}", "{nft}", "{price}", "{gift}"]
        .map(
          (x) => `<button class="ph" data-a="ph" data-p="${x}">${x}</button>`
        )
        .join("")}</div>
      <div class="legend">
        <code>{id}</code><span>айди продавца</span>
        <code>{user}</code><span>юз продавца, @username</span>
        <code>{nft}</code><span>ссылка на NFT</span>
        <code>{price}</code><span>цена в валюте лота: 30g или 1500s</span>
        <code>{gift}</code><span>подарок и номер</span>
      </div>
      <div class="preview"><small>Как будет выглядеть</small><div id="tplPreview"></div></div>
    </div>
    <div class="group-title">Цена в шаблоне</div>
    <div class="glass list">
      <label class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">Своя цена в {price}</div><div class="hint">Выключено: в шаблон идет цена лота как есть</div></div>
        <span class="switch"><input type="checkbox" id="priceOn" ${
          p.price_on ? "checked" : ""
        }><span></span></span>
      </label>
      <div id="priceBox" class="${p.price_on ? "" : "hidden"}">
        <div class="seg">
          <button data-a="pmode" data-m="pct" class="${
            pct ? "on" : ""
          }">В процентах</button>
          <button data-a="pmode" data-m="minus" class="${
            pct ? "" : "on"
          }">Минус число</button>
        </div>
        <div class="amount"><input id="priceVal" type="number" inputmode="decimal" min="0" step="0.1" value="${plain(
          p.price_value
        )}"><span>${pct ? "%" : "g / ⭐"}</span></div>
        <div class="group-foot" id="priceEx" style="margin:0 16px 14px"></div>
      </div>
    </div>
    <div class="group-title">Быстрая ссылка</div>
    <div class="glass list"><div class="prefix"><span>t.me/</span><input id="link" value="${esc(
      p.link
    )}" placeholder="username" autocapitalize="off" autocomplete="off" spellcheck="false"></div></div>
    <div class="group-foot">Будет под каждой карточкой: один тап и ты в этом чате</div>
    <div class="group-title">Экран</div>
    <div class="glass list">
      <label class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">Во весь экран</div><div class="hint">${
          canFull()
            ? "Без шапки Telegram, трекер на весь телефон"
            : "Нужен Telegram посвежее, обнови приложение"
        }</div></div>
        <span class="switch"><input type="checkbox" id="fullscreen" ${
          p.fullscreen ? "checked" : ""
        } ${canFull() ? "" : "disabled"}><span></span></span>
      </label>
    </div>
    <div class="group-title">Выдача</div>
    <div class="glass list">
      <div class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">За раз по умолчанию</div></div>
        <button class="round" data-a="pbatch" data-d="-1" ${
          p.batch <= 1 ? "disabled" : ""
        }>${ic("minus")}</button>
        <b style="min-width:28px;text-align:center;font-size:19px">${
          p.batch
        }</b>
        <button class="round" data-a="pbatch" data-d="1" ${
          p.batch >= 10 ? "disabled" : ""
        }>${ic("plus")}</button>
      </div>
      <label class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">Сообщать, когда пачка готова</div><div class="hint">Бот напишет, если пачка собиралась долго, а трекер был закрыт</div></div>
        <span class="switch"><input type="checkbox" id="notify" ${
          p.notify !== false ? "checked" : ""
        }><span></span></span>
      </label>
      <label class="row plain">
        <div class="grow"><div class="title" style="font-weight:500">Вибрация</div></div>
        <span class="switch"><input type="checkbox" id="haptics" ${
          p.haptics ? "checked" : ""
        }><span></span></span>
      </label>
    </div>`;
}
function settingsLive() {
  const prev = $("#tplPreview");
  if (prev) {
    const card = (S.batch && S.batch.cards[0]) || SAMPLE;
    prev.textContent = S.prefs.template
      ? fill(S.prefs.template, card)
      : "Пока пусто";
    prev.style.color = S.prefs.template ? "" : "var(--text-3)";
  }
  const ex = $("#priceEx");
  if (ex) {
    const p = S.prefs;
    const base = p.price_mode === "pct" ? 100 : 110;
    const ton = { currency: "ton", price: base };
    const stars = { currency: "stars", stars: base * 15 };
    ex.textContent = `Пример: лот за ${base}g, в шаблоне ${priceFor(
      ton
    )}. Лот за ${base * 15}⭐, в шаблоне ${priceFor(stars)}`;
  }
}
function queueSave(patch) {
  Object.assign(S.pending, patch);
  clearTimeout(S.saveT);
  S.saveT = setTimeout(async () => {
    const body = S.pending;
    S.pending = {};
    try {
      const d = await api("prefs", body);
      if (body.link != null && d.prefs.link !== body.link.replace(/^@/, ""))
        toast("Такого юза не бывает: латиница, от 4 символов", "err");
      S.prefs = { ...S.prefs, ...d.prefs, template: S.prefs.template };
    } catch (e) {
      toast(e.message, "err");
    }
  }, 500);
}

/* profile */
function profileView() {
  const u = (S.me && S.me.user) || {};
  const name =
    [u.first_name, u.last_name].filter(Boolean).join(" ") || "Без имени";
  const pr = S.profile;
  const st = (pr && pr.stats) || {};
  const sub = (pr && pr.sub) || {};
  let subTitle = "Подписка";
  let subText = "…";
  if (pr) {
    if (sub.admin) {
      subTitle = "Доступ навсегда";
      subText = "Ты админ, бета открыта для тебя";
    } else if (sub.forever) {
      subTitle = "Подписка навсегда";
      subText = "Продлевать не нужно";
    } else if (sub.active) {
      subTitle = "Подписка активна";
      subText = sub.left
        ? `Осталось ${Math.max(1, Math.round(sub.left / 86400))} дн.`
        : "";
    } else {
      subTitle = "Подписки нет";
      subText = "Купить можно в боте";
    }
  }
  const stat = (icon, label, v) =>
    `<div class="glass stat">${ic(icon)}<small>${label}</small><b class="${
      pr ? "" : "shimmer"
    }">${pr ? fmtInt(v || 0) : "00"}</b></div>`;
  const conv =
    pr && st.given
      ? `Занимаешь ${Math.round(
          ((st.claimed || 0) / st.given) * 100
        )}% из выданных`
      : "";
  const list = !pr
    ? '<div class="empty-note">Загружаю…</div>'
    : pr.claimed.length
    ? pr.claimed
        .map(
          (c, i) => `
      <button class="row" data-a="hist" data-i="${i}">
        <div class="thumb"><img src="${esc(
          c.img
        )}" alt="" onerror="this.onerror=null;this.src='${esc(
            c.img_alt
          )}'"></div>
        <div class="grow"><div class="title" style="font-size:16px">${esc(
          c.title
        )}</div><div class="hint">@${esc(c.seller.username)} · ${money(
            c,
            native(c)
          )} · ${ago(c.claimed_at)} назад</div></div>
        ${ic("right", "ic-s")}
      </button>`
        )
        .join("")
    : '<div class="empty-note">Тут будут все, кого ты занял. Их всегда можно открыть снова</div>';
  return `
    <div class="me">
      <div class="ava">${
        u.photo_url
          ? `<img src="${esc(u.photo_url)}" alt="">`
          : esc(name.charAt(0).toUpperCase())
      }</div>
      <h1>${esc(name)}</h1>
      ${u.username ? `<div class="un">@${esc(u.username)}</div>` : ""}
      <div class="badges">${
        S.me && S.me.admin ? '<span class="badge">Админ</span>' : ""
      }${S.me && S.me.beta ? '<span class="badge dim">Бета</span>' : ""}</div>
    </div>
    <div class="glass sub-card mt"><div class="tile g-gem">${ic(
      "shield"
    )}</div><div class="grow"><b>${subTitle}</b><span>${esc(
    subText
  )}</span></div></div>
    <div class="group-title">Статистика</div>
    <div class="stats">
      ${stat("radar", "Выдано сегодня", st.given_today)}
      ${stat("flag", "Занято сегодня", st.claimed_today)}
      ${stat("grid", "Выдано всего", st.given)}
      ${stat("target", "Занято всего", st.claimed)}
    </div>
    ${conv ? `<div class="group-foot">${conv}</div>` : ""}
    ${refView(pr)}
    <div class="group-title">Промокод</div>
    <div class="promo-box glass"><input id="promoIn" class="input" maxlength="32" placeholder="Промокод" autocapitalize="characters" autocomplete="off" spellcheck="false"><button class="btn primary small" data-a="promo">Активировать</button></div>
    <div class="group-title">Мои занятые</div>
    <div class="glass list">${list}</div>
    ${
      S.me && S.me.admin
        ? `<button class="link-chip" data-a="preview-open">${ic(
            "lock",
            "ic-s"
          )}<span class="grow">Экран оплаты</span><small>как видят без подписки</small></button>`
        : ""
    }
    <div class="group-foot" style="text-align:center;margin-top:22px">Ocerao Tracker${
      S.me && S.me.beta ? " · beta" : ""
    }</div>`;
}
function refView(pr) {
  const r = pr && pr.ref;
  if (!r || !r.bonus) return "";
  return `
    <div class="group-title">Пригласить друга</div>
    <div class="glass ref">
      <b>${ic("spark", "ic-s")} +${esc(r.bonus)} за каждого друга</b>
      <span>Друг покупает подписку по вашей ссылке, вам время в подарок</span>
      <button class="pay-row" data-a="copy-text" data-v="${esc(
        r.link
      )}"><small>Ссылка</small><span>${esc(
    r.link.replace("https://", "")
  )}</span>${ic("copy", "ic-s")}</button>
      <button class="btn primary small mt-s" data-a="ref-share">${ic(
        "send",
        "ic-s"
      )} Поделиться</button>
      <div class="ref-stats"><span>Пришли <b>${fmtInt(
        r.invited
      )}</b></span><span>Купили <b>${fmtInt(
    r.paid
  )}</b></span><span>Получено <b>${esc(r.got)}</b></span></div>
    </div>`;
}
async function loadProfile() {
  try {
    S.profile = await api("profile");
    if (S.tab === "profile") render();
  } catch (e) {
    toast(e.message, "err");
  }
}

/* sheet */
function renderLayer() {
  const layer = $("#layer");
  if (S.cpick) {
    layer.innerHTML = pickSheet();
    return;
  }
  if (!S.sheet) {
    layer.innerHTML = "";
    return;
  }
  layer.innerHTML = `<div class="sheet-bg" data-a="close"></div><div class="sheet"><div class="grabber"></div>${cardView(
    S.sheet,
    "",
    true
  )}${tplView(S.sheet)}</div>`;
}

/* data */
function findCard(listing) {
  const all = [
    ...((S.batch && S.batch.cards) || []),
    ...((S.profile && S.profile.claimed) || []),
    ...(S.sheet ? [S.sheet] : []),
  ];
  return all.find((c) => String(c.listing) === String(listing));
}
function signature(b) {
  return b
    ? JSON.stringify([
        b.id,
        b.done,
        b.note,
        b.cards.map((c) => [
          c.listing,
          c.claimed,
          c.taken,
          c.seller.loading,
          c.seller.level,
          c.seller.nft,
          c.seller.avatar,
        ]),
      ])
    : "";
}
function setBatch(b) {
  S.batch = b;
  const sig = signature(b);
  const changed = sig !== S.sig;
  S.sig = sig;
  return changed;
}
function schedulePoll() {
  clearTimeout(S.pollT);
  const b = S.batch;
  if (!b || document.hidden) return;
  if (b.done && !b.cards.some((c) => c.seller.loading || c.seller.avatar_wait))
    return;
  S.pollT = setTimeout(async () => {
    try {
      const d = await api("batch");
      if (
        d.batch &&
        S.batch &&
        d.batch.id === S.batch.id &&
        setBatch(d.batch) &&
        S.tab === "tracker" &&
        S.view === "batch"
      )
        render();
    } catch (e) {
      /* next round */
    }
    schedulePoll();
  }, 1500);
}
async function refreshMe() {
  try {
    const me = await api("me");
    S.me = me;
    S.sections = me.sections;
    if (S.tab === "tracker" && S.view === "picker") render();
  } catch (e) {
    /* keep the old one */
  }
}
function toPicker() {
  S.view = "picker";
  render();
  refreshMe();
}
async function startBatch(section, count) {
  hap("medium");
  try {
    const d = await api("batch", { section, count });
    setBatch(d.batch);
    S.idx = 0;
    S.view = "batch";
    S.anim = "in-l";
    render();
    schedulePoll();
  } catch (e) {
    hap("err");
    toast(e.message, "err");
  }
}
function go(step) {
  const b = S.batch;
  const max = b.cards.length;
  const next = S.idx + step;
  if (next < 0 || next > max) return;
  S.idx = next;
  S.anim = step > 0 ? "in-l" : "in-r";
  hap("sel");
  render();
}

/* actions */
const A = {
  tariff(el) {
    const t = S.shop.tariffs.find((x) => x.code === el.dataset.c);
    if (!t) return;
    if (S.shop.channel && S.shop.channel.need) {
      hap("err");
      toast("Сначала подпишитесь на канал", "err");
      return;
    }
    if (t.options.length === 1) {
      buy(t, t.options[0]);
      return;
    }
    S.pick = t;
    hap("light");
    render();
  },
  option(el) {
    const o = S.pick && S.pick.options.find((x) => x.key === el.dataset.k);
    if (o) buy(S.pick, o);
  },
  "pick-close"() {
    S.pick = null;
    render();
  },
  "step-tariffs"() {
    S.step = "tariffs";
    hap("light");
    render();
    window.scrollTo(0, 0);
  },
  "step-back"() {
    S.step = "intro";
    hap("light");
    render();
  },
  "pay-open"() {
    hap("light");
    payOpen();
  },
  async "pay-check"(el) {
    el.disabled = true;
    try {
      const d = await api("pay", { id: S.pay.id, action: "check" });
      if (d.status === "paid") unlocked();
      else
        toast("Оплату пока не вижу. Если уже оплатил, подожди минуту", "err");
    } catch (e) {
      toast(e.message, "err");
    }
    el.disabled = false;
  },
  async "pay-cancel"() {
    const p = S.pay;
    clearTimeout(S.payT);
    S.pay = null;
    render();
    // a TON transfer can still be on its way, only an unpaid stars or CryptoBot invoice is cancelled
    if (p && p.method !== "ton") {
      try {
        await api("pay", { id: p.id, action: "cancel" });
      } catch (e) {
        /* it runs out by itself */
      }
    }
  },
  "copy-text"(el) {
    copyText(el.dataset.v);
  },
  async trial(el) {
    if (S.preview) {
      hap("light");
      toast("Это превью: новичку тут сразу откроется пробный доступ");
      return;
    }
    el.disabled = true;
    hap("medium");
    try {
      await api("trial", {});
      unlocked();
    } catch (e) {
      hap("err");
      toast(e.message, "err");
      el.disabled = false;
    }
  },
  "promo-open"() {
    S.promoOpen = true;
    hap("light");
    render();
    const i = $("#promoIn");
    if (i) i.focus();
  },
  async promo(el) {
    const inp = $("#promoIn");
    const code = ((inp && inp.value) || "").trim();
    if (!code) {
      hap("err");
      toast("Впиши промокод", "err");
      return;
    }
    if (S.preview) {
      hap("light");
      toast("Это превью: тут промокод сразу откроет трекер");
      return;
    }
    el.disabled = true;
    hap("medium");
    try {
      const d = await api("promo", { code });
      if (!d.ok) {
        hap("err");
        toast(d.message, "err");
        return;
      }
      toast(d.message);
      if (inp) inp.value = "";
      if (S.paywall) unlocked();
      else {
        hap("ok");
        loadProfile();
      }
    } catch (e) {
      hap("err");
      toast(e.message, "err");
    } finally {
      el.disabled = false;
    }
  },
  "chan-open"() {
    if (S.shop.channel.url) {
      hap("light");
      openTg(S.shop.channel.url);
    }
  },
  async "chan-check"(el) {
    el.disabled = true;
    try {
      const d = await api("channel", {});
      if (!d.ok) {
        hap("err");
        toast("Подписки на канал пока не вижу", "err");
        el.disabled = false;
        return;
      }
      hap("ok");
      const me = await api("me");
      if (me.access) {
        unlocked();
        return;
      }
      await loadShop();
    } catch (e) {
      toast(e.message, "err");
      el.disabled = false;
    }
  },
  support() {
    if (S.shop.support) openTg(S.shop.support);
  },
  "preview-open"() {
    S.preview = true;
    S.shop = null;
    S.step = "intro";
    hap("light");
    render();
    loadShop();
    window.scrollTo(0, 0);
  },
  "preview-close"() {
    S.preview = false;
    S.pay = null;
    S.pick = null;
    S.step = "intro";
    clearTimeout(S.payT);
    render();
  },
  tab(el) {
    const t = el.dataset.t;
    if (t === S.tab) return;
    hap("sel");
    S.tab = t;
    if (t === "profile") loadProfile();
    render();
    if (t === "settings") settingsLive();
    window.scrollTo(0, 0);
  },
  pick(el) {
    S.sel = +el.dataset.id;
    hap("sel");
    render();
  },
  "ref-share"() {
    const r = S.profile && S.profile.ref;
    if (!r) return;
    hap("light");
    openTg(
      `https://t.me/share/url?url=${encodeURIComponent(
        r.link
      )}&text=${encodeURIComponent(
        "Трекер лотов маркета подарков: занял продавца, и он только твой"
      )}`
    );
  },
  async "c-edit"() {
    S.cdraft = draftOf(S.prefs.custom);
    S.view = "custom";
    hap("light");
    render();
    window.scrollTo(0, 0);
    if (!S.catalog) {
      try {
        S.catalog = await api("catalog");
      } catch (e) {
        /* the sheet says so */
      }
    }
  },
  "c-back"() {
    S.view = "picker";
    render();
  },
  "c-set"(el) {
    const k = el.dataset.k;
    const v = el.dataset.v;
    S.cdraft[k] = v === "" ? null : ["events", "premium"].includes(k) ? v : +v;
    hap("sel");
    render();
  },
  "c-poor"() {
    Object.assign(S.cdraft, POOR_PRESET);
    hap("ok");
    toast("Выставил как у нищуков");
    render();
  },
  "c-del"(el) {
    const k = el.dataset.k;
    S.cdraft[k] = S.cdraft[k].filter((v) => v !== el.dataset.v);
    hap("sel");
    render();
  },
  "c-add"(el) {
    S.cpick = el.dataset.k;
    hap("light");
    renderLayer();
    syncBack();
  },
  "c-toggle"(el) {
    const k = el.dataset.k;
    const v = el.dataset.v;
    const list = S.cdraft[k];
    S.cdraft[k] = list.includes(v) ? list.filter((x) => x !== v) : [...list, v];
    hap("sel");
    const q = ($("#cSearch") || {}).value || "";
    $("#cList").innerHTML = pickRows(k, (S.catalog && S.catalog[k]) || [], q);
  },
  "c-done"() {
    S.cpick = null;
    render();
  },
  async "c-save"(el) {
    el.disabled = true;
    try {
      const d = await api("prefs", { custom: S.cdraft });
      S.prefs = { ...S.prefs, ...d.prefs };
      await refreshMe();
      const own = S.sections.find((s) => s.custom);
      if (own && own.set) S.sel = own.id;
      else if (S.sel === 0)
        S.sel = (S.sections.find((s) => !s.custom) || {}).id;
      S.view = "picker";
      hap("ok");
      toast(
        own && own.set ? "Свой раздел готов" : "Фильтр пустой, раздел выключен"
      );
      render();
    } catch (e) {
      toast(e.message, "err");
      el.disabled = false;
    }
  },
  "c-clear"() {
    S.cdraft = JSON.parse(JSON.stringify(EMPTY_CUSTOM));
    hap("sel");
    render();
  },
  count(el) {
    S.count = Math.min(Math.max(S.count + +el.dataset.d, 1), 10);
    hap("sel");
    render();
  },
  countset(el) {
    S.count = +el.dataset.n;
    hap("sel");
    render();
  },
  start() {
    if (S.sel != null) startBatch(S.sel, S.count);
  },
  resume() {
    S.view = "batch";
    S.idx = Math.min(S.idx, S.batch.cards.length);
    hap("light");
    render();
    schedulePoll();
  },
  picker() {
    toPicker();
  },
  prev() {
    go(-1);
  },
  next() {
    go(1);
  },
  more() {
    startBatch(S.batch.section, S.batch.want);
  },
  other() {
    S.sel = S.batch ? S.batch.section : S.sel;
    toPicker();
  },
  async claim(el) {
    el.disabled = true;
    hap("medium");
    try {
      const d = await api("claim", { listing: +el.dataset.l });
      if (d.batch) setBatch(d.batch);
      if (d.ok) {
        hap("ok");
        toast("Занял, он только твой. Жми Написать");
      } else {
        hap("err");
        toast(d.message, "err");
      }
    } catch (e) {
      hap("err");
      toast(e.message, "err");
    }
    render();
  },
  write(el) {
    const card = findCard(el.dataset.l);
    if (!card || !card.claimed) return;
    const tpl = S.prefs.template;
    const text = tpl ? fill(tpl, card) : "";
    const url = `https://t.me/${card.seller.username}${
      text ? `?text=${encodeURIComponent(text)}` : ""
    }`;
    hap("light");
    // what goes to Telegram, so a text that does not show up in the input can be traced
    api("log", {
      e: "write",
      seller: card.seller.username,
      text: !!text,
      len: url.length,
      head: url.slice(0, 60),
      platform: tg && tg.platform,
      version: tg && tg.version,
    }).catch(() => {});
    if (!text) {
      openTg(url);
      return;
    }
    // Telegram puts the text into the input only when he can write to the seller: it is in the clipboard anyway
    copyText(text, true);
    toast("Текст скопирован. Не вставился, значит вставь сам");
    setTimeout(() => openTg(url), 450);
  },
  copy(el) {
    const card = findCard(el.dataset.l);
    if (card && S.prefs.template) copyText(fill(S.prefs.template, card));
  },
  nft(el) {
    const card = findCard(el.dataset.l);
    if (card) {
      hap("light");
      openTg(card.url);
    }
  },
  user(el) {
    hap("light");
    openTg(`https://t.me/${el.dataset.u}`);
  },
  link() {
    if (S.prefs.link) {
      hap("light");
      openTg(`https://t.me/${S.prefs.link}`);
    }
  },
  hist(el) {
    S.sheet = S.profile.claimed[+el.dataset.i];
    hap("light");
    renderLayer();
    syncBack();
  },
  close() {
    S.sheet = null;
    renderLayer();
    syncBack();
  },
  ph(el) {
    const t = $("#tpl");
    const at = t.selectionStart != null ? t.selectionStart : t.value.length;
    t.value =
      t.value.slice(0, at) +
      el.dataset.p +
      t.value.slice(t.selectionEnd != null ? t.selectionEnd : at);
    t.focus();
    const pos = at + el.dataset.p.length;
    t.setSelectionRange(pos, pos);
    S.prefs.template = t.value;
    hap("sel");
    settingsLive();
    queueSave({ template: t.value });
  },
  pmode(el) {
    S.prefs.price_mode = el.dataset.m;
    if (S.prefs.price_mode === "pct" && S.prefs.price_value > 99)
      S.prefs.price_value = 10;
    hap("sel");
    render();
    settingsLive();
    queueSave({
      price_mode: S.prefs.price_mode,
      price_value: S.prefs.price_value,
    });
  },
  pbatch(el) {
    S.prefs.batch = Math.min(Math.max(S.prefs.batch + +el.dataset.d, 1), 10);
    S.count = S.prefs.batch;
    hap("sel");
    render();
    settingsLive();
    queueSave({ batch: S.prefs.batch });
  },
};

document.addEventListener("click", (e) => {
  const el = e.target.closest("[data-a]");
  if (!el || el.disabled) return;
  const fn = A[el.dataset.a];
  if (fn) fn(el);
});
document.addEventListener("input", (e) => {
  const t = e.target;
  if (t.id === "tpl") {
    S.prefs.template = t.value;
    settingsLive();
    queueSave({ template: t.value });
  }
  if (t.id === "priceVal") {
    const v = parseFloat(String(t.value).replace(",", "."));
    if (!Number.isNaN(v)) {
      S.prefs.price_value = v;
      settingsLive();
      queueSave({ price_value: v });
    }
  }
  if (t.id === "cSearch") {
    $("#cList").innerHTML = pickRows(
      S.cpick,
      (S.catalog && S.catalog[S.cpick]) || [],
      t.value
    );
  }
  if (t.id === "cMin" || t.id === "cMax") {
    const v = parseFloat(String(t.value).replace(",", "."));
    S.cdraft[t.id === "cMin" ? "min_ton" : "max_ton"] =
      Number.isNaN(v) || v <= 0 ? null : v;
  }
  if (t.id === "link") {
    const v = t.value.trim().replace(/^@/, "");
    S.prefs.link = v;
    queueSave({ link: v });
  }
});
document.addEventListener("change", (e) => {
  const t = e.target;
  if (t.id === "priceOn") {
    S.prefs.price_on = t.checked;
    $("#priceBox").classList.toggle("hidden", !t.checked);
    hap("sel");
    settingsLive();
    queueSave({ price_on: t.checked });
  }
  if (t.id === "haptics") {
    S.prefs.haptics = t.checked;
    hap("sel");
    queueSave({ haptics: t.checked });
  }
  if (t.dataset && t.dataset.c && S.cdraft) {
    S.cdraft[t.dataset.c] = t.checked;
    hap("sel");
  }
  if (t.id === "notify") {
    S.prefs.notify = t.checked;
    hap("sel");
    queueSave({ notify: t.checked });
  }
  if (t.id === "fullscreen") {
    S.prefs.fullscreen = t.checked;
    hap("sel");
    applyFullscreen(t.checked);
    queueSave({ fullscreen: t.checked });
  }
});

/* swipes through the cards */
let touch = null;
document.addEventListener(
  "touchstart",
  (e) => {
    if (S.tab !== "tracker" || S.view !== "batch" || S.sheet) return;
    const p = e.touches[0];
    touch = { x: p.clientX, y: p.clientY, t: Date.now() };
  },
  { passive: true }
);
document.addEventListener(
  "touchend",
  (e) => {
    if (!touch) return;
    const p = e.changedTouches[0];
    const dx = p.clientX - touch.x;
    const dy = p.clientY - touch.y;
    touch = null;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.6)
      go(dx < 0 ? 1 : -1);
  },
  { passive: true }
);

document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    schedulePoll();
    if (S.tab === "tracker" && S.view === "picker") refreshMe();
  }
});

/* gates */
function gate(kind, text) {
  const t = {
    nobot: [
      "Открой через бота",
      'Трекер работает только внутри Telegram, кнопка "Трекер" в меню бота',
    ],
    beta: [
      "Закрытая бета",
      "Сейчас трекер видят только админы. Скоро откроем для всех",
    ],
    error: ["Нет связи", text || "Сервер не ответил, попробуй еще раз"],
  }[kind];
  $("#app").innerHTML = `
    <div class="gate">
      <div class="lock">${ic(kind === "error" ? "warn" : "lock")}</div>
      <h1>${esc(t[0])}</h1><p>${esc(t[1])}</p>
      ${
        kind === "error"
          ? '<button class="btn primary mt" style="max-width:240px" onclick="location.reload()">Еще раз</button>'
          : ""
      }
    </div>`;
}

function applyMe(me) {
  S.me = me;
  S.prefs = me.prefs;
  S.sections = me.sections;
  S.count = me.prefs.batch;
  const usable = me.sections.filter((s) => !s.custom || s.set);
  if (S.sel == null || !usable.some((s) => s.id === S.sel))
    S.sel = usable.length ? usable[0].id : null;
}

async function init() {
  if (tg) {
    try {
      tg.ready();
      tg.expand();
    } catch (e) {
      /* old client */
    }
    try {
      tg.setHeaderColor("#000000");
      tg.setBackgroundColor("#000000");
    } catch (e) {
      /* old client */
    }
    try {
      if (tg.setBottomBarColor) tg.setBottomBarColor("#000000");
    } catch (e) {
      /* old client */
    }
    try {
      if (tg.disableVerticalSwipes) tg.disableVerticalSwipes();
    } catch (e) {
      /* old client */
    }
    try {
      tg.BackButton.onClick(onBack);
    } catch (e) {
      /* old client */
    }
    try {
      tg.onEvent("fullscreenFailed", () => {
        toast("Telegram не дал весь экран", "err");
        const box = $("#fullscreen");
        if (box) box.checked = false;
      });
    } catch (e) {
      /* old client */
    }
  }
  if (!tg || !tg.initData) {
    gate("nobot");
    return;
  }
  try {
    const me = await api("me");
    applyMe(me);
    if (me.prefs.fullscreen) applyFullscreen(true);
    if (!me.access) {
      toPaywall();
      return;
    }
  } catch (e) {
    if (e.status === 402) return;
    gate(
      e.status === 403 ? "beta" : e.status === 401 ? "nobot" : "error",
      e.message
    );
    return;
  }
  try {
    const d = await api("batch");
    if (d.batch) {
      setBatch(d.batch);
      if (d.batch.section != null) S.sel = d.batch.section;
      if (!d.batch.done) S.view = "batch";
    }
  } catch (e) {
    /* no batch yet */
  }
  render();
  schedulePoll();
}

init();
