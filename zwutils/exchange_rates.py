import pdfplumber
import requests
import pandas as pd

# 1. Download the PDF
url = "https://www.rbz.co.zw/documents/Exchange_Rates/2025/December/RATES_12_DECEMBER_2025.pdf"
response = requests.get(url)
pdf_path = "rates.pdf"
with open(pdf_path, "wb") as f:
    f.write(response.content)

# 2. Extract text and parse
data = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            # Skip headers/footers, find lines with actual rates
            # Usually rates lines have currency code + buy + sell
            parts = line.split()
            if len(parts) >= 3 and parts[0].isalpha():
                data.append(parts)

# 3. Convert to DataFrame
df = pd.DataFrame(data, columns=["Currency", "Buy", "Sell"])
print(df)

# 4. Optional: save to CSV
df.to_csv("rbz_exchange_rates.csv", index=False)
