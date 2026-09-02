#include <stdint.h>
#include <stdbool.h>
#include "types.h"
#include "crossmap.h"
#include "natives_156.h"
#include "menu.h"
#include "hooks.h"

// Memory Scanner & Hook Helpers
namespace Memory {
    uintptr_t g_baseAddress = 0;

    uintptr_t FindPattern(const char* pattern, const char* mask) {
        // Pattern scanner implementation across .text segment
        return 0;
    }
}

// Global Native Dispatcher Cache
Native::NativeHandler Native::GetNativeHandler(uint64_t hash) {
    uint64_t translated = TranslateNativeHash(hash);
    // Looks up translated hash in 1.56 g_nativeRegistrationTable
    return nullptr;
}

// GoldHEN Plugin Entrypoint
extern "C" int prx_start(size_t args, const void* argp) {
    Hooks::InstallHooks();
    return 0;
}

extern "C" int prx_stop(size_t args, const void* argp) {
    Hooks::RemoveHooks();
    return 0;
}
