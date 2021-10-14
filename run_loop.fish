#!/usr/bin/fish

while true
      set file (inotifywait -qc -e close_write *.py | cut -d ',' -f1)
      clear
      flake8 $file
      ./main.py
end
