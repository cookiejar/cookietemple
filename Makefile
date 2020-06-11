ifeq ($(OS),Windows_NT)
include cookietemple/util/BuildTools/Windows.mk
else
include cookietemple/util/BuildTools/Linux.mk
endif