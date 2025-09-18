import sys, requests, json

if len(sys.argv) < 2:
    print("Usage: python scripts/ingest_folder.py <path> [host]")
    sys.exit(1)

path = sys.argv[1]
host = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"

r = requests.post(f"{host}/ingest", json={"path": path}, timeout=60)
print(r.status_code, r.text)
