const CACHE_NAME = 'pilates-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/learn.html',
  '/flashcard.html',
  '/roots.html',
  '/progress.html',
  '/css/minimal.css',
  '/js/wordData.js',
  '/js/siteConfig.js',
  '/js/storage.js',
  '/icon-192.png',
  '/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
