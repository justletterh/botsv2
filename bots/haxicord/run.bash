#!/bin/bash
cd /app
haxe build.hxml&>/dev/null&&(bin/cpp/Main>/dev/null)&>/dev/stdout||haxe build.hxml