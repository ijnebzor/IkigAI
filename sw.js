// IkigAI service worker
// Forked from RenovAIter pattern; cache-first for shell, network-first for everything else.

const CACHE = 'ikigai-v0.2.0';
const CORE = [
  './',
  './index.html',
  './app.html',
  './roadmap-reference.html',
  './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE).catch(err => console.warn('SW cache:', err)))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Don't cache Drive API calls or anything cross-origin
  if (url.origin !== location.origin) return;
  // Don't cache POST/PUT
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (!res || res.status !== 200) return res;
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        return res;
      }).catch(() => caches.match('./app.html'));
    })
  );
});
