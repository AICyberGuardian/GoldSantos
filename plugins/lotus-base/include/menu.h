#pragma once
#include "types.h"
#include "natives_156.h"

enum Submenu {
    SUB_MAIN,
    SUB_PLAYER,
    SUB_WEAPONS,
    SUB_VEHICLES,
    SUB_DLC_VEHICLES,
    SUB_WORLD_CHAOS,
    SUB_TELEPORTS,
    SUB_OBJECT_SPOONER,
    SUB_SETTINGS
};

struct MenuState {
    bool isOpen;
    Submenu currentSubmenu;
    Submenu lastSubmenu;
    int currentOption;
    int optionCount;
    
    // Feature Toggles
    bool godMode;
    bool neverWanted;
    bool infiniteAmmo;
    bool superJump;
    bool fastRun;
    bool vehicleGod;
    bool riotMode;
    bool snowActive;
};

extern MenuState g_Menu;

void Menu_Init();
void Menu_Update();
void Menu_Draw();
void Menu_HandleInput();

// Submenu Drawing Handlers
void Draw_MainMenu();
void Draw_PlayerMenu();
void Draw_WeaponsMenu();
void Draw_VehiclesMenu();
void Draw_DLCVehiclesMenu();
void Draw_WorldChaosMenu();
void Draw_TeleportsMenu();
