import pandas as pd
from prisma import Prisma
from datetime import datetime

tables = pd.read_html("data.html")
df = tables[0]
if 'instrument' in df.columns:
    df = df.drop(columns=['instrument'])

