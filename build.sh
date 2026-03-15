# Install Python dependencies
pip install -r requirements.txt

# Download and extract FFmpeg (Linux version)
mkdir -p ffmpeg
cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xvf ffmpeg-release-amd64-static.tar.xz --strip-components=1
cd ..
