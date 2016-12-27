


"""
You can append to a csv by opening the file in append mode:

with open('my_csv.csv', 'a') as f:
    df.to_csv(f, header=False)
If this was your csv, foo.csv:

,A,B,C
0,1,2,3
1,4,5,6
If you read that and then append, for example, df + 6:

In [1]: df = pd.read_csv('foo.csv', index_col=0)

In [2]: df
Out[2]:
   A  B  C
0  1  2  3
1  4  5  6

In [3]: df + 6
Out[3]:
    A   B   C
0   7   8   9
1  10  11  12

In [4]: with open('foo.csv', 'a') as f:
             (df + 6).to_csv(f, header=False)
foo.csv becomes:

,A,B,C
0,1,2,3
1,4,5,6
0,7,8,9
1,10,11,12

"""