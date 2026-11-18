# -*- coding: utf-8 -*-
"""Builds the two copies of Study Den that run outside Claude.

  index.html               the hosted copy: installable, works offline
  study-den-offline.html   one self-contained file to open from disk

Both wrap study-den.html (the artifact source) in the document skeleton the
claude.ai viewer normally supplies. Run: python3 -I build-site.py
"""
import io, os, json, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'study-den.html')
SITE = HERE   # GitHub Pages serves this repository from its root

body = io.open(SRC, encoding='utf-8').read()

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="A gamified study hub: launchpad, exam countdowns, study plan and a companion that levels up when you show up.">
<meta name="theme-color" content="#f5f6f8">
__EXTRA__<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head>
<body>
'''

PWA_HEAD = '''<title>Study Den</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Study Den">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
'''

SW_REG = '''
<script>
/* Keeps the den openable with no signal. Network first, so an update to the
   site is picked up as soon as the phone is online again. */
if('serviceWorker' in navigator){
  addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});
}
</script>
'''

# ---- hosted copy -----------------------------------------------------------
io.open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(
    HEAD.replace('__EXTRA__', PWA_HEAD) + body + SW_REG + '\n</body>\n</html>\n')

# ---- single-file copy ------------------------------------------------------
io.open(os.path.join(HERE, 'study-den-offline.html'), 'w', encoding='utf-8').write(
    HEAD.replace('__EXTRA__', '') + body + '\n</body>\n</html>\n')

# ---- manifest --------------------------------------------------------------
manifest = {
    "name": "Study Den",
    "short_name": "Study Den",
    "description": "A gamified study hub: launchpad, exam countdowns, study plan and a companion that levels up when you show up.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#f5f6f8",
    "theme_color": "#0d85a0",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
io.open(os.path.join(SITE, 'manifest.webmanifest'), 'w', encoding='utf-8').write(
    json.dumps(manifest, indent=2) + '\n')

# ---- service worker --------------------------------------------------------
SW = '''/* Study Den offline shell. Network first with a cache fallback, so the
   page is always fresh online and still opens with no connection. */
var CACHE = 'study-den-v__V__';
var SHELL = ['./', './index.html', './manifest.webmanifest',
             './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(SHELL); })
    .then(function(){ return self.skipWaiting(); }).catch(function(){}));
});

self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){ return k === CACHE ? null : caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});

self.addEventListener('fetch', function(e){
  if(e.request.method !== 'GET') return;
  /* The page itself is always revalidated against the server, so an update
     shows up on the next open instead of waiting out the CDN cache. The
     server answers 304 when nothing changed, so this costs almost nothing. */
  var req = e.request.mode === 'navigate'
    ? new Request(e.request.url, {cache: 'no-cache', credentials: 'same-origin'})
    : e.request;
  e.respondWith(
    fetch(req).then(function(res){
      var copy = res.clone();
      caches.open(CACHE).then(function(c){ c.put(e.request, copy); }).catch(function(){});
      return res;
    }).catch(function(){
      return caches.match(e.request).then(function(hit){
        return hit || (e.request.mode === 'navigate' ? caches.match('./index.html') : undefined);
      });
    })
  );
});
'''
# the cache name changes with the build so a new deploy replaces the old shell
stamp = str(zlib.crc32(body.encode('utf-8')))
io.open(os.path.join(SITE, 'sw.js'), 'w', encoding='utf-8').write(SW.replace('__V__', stamp))

io.open(os.path.join(SITE, '.nojekyll'), 'w', encoding='utf-8').write('')

for f in ('index.html', 'manifest.webmanifest', 'sw.js', 'study-den-offline.html'):
    print('%-24s %8d' % (f, os.path.getsize(os.path.join(HERE, f))))
