import sys, pathlib, datetime, zoneinfo, yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data" / "profile.yaml"
TPL_DIR = ROOT / "templates"
OUT_DIR = ROOT / "dist"
OUT_DIR.mkdir(exist_ok=True)

def calc_age(birthdate_str: str, tz: str = "Asia/Tokyo") -> int:
    tzinfo = zoneinfo.ZoneInfo(tz)
    today = datetime.datetime.now(tzinfo).date()
    y, m, d = map(int, birthdate_str.split("-"))
    bd = datetime.date(y, m, d)
    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    return age

def today_str(tz: str = "Asia/Tokyo") -> str:
    tzinfo = zoneinfo.ZoneInfo(tz)
    return datetime.datetime.now(tzinfo).strftime("%Y-%m-%d")

def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))

    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(["html", "xml"])
    )
    # カスタムフィルタ/関数
    env.globals["age"] = calc_age
    env.globals["today"] = today_str

    tpl = env.get_template("resume.html.j2")
    html_str = tpl.render(**data)

    # HTML保存（デバッグ用）
    (OUT_DIR / "resume.html").write_text(html_str, encoding="utf-8")

    # PDF生成
    HTML(string=html_str, base_url=str(TPL_DIR)).write_pdf(str(OUT_DIR / "resume.pdf"))
    print("Generated: dist/resume.pdf")

if __name__ == "__main__":
    sys.exit(main())
