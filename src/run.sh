cd "$(dirname "$0")"
# Check if /usr/local/bin/python3 exists and is executable
if [ -x /usr/local/bin/python3 ]; then
    /usr/local/bin/python3 ./main.py
else
    python ./main.py
fi
