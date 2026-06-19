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


def build_filename(page_url):
    safe = page_url.rstrip("/").replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "_")
    if not safe:
        safe = "page"
    return f"{safe}_keywords_{datetime.now().strftime('%Y%m%d')}.csv"


def main():
    parser = argparse.ArgumentParser(description="Download keywords for a specific page from Google Search Console")
    parser.add_argument("site", help="Site URL or number from --list")
    parser.add_argument("page", help="Page URL path or full URL to analyze (e.g. /blog/post or https://site.com/blog/post)")
    parser.add_argument("-d", "--days", type=int, default=30, help="Days of data (default: 30)")
    parser.add_argument("-o", "--output", help="Output CSV path (default: auto-generated)")
    parser.add_argument("-l", "--list", action="store_true", help="List available sites and exit")
    parser.add_argument("--exact", action="store_true", help="Use exact match instead of contains")
    parser.add_argument("--client-secrets", default=resolve_path("client_secrets.json"), help="Path to client_secrets.json")
    parser.add_argument("--credentials", default=resolve_path("credentials.json"), help="Path to credentials.json")
    args = parser.parse_args()

    account = get_account(args.client_secrets, args.credentials)

    if args.list:
        list_sites(account)
        return

    wp = select_webproperty(account, args.site)

    operator = "equals" if args.exact else "contains"
    print(f"Fetching keywords for page: {args.page} (last {args.days} days, filter: {operator})", file=sys.stderr)

    report = (
        wp.query
        .range("today", days=-args.days)
        .dimension("query")
        .filter("page", args.page, operator)
        .get()
    )

    rows = report.rows
    if not rows:
        print("No data returned for this page", file=sys.stderr)
        sys.exit(0)

    output = args.output or resolve_path(build_filename(args.page))

    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["kw", "impressions", "clicks", "ctr", "avg_position", "page"])
        for row in rows:
            writer.writerow([row.query, row.impressions, row.clicks, row.ctr, row.position, args.page])

    print(f"{len(rows)} keywords -> {output}")


if __name__ == "__main__":
    main()
