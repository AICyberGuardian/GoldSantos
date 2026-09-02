# Ped Damage Decals & Blood Persistence Specification

## Target Asset:
* **Internal Path:** `update.rpf / x64 / textures / peddamagedecals.rpf`
* **Texture Dicts:** `peddamagedecals.ytd`

## Modding Parameters:
1. **Decal Lifetime:** Stock GTA V fades blood decals on pedestrian clothing and skin after 3–5 seconds. By increasing decal lifetime and buffer capacity in `visualsettings.dat`, bullet wounds remain visible during sustained shootouts.
2. **Texture Replacement:** High-contrast arterial spray and exit wound textures can be imported into `peddamagedecals.ytd` using OpenIV (DDS format: DXT5/BC3 with mipmaps).
3. **PS4 VRAM Safety:** Maintain texture resolution at $512 \times 512$ or $1024 \times 1024$. Do NOT use $4096 \times 4096$ textures on PS4 Fat to avoid texture memory thrashing.
