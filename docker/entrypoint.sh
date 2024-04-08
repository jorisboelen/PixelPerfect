#!/usr/bin/env bash
pixelperfect migrate
exec pixelperfect runserver --host 0.0.0.0 "$@"
