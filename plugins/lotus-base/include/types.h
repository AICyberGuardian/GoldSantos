#pragma once
#include <stdint.h>
#include <stdbool.h>

typedef int32_t Entity;
typedef int32_t Ped;
typedef int32_t Vehicle;
typedef int32_t Cam;
typedef int32_t Object;
typedef int32_t Pickup;
typedef int32_t Player;
typedef uint32_t Hash;
typedef int32_t BOOL;

struct Vector3 {
    float x;
    float _padX;
    float y;
    float _padY;
    float z;
    float _padZ;
};

namespace rage {
    class scrNativeCallContext {
    public:
        void* m_pReturn;
        uint32_t m_nArgCount;
        void* m_pArgs;
        uint32_t m_nDataCount;
        Vector3* m_pOutVectors[4];

        template <typename T>
        inline T GetArgument(int index) {
            return reinterpret_cast<T*>(m_pArgs)[index];
        }

        template <typename T>
        inline void SetResult(int index, T value) {
            reinterpret_cast<T*>(m_pReturn)[index] = value;
        }
    };
}
