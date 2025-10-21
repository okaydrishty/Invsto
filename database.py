import pandas as pd
from prisma import Prisma
from datetime import datetime


def main():
    
    df = pd.read_csv("data.csv")
     
    print("1")

    if 'instrument' in df.columns:
        df = df.drop(columns=['instrument'])
    print("2")

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    df = df.dropna(subset=['datetime'])
    print("3")

    db=Prisma()
    db.connect()
    print("4")
   
    
    data={}
    for _, row in df.iterrows():
        db.post.create(
            data= {
                'datetime': row['datetime'].to_pydatetime(),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume']),
            }
            
        )
        print(row)

    db.disconnect()
    print(" Data successfully imported into Prisma Post model!")
    

if __name__ == "__main__":
    main()