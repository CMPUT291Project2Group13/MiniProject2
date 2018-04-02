import connectDB

def write_to_output(Decomp):
	# -inserts the normalized schemas into the OutputRelationSchemas table
	##delete this before submitting!!!##########
	connectDB.c.execute('''DELETE FROM OutputRelationSchemas''')
	############################################
	
	for schema in Decomp:
		schema_name,attributes,FD = format_schema(schema)
		connectDB.c.execute('''INSERT INTO OutputRelationSchemas VALUES(?,?,?)''',(schema_name,attributes,FD))
	connectDB.conn.commit()
	return
	
	
def format_schema(schema):
	# -returns the schema name, attribute list and FDs in the same format as they appear in the InputRelationSchema table
	schema_name = schema[0]
	attributes = ','.join(schema[1])
	LHS_attr = '{' + ','.join(schema[2][0][0]) + '}'
	RHS_attr = '{' + ','.join(schema[2][1]) + '}'
	FD = LHS_attr + '=>' + RHS_attr
	return schema_name,attributes,FD	
