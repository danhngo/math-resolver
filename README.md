# math resolver

# 1. Create Virttual Environmen
virtualenv venv
python3 -m venv venv
source venv/bin/activate

# 2. Install requirment
pip3 install -r requirement.txt

# 3. Run App al local
python3 app.py

# 4. Run App at server (if any)

ssh danh@172.208.119.43
cd /home/danh/math-resolver

nohup python3 app.py &

http://172.208.119.43:8050/
lsof -i tcp:8050
