import file
import threading
from flask import Flask, Response, stream_with_context
import time

app = Flask(__name__)

@app.route("/")
def index():
    return r"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="content"></div>
<script>
const es = new EventSource("/stream");
es.onmessage = e => {
  const html = e.data.replace(/\\n/g, "\n").replace(/\\t/g, "\t");
  document.open();
  document.write(html);
  document.close();
};
</script>
</body>
</html>"""

@app.route("/stream")
def stream():
    def event_stream():
        last = None
        while True:
            current = file.currentFile
            if current != last:
                # SSE format: "data: ...\n\n"
                # Escape newlines so multi-line HTML stays as one SSE message
                escaped = current.replace("\n", "\\n")
                yield f"data: {escaped}\n\n"
                last = current
            time.sleep(0.2)
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

threading.Thread(target=app.run, kwargs={"port": 8080}, daemon=True).start()