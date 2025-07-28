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
        "description": "Sales Management System for Coffee Shops",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#2c5aa0",
        "orientation": "portrait",
        "scope": "/",
        "categories": ["business", "productivity"],
        "lang": "en",
        "icons": [
            {
                "src": "/static/icons/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icons/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icons/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icons/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icons/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any maskable",
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
                "purpose": "any maskable",
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
        ],
    }

    return JsonResponse(manifest_data, content_type="application/manifest+json")


@login_required(login_url="/login/")
def service_worker(request):
    """Serve service worker"""
    service_worker_content = """
// Coffee Shop Manager Service Worker
const CACHE_NAME = 'coffee-shop-v2';
const STATIC_CACHE = 'static-v2';
const DYNAMIC_CACHE = 'dynamic-v2';

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
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activate event
self.addEventListener('activate', event => {
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
        })
    );
});

// Fetch event
self.addEventListener('fetch', event => {
    const { request } = event;

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Handle API requests
    if (request.url.includes('/api/')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Clone the response
                    const responseClone = response.clone();

                    // Cache the response
                    caches.open(DYNAMIC_CACHE)
                        .then(cache => {
                            cache.put(request, responseClone);
                        });

                    return response;
                })
                .catch(() => {
                    // Return cached response if network fails
                    return caches.match(request);
                })
        );
        return;
    }

    // Handle static assets
    event.respondWith(
        caches.match(request)
            .then(response => {
                if (response) {
                    return response;
                }

                return fetch(request)
                    .then(response => {
                        // Check if we received a valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone the response
                        const responseToCache = response.clone();

                        caches.open(DYNAMIC_CACHE)
                            .then(cache => {
                                cache.put(request, responseToCache);
                            });

                        return response;
                    });
            })
    );
});

// Background sync for offline data
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    // Handle offline data sync
    console.log('Background sync triggered');
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
