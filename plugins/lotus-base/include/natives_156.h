#pragma once
#include "types.h"
#include "crossmap.h"

namespace Native {
    typedef void (*NativeHandler)(rage::scrNativeCallContext* context);
    NativeHandler GetNativeHandler(uint64_t hash);

    namespace PLAYER {
        inline Player PLAYER_ID() {
            rage::scrNativeCallContext ctx;
            GetNativeHandler(0x4F8644AF03D0E0D6)(&ctx);
            return ctx.GetArgument<Player>(0);
        }

        inline Ped GET_PLAYER_PED(Player player) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            GetNativeHandler(0xD4B0AE9D530A24A6)(&ctx);
            return ctx.GetArgument<Ped>(0);
        }

        inline void SET_PLAYER_INVINCIBLE(Player player, BOOL toggle) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            ctx.Push(toggle);
            GetNativeHandler(0x48DA92019A82B340)(&ctx);
        }

        inline void SET_PLAYER_WANTED_LEVEL(Player player, int wantedLevel, BOOL disableSpeed) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            ctx.Push(wantedLevel);
            ctx.Push(disableSpeed);
            GetNativeHandler(0xF3F92C78AE19F0D2)(&ctx);
        }

        inline void CLEAR_PLAYER_WANTED_LEVEL(Player player) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            GetNativeHandler(0xE8912A34F901EBC3)(&ctx);
        }

        inline void SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER(Player player, float mult) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            ctx.Push(mult);
            GetNativeHandler(0x10B63496350E72C3)(&ctx);
        }

        inline void SET_SWIM_MULTIPLIER_FOR_PLAYER(Player player, float mult) {
            rage::scrNativeCallContext ctx;
            ctx.Push(player);
            ctx.Push(mult);
            GetNativeHandler(0x9A440D9B38B429A8)(&ctx);
        }
    }

    namespace ENTITY {
        inline Vector3 GET_ENTITY_COORDS(Entity entity, BOOL alive) {
            rage::scrNativeCallContext ctx;
            ctx.Push(entity);
            ctx.Push(alive);
            GetNativeHandler(0x6B764E1A4AA4C4C3)(&ctx);
            return ctx.GetArgument<Vector3>(0);
        }

        inline void SET_ENTITY_COORDS(Entity entity, float x, float y, float z, BOOL xAxis, BOOL yAxis, BOOL zAxis, BOOL clearArea) {
            rage::scrNativeCallContext ctx;
            ctx.Push(entity);
            ctx.Push(x);
            ctx.Push(y);
            ctx.Push(z);
            ctx.Push(xAxis);
            ctx.Push(yAxis);
            ctx.Push(zAxis);
            ctx.Push(clearArea);
            GetNativeHandler(0x06843DA7060A026B)(&ctx);
        }

        inline void SET_ENTITY_HEALTH(Entity entity, int health) {
            rage::scrNativeCallContext ctx;
            ctx.Push(entity);
            ctx.Push(health);
            GetNativeHandler(0x6B764E1A4AA4C4C3)(&ctx);
        }

        inline void SET_ENTITY_VISIBLE(Entity entity, BOOL toggle, BOOL unk) {
            rage::scrNativeCallContext ctx;
            ctx.Push(entity);
            ctx.Push(toggle);
            ctx.Push(unk);
            GetNativeHandler(0xAE3C4387C5D23055)(&ctx);
        }
    }

    namespace VEHICLE {
        inline Vehicle CREATE_VEHICLE(Hash modelHash, float x, float y, float z, float heading, BOOL isNetwork, BOOL netMissionEntity) {
            rage::scrNativeCallContext ctx;
            ctx.Push(modelHash);
            ctx.Push(x);
            ctx.Push(y);
            ctx.Push(z);
            ctx.Push(heading);
            ctx.Push(isNetwork);
            ctx.Push(netMissionEntity);
            GetNativeHandler(0xAF35D0D2583051B0)(&ctx);
            return ctx.GetArgument<Vehicle>(0);
        }

        inline void SET_VEHICLE_ON_GROUND_PROPERLY(Vehicle vehicle) {
            rage::scrNativeCallContext ctx;
            ctx.Push(vehicle);
            GetNativeHandler(0x6BC97F4F4D50EB04)(&ctx);
        }

        inline void SET_VEHICLE_FORWARD_SPEED(Vehicle vehicle, float speed) {
            rage::scrNativeCallContext ctx;
            ctx.Push(vehicle);
            ctx.Push(speed);
            GetNativeHandler(0x10B63496350E72C3)(&ctx);
        }

        inline void SET_VEHICLE_FIXED(Vehicle vehicle) {
            rage::scrNativeCallContext ctx;
            ctx.Push(vehicle);
            GetNativeHandler(0x1121E9A424F3D434)(&ctx);
        }

        inline void SET_VEHICLE_DIRT_LEVEL(Vehicle vehicle, float dirt) {
            rage::scrNativeCallContext ctx;
            ctx.Push(vehicle);
            ctx.Push(dirt);
            GetNativeHandler(0xAB22A1E86E243F24)(&ctx);
        }

        inline void SET_VEHICLE_BOOST_ACTIVE(Vehicle vehicle, BOOL active) {
            rage::scrNativeCallContext ctx;
            ctx.Push(vehicle);
            ctx.Push(active);
            GetNativeHandler(0x260BE8F093C29324)(&ctx);
        }
    }

    namespace WEAPON {
        inline void GIVE_WEAPON_TO_PED(Ped ped, Hash weaponHash, int ammoCount, BOOL isHidden, BOOL equipNow) {
            rage::scrNativeCallContext ctx;
            ctx.Push(ped);
            ctx.Push(weaponHash);
            ctx.Push(ammoCount);
            ctx.Push(isHidden);
            ctx.Push(equipNow);
            GetNativeHandler(0x0E1E269AC7F9B611)(&ctx);
        }

        inline void SET_PED_INFINITE_AMMO(Ped ped, BOOL toggle, Hash weaponHash) {
            rage::scrNativeCallContext ctx;
            ctx.Push(ped);
            ctx.Push(toggle);
            ctx.Push(weaponHash);
            GetNativeHandler(0xADF692F2619F232A)(&ctx);
        }

        inline void SET_PED_INFINITE_AMMO_CLIP(Ped ped, BOOL toggle) {
            rage::scrNativeCallContext ctx;
            ctx.Push(ped);
            ctx.Push(toggle);
            GetNativeHandler(0x14E48453700E778B)(&ctx);
        }

        inline void REMOVE_ALL_PED_WEAPONS(Ped ped, BOOL p1) {
            rage::scrNativeCallContext ctx;
            ctx.Push(ped);
            ctx.Push(p1);
            GetNativeHandler(0xBF0FD6E45C50B657)(&ctx);
        }
    }

    namespace MISC {
        inline void SET_WEATHER_TYPE_NOW_PERSIST(const char* weatherType) {
            rage::scrNativeCallContext ctx;
            ctx.Push(weatherType);
            GetNativeHandler(0x2F46E6B4A8D3F982)(&ctx);
        }

        inline void SET_TIME_SCALE(float timeScale) {
            rage::scrNativeCallContext ctx;
            ctx.Push(timeScale);
            GetNativeHandler(0x8C17F7A250B94A67)(&ctx);
        }

        inline void SET_RIOT_MODE_ENABLED(BOOL toggle) {
            rage::scrNativeCallContext ctx;
            ctx.Push(toggle);
            GetNativeHandler(0x7D6487E120A30784)(&ctx);
        }

        inline void SET_ARTIFICIAL_LIGHTS_STATE(BOOL state) {
            rage::scrNativeCallContext ctx;
            ctx.Push(state);
            GetNativeHandler(0x165583AE32304859)(&ctx);
        }
    }

    namespace GRAPHICS {
        inline void DRAW_RECT(float x, float y, float width, float height, int r, int g, int b, int a) {
            rage::scrNativeCallContext ctx;
            ctx.Push(x);
            ctx.Push(y);
            ctx.Push(width);
            ctx.Push(height);
            ctx.Push(r);
            ctx.Push(g);
            ctx.Push(b);
            ctx.Push(a);
            GetNativeHandler(0x3A618A23B2A10F44)(&ctx);
        }
    }
}
