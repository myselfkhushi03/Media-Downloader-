from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL required"}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'noplaylist': True}) as ydl:
            data = ydl.extract_info(url, download=False)
            if 'entries' in data: data = data['entries'][0]

            video_formats, audio_formats = {}, {}
            for f in data.get('formats', []):
                if not f.get('url'): continue
                height = f.get('height')
                abr = f.get('abr')
                size = f.get('filesize') or f.get('filesize_approx')
                size_str = f"{round(size/1024/1024,1)} MB" if size else "Auto"

                if f.get('vcodec')!= 'none' and height:
                    q = f"{height}p"
                    if q not in video_formats:
                        video_formats[q] = {"quality": q, "ext": f['ext'], "url": f['url'], "size": size_str}

                if f.get('vcodec') == 'none' and f.get('acodec')!= 'none':
                    q = f"{int(abr)}kbps" if abr else "128kbps"
                    if q not in audio_formats:
                        audio_formats[q] = {"quality": q, "ext": f['ext'], "url": f['url'], "size": size_str}

            v_final = sorted(video_formats.values(), key=lambda x: int(x['quality'].replace('p','')), reverse=True)
            a_final = sorted(audio_formats.values(), key=lambda x: int(x['quality'].replace('kbps','')), reverse=True)

            if not v_final: v_final = [{"quality":"Original","ext":"mp4","url":data.get('url'),"size":"Best"}]

            platform = "YouTube"
            if "instagram" in url: platform = "Instagram"
            elif "facebook" in url: platform = "Facebook"

            return jsonify({
                "title": data.get('title') or "Video",
                "thumbnail": data.get('thumbnail'),
                "duration": data.get('duration_string') or f"{data.get('duration',0)}s",
                "platform": platform,
                "video": v_final[:8],
                "audio": a_final[:6]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
