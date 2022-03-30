
l = []
def store(object_dict, table_name):
    conn = "create db connection"
    # crs = conn.cursor()
    fields_list = object_dict.keys()
    values_list = object_dict.values()
    query = "insert into {table_name} ({field_list}) values ({values_list});".format(table_name=table_name,
                                                                                            fields_list=(',').join(
                                                                                                fields_list),
                                                                                            values_list=values_list.join(
                                                                                                ','))
    # crs.execute(query)
    # crs.commit()
    return query