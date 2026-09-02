#include "hooks.h"
#include "menu.h"
#include <stdint.h>

namespace Hooks {
    bool InstallHooks() {
        Menu_Init();
        // 1. Scan for eboot.bin memory base
        // 2. Install hook into scePadRead or game script fiber tick
        return true;
    }

    void RemoveHooks() {
        // Restore original bytes
    }
}
