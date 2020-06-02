import pandas as pd 
from sqlalchemy import create_engine
engine = create_engine(r"postgresql://postgres:1@localhost:5432/project1")

df = pd.read_sql("SELECT * FROM "Blogs" ",engine,index_col=0)
print(df)