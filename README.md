# sd-wan-edge
sd-wan edge scripts


# First install
```
git clone https://github.com/vewe-richard/sd-wan-edge.git
```


# Run it
```
cd sd-wan-edge
vim config.json
vim poll.y        #remove break after loop() and set sleep time to 6 or some others
export PYTHONPATH="$PWD"
python3 ./poll.py
```

