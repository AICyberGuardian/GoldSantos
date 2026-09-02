# Upstream Ecosystem & Tooling Integrations

This document tracks upstream projects, tools, and repositories in the PS4 and GTA V homebrew ecosystem that **GoldSantos** integrates with, references, or builds upon, ensuring zero duplication and maximum interoperability.

---

## 🗺️ Upstream Reference Matrix

| Project | Author / Maintainer | Role in Ecosystem | GoldSantos Integration & Differentiation |
| :--- | :--- | :--- | :--- |
| [**`PS4-GTA-V-Menu-Base`**](https://github.com/2much4u/PS4-GTA-V-Menu-Base) | `2much4u` | Foundational MIT-licensed C++ menu GUI, button handler, and native caller for PS4 GTA V. | **Architecture Base:** GoldSantos adopts this clean GUI architecture and updates the native call tables from 1.27 to 1.56 via `crossmap.h`. |
| [**`PS4-GTA-V-Native-Updater`**](https://github.com/2much4u/PS4-GTA-V-Native-Updater) | `2much4u` | IDA Pro plugin to scan new EBOOTs, associate hashes with `registerNative`, and export `natives.h`. | **Tooling Workflow:** Documented in [NATIVE_CROSSMAP_AND_PORTING.md](NATIVE_CROSSMAP_AND_PORTING.md) as the standard reverse-engineering tool for future title updates. |
| [**`PS-Game-Patch`**](https://github.com/illusionyy/PS-Game-Patch) | `illusion0001` | Upstream XML patch database for GoldHEN `game_patch.prx`. | **Zero Duplication:** GoldSantos directly pulls illusion's verified 1.56 60 FPS and skip-intro patches rather than fabricating unverified bytecode masks. |
| [**`GoldHEN_Cheat_Repository`**](https://github.com/GoldHEN/GoldHEN_Cheat_Repository) | `GoldHEN Team` | Central cheat repository for PS4 GoldHEN Cheat Manager. | **Filling the 1.56 Void:** The official repository stopped at update 1.49 for `CUSA00411`. GoldSantos provides `CUSA00411_01.56.json`, ready for upstream submission. |
| [**`rpf-cli`**](https://github.com/VIRUXE/rpf-cli) | `VIRUXE` | Modern cross-platform Rust CLI for reading, extracting, and creating GTA V RPF7 archives. | **Automated Packaging:** Integrated into our `tools/rpf_afr_builder.py` pipeline to enable 1-click terminal packaging of `update.rpf` without needing Windows GUI OpenIV. |
| [**`gameconfig`**](https://github.com/pnwparksfan/gameconfig) | `pnwparksfan` | Community repository for scaled `gameconfig.xml` pool sizes. | **Stability Invariant:** References engine memory pool scaling to prevent crashes when spawning numerous DLC vehicles or spooner props. |
| [**`PS4-GoldHEN-Plugin-Installer`**](https://github.com/AnarchyNR/PS4-GoldHEN-Plugin-Installer) | `AnarchyNR` | Windows GUI for installing GoldHEN plugins over FTP. | **Alternative GUI:** Recommended as a visual alternative to our CLI `tools/deploy_mod_stack_lan.py`. |

---

## 🛠️ Automated RPF Tooling: `rpf-cli`

To avoid requiring users to manually run proprietary GUI tools like OpenIV on Windows, GoldSantos supports **`rpf-cli`** (written in Rust) for headless archive manipulation:

```bash
# Extract vanilla update.rpf:
rpf-cli extract update.rpf ./extracted/

# Inject modified handling and visual settings:
cp afr/src/handling/handling_chaos_boost.meta ./extracted/common/data/handling.meta
cp afr/src/visualsettings/visualsettings_clean.dat ./extracted/common/data/visualsettings.dat

# Repack into staged AFR destination:
rpf-cli create ./extracted/ afr/CUSA00411/update/update.rpf
```

---

## 🤝 Upstream Contribution Plan

1. **Pull Request to `GoldHEN_Cheat_Repository`:**  
   Submit our validated `CUSA00411_01.56.json` to the official GoldHEN database so all PS4 jailbreak users worldwide can access verified GTA V 1.56 cheats directly via the GoldHEN dashboard.
2. **Open-Source OpenOrbis Releases:**  
   Provide pre-compiled GitHub release artifacts for `gtav_menu_156.prx` tagged with exact Git commit hashes.
