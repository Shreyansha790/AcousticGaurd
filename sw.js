/*
 * AcousticGuard service worker
 *
 * Goal: keep the live demo working even on a flaky judge-room network.
 * Strategy:
 *   - Pre-cache the YAMNet label CSV and the TF.js library on install
 *     (small enough to not bloat the cache, big enough to matter).
 *   - Stale-while-revalidate for the YAMNet model + shards, Leaflet,
 *     Chart.js, basemap tiles, and Google Fonts. First load fetches
 *     from network and caches; later loads serve from cache instantly
 *     while a background revalidation refreshes the entry.
 *   - Pass through everything else (Firebase RTDB, TomTom APIs,
 *     same-origin app files) so live data stays live.
 */

const CACHE_VERSION = 'acousticguard-v1';

const PRECACHE_URLS = [
  'https://storage.googleapis.com/audioset/yamnet/yamnet_class_map.csv',
  'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

const SWR_HOST_ALLOWLIST = [
  'tfhub.dev',
  'storage.googleapis.com',
  'cdn.jsdelivr.net',
  'unpkg.com',
  'fonts.googleapis.com',
  'fonts.gstatic.com',
  'basemaps.cartocdn.com'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) =>
      Promise.all(
        PRECACHE_URLS.map((url) =>
          cache.add(new Request(url, { mode: 'no-cors' })).catch(() => null)
        )
      )
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch (e) { return; }

  const isAllowedHost = SWR_HOST_ALLOWLIST.some((h) => url.hostname === h || url.hostname.endsWith('.' + h));
  if (!isAllowedHost) return;

  event.respondWith(
    caches.open(CACHE_VERSION).then(async (cache) => {
      const cached = await cache.match(req);
      const networkPromise = fetch(req)
        .then((res) => {
          if (res && (res.ok || res.type === 'opaque')) {
            cache.put(req, res.clone()).catch(() => {});
          }
          return res;
        })
        .catch(() => null);
      return cached || (await networkPromise) || new Response('', { status: 504 });
    })
  );
});
