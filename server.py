#!/usr/bin/env python3
"""
统一服务器，同时提供前端静态文件和后端API服务
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import uuid

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据文件路径
LITERATURE_FILE = 'literature.json'
TAXONOMY_FILE = 'taxonomy.json'
SAMPLE_FILE = 'sample.json'


def load_json_data(file_path):
    """加载JSON数据文件"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json_data(file_path, data):
    """保存数据到JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# API路由
@app.route('/api/literature', methods=['GET'])
def get_literature():
    """获取所有文献数据"""
    literature_data = load_json_data(LITERATURE_FILE)
    
    # 处理搜索查询参数
    search_term = request.args.get('search', '').lower()
    if search_term:
        literature_data = [
            item for item in literature_data
            if search_term in item.get('id', '').lower() or
               search_term in item.get('title', '').lower() or
               search_term in item.get('authors', '').lower() or
               search_term in item.get('journal', '').lower() or
               search_term in item.get('year', '').lower() or
               search_term in item.get('doi', '').lower() or
               search_term in item.get('abstract', '').lower()
        ]
    
    return jsonify(literature_data)


@app.route('/api/literature', methods=['POST'])
def add_literature():
    """添加新的文献"""
    data = request.get_json()
    
    # 如果没有提供ID，则生成一个新的UUID
    if not data.get('id'):
        data['id'] = f"LIT-{str(uuid.uuid4())}"
    
    # 验证必需字段
    if not data.get('title'):
        return jsonify({'error': '标题不能为空'}), 400
    
    literature_data = load_json_data(LITERATURE_FILE)
    
    # 检查是否已存在相同ID的文献
    for i, lit in enumerate(literature_data):
        if lit.get('id') == data.get('id'):
            literature_data[i] = data
            break
    else:
        literature_data.append(data)
    
    save_json_data(LITERATURE_FILE, literature_data)
    return jsonify(data), 201


@app.route('/api/taxonomy', methods=['GET'])
def get_taxonomy():
    """获取所有分类数据"""
    taxonomy_data = load_json_data(TAXONOMY_FILE)
    
    # 处理搜索查询参数
    search_term = request.args.get('search', '').lower()
    if search_term:
        taxonomy_data = [
            item for item in taxonomy_data
            if search_term in item.get('id', '').lower() or
               search_term in item.get('name', '').lower() or
               search_term in item.get('level', '').lower() or
               search_term in item.get('type', '').lower() or
               search_term in item.get('lit_id', '').lower() or
               search_term in item.get('description', '').lower()
        ]
    
    return jsonify(taxonomy_data)


@app.route('/api/taxonomy', methods=['POST'])
def add_taxonomy():
    """添加新的分类"""
    data = request.get_json()
    
    # 如果没有提供ID，则生成一个新的UUID
    if not data.get('id'):
        data['id'] = f"TAX-{str(uuid.uuid4())}"
    
    # 验证必需字段
    if not data.get('name'):
        return jsonify({'error': '分类名称不能为空'}), 400
    
    taxonomy_data = load_json_data(TAXONOMY_FILE)
    
    # 检查是否已存在相同ID的分类
    for i, tax in enumerate(taxonomy_data):
        if tax.get('id') == data.get('id'):
            taxonomy_data[i] = data
            break
    else:
        taxonomy_data.append(data)
    
    save_json_data(TAXONOMY_FILE, taxonomy_data)
    return jsonify(data), 201


@app.route('/api/samples', methods=['GET'])
def get_samples():
    """获取所有样本数据"""
    sample_data = load_json_data(SAMPLE_FILE)
    
    # 处理搜索查询参数
    search_term = request.args.get('search', '').lower()
    if search_term:
        sample_data = [
            item for item in sample_data
            if search_term in item.get('id', '').lower() or
               search_term in item.get('tax_id', '').lower() or
               search_term in item.get('collector', '').lower() or
               search_term in str(item.get('latitude', '')).lower() or
               search_term in str(item.get('longitude', '')).lower() or
               search_term in item.get('description', '').lower()
        ]
    
    return jsonify(sample_data)


@app.route('/api/samples', methods=['POST'])
def add_sample():
    """添加新的样本"""
    data = request.get_json()
    
    # 如果没有提供ID，则生成一个新的UUID
    if not data.get('id'):
        data['id'] = f"SMP-{str(uuid.uuid4())}"
    
    # 验证必需字段
    if not data.get('tax_id'):
        return jsonify({'error': '分类ID不能为空'}), 400
    
    sample_data = load_json_data(SAMPLE_FILE)
    
    # 检查是否已存在相同ID的样本
    for i, sample in enumerate(sample_data):
        if sample.get('id') == data.get('id'):
            sample_data[i] = data
            break
    else:
        sample_data.append(data)
    
    save_json_data(SAMPLE_FILE, sample_data)
    return jsonify(data), 201


@app.route('/api/generate-id/<item_type>', methods=['GET'])
def generate_id(item_type):
    """生成指定类型的UUID"""
    if item_type == 'literature':
        return jsonify({'id': f"LIT-{str(uuid.uuid4())}"})
    elif item_type == 'taxonomy':
        return jsonify({'id': f"TAX-{str(uuid.uuid4())}"})
    elif item_type == 'sample':
        return jsonify({'id': f"SMP-{str(uuid.uuid4())}"})
    else:
        return jsonify({'error': '不支持的项目类型'}), 400


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    literature_count = len(load_json_data(LITERATURE_FILE))
    taxonomy_count = len(load_json_data(TAXONOMY_FILE))
    sample_count = len(load_json_data(SAMPLE_FILE))
    
    return jsonify({
        'literature_count': literature_count,
        'taxonomy_count': taxonomy_count,
        'sample_count': sample_count
    })


# 静态文件路由
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


if __name__ == '__main__':
    print("服务器启动在 http://localhost:8000")
    print("按 Ctrl+C 停止服务器")
    app.run(host='0.0.0.0', port=8000, debug=True)