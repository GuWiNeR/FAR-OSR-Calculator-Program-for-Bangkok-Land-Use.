# FAR/OSR-Calculator-Program-for-Bangkok-Land-Use.
This program is designed to calculate the Floor Area Ratio (FAR) and Open Space Ratio (OSR) for land use projects in Bangkok. It allows users to input project details, calculate FAR and OSR based on zoning regulations, and compare different projects.


---

## Features

- **project management** : create, edit, delete your projects
- **FAR/OSR calculation** : Automatic calculation based on Bangkok's landued regulation
- **FAR bonus** : estimate 20% bonus for extra Floor Area Ratio due to the  qualifying criteria
- **PDF export** : one-page summary report with Thai language
- **Project comparison** : compare FAR/OSR across multiple sites


---

## Tech Stack

- Python 3.12
- Streamlit
- pandas / matplotlib
- fpdf2 (Thai font support via THSarabun)

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Data Source

FAR/OSR values based on กฎกระทรวงให้ใช้บังคับผังเมืองรวมกรุงเทพมหานคร พ.ศ. 2556 .

This program is developed for educational purposes and is not intended for commercial use. The calculations are based on the regulations provided by the Bangkok Metropolitan Administration and may not reflect the most current zoning laws. Users should verify the results with official sources before making any decisions based on the calculations.

---




