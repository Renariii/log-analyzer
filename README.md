# LogAnalyzer

LogAnalyzer on eraldiseisev Python projekt, mille eesmärk on analüüsida serverilogisid ning koondada kindlad sündmused Exceli faili eraldi töölehtedele.

Projekt on loodud õppetöö eesmärgil ning vastab etteantud nõuetele:
- eraldi projekt (mitte SimServerLog lisa)
- konsooli väljund, DocStringid ja kommentaarid eesti keeles
- Pythoni kood inglise keeles
- tulemuseks Exceli fail mitme töölehega

---

## Projekti struktuur

LogAnalyzer/
├── logs/
│ └── application.log
├── log_analyzer.py
├── analysis_results.xlsx
├── requirements.txt
└── README.md

---

## Nõuded

- Python 3.10+
- pip
- Virtuaalkeskkond (soovituslik)

Vajalikud teegid on kirjas failis `requirements.txt`.

---

## Paigaldamine

1. Klooni projekt GitHubist või ava PyCharmis
2. Loo ja aktiveeri virtuaalkeskkond
3. Paigalda vajalikud teegid:

```bash
pip install -r requirements.txt

## GitHub Repo
https://github.com/Renariii/log-analyzer
