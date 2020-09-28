from flask import request, render_template
from attu import app
from attu.models import Reader, parse_reference


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<refe>')
def passage(refe):
    return styled_passage(refe, 'wood')


@app.route('/<style>/<refe>')
def styled_passage(refe, style):
    text = request.args.get('reference', refe)

    try:
        reference = parse_reference(text)
    except Exception:
        return render_template('error.html', message='Could not read your '
                                                     'scripture reference.')

    with Reader() as r:
        verses = []
        for v in reference:
            content = r.read_verse(v[0], v[1], v[2])
            if content is None:
                app.logger.debug('Verse not found: %s', v)
                message = ('Could not find: %s %d:%d' % v)
                return render_template('error.html', message=message)
            verses.append({'no': v[2], 'text': content})

    p = {'reference': text, 'verses': verses}
    return render_template('passage.html', p=p, style=style)
