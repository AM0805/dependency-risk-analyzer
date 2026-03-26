import csv
import math
import time
from cve_fetcher import get_cve_data
from github_analyzer import get_github_data

PACKAGES = [
    # Popular
    "numpy", "pandas", "requests", "flask", "django", "fastapi", "scipy",
    "matplotlib", "scikit-learn", "tensorflow", "torch", "keras", "sqlalchemy",
    "celery", "redis", "pillow", "boto3", "paramiko", "cryptography", "pyjwt",
    "aiohttp", "httpx", "uvicorn", "gunicorn", "pydantic", "click", "rich",
    "pytest", "black", "mypy", "flake8", "isort", "poetry", "setuptools",
    "wheel", "pip", "virtualenv", "tox", "coverage", "hypothesis",
    "alembic", "psycopg2", "pymongo", "motor", "elasticsearch", "kafka-python",
    "grpcio", "protobuf", "thrift", "zeromq", "pika", "kombu",
    "arrow", "pendulum", "dateutil", "pytz", "humanize",
    "lxml", "beautifulsoup4", "scrapy", "selenium", "playwright",
    "openai", "anthropic", "langchain", "transformers", "tokenizers",
    "networkx", "sympy", "statsmodels", "xgboost", "lightgbm", "catboost",
    "opencv-python", "imageio", "albumentations",
    "pyyaml", "toml", "dotenv", "python-dotenv", "configparser",
    "loguru", "structlog", "sentry-sdk",
    "stripe", "twilio", "sendgrid",
    # Obscure / less maintained
    "easydict", "bunch", "attrdict", "addict", "munch",
    "pexpect", "ptyprocess", "sh", "plumbum",
    "tabulate", "texttable", "terminaltables",
    "colorama", "termcolor", "blessed",
    "tqdm", "alive-progress", "progressbar2",
    "retry", "tenacity", "backoff",
    "cachetools", "diskcache", "dogpile.cache",
    "wrapt", "decorator", "boltons",
    "more-itertools", "toolz", "cytoolz", "funcy",
    "sortedcontainers", "blist", "pyrsistent",
    "construct", "bitstruct", "bitarray",
    "pyserial", "hidapi", "usb",
    "geocoder", "geopy", "shapely",
    "qrcode", "barcode", "zxing",
    "pycparser", "ply", "lark",
    "dill", "cloudpickle", "joblib",
    "natsort", "fuzzywuzzy", "thefuzz", "rapidfuzz",
    "unidecode", "chardet", "charset-normalizer",
    "xmltodict", "dicttoxml", "flatten-dict",
    "schedule", "apscheduler", "rq",
    "pyperclip", "pyautogui", "keyboard", "mouse",
    "psutil", "py-cpuinfo", "gputil",
    "pywin32", "wmi", "winreg",
    "fabric", "invoke", "doit",
    "mkdocs", "sphinx", "pdoc",
]


def compute_risk_score(cve_count, avg_cvss, stars, last_updated_days):
    log_stars = math.log10(stars) if stars > 0 else 0
    # Higher weights on CVE counts and severity
    score = (cve_count * 2) + (avg_cvss * 5) + (last_updated_days / 50) - (log_stars * 2)
    return round(max(0, min(100, score)), 4)


def main():
    output_file = "training_data.csv"
    fieldnames = ["package", "cve_count", "avg_cvss", "stars", "open_issues", "last_updated_days", "risk_score"]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, package in enumerate(PACKAGES):
            print(f"[{i+1}/{len(PACKAGES)}] Fetching: {package}")
            try:
                cve_info = get_cve_data(package)
                github_info = get_github_data(package)

                # Skip if the data is junk/not found
                if github_info["stars"] == 0 and github_info["last_updated_days"] == 999:
                    continue

                risk_score = compute_risk_score(
                    cve_info["cve_count"], cve_info["avg_cvss"],
                    github_info["stars"], github_info["last_updated_days"]
                )

                writer.writerow({
                    "package": package,
                    "cve_count": cve_info["cve_count"],
                    "avg_cvss": cve_info["avg_cvss"],
                    "stars": github_info["stars"],
                    "open_issues": github_info["open_issues"],
                    "last_updated_days": github_info["last_updated_days"],
                    "risk_score": risk_score,
                })
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

    print(f"\nDataset saved to {output_file}")


if __name__ == "__main__":
    main()
