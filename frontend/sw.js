/* ============================================
   Beacon Service Worker
   Caches frontend assets for offline use.
   AI analysis still requires Ollama running locally.
   ============================================ */

const CACHE_NAME = 'beacon-v1';

const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/css/styles.css',
    '/js/app.js',
    '/manifest.json',
    '/assets/icon-192.svg',
    '/assets/icon-512.svg'
];

// Install: pre-cache all static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
    // Activate immediately without waiting for old SW to finish
    self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            );
        })
    );
    // Claim all open clients immediately
    self.clients.claim();
});

// Fetch: route requests through appropriate strategy
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // API calls (to backend routers): network-first strategy
    if (url.pathname.startsWith('/api/') || url.pathname === '/health') {
        event.respondWith(networkFirst(event.request));
        return;
    }

    // Static assets: cache-first strategy
    event.respondWith(cacheFirst(event.request));
});

// Cache-first: return cached version, fall back to network
async function cacheFirst(request) {
    const cached = await caches.match(request);
    if (cached) {
        return cached;
    }
    try {
        const response = await fetch(request);
        // Cache successful responses for future offline use
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        // For navigation requests, return the cached index page
        if (request.mode === 'navigate') {
            const cachedIndex = await caches.match('/');
            if (cachedIndex) return cachedIndex;
        }
        return new Response('Offline -- cached version not available', {
            status: 503,
            headers: { 'Content-Type': 'text/plain' }
        });
    }
}

// Network-first: try network, fall back to cache, then offline message
async function networkFirst(request) {
    try {
        const response = await fetch(request);
        return response;
    } catch (error) {
        // Network failed -- try cache
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        // Both failed -- return a friendly offline JSON response
        return new Response(
            JSON.stringify({
                error: 'offline',
                message: 'Beacon is offline. Make sure Ollama is running locally (ollama serve) and try again. The UI is available offline, but AI analysis requires the local Ollama server.'
            }),
            {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}
