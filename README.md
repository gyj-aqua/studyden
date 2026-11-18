# Study Den

A gamified study hub: a launchpad for the sites and artifacts you study from,
exam countdowns, a study plan, a focus timer, and a companion that levels up
when you show up (and sulks when you don't).

| | |
|---|---|
| **Live site** | https://gyj-aqua.github.io/study-den/ |
| **Claude artifact** | https://claude.ai/artifact/2L4tdwyy9iDsJYFwWitUdP |

Two copies, same app:

- **The artifact** saves to your Claude account, so it follows you to any
  device you sign in on.
- **This site** saves in whichever browser you open it in. It installs to a
  phone home screen and keeps working with no signal.

Move progress between them with **Download backup** / **Restore from a backup**
in the World tab.

## Building

`study-den.html` is the source — it is the artifact body, with no document
skeleton (claude.ai adds one at publish time).

```sh
python3 -I make-icon.py    # redraw the app icons
python3 -I build-site.py   # -> docs/ (hosted copy) and study-den-offline.html
```

`docs/` is what GitHub Pages serves. `study-den-offline.html` is the same app
as a single self-contained file you can open straight from disk.
