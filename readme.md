ollama run mistral

uvicorn hackrx_fastapi_llm:app --reload

http://127.0.0.1:8000/docs


curl -X POST http://127.0.0.1:8000/hackrx/run -H "Content-Type: application/json" -H "Authorization: Bearer 6890cfc475e4b61cf6b049684a7c7fa65ebb88696d672f1a9ce7d86f901bdbb8" -d @payload.json

curl -X POST "http://127.0.0.1:8000/hackrx/run" ^
 -H "Content-Type: application/json" ^
 -H "Authorization: Bearer 6890cfc475e4b61cf6b049684a7c7fa65ebb88696d672f1a9ce7d86f901bdbb8" ^
 -d @payload.json



ssh -i C:\Users\Administrator\Downloads\bajaj.pem ec2-user@18.206.252.22
sudo yum update -y
sudo yum install python3 -y
sudo yum install git -y
git clone https://github.com/anamika3094/HackRx.git
cd HackRx
sudo yum install python3 python3-pip -y
pip3 --version
pip3 install --upgrade pip
pip3 install -r requirements.txt



ls
chmod 400 bajaj.pem
ssh -i bajaj.pem ec2-user@18.206.252.22
sudo yum update -y
sudo yum install git -y
git clone https://github.com/anamika3094/HackRx.git
cd HackRx
sudo yum install python3 python3-pip -y
pip3 install --upgrade pip
sudo growpart /dev/nvme0n1 1
sudo xfs_growfs -d /
rm -rf ~/.cache/pip
sudo yum clean all
df -h  # Check space again
sudo growpart /dev/xvda 1
lsblk -f
sudo xfs_growfs -d /
df -h
rm -rf ~/.cache/pip
sudo yum clean all
TMPDIR=$HOME pip3 install --no-cache-dir -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
