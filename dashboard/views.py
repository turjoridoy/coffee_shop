from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import json


@login_required(login_url="/login/")
def dashboard(request):
    """Main dashboard view"""
    return render(request, "dashboard/index.html")


@login_required(login_url="/login/")
def manifest(request):
    """Serve PWA manifest"""
    manifest_data = {
        "name": "Coffee Shop Manager",
        "short_name": "Coffee Shop",
        "description": "Professional Sales Management System for Coffee Shops - Track sales, manage inventory, and generate reports",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#2c5aa0",
        "orientation": "portrait",
        "scope": "/",
        "categories": ["business", "productivity", "finance"],
        "lang": "en",
        "prefer_related_applications": False,
        "icons": [
            {
                "src": "/static/icons/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icons/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/static/icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable",
            },
        ],
        "shortcuts": [
            {
                "name": "Add Sale",
                "short_name": "Add Sale",
                "description": "Quickly add a new sale",
                "url": "/?tab=sales",
                "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}],
            },
            {
                "name": "Today's Sales",
                "short_name": "Today",
                "description": "View today's sales",
                "url": "/?tab=today",
                "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}],
            },
            {
                "name": "Dashboard",
                "short_name": "Dashboard",
                "description": "View sales dashboard",
                "url": "/?tab=dashboard",
                "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}],
            },
        ],
    }

    return JsonResponse(manifest_data, content_type="application/manifest+json")


@login_required(login_url="/login/")
def browserconfig(request):
    """Serve browserconfig.xml for Windows tiles"""
    from django.http import HttpResponse
    browserconfig_content = """<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square150x150logo src="/static/icons/icon-144x144.png"/>
            <square310x310logo src="/static/icons/icon-512x512.png"/>
            <TileColor>#2c5aa0</TileColor>
        </tile>
    </msapplication>
</browserconfig>"""
    return HttpResponse(browserconfig_content, content_type="application/xml")


@login_required(login_url="/login/")
def service_worker(request):
    """Serve service worker"""
    service_worker_content = """
// Coffee Shop Manager Service Worker
const CACHE_NAME = 'coffee-shop-v3';
const STATIC_CACHE = 'static-v3';
const DYNAMIC_CACHE = 'dynamic-v3';

const urlsToCache = [
    '/',
    '/static/css/app.css',
    '/static/js/app.js',
    '/static/icons/icon-72x72.png',
    '/static/icons/icon-96x96.png',
    '/static/icons/icon-128x128.png',
    '/static/icons/icon-144x144.png',
    '/static/icons/icon-152x152.png',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-384x384.png',
    '/static/icons/icon-512x512.png'
];

// Install event
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('Service Worker installed successfully');
                return self.skipWaiting();
            })
    );
});

// Activate event
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('Service Worker activated');
            return self.clients.claim();
        })
    );
});

// Fetch event
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Handle API requests with network-first strategy
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Only cache successful responses
                    if (response && response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(DYNAMIC_CACHE)
                            .then(cache => {
                                cache.put(request, responseClone);
                            });
                    }
                    return response;
                })
                .catch(() => {
                    // Return cached response if network fails
                    return caches.match(request);
                })
        );
        return;
    }

    // Handle static assets with cache-first strategy
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(request)
                .then(response => {
                    if (response) {
                        return response;
                    }
                    return fetch(request)
                        .then(response => {
                            if (response && response.status === 200) {
                                const responseToCache = response.clone();
                                caches.open(STATIC_CACHE)
                                    .then(cache => {
                                        cache.put(request, responseToCache);
                                    });
                            }
                            return response;
                        });
                })
        );
        return;
    }

    // Handle HTML pages with network-first strategy
    if (request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    if (response && response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(DYNAMIC_CACHE)
                            .then(cache => {
                                cache.put(request, responseClone);
                            });
                    }
                    return response;
                })
                .catch(() => {
                    return caches.match(request);
                })
        );
        return;
    }

    // Default: try network first, fallback to cache
    event.respondWith(
        fetch(request)
            .then(response => {
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(DYNAMIC_CACHE)
                        .then(cache => {
                            cache.put(request, responseClone);
                        });
                }
                return response;
            })
            .catch(() => {
                return caches.match(request);
            })
    );
});

// Background sync for offline data
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Push notifications (for future use)
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body || 'New notification from Coffee Shop Manager',
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/icon-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            },
            actions: [
                {
                    action: 'explore',
                    title: 'View',
                    icon: '/static/icons/icon-72x72.png'
                },
                {
                    action: 'close',
                    title: 'Close',
                    icon: '/static/icons/icon-72x72.png'
                }
            ]
        };

        event.waitUntil(
            self.registration.showNotification('Coffee Shop Manager', options)
        );
    }
});

// Notification click handler
self.addEventListener('notificationclick', event => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

function doBackgroundSync() {
    console.log('Background sync triggered');
    // Future: Sync offline data when connection is restored
}
"""

    return JsonResponse(service_worker_content, content_type="application/javascript")


def logout_view(request):
    """Custom logout view"""
    logout(request)
    return redirect("login")


def custom_login(request):
    """Custom login view to handle inactive users"""
    if request.method == "POST":
        phone = request.POST.get(
            "username"
        )  # Django uses 'username' field for USERNAME_FIELD
        password = request.POST.get("password")

        try:
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid phone number or password.")
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An error occurred during login.")

    return render(request, "auth/login.html")
