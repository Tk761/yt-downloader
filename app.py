from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# On Render, we must use the /tmp folder for temporary downloads
DOWNLOAD_FOLDER = '/tmp'

def format_size(bytes):
    if not bytes: return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form.get('url')
    ydl_opts = {'quiet': True, 'format_sort': ['res', 'ext:mp4:m4a']}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none':
                    formats.append({
                        'format_id': f['format_id'],
                        'resolution': f.get('resolution', 'N/A'),
                        'ext': f['ext'],
                        'size': format_size(f.get('filesize') or f.get('filesize_approx')),
                        'type': 'video'
                    })
            
            return render_template('index.html', 
                                 formats=formats, 
                                 title=info.get('title'), 
                                 thumbnail=info.get('thumbnail'),
                                 url=url)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    f_id = request.form.get('format_id')
    is_audio = request.form.get('is_audio') == 'True'

    # Set up options for Linux/Render
    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else f'{f_id}+bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Correct Linux path
        'noplaylist': True
    }

    if is_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Adjust path for audio conversion
            if is_audio:
                filename = os.path.splitext(filename)[0] + ".mp3"

            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Download Error: {str(e)}"

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)