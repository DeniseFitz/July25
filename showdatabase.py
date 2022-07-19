from demo import db, User
# from demo import engine


# query_result = engine.execute("SELECT * FROM table;").fetchall()
# print(pd.DataFrame(query_result))

print(User.query.all())