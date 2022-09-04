import pandas as pd

scan_data = pd.DataFrame([["Naam1"], ["Naam2"]],columns=["naam"]);
scan_data.to_csv('c:\\temp\\scans.csv', index=False)