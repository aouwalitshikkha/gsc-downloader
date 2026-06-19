import searchconsole
import csv
import os
import sys
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_path(p):
    return os.path.join(SCRIPT_DIR, p) if not os.path.isabs(p) else p


def get_account(client_secrets, credentials):
    if not os.path.exists(client_secrets):
        print(f"Error: {client_secrets} not found", file=sys.stderr)
        sys.exit(1)
    creds = credentials if os.path.exists(credentials) else None
    return searchconsole.authenticate(client_config=client_secrets, credentials=creds)


def list_sites(account):
    props = account.webproperties
    if not props:
        print("No web properties found.")
        return
    for i, wp in enumerate(props, 1):
        print(f"{i}. {wp.url}")


def select_webproperty(account, site_arg):
    props = account.webproperties
    if not props:
        print("Error: No web properties in account", file=sys.stderr)
        sys.exit(1)
    try:
        idx = int(site_arg) - 1
        if 0 <= idx < len(props):
            return props[idx]
        print(f"Error: Invalid number. Choose 1-{len(props)}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        wp = account[site_arg]
        if not wp:
            print(f"Error: Site '{site_arg}' not found in account", file=sys.stderr)
            sys.exit(1)
        return wp


def build_filename(site_name):
    safe = site_name.rstrip("/").replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "_")
    if not safe:
        safe = "site"
    return f"{safe}_gsc_{datetime.now().strftime('%Y%m%d')}.csv"


def main():
    parser = argparse.ArgumentParser(description="Download Google Search Console data to CSV")
    parser.add_argument("site", nargs="?", help="Site URL or number from --list")
    parser.add_argument("-d", "--days", type=int, default=30, help="Days of data to fetch (default: 30)")
    parser.add_argument("-o", "--output", help="Output CSV path (default: auto-generated)")
    parser.add_argument("-l", "--list", action="store_true", help="List available sites and exit")
    parser.add_argument("--client-secrets", default=resolve_path("client_secrets.json"), help="Path to client_secrets.json")
    parser.add_argument("--credentials", default=resolve_path("credentials.json"), help="Path to credentials.json")
    args = parser.parse_args()

    account = get_account(args.client_secrets, args.credentials)

    if args.list:
        list_sites(account)
        return

    if not args.site:
        print("Error: site argument required (use --list to see available sites)", file=sys.stderr)
        sys.exit(1)

    wp = select_webproperty(account, args.site)

    print(f"Fetching last {args.days} days for {wp.url} ...", file=sys.stderr)

    report = wp.query.range("today", days=-args.days).dimension("query", "page").get()
    rows = report.rows

    if not rows:
        print("No data returned", file=sys.stderr)
        sys.exit(0)

    output = args.output or resolve_path(build_filename(wp.url))

    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["kw", "page", "impressions", "clicks", "ctr", "avg_position", "site"])
        for row in rows:
            writer.writerow([row.query, row.page, row.impressions, row.clicks, row.ctr, row.position, wp.url])

    print(f"{len(rows)} rows -> {output}")


if __name__ == "__main__":
    main()
