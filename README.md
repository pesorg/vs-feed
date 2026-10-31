# vs-vpn-feed

Every 2 hours a GitHub Action reads the public Telegram channel **@persianvpnhub**, takes the latest 50 V2Ray share links (duplicates removed, newest first) and saves them to `feed/configs.txt` — one link per line.

The vs vpn app reads this file instead of Telegram, so it works in Iran without a VPN.

## Links for the app
Replace `<USER>` with your GitHub username:

- Primary: `https://raw.githubusercontent.com/<USER>/vs-vpn-feed/main/feed/configs.txt`
- Fallback (CDN): `https://cdn.jsdelivr.net/gh/<USER>/vs-vpn-feed@main/feed/configs.txt`
- Last update time (UTC): `feed/updated.txt`

## Manual run
Actions tab → **Update config feed** → **Run workflow**.

## Notes
- If no configs are found (or Telegram fails), the old file is kept and nothing is committed.
- Configs are collected from a public channel; they are free, unverified servers — test before use.
