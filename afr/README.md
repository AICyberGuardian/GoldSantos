# GoldHEN Application File Redirector (AFR) Subsystem

## Overview
GoldHEN's AFR (`afr.prx`) intercepts file requests from `/app0/` and transparently redirects them to `/data/GoldHEN/AFR/<TitleID>/`.

## GTA V Archive Interception Protocol:
Because GTA V reads data from compressed RPF archives, individual loose files (like `handling.meta`) are NOT requested as `/app0/handling.meta`. Instead, the game requests:
```text
/app0/update/update.rpf
```

Therefore, all custom handling, visual settings, and blood decals must be packed inside an `update.rpf` container located at:
```text
/data/GoldHEN/AFR/CUSA00411/update/update.rpf
```

## `plugins.ini` Configuration:
Ensure the following line is added to `/data/GoldHEN/plugins.ini` on your PS4:
```ini
[CUSA00411]
/data/GoldHEN/plugins/afr.prx=true
```

## Workflow to Build Custom `update.rpf`:
1. Extract vanilla `update.rpf` from PS4 GTA V v1.56.
2. Edit target assets in `src/` (e.g. `src/handling/handling_chaos_boost.meta` -> `common/data/handling.meta`).
3. Repack `update.rpf` using OpenIV or `rpftool`.
4. Place the finished `update.rpf` in `afr/CUSA00411/update/`.
5. Deploy via `python gtav-modding/tools/deploy_mod_stack_lan.py --afr`.
