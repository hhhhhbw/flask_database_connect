from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper


# 创建 Flask 应用实例
app = Flask(__name__)
# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/supplementary_tables'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 定义 S1Description 数据表模型
class S1Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Biovar = db.Column(db.String(255), nullable=True)
    Time = db.Column(db.String(255), nullable=True)
    Province = db.Column(db.String(255), nullable=True)
    Region = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Continent = db.Column(db.String(255), nullable=True)
    Source = db.Column(db.String(255), nullable=True)
    total_sample_size = db.Column(db.Integer, nullable=True)
    positive_sample_size = db.Column(db.Integer, nullable=True)
    positive_rate = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<S1Description {self.id}>'

# 将 ORM 对象转换为字典
def object_as_dict(obj):
    return {column.key: getattr(obj, column.key)
            for column in class_mapper(obj.__class__).columns}

# 定义查询接口，通过 biovar 类型进行查询
@app.route('/query', methods=['GET'])
def query_data_by_biovar():
    biovar = request.args.get('biovar')
    data = S1Description.query.filter(S1Description.Biovar == biovar).all()
    result = [object_as_dict(row) for row in data]
    # 只返回需要的字段
    return jsonify([{'total_sample_size': row['total_sample_size'],
                     'positive_sample_size': row['positive_sample_size'],
                     'positive_rate': row['positive_rate']} for row in result])

# 主程序入口
if __name__ == '__main__':
    # 使用应用上下文，确保正确执行查询
    with app.app_context():
        # 启动 Flask 服务器
        app.run(debug=True)