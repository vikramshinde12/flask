# flask
The Repo of flask sample code that includes Flask, Flask-Restful, Flask-JWT, Sqllite3, SQLAlchemy.

This is executing on `MySQL` Docker container


 docker run -v $PWD/database:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=password  -p 3306:3306 mysql

change the config variable SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.17.0.1:3306/api'
