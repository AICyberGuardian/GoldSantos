#include "menu.h"
#include <stdio.h>

MenuState g_Menu = {0};

// GTA Online DLC Vehicle Model Hashes
#define HASH_OPPRESSOR2  0x7B7E623E  // Oppressor Mk II
#define HASH_DELUXO      0x58210FCD  // Deluxo (Hovering/Flying)
#define HASH_VIGILANTE   0xB390F240  // Vigilante (Batmobile)
#define HASH_THRAX       0xC586C6B3  // Truffade Thrax
#define HASH_KRIEGER     0x8CE6B500  // Benefactor Krieger
#define HASH_EMERUS      0x7C9A4B82  // Progen Emerus
#define HASH_KHANJALI    0xAA6F19A2  // TM-02 Khanjali Tank
#define HASH_SCRAMJET    0x51E28330  // Declasse Scramjet (Rocket Jump)
#define HASH_BUZZARD     0x2F03547B  // Buzzard Attack Chopper

void SpawnVehicle(Hash modelHash) {
    Player player = Native::PLAYER::PLAYER_ID();
    Ped playerPed = Native::PLAYER::GET_PLAYER_PED(player);
    Vector3 coords = Native::ENTITY::GET_ENTITY_COORDS(playerPed, true);

    // Spawn 5 units in front of player
    Vehicle veh = Native::VEHICLE::CREATE_VEHICLE(modelHash, coords.x + 3.0f, coords.y + 3.0f, coords.z, 0.0f, true, false);
    Native::VEHICLE::SET_VEHICLE_ON_GROUND_PROPERLY(veh);
    Native::VEHICLE::SET_VEHICLE_FORWARD_SPEED(veh, 0.0f);
}

void TeleportTo(float x, float y, float z) {
    Player player = Native::PLAYER::PLAYER_ID();
    Ped playerPed = Native::PLAYER::GET_PLAYER_PED(player);
    Native::ENTITY::SET_ENTITY_COORDS(playerPed, x, y, z, false, false, false, true);
}

void Menu_Init() {
    g_Menu.isOpen = false;
    g_Menu.currentSubmenu = SUB_MAIN;
    g_Menu.currentOption = 1;
    g_Menu.godMode = false;
    g_Menu.neverWanted = false;
    g_Menu.infiniteAmmo = false;
    g_Menu.superJump = false;
    g_Menu.fastRun = false;
    g_Menu.vehicleGod = false;
    g_Menu.riotMode = false;
    g_Menu.snowActive = false;
}

void Menu_Update() {
    Player player = Native::PLAYER::PLAYER_ID();
    Ped playerPed = Native::PLAYER::GET_PLAYER_PED(player);

    if (g_Menu.godMode) {
        Native::PLAYER::SET_PLAYER_INVINCIBLE(player, true);
        Native::ENTITY::SET_ENTITY_HEALTH(playerPed, 200);
    }
    if (g_Menu.neverWanted) {
        Native::PLAYER::CLEAR_PLAYER_WANTED_LEVEL(player);
    }
    if (g_Menu.fastRun) {
        Native::PLAYER::SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER(player, 1.49f);
    }
    if (g_Menu.riotMode) {
        Native::MISC::SET_RIOT_MODE_ENABLED(true);
    }
}

void Draw_MainMenu() {
    // Render options: 1. Player, 2. Weapons, 3. DLC Vehicles, 4. World Chaos, 5. Teleports
}

void Draw_DLCVehiclesMenu() {
    // 1. Oppressor Mk II
    // 2. Deluxo (Flying)
    // 3. Vigilante (Batmobile)
    // 4. Truffade Thrax
    // 5. Benefactor Krieger
    // 6. TM-02 Khanjali Tank
    // 7. Scramjet
    // 8. Buzzard Attack Chopper
}

void Draw_TeleportsMenu() {
    // 1. Mount Chiliad (x: 450.7, y: 5566.5, z: 781.1)
    // 2. Maze Bank Tower (x: -75.0, y: -818.0, z: 326.0)
    // 3. LS Airport Runway (x: -1336.0, y: -3044.0, z: 13.9)
    // 4. Fort Zancudo Military (x: -2047.0, y: 3132.0, z: 32.8)
}

void Menu_Draw() {
    if (!g_Menu.isOpen) return;

    // Draw Background Rect (X: 0.15, Y: 0.35, W: 0.22, H: 0.45, RGBA: 0, 0, 0, 200)
    Native::GRAPHICS::DRAW_RECT(0.15f, 0.35f, 0.22f, 0.45f, 0, 0, 0, 200);

    // Draw Title Banner (X: 0.15, Y: 0.15, W: 0.22, H: 0.08, RGBA: 180, 0, 0, 255)
    Native::GRAPHICS::DRAW_RECT(0.15f, 0.15f, 0.22f, 0.08f, 180, 0, 0, 255);
}
