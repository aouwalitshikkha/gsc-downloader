# GSC Downloader

CLI tools to download Google Search Console data to CSV.

Built on top of [google-searchconsole](https://github.com/joshcarty/google-searchconsole) by Josh Carty.

## Requirements

- Python 3.8+
- Google Search Console API access
- `client_secrets.json` from Google Cloud Console

## Setup

```bash
# Install the library
pip install git+https://github.com/joshcarty/google-searchconsole

# Place your files in the same folder
client_secrets.json      # From Google Cloud Console (OAuth client ID)
credentials.json         # Auto-generated after first auth
```

### Getting credentials

1. Go to [Google Cloud Console](https://console.developers.google.com)
2. Create a project, enable **Google Search Console API**
3. Create OAuth 2.0 Client ID (type: Desktop app)
4. Download JSON → save as `client_secrets.json`
5. Place it in the script folder

## Scripts

The scripts are available in the **root folder** and also mirrored in `.opencode/skills/ctr-optimization/resource/` for use with the CTR optimization skill.

### 1. `download_gsc_data.py` — Download all queries & pages for a site

```bash
# List available sites
python download_gsc_data.py --list

# Download by index
python download_gsc_data.py 1 -d 30 -o data.csv

# Download by URL
python download_gsc_data.py "https://example.com/" -d 90
```

**Output columns:** `kw`, `page`, `impressions`, `clicks`, `ctr`, `avg_position`, `site`

### 2. `page_keywords.py` — Download keywords for a specific page

```bash
# List available sites
python page_keywords.py --list

# Contains match (default, more forgiving)
python page_keywords.py 1 "schema-markup-generator" -o kw.csv

# Exact match
python page_keywords.py "https://example.com/" "https://example.com/page/" --exact -o kw.csv
```

**Output columns:** `kw`, `impressions`, `clicks`, `ctr`, `avg_position`, `page`

## Common options

| Flag | Description |
|------|-------------|
| `-d`, `--days` | Days of data to fetch (default: 30) |
| `-o`, `--output` | Output CSV file path |
| `-l`, `--list` | List available sites |
| `--exact` | Use exact page match (page_keywords only) |
| `--client-secrets` | Path to client_secrets.json |
| `--credentials` | Path to credentials.json |

## .gitignore

The repo ignores `*.json`, `*.csv`, `*.xlsx`, `*.html` to keep secrets and data files out of version control.

## CTR Optimization Skill

The `.opencode/skills/ctr-optimization/` folder contains a reusable skill for optimizing meta titles using GSC data. It includes the same scripts (`download_gsc_data.py`, `page_keywords.py`) and a `SKILLS.md` workflow guide for generating data-driven title tag recommendations.
