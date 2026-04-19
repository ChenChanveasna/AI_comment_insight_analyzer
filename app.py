import os

from flask import Flask, render_template, request

from analysis import analyze_comments
from youtube_comment import API_KEY, fetch_comments, get_video_id


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "comment-insight-analyzer")


@app.after_request
def disable_cache(response):
    # Always serve fresh analytics so each new link submission replaces old results.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/", methods=["GET"])
def index():
    context = {
        "youtube_url": "",
        "analysis": None,
        "error": None,
        "info": None,
        "api_ready": bool(API_KEY),
    }

    youtube_url = request.args.get("youtube_url", "").strip()
    if youtube_url:
        context["youtube_url"] = youtube_url

        if not API_KEY:
            context["error"] = "YOUTUBE_API_KEY is missing. Add it to your .env file before analyzing a video."
            return render_template("index.html", **context)

        video_id = get_video_id(youtube_url)
        if not video_id:
            context["error"] = "That does not look like a valid YouTube video URL."
            return render_template("index.html", **context)

        try:
            comments = fetch_comments(video_id)
        except Exception as exc:
            context["error"] = f"Unable to load comments: {exc}"
            return render_template("index.html", **context)

        if not comments:
            context["error"] = "No comments were returned for that video. Comments may be disabled or filtered."
            return render_template("index.html", **context)

        analysis = analyze_comments(comments)
        context["analysis"] = analysis
        context["chart_data"] = {
            "labels": ["Positive", "Neutral", "Negative"],
            "values": [
                analysis["sentiment_counts"]["positive"],
                analysis["sentiment_counts"]["neutral"],
                analysis["sentiment_counts"]["negative"],
            ],
            "topWords": [{"word": word, "count": count} for word, count in analysis["top_words"]],
        }
        context["info"] = f"Loaded {analysis['total_comments']} comments and built the dashboard below."

    return render_template("index.html", **context)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
