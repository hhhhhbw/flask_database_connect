from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
from sqlalchemy import func
from flask_cors import CORS

# 创建 Flask 应用实例
app = Flask(__name__)
# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/supplementary_tables'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)
CORS(app,resources=r'/*')

# 定义数据表模型
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
class S2_meta_analysis(db.Model):
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
        return f'<S2_meta_analysis {self.id}>'
class S3_chick_breed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Biovar = db.Column(db.String(255), nullable=True)
    Time = db.Column(db.String(255), nullable=True)
    Province = db.Column(db.String(255), nullable=True)
    Region = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Continent = db.Column(db.String(255), nullable=True)
    Source = db.Column(db.String(255), nullable=True)
    Breed = db.Column(db.String(255), nullable=True)
    total_sample_size = db.Column(db.Integer, nullable=True)
    positive_sample_size = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<S3_chick_breed {self.id}>'
class S4_farm_mode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Biovar = db.Column(db.String(255), nullable=True)
    Time = db.Column(db.String(255), nullable=True)
    Province = db.Column(db.String(255), nullable=True)
    Region = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Continent = db.Column(db.String(255), nullable=True)
    Source = db.Column(db.String(255), nullable=True)
    Raising_mode = db.Column(db.String(255), nullable=True)
    total_sample_size = db.Column(db.Integer, nullable=True)
    positive_sample_size = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<S4_farm_mode {self.id}>'
class S5_chick_economic_usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Biovar = db.Column(db.String(255), nullable=True)
    Time = db.Column(db.String(255), nullable=True)
    Province = db.Column(db.String(255), nullable=True)
    Region = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Continent = db.Column(db.String(255), nullable=True)
    Source = db.Column(db.String(255), nullable=True)
    Economic_use = db.Column(db.String(255), nullable=True)
    Growth_stage = db.Column(db.String(255), nullable=True)
    total_sample_size = db.Column(db.Integer, nullable=True)
    positive_sample_size = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<S5_chick_economic_usage {self.id}>'
class S6_chick_sex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Biovar = db.Column(db.String(255), nullable=True)
    Time = db.Column(db.String(255), nullable=True)
    Province = db.Column(db.String(255), nullable=True)
    Region = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Continent = db.Column(db.String(255), nullable=True)
    Source = db.Column(db.String(255), nullable=True)
    Gender = db.Column(db.String(255), nullable=True)
    total_sample_size = db.Column(db.Integer, nullable=True)
    positive_sample_size = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<s6_chick_sex {self.id}>'
def object_as_dict(obj):
    return {column.key: getattr(obj, column.key)
            for column in class_mapper(obj.__class__).columns}
