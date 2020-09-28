from flask import request, render_template, url_for, redirect
from attu import app
from attu.models import Reader, parse_reference


@app.route("/")
def index():
    reference = request.args.get("reference")
    if reference:
        args = {"refe": reference}
        theme = request.args.get("theme")
        if theme:
            args["theme"] = theme
        return redirect(url_for("passage", **args))
    demo_references = ["1 Nephi 3:7", "Moroni 10:3-5", "3 Nephi 2:1-4; 4:1-2"]
    demo_urls = [
        {"reference": r, "url": url_for("passage", refe=r, _external=True)} for r in demo_references
    ]
    return render_template("index.html", demo_urls=demo_urls)


@app.route("/p/<refe>")
def passage(refe):
    style = request.args.get("theme") or "wood"
    text = request.args.get("reference", refe)

    try:
        print("reference", text)
        try:
            reference = parse_reference(text)
        except Exception:
            app.logger.exception("error")
            raise
    except Exception:
        return render_template("error.html", message="Could not read your scripture reference.")

    with Reader() as r:
        verses = []
        for v in reference:
            content = r.read_verse(v[0], v[1], v[2])
            if content is None:
                app.logger.debug("Verse not found: %s", v)
                message = "Could not find: %s %d:%d" % v
                return render_template("error.html", message=message)
            verses.append({"no": v[2], "text": content})

    p = {"reference": text, "verses": verses}
    return render_template("passage.html", p=p, style=style)
