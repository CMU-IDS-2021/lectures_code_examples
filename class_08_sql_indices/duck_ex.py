import streamlit as st
import duckdb

__authors__ = "Dominik Moritz, Hendrik Strobelt"

def create_db():
    con = duckdb.connect(database=":memory:", read_only=False)

    con.execute("create table weather as select * from read_csv_auto('weather.csv');");
    con.execute("create table locations as select * from read_csv_auto('locations.csv');")

    return con

con = create_db()

def query(query):
    st.write(f"```sql\n{query.strip()}\n```")

    con.execute(query)

    df = con.fetchdf()
    st.write(df)
    st.write(f"Number of Rows: {len(df)}")
    st.write("---")


query("""
select t.*, l.*
from weather t, locations l
where t.location=l.location 
and t.location LIKE 'P%'
""")

query("""
select t.*, l.*
from weather t, locations l
where t.location=l.location
""")

query("""
select location from weather
where temp_min = (select min(temp_min) from weather)
""")

query("""
select location, min(temp_min), max(temp_max) 
from weather 
group by location
""")

query("""
select location,count(*) from weather group by location
""")