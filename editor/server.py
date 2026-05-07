#!/usr/bin/env python3
"""
Blog editor server — no external dependencies.
Usage: python3 server.py
"""
import http.server
import json
import os
import re
import subprocess
import threading
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

REPO_ROOT  = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / 'source'
TOC_FILE   = SOURCE_DIR / '_toc.yml'
BUILD_SH   = REPO_ROOT / 'build.sh'
PORT       = 3131

# ── Build state (shared across handler threads) ───────────────────────────────
BUILD_STATE = {
    'running':     False,
    'output':      '',
    'exit_code':   None,
    'started_at':  None,
    'finished_at': None,
}
BUILD_LOCK = threading.Lock()


def find_conda_sh():
    """Locate conda.sh from common install paths, or via `conda info --base`."""
    home = Path.home()
    candidates = [
        home / 'miniconda3'  / 'etc/profile.d/conda.sh',
        home / 'anaconda3'   / 'etc/profile.d/conda.sh',
        home / 'miniforge3'  / 'etc/profile.d/conda.sh',
        home / 'mambaforge'  / 'etc/profile.d/conda.sh',
        Path('/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh'),
        Path('/opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh'),
        Path('/opt/miniconda3/etc/profile.d/conda.sh'),
        Path('/opt/anaconda3/etc/profile.d/conda.sh'),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    try:
        r = subprocess.run(['conda', 'info', '--base'],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            p = Path(r.stdout.strip()) / 'etc/profile.d/conda.sh'
            if p.exists():
                return str(p)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def run_build_async():
    """Run build.sh in a background thread; stream output into BUILD_STATE."""
    try:
        conda_sh = find_conda_sh()
        if conda_sh:
            # `source build.sh` (not `bash build.sh`) so the script runs in the
            # SAME shell that has conda's hook — `conda activate` is a shell
            # function, not an executable, and won't survive a fresh subshell.
            cmd = f'source "{conda_sh}" && source "{BUILD_SH}"'
        else:
            with BUILD_LOCK:
                BUILD_STATE['output'] += '[editor] Could not locate conda.sh — falling back to interactive zsh.\n'
            cmd = f'source "{BUILD_SH}"'

        proc = subprocess.Popen(
            ['/bin/bash', '-c', cmd],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        for line in iter(proc.stdout.readline, ''):
            with BUILD_LOCK:
                BUILD_STATE['output'] += line
        proc.wait()
        rc = proc.returncode
    except Exception as e:
        with BUILD_LOCK:
            BUILD_STATE['output'] += f'\n[editor] {type(e).__name__}: {e}\n'
        rc = 1
    with BUILD_LOCK:
        BUILD_STATE['exit_code']   = rc
        BUILD_STATE['running']     = False
        BUILD_STATE['finished_at'] = time.time()


# ── TOC helpers ───────────────────────────────────────────────────────────────

def read_toc():
    """Return ordered list of slugs from _toc.yml."""
    content = TOC_FILE.read_text()
    return re.findall(r'- file:\s*(\S+)', content)


def write_toc(slugs):
    lines = ['format: jb-book\n', 'root: index\n', 'chapters:\n']
    for s in slugs:
        lines.append(f'  - file: {s}\n')
    TOC_FILE.write_text(''.join(lines))


# ── Path validation ───────────────────────────────────────────────────────────

def valid_slug(s):
    return isinstance(s, str) and bool(re.match(r'^[a-z0-9][a-z0-9-]*$', s))


def safe_post_path(slug):
    """Return resolved Path only if slug is safe and within SOURCE_DIR."""
    if not valid_slug(slug):
        return None
    p = (SOURCE_DIR / (slug + '.md')).resolve()
    if not str(p).startswith(str(SOURCE_DIR) + os.sep):
        return None
    return p


# ── Misc helpers ──────────────────────────────────────────────────────────────

def extract_title(content):
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return m.group(1) if m else None


def format_date(dt):
    suffixes = {1:'st',2:'nd',3:'rd'}
    suffix = suffixes.get(dt.day if dt.day not in (11,12,13) else 0, 'th')
    return dt.strftime(f'%B %-d{suffix}, %Y')


# ── HTTP handler ──────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / 'public'), **kwargs)

    def log_message(self, fmt, *args):
        pass  # quiet

    # ── Response helpers ──────────────────────────────────────────────────────

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n)) if n else {}

    # ── Routing ───────────────────────────────────────────────────────────────

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == '/api/posts':
            self._list_posts()
        elif path.startswith('/api/posts/'):
            self._get_post(urllib.parse.unquote(path[len('/api/posts/'):]))
        elif path == '/api/git/status':
            self._git_status()
        elif path == '/api/build':
            self._build_status()
        elif path.startswith('/_static/'):
            self._serve_static(path[len('/_static/'):])
        else:
            super().do_GET()

    def _serve_static(self, rel):
        base = (SOURCE_DIR / '_static').resolve()
        target = (base / rel).resolve()
        if not str(target).startswith(str(base) + os.sep):
            return self.send_error(403)
        if not target.exists() or not target.is_file():
            return self.send_error(404)
        ctype = {
            '.css': 'text/css', '.js': 'application/javascript',
            '.woff': 'font/woff', '.woff2': 'font/woff2',
            '.ttf': 'font/ttf', '.eot': 'application/vnd.ms-fontobject',
            '.svg': 'image/svg+xml', '.png': 'image/png',
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        }.get(target.suffix.lower(), 'application/octet-stream')
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(target.stat().st_size))
        self.end_headers()
        with open(target, 'rb') as f:
            self.wfile.write(f.read())

    def do_PUT(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith('/api/posts/'):
            self._save_post(urllib.parse.unquote(path[len('/api/posts/'):]))
        else:
            self.send_json({'error': 'Not found'}, 404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/api/posts':
            self._create_post()
        elif path == '/api/commit':
            self._commit()
        elif path == '/api/build':
            self._build_start()
        else:
            self.send_json({'error': 'Not found'}, 404)

    def do_DELETE(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith('/api/posts/'):
            self._delete_post(urllib.parse.unquote(path[len('/api/posts/'):]))
        else:
            self.send_json({'error': 'Not found'}, 404)

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _list_posts(self):
        posts = []
        for slug in read_toc():
            pp = safe_post_path(slug)
            title = slug
            if pp and pp.exists():
                t = extract_title(pp.read_text())
                if t:
                    title = t
            posts.append({'slug': slug, 'title': title})
        self.send_json(posts)

    def _get_post(self, slug):
        pp = safe_post_path(slug)
        if not pp:
            return self.send_json({'error': 'Invalid slug'}, 400)
        if not pp.exists():
            return self.send_json({'error': 'Not found'}, 404)
        self.send_json({'content': pp.read_text()})

    def _save_post(self, slug):
        pp = safe_post_path(slug)
        if not pp:
            return self.send_json({'error': 'Invalid slug'}, 400)
        data = self.read_body()
        content = data.get('content', '')
        if not isinstance(content, str):
            return self.send_json({'error': 'Invalid content'}, 400)
        pp.write_text(content)
        self.send_json({'ok': True})

    def _create_post(self):
        data = self.read_body()
        slug  = data.get('slug', '')
        title = data.get('title', '').strip()
        pp = safe_post_path(slug)
        if not pp:
            return self.send_json(
                {'error': 'Invalid slug (lowercase letters, numbers, hyphens only)'}, 400)
        if not title:
            return self.send_json({'error': 'Title required'}, 400)
        if pp.exists():
            return self.send_json({'error': 'A post with that slug already exists'}, 400)

        date_str  = format_date(datetime.now())
        escaped   = title.replace('"', '\\"')
        content   = f'---\ntitle: "{escaped}"\n---\n\n# {title}\n\n*{date_str}*\n\n'
        pp.write_text(content)

        slugs = [slug] + [s for s in read_toc() if s != slug]
        write_toc(slugs)

        self.send_json({'ok': True, 'slug': slug, 'title': title})

    def _delete_post(self, slug):
        pp = safe_post_path(slug)
        if not pp:
            return self.send_json({'error': 'Invalid slug'}, 400)
        if pp.exists():
            pp.unlink()
        write_toc([s for s in read_toc() if s != slug])
        self.send_json({'ok': True})

    def _git_status(self):
        r = subprocess.run(
            ['git', 'status', '--porcelain', 'source/'],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.send_json({'dirty': bool(r.stdout.strip()), 'output': r.stdout.strip()})

    def _commit(self):
        data = self.read_body()
        msg  = data.get('message', '').strip()
        if not msg:
            return self.send_json({'error': 'Commit message required'}, 400)

        add = subprocess.run(
            ['git', 'add', 'source/'],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        if add.returncode != 0:
            return self.send_json({'error': add.stderr or 'git add failed'}, 500)

        commit = subprocess.run(
            ['git', 'commit', '-m', msg],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        if commit.returncode != 0:
            return self.send_json({'error': commit.stderr or commit.stdout or 'commit failed'}, 500)

        self.send_json({'ok': True, 'output': commit.stdout.strip()})

    def _build_start(self):
        with BUILD_LOCK:
            if BUILD_STATE['running']:
                return self.send_json({'error': 'Build already running'}, 409)
            BUILD_STATE.update({
                'running':     True,
                'output':      '',
                'exit_code':   None,
                'started_at':  time.time(),
                'finished_at': None,
            })
        threading.Thread(target=run_build_async, daemon=True).start()
        self.send_json({'ok': True})

    def _build_status(self):
        with BUILD_LOCK:
            now = time.time()
            elapsed = (now - BUILD_STATE['started_at']) if BUILD_STATE['started_at'] else 0
            self.send_json({
                'running':   BUILD_STATE['running'],
                'output':    BUILD_STATE['output'][-100_000:],  # cap
                'exit_code': BUILD_STATE['exit_code'],
                'elapsed':   round(elapsed, 1),
            })


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import webbrowser
    url = f'http://localhost:{PORT}'
    server = http.server.ThreadingHTTPServer(('localhost', PORT), Handler)
    print(f'Blog editor → {url}  (Ctrl-C to stop)')
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
