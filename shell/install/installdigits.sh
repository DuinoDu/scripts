cd ~/Downloads
git clone https://github.com/NVIDIA/DIGITS.git digits  
cd digits  
sudo apt-get install graphviz gunicorn  
for req in $(cat requirements.txt); do sudo pip install $req; done 
./digits-devserver && \
echo "Go to http://localhost:5000 to use DIGITS" 
