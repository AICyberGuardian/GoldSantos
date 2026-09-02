# OpenOrbis Makefile for GTA V v1.56 GoldHEN PRX Plugin

TARGET = gtav_menu_156
CXX = orbis-clang++
CC = orbis-clang
LD = orbis-ld

CFLAGS = -target x86_64-scei-ps4 -O2 -Wall -std=c++17 -Iinclude -I$(GOLDHEN_SDK)/include
LDFLAGS = -target x86_64-scei-ps4 -shared -L$(GOLDHEN_SDK)/lib -lkernel -lScePad

SRCS = src/main.cpp src/menu.cpp src/hooks.cpp
OBJS = $(SRCS:.cpp=.o)

all: $(TARGET).prx

$(TARGET).prx: $(OBJS)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.cpp
	$(CXX) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET).prx
