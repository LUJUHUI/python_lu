from lda import df

classes = df['class'].values.tolist()
classrooms = df['classroom'].values.tolist()
nodes = list(set(classes + classrooms))
weights = [(df.loc[index, 'classes'], df.loc[index, 'classroom']) for index in df.index]
weights = list(set(weights))
