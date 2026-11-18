# Study Den

A gamified study hub: a launchpad for the sites and artifacts you study from,
exam countdowns, a study plan, a focus timer, and one of eighteen companions
that levels up when you show up (and sulks when you don't).

| | |
|---|---|
| **Live site** | https://gyj-aqua.github.io/studyden/ |
| **Claude artifact** | https://claude.ai/artifact/2L4tdwyy9iDsJYFwWitUdP |

Two copies, same app:

- **The artifact** saves to your Claude account, so it follows you to any
  device you sign in on.
- **This site** saves in whichever browser you open it in. It installs to a
  phone home screen and keeps working with no signal.

Move progress between them with **Download backup** / **Restore from a backup**
in the World tab.

## Layout

GitHub Pages serves this repository from the root of `main`, so `index.html`
lives here beside the source. Every path in the page is relative, so the site
works whether it is served from a root domain or from a `/studyden/` prefix.

| file | what it is |
|---|---|
| `study-den.html` | the source: the artifact body, with no document skeleton (claude.ai adds one at publish time) |
| `index.html` | the hosted copy — the source wrapped in that skeleton, plus the manifest, icons and service worker |
| `study-den-offline.html` | the same app as one self-contained file you can open straight from disk |
| `sw.js` | caches the app so it opens with no connection; network first, so it refreshes as soon as you are online |
| `build-site.py` | rebuilds `index.html` and `study-den-offline.html` from the source |
| `art/` | the eighteen companions, cut out of the reference sheets as transparent PNGs — the source of truth for the artwork |
| `inline-art.py` | rebuilds the `ART` block in `study-den.html` from `art/`, so the images travel inside the page |
| `make-icon.py` | builds the app icon from `art/mochi.png` at 512 / 192 / 180 px |

## Building

Edit `study-den.html`, then:

```sh
python3 -I build-site.py
```

After changing anything in `art/`:

```sh
python3 -I inline-art.py && python3 -I make-icon.py && python3 -I build-site.py
```
