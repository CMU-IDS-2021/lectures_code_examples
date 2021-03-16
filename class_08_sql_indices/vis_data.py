import streamlit as st
import duckdb
import altair as alt

__authors__ = "Hendrik Strobelt, Dominik Moritz"

st.set_page_config(layout="wide")

# @st.cache
def create_db():
    con = duckdb.connect(database=":memory:", read_only=False)
    con.execute("CREATE TABLE papers AS SELECT * FROM read_csv_auto('vis_papers_2020.csv');")
    return con


con = create_db()


def query(query):
    st.write(f"```sql\n{query.strip()}\n```")

    con.execute(query)

    df = con.fetchdf()
    st.write(df)
    st.write(f"Number of Rows: {len(df)}")
    st.write("---")
    return df


query("select * from papers")

firstC = query("""
select count(*) count,left(title,1) firstC from papers 
group by firstC
order by count(*) desc 
""") 

chart = alt.Chart(firstC).mark_bar(
    tooltip=True
).encode(
    x=alt.X('firstc', sort='-y'),
    y='count'
)
st.write(chart)

with st.beta_expander('schema'):
    query("""
    describe papers 
    """)


con.execute("explain select * from papers")
