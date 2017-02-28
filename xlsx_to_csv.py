import pandas as pd
#file_name = 'feedback_cs2012_6'
#file_name = 'feedback_cs2062_2'
file_name = 'feedback_cs2202_19'
data_xls = pd.read_excel('feedback/'+file_name+'.xlsx', 0, skiprows=5, parse_cols='C')
data_xls.to_csv('feedback_csv/'+file_name+'.csv', encoding='utf-8', index=True)

raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
df.to_csv('../data/example.csv')
df = pd.read_csv('../data/example.csv')