##S1
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
            'total_sample_size': row.Total_sample_size_sum,
            'positive_sample_size': row.Positive_sample_size_sum,
            'positive_rate': row.positive_rate
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
            'name': row.province,
            'total_sample_size': row.Total_sample_size_sum,
            'positive_sample_size': row.Positive_sample_size_sum,
            'positive_rate': row.positive_rate
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
            "name": row.Province,
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
# @app.route('/zhuzhuangtu', methods=['GET'])
# def get_zhuzhuangtu_data():
#     data = (
#         db.session.query(
#             func.trim(S1Description.Province).label('province'),
#             S1Description.Biovar.label('biovar'),
#             func.sum(S1Description.total_sample_size).label('Total_sample_size_sum'),
#             func.sum(S1Description.positive_sample_size).label('Positive_sample_size_sum'),
#             func.round(func.sum(S1Description.positive_sample_size) / func.sum(S1Description.total_sample_size) * 100, 2).label('positive_rate')
#         )
#         .filter(S1Description.Country == 'China')
#         .filter(S1Description.Province != 'NA')
#         .filter(S1Description.Biovar.in_(['bvSG', 'bvSP']))
#         .group_by(func.trim(S1Description.Province), S1Description.Biovar)
#         .order_by(func.trim(S1Description.Province), S1Description.Biovar)
#         .all()
#     )
#     result = [
#         {
#             'province': row.province,
#             'biovar': row.biovar,
#             'total_sample_size': row.Total_sample_size_sum,
#             'positive_sample_size': row.Positive_sample_size_sum,
#             'positive_rate': row.positive_rate if row.positive_rate else 0
#         } for row in data
#     ]
#
#     province_list = sorted(list(set([item['province'] for item in result])))
#     final_result = {
#         'nameData': [],
#         'bvSGData': [],
#         'bvSPData': [],
#     }
#
#     for province in province_list:
#         bvSGData = 0.0
#         bvSPData = 0.0
#         for item in result:
#             if item['province'] == province:
#                 if item['biovar'] == 'bvSG':
#                     bvSGData = item['positive_rate']
#                 if item['biovar'] == 'bvSP':
#                     bvSPData = item['positive_rate']
#         final_result['nameData'].append(province)
#         final_result['bvSGData'].append(bvSGData if bvSGData else 0.0)
#         final_result['bvSPData'].append(bvSPData if bvSPData else 0.0)
#     return app.response_class(
#         response=json.dumps(final_result, ensure_ascii=False),
#         status=200,
#         mimetype='application/json'
#     )
@app.route('/china_zhuzhuangtu', methods=['GET'])
def get_china_zhuzhuangtu_data():
    data = (
        db.session.query(
            func.trim(S1Description.Province).label('province'),
            S1Description.Biovar.label('biovar'),
            func.sum(S1Description.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S1Description.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S1Description.positive_sample_size) / func.sum(S1Description.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S1Description.Country == 'China')
        .filter(S1Description.Province != 'NA')
        .filter(S1Description.Biovar.in_(['bvSG', 'bvSP']))
        .group_by(func.trim(S1Description.Province), S1Description.Biovar)
        .order_by(func.trim(S1Description.Province), S1Description.Biovar)
        .all()
    )
    result = {}
    for row in data:
        province = row.province
        biovar = row.biovar
        positive_rate = row.positive_rate if row.positive_rate else 0.0
        if province not in result:
            result[province] = {
                'nameData': province,
                'bvSGData': 0.0,
                'bvSPData': 0.0
            }
        if biovar == 'bvSG':
            result[province]['bvSGData'] = positive_rate
        elif biovar == 'bvSP':
            result[province]['bvSPData'] = positive_rate

    response_data = {'data': list(result.values())}
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


##s2
@app.route('/S2_query', methods=['GET'])
def S2_query_data_by_biovar():
    biovar = request.args.get('biovar')
    data = S2_meta_analysis.query.filter(S2_meta_analysis.Biovar == biovar).all()
    result = [object_as_dict(row) for row in data]
    # 只返回需要的字段
    return jsonify([{'total_sample_size': row['total_sample_size'],
                     'positive_sample_size': row['positive_sample_size'],
                     'positive_rate': row['positive_rate']} for row in result])

@app.route('/S2_Total_sample_size', methods=['GET'])
def S2_get_Total_sample_size_data():
    data = (
        db.session.query(
            func.trim(S2_meta_analysis.Country).label('country'),
            S2_meta_analysis.total_sample_size.label('Total_sample_size')
        )
        .filter(S2_meta_analysis.Country != "")
        .filter(S2_meta_analysis.total_sample_size != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Total_sample_size
        } for row in data
    ]
    return jsonify(data=result)

@app.route('/S2_Positive_sample_size', methods=['GET'])
def S2_get_Positive_sample_size_data():
    data = (
        db.session.query(
            func.trim(S2_meta_analysis.Country).label('country'),
            S2_meta_analysis.positive_sample_size.label('Positive_sample_size')
        )
        .filter(S2_meta_analysis.Country != "")
        .filter(S2_meta_analysis.positive_sample_size != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Positive_sample_size
        } for row in data
    ]
    return jsonify(data=result)

@app.route('/S2_Positive_rate', methods=['GET'])
def S2_get_Positive_rate_data():
    data = (
        db.session.query(
            func.trim(S2_meta_analysis.Country).label('country'),
            func.round(S2_meta_analysis.positive_rate, 2).label('Positive_rate')
        )
        .filter(S2_meta_analysis.Country != "")
        .filter(S2_meta_analysis.positive_rate != None)
        .all()
    )
    result = [
        {
            'name': row.country,
            'value': row.Positive_rate
        } for row in data
    ]
    return jsonify(data=result)

@app.route('/S2_description', methods=['GET'])
def S2_get_description_data():
    data = (
        db.session.query(
            func.trim(S2_meta_analysis.Country).label('country'),
            func.sum(S2_meta_analysis.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S2_meta_analysis.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S2_meta_analysis.positive_sample_size) / func.sum(S2_meta_analysis.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S2_meta_analysis.Country != "")
        .filter(S2_meta_analysis.total_sample_size != None)
        .filter(S2_meta_analysis.positive_sample_size != None)
        .group_by(func.trim(S2_meta_analysis.Country))
        .order_by(func.trim(S2_meta_analysis.Country))
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

@app.route('/S2_description_province', methods=['GET'])
def S2_get_description_province_data():
    data = (
        db.session.query(
            func.trim(S2_meta_analysis.Province).label('province'),
            func.sum(S2_meta_analysis.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S2_meta_analysis.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S2_meta_analysis.positive_sample_size) / func.sum(S2_meta_analysis.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S2_meta_analysis.Country == 'China')
        .filter(S2_meta_analysis.Province != 'NA')
        .group_by(func.trim(S2_meta_analysis.Province))
        .order_by(func.trim(S2_meta_analysis.Province))
        .all()
    )
    result = [
        {
            'name': row.province,
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

@app.route('/S2_biovar_country_stats', methods=['GET'])
def S2_get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S2_meta_analysis.Country,
            func.sum(S2_meta_analysis.total_sample_size).label("total_sample_size"),
            func.sum(S2_meta_analysis.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S2_meta_analysis.Biovar == biovar)
        .group_by(S2_meta_analysis.Country)
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

@app.route('/S2_biovar_province_stats', methods=['GET'])
def S2_get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S2_meta_analysis.Province,
            func.sum(S2_meta_analysis.total_sample_size).label("total_sample_size"),
            func.sum(S2_meta_analysis.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S2_meta_analysis.Biovar == biovar)
        .filter(S2_meta_analysis.Country == 'China')
        .filter(S2_meta_analysis.Province != 'NA')
        .group_by(S2_meta_analysis.Province)
        .all()
    )
    result = [
        {
            "name": row.Province,
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
##S3
@app.route('/S3_description', methods=['GET'])
def S3_get_description_data():
    data = (
        db.session.query(
            func.trim(S3_chick_breed.Country).label('country'),
            S3_chick_breed.Breed,
            func.sum(S3_chick_breed.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S3_chick_breed.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S3_chick_breed.positive_sample_size) / func.sum(S3_chick_breed.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S3_chick_breed.Country != "")
        .filter(S3_chick_breed.total_sample_size != None)
        .filter(S3_chick_breed.positive_sample_size != None)
        .group_by(func.trim(S3_chick_breed.Country))
        .order_by(func.trim(S3_chick_breed.Country))
        .all()
    )
    result = [
        {
            'name': row.country,
            'Breed': row.Breed,
            'Total_sample_size': row.Total_sample_size_sum,
            'Positive_sample_size': row.Positive_sample_size_sum,
            'Positive_rate': row.positive_rate
        } for row in data
    ]
    return jsonify(data=result)
@app.route('/S3_description_province', methods=['GET'])
def S3_get_description_province_data():
    data = (
        db.session.query(
            func.trim(S3_chick_breed.Province).label('province'),
            S3_chick_breed.Breed,
            func.sum(S3_chick_breed.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S3_chick_breed.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S3_chick_breed.positive_sample_size) / func.sum(S3_chick_breed.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S3_chick_breed.Country == 'China')
        .filter(S3_chick_breed.Province != 'NA')
        .group_by(func.trim(S3_chick_breed.Province), S3_chick_breed.Breed)
        .order_by(func.trim(S3_chick_breed.Province))
        .all()
    )
    result = [
        {
            'name': row.province,
            'Breed': row.Breed,
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

@app.route('/S3_biovar_country_stats', methods=['GET'])
def S3_get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S3_chick_breed.Country,
            S3_chick_breed.Breed,
            func.sum(S3_chick_breed.total_sample_size).label("total_sample_size"),
            func.sum(S3_chick_breed.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S3_chick_breed.Biovar == biovar)
        .group_by(S3_chick_breed.Country, S3_chick_breed.Breed)
        .all()
    )
    result = [
        {
            "name": row.Country,
            "Breed": row.Breed,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)

@app.route('/S3_biovar_province_stats', methods=['GET'])
def S3_get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S3_chick_breed.Province,
            S3_chick_breed.Breed,
            func.sum(S3_chick_breed.total_sample_size).label("total_sample_size"),
            func.sum(S3_chick_breed.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S3_chick_breed.Biovar == biovar)
        .filter(S3_chick_breed.Country == 'China')
        .filter(S3_chick_breed.Province != 'NA')
        .group_by(S3_chick_breed.Province, S3_chick_breed.Breed)
        .all()
    )
    result = [
        {
            "name": row.Province,
            "Breed": row.Breed,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)
##S4_farm_mode
@app.route('/S4_description', methods=['GET'])
def S4_get_description_data():
    data = (
        db.session.query(
            func.trim(S4_farm_mode.Country).label('country'),
            S4_farm_mode.Raising_mode,
            func.sum(S4_farm_mode.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S4_farm_mode.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S4_farm_mode.positive_sample_size) / func.sum(S4_farm_mode.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S4_farm_mode.Country != "")
        .filter(S4_farm_mode.total_sample_size != None)
        .filter(S4_farm_mode.positive_sample_size != None)
        .group_by(func.trim(S4_farm_mode.Country))
        .order_by(func.trim(S4_farm_mode.Country))
        .all()
    )
    result = [
        {
            'name': row.country,
            'Raising_mode': row.Raising_mode,
            'Total_sample_size': row.Total_sample_size_sum,
            'Positive_sample_size': row.Positive_sample_size_sum,
            'Positive_rate': row.positive_rate
        } for row in data
    ]
    return jsonify(data=result)
@app.route('/S4_description_province', methods=['GET'])
def S4_get_description_province_data():
    data = (
        db.session.query(
            func.trim(S4_farm_mode.Province).label('province'),
            S4_farm_mode.Raising_mode,
            func.sum(S4_farm_mode.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S4_farm_mode.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S4_farm_mode.positive_sample_size) / func.sum(S4_farm_mode.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S4_farm_mode.Country == 'China')
        .filter(S4_farm_mode.Province != 'NA')
        .group_by(func.trim(S4_farm_mode.Province), S4_farm_mode.Raising_mode)
        .order_by(func.trim(S4_farm_mode.Province))
        .all()
    )
    result = [
        {
            'name': row.province,
            'Raising_mode': row.Raising_mode,
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

@app.route('/S4_biovar_country_stats', methods=['GET'])
def S4_get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S4_farm_mode.Country,
            S4_farm_mode.Raising_mode,
            func.sum(S4_farm_mode.total_sample_size).label("total_sample_size"),
            func.sum(S4_farm_mode.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S4_farm_mode.Biovar == biovar)
        .group_by(S4_farm_mode.Country, S4_farm_mode.Raising_mode)
        .all()
    )
    result = [
        {
            "name": row.Country,
            "Raising_mode": row.Raising_mode,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)

@app.route('/S4_biovar_province_stats', methods=['GET'])
def S4_get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S4_farm_mode.Province,
            S4_farm_mode.Raising_mode,
            func.sum(S4_farm_mode.total_sample_size).label("total_sample_size"),
            func.sum(S4_farm_mode.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S4_farm_mode.Biovar == biovar)
        .filter(S4_farm_mode.Country == 'China')
        .filter(S4_farm_mode.Province != 'NA')
        .group_by(S4_farm_mode.Province, S4_farm_mode.Raising_mode)
        .all()
    )
    result = [
        {
            "name": row.Province,
            "Raising_mode": row.Raising_mode,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)
##S5
@app.route('/S5_description', methods=['GET'])
def S5_get_description_data():
    data = (
        db.session.query(
            func.trim(S5_chick_economic_usage.Country).label('country'),
            S5_chick_economic_usage.Economic_use,
            S5_chick_economic_usage.Growth_stage,
            func.sum(S5_chick_economic_usage.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S5_chick_economic_usage.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S5_chick_economic_usage.positive_sample_size) / func.sum(S5_chick_economic_usage.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S5_chick_economic_usage.Country != "")
        .filter(S5_chick_economic_usage.total_sample_size != None)
        .filter(S5_chick_economic_usage.positive_sample_size != None)
        .group_by(func.trim(S5_chick_economic_usage.Country))
        .order_by(func.trim(S5_chick_economic_usage.Country))
        .all()
    )
    result = [
        {
            'name': row.country,
            'Economic_use': row.Economic_use,
            'Growth_stage': row.Growth_stage,
            'Total_sample_size': row.Total_sample_size_sum,
            'Positive_sample_size': row.Positive_sample_size_sum,
            'Positive_rate': row.positive_rate
        } for row in data
    ]
    return jsonify(data=result)
@app.route('/S5_description_province', methods=['GET'])
def S5_get_description_province_data():
    data = (
        db.session.query(
            func.trim(S5_chick_economic_usage.Province).label('province'),
            S5_chick_economic_usage.Economic_use,
            S5_chick_economic_usage.Growth_stage,
            func.sum(S5_chick_economic_usage.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S5_chick_economic_usage.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S5_chick_economic_usage.positive_sample_size) / func.sum(S5_chick_economic_usage.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S5_chick_economic_usage.Country == 'China')
        .filter(S5_chick_economic_usage.Province != 'NA')
        .group_by(func.trim(S5_chick_economic_usage.Province), S5_chick_economic_usage.Economic_use, S5_chick_economic_usage.Growth_stage)
        .order_by(func.trim(S5_chick_economic_usage.Province))
        .all()
    )
    result = [
        {
            'name': row.province,
            'Economic_use': row.Economic_use,
            'Growth_stage': row.Growth_stage,
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

@app.route('/S5_biovar_country_stats', methods=['GET'])
def S5_get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S5_chick_economic_usage.Country,
            S5_chick_economic_usage.Economic_use,
            S5_chick_economic_usage.Growth_stage,
            func.sum(S5_chick_economic_usage.total_sample_size).label("total_sample_size"),
            func.sum(S5_chick_economic_usage.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S5_chick_economic_usage.Biovar == biovar)
        .group_by(S5_chick_economic_usage.Country, S5_chick_economic_usage.Economic_use, S5_chick_economic_usage.Growth_stage)
        .all()
    )
    result = [
        {
            "name": row.Country,
            "Economic_use": row.Economic_use,
            "Growth_stage": row.Growth_stage,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)
@app.route('/S5_biovar_province_stats', methods=['GET'])
def S5_get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S5_chick_economic_usage.Province,
            S5_chick_economic_usage.Economic_use,
            S5_chick_economic_usage.Growth_stage,
            func.sum(S5_chick_economic_usage.total_sample_size).label("total_sample_size"),
            func.sum(S5_chick_economic_usage.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S5_chick_economic_usage.Biovar == biovar)
        .filter(S5_chick_economic_usage.Country == 'China')
        .filter(S5_chick_economic_usage.Province != 'NA')
        .group_by(S5_chick_economic_usage.Province, S5_chick_economic_usage.Economic_use, S5_chick_economic_usage.Growth_stage)
        .all()
    )
    result = [
        {
            "name": row.Province,
            "Economic_use": row.Economic_use,
            "Growth_stage": row.Growth_stage,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)
#S6
@app.route('/S6_description', methods=['GET'])
def S6_get_description_country_data():
    data = (
        db.session.query(
            func.trim(S6_chick_sex.Country).label('country'),
            func.trim(S6_chick_sex.Gender).label('gender'),
            func.sum(S6_chick_sex.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S6_chick_sex.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S6_chick_sex.positive_sample_size) / func.sum(S6_chick_sex.total_sample_size) * 100, 2).label('positive_rate')
        )
        .group_by(func.trim(S6_chick_sex.Country), func.trim(S6_chick_sex.Gender))
        .order_by(func.trim(S6_chick_sex.Country), func.trim(S6_chick_sex.Gender))
        .all()
    )
    result = [
        {
            'name': row.country,
            'Gender': row.gender,
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
@app.route('/S6_description_province', methods=['GET'])
def S6_get_description_province_data():
    data = (
        db.session.query(
            func.trim(S6_chick_sex.Province).label('province'),
            func.trim(S6_chick_sex.Gender).label('gender'),
            func.sum(S6_chick_sex.total_sample_size).label('Total_sample_size_sum'),
            func.sum(S6_chick_sex.positive_sample_size).label('Positive_sample_size_sum'),
            func.round(func.sum(S6_chick_sex.positive_sample_size) / func.sum(S6_chick_sex.total_sample_size) * 100, 2).label('positive_rate')
        )
        .filter(S6_chick_sex.Country == 'China')
        .filter(S6_chick_sex.Province != 'NA')
        .group_by(func.trim(S6_chick_sex.Province), func.trim(S6_chick_sex.Gender))
        .order_by(func.trim(S6_chick_sex.Province))
        .all()
    )
    result = [
        {
            'name': row.province,
            'Gender': row.gender,
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

@app.route('/S6_biovar_country_stats', methods=['GET'])
def S6_get_biovar_country_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S6_chick_sex.Country,
            S6_chick_sex.Gender,
            func.sum(S6_chick_sex.total_sample_size).label("total_sample_size"),
            func.sum(S6_chick_sex.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S6_chick_sex.Biovar == biovar)
        .group_by(S6_chick_sex.Country, S6_chick_sex.Gender)
        .all()
    )
    result = [
        {
            "name": row.Country,
            "Gender": row.Gender,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)

@app.route('/S6_biovar_province_stats', methods=['GET'])
def S6_get_biovar_province_stats():
    biovar = request.args.get('biovar')
    if biovar not in ['bvSP', 'bvSG', 'unclear']:
        return jsonify({"error": "Invalid biovar value"}), 400
    data = (
        db.session.query(
            S6_chick_sex.Province,
            S6_chick_sex.Gender,
            func.sum(S6_chick_sex.total_sample_size).label("total_sample_size"),
            func.sum(S6_chick_sex.positive_sample_size).label("positive_sample_size"),
        )
        .filter(S6_chick_sex.Biovar == biovar)
        .filter(S6_chick_sex.Country == 'China')
        .filter(S6_chick_sex.Province != 'NA')
        .group_by(S6_chick_sex.Province, S6_chick_sex.Gender)
        .all()
    )
    result = [
        {
            "name": row.Province,
            "Gender": row.Gender,
            "total_sample_size": row.total_sample_size,
            "positive_sample_size": row.positive_sample_size,
            "positive_rate": round(row.positive_sample_size / row.total_sample_size * 100, 2),
        }
        for row in data
    ]
    return jsonify(result)

# 主程序入口
if __name__ == '__main__':
    # 使用应用上下文，确保正确执行查询
    with app.app_context():
        # 启动 Flask 服务器
        app.run(debug=True)
