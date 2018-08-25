import pandas, numpy, sqlite3, os
from scipy.stats import sem

db_file = os.path.join('.', 'wafergen_data.db')

assert os.path.isfile(db_file)

conn = sqlite3.connect(db_file)
sql = "select * from dct"
df = pandas.read_sql(sql, conn, index_col='index')

mean = df.groupby(by=['cell_line', 'gene', 'treatment', 'time']).agg(numpy.mean).reset_index()
std = df.groupby(by=['cell_line', 'gene', 'treatment', 'time']).agg(numpy.std).reset_index()
sem = df.groupby(by=['cell_line', 'gene', 'treatment', 'time']).agg(sem).reset_index()

for i in [mean, std, sem]:
    i.drop('replicate', axis=1, inplace=True)

print (mean)
mean.to_sql('mean', conn, if_exists='replace')
std.to_sql('std', conn, if_exists='replace')
sem.to_sql('sem', conn, if_exists='replace')

conn.close()
