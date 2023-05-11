from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
from sqlalchemy import func

# 创建 Flask 应用实例
app = Flask(__name__)
# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/supplementary_tables'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

provinces = {
    "Anhui": "安徽",
    "Fujian": "福建",
    "Gansu": "甘肃",
    "Guangdong": "广东",
    "Guizhou": "贵州",
    "Hainan": "海南",
    "Hebei": "河北",
    "Heilongjiang": "黑龙江",
    "Henan": "河南",
    "Hennan": "河南",
    "Hubei": "湖北",
    "Hunan": "湖南",
    "Jiangsu": "江苏",
    "Jiangxi": "江西",
    "Jilin": "吉林",
    "Liaoning": "辽宁",
    "Qinghai": "青海",
    "Shaanxi": "陕西",
    "Shanxi": "山西",
    "Shandong": "山东",
    "Sichuan": "四川",
    "Yunnan": "云南",
    "Zhejiang": "浙江",
    "Guangxi": "广西",
    "Inner Mongolia": "内蒙古",
    "Ningxia": "宁夏",
    "Xinjiang": "新疆",
    "Tibet": "西藏",
    "Beijing": "北京",
    "Tianjin": "天津",
    "Shanghai": "上海",
    "Chongqing": "重庆",
    "Hong Kong": "香港",
    "Macau": "澳门",
    "Taiwan": "台湾",
}
# 将英文名称转换为中文名称
def translate_province_name(input_string):
    # 分割输入字符串
    province_names = input_string.split(", ")
    # 将英文名称转换为中文名称
    chinese_names = [provinces[name] for name in province_names]
    # 将结果合并为一个字符串
    result = ",".join(chinese_names)
    return result

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

@app.route('/Total_sample_size', methods=['GET'])
def get_Total_sample_size_data():
    data = (
        db.session.query(
            func.trim(S1Description.Country).label('country'),
            S1Description.total_sample_size.label('Total_sample_size')
        )
        .filter(S1Description.Country != "")
        .filter(S1Description.total_sample_size != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Total_sample_size
        } for row in data
    ]

    return jsonify(data=result)
@app.route('/Positive_sample_size', methods=['GET'])
def get_Positive_sample_size_data():
    data = (
        db.session.query(
            func.trim(S1Description.Country).label('country'),
            S1Description.positive_sample_size.label('Positive_sample_size')
        )
        .filter(S1Description.Country != "")
        .filter(S1Description.positive_sample_size != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Positive_sample_size
        } for row in data
    ]
    return jsonify(data=result)
@app.route('/Positive_rate', methods=['GET'])
def get_Positive_rate_data():
    data = (
        db.session.query(
            func.trim(S1Description.Country).label('country'),
            # 保留两位小数，四舍五入
            func.round(S1Description.positive_rate, 2).label('Positive_rate')
        )
        .filter(S1Description.Country != "")
        .filter(S1Description.positive_rate != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Positive_rate
        } for row in data
    ]
    return jsonify(data=result)


@app.route('/description', methods=['GET'])
def get_description_data():
    data = (
        db.session.query(
            func.trim(S1Description.Country).label('country'),
            func.sum(S1Description.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S1Description.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S1Description.positive_sample_size) / func.sum(S1Description.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S1Description.Country != "")
        .filter(S1Description.total_sample_size != None)
        .filter(S1Description.positive_sample_size != None)
        .group_by(func.trim(S1Description.Country))
        .order_by(func.trim(S1Description.Country))
        .all()
    )
    result = [
        {
            'name': row.country,
            'Total_sample_size': row.Total_sample_size_sum,
            'Positive_sample_size': row.Positive_sample_size_sum,
            'Positive_rate': row.positive_rate
        } for row in data
    ]
    return jsonify(data=result)
@app.route('/description_province', methods=['GET'])
def get_description_province_data():
    data = (
        db.session.query(
            func.trim(S1Description.Province).label('province'),
            func.sum(S1Description.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S1Description.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S1Description.positive_sample_size) / func.sum(S1Description.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S1Description.Country == 'China')
        .filter(S1Description.Province != 'NA')
        .group_by(func.trim(S1Description.Province))
        .order_by(func.trim(S1Description.Province))
        .all()
    )
    result = [
        {
            'name': translate_province_name(row.province),
            'Total_sample_size': row.Total_sample_size_sum,
            'Positive_sample_size': row.Positive_sample_size_sum,
            'Positive_rate': row.positive_rate
        } for row in data
    ]
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

@app.route('/biovar_country_stats', methods=['GET'])
def get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S1Description.Country,
            func.sum(S1Description.total_sample_size).label("total_sample_size"),
            func.sum(S1Description.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S1Description.Biovar == biovar)
        .group_by(S1Description.Country)
        .all()
    )
    result = [
        {
            "name": row.Country,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)
from flask import json

@app.route('/biovar_province_stats', methods=['GET'])
def get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S1Description.Province,
            func.sum(S1Description.total_sample_size).label("total_sample_size"),
            func.sum(S1Description.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S1Description.Biovar == biovar)
        .filter(S1Description.Country == 'China')
        .filter(S1Description.Province != 'NA')
        .group_by(S1Description.Province)
        .all()
    )
    result = [
        {
            "name": translate_province_name(row.Province),
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


# 主程序入口
if __name__ == '__main__':
    # 使用应用上下文，确保正确执行查询
    with app.app_context():
        # 启动 Flask 服务器
        app.run(debug=True)
