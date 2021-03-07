set botFolder=%1

mkdir empty
robocopy .\empty .\published /MIR
rmdir empty

robocopy .\%botFolder% .\published /MIR /XD venv scripts .idea logs __pycache__ /XF replay.json README