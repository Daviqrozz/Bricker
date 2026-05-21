const STATIC_CACHE = 'bricker-static-v2';

const STATIC_ASSETS = [
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/img/icons/help-circle.svg',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== STATIC_CACHE)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // Nunca intercepta métodos que alteram estado
  if (request.method !== 'GET') {
    return;
  }

  // Nunca intercepta navegação HTML nem rotas autenticadas/dinâmicas
  if (
    request.mode === 'navigate' ||
    url.pathname.startsWith('/login') ||
    url.pathname.startsWith('/logout') ||
    url.pathname.startsWith('/admin') ||
    url.pathname.startsWith('/products') ||
    url.pathname.startsWith('/sell') ||
    url.pathname.startsWith('/edit') ||
    url.pathname.startsWith('/accounts')
  ) {
    event.respondWith(fetch(request));
    return;
  }

  // Cache-first somente para arquivos estáticos
  if (
    url.pathname.startsWith('/static/') ||
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.js') ||
    url.pathname.endsWith('.png') ||
    url.pathname.endsWith('.jpg') ||
    url.pathname.endsWith('.jpeg') ||
    url.pathname.endsWith('.svg') ||
    url.pathname.endsWith('.webp') ||
    url.pathname.endsWith('.woff') ||
    url.pathname.endsWith('.woff2')
  ) {
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(request).then(networkResponse => {
          if (!networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }

          const responseClone = networkResponse.clone();

          caches.open(STATIC_CACHE).then(cache => {
            cache.put(request, responseClone);
          });

          return networkResponse;
        });
      })
    );
  }
});