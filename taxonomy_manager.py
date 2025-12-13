import sys
import json
import os
import re
import uuid
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
                             QTabWidget, QGroupBox, QFormLayout, QDoubleSpinBox)
from PyQt5.QtCore import Qt


class TaxonomyManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.literature_data = []
        self.taxonomy_data = []
        self.sample_data = []
        
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('分类学管理系统')
        self.setGeometry(100, 100, 1000, 700)

        # 创建标签页
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # 添加各个标签页
        tab_widget.addTab(self.create_literature_tab(), "文献管理 (LITid)")
        tab_widget.addTab(self.create_taxonomy_tab(), "分类管理 (TAXid)")
        tab_widget.addTab(self.create_sample_tab(), "样本管理 (SMPid)")

    def create_literature_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 输入区域
        input_group = QGroupBox("添加/编辑文献")
        form_layout = QFormLayout()
        
        self.lit_id_input = QLineEdit()
        self.lit_id_input.setPlaceholderText("例如: LIT-xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.lit_title_input = QLineEdit()
        self.lit_authors_input = QLineEdit()
        self.lit_journal_input = QLineEdit()
        self.lit_year_input = QLineEdit()
        self.lit_doi_input = QLineEdit()
        self.lit_url_input = QLineEdit()
        self.lit_is_oa_input = QLineEdit()  # 添加OA字段输入框
        self.lit_abstract_input = QTextEdit()
        self.lit_abstract_input.setMaximumHeight(100)
        self.lit_ris_input = QTextEdit()
        self.lit_ris_input.setMaximumHeight(100)
        
        form_layout.addRow("文献ID:", self.lit_id_input)
        form_layout.addRow("标题:", self.lit_title_input)
        form_layout.addRow("作者:", self.lit_authors_input)
        form_layout.addRow("期刊:", self.lit_journal_input)
        form_layout.addRow("年份:", self.lit_year_input)
        form_layout.addRow("DOI:", self.lit_doi_input)
        form_layout.addRow("URL:", self.lit_url_input)
        form_layout.addRow("是否OA (true/false):", self.lit_is_oa_input)  # 添加OA字段
        form_layout.addRow("摘要:", self.lit_abstract_input)
        form_layout.addRow("RIS内容:", self.lit_ris_input)
        
        input_layout = QHBoxLayout()
        self.lit_save_btn = QPushButton("保存文献")
        self.lit_clear_btn = QPushButton("清空表单")
        self.lit_import_ris_btn = QPushButton("从RIS导入")
        self.lit_generate_id_btn = QPushButton("生成ID")
        
        input_layout.addWidget(self.lit_generate_id_btn)
        input_layout.addWidget(self.lit_save_btn)
        input_layout.addWidget(self.lit_clear_btn)
        input_layout.addWidget(self.lit_import_ris_btn)
        
        input_group.setLayout(form_layout)
        
        # 按钮连接
        self.lit_save_btn.clicked.connect(self.save_literature)
        self.lit_clear_btn.clicked.connect(self.clear_literature_form)
        self.lit_import_ris_btn.clicked.connect(self.import_from_ris)
        self.lit_generate_id_btn.clicked.connect(self.generate_literature_id)
        
        # 表格显示
        self.lit_table = QTableWidget()
        self.lit_table.setColumnCount(6)
        self.lit_table.setHorizontalHeaderLabels(["文献ID", "标题", "作者", "期刊", "年份", "操作"])
        
        layout.addWidget(input_group)
        layout.addLayout(input_layout)
        layout.addWidget(self.lit_table)
        
        tab.setLayout(layout)
        return tab

    def create_taxonomy_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 输入区域
        input_group = QGroupBox("添加/编辑分类")
        form_layout = QFormLayout()
        
        self.tax_lit_id_input = QComboBox()
        self.tax_level_input = QComboBox()
        self.tax_level_input.addItems(["Phylum", "Class", "Order", "Family", "Genus", "Species"])
        self.tax_type_input = QComboBox()
        self.tax_type_input.addItems(["new taxon", "new combination", "taxon swap [new synonym]"])
        self.tax_parent_input = QComboBox()
        self.tax_id_input = QLineEdit()
        self.tax_id_input.setPlaceholderText("例如: TAX-xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.tax_name_input = QLineEdit()
        self.tax_description_input = QTextEdit()
        self.tax_description_input.setMaximumHeight(100)
        
        form_layout.addRow("继承的LITid:", self.tax_lit_id_input)
        form_layout.addRow("级别:", self.tax_level_input)
        form_layout.addRow("类型:", self.tax_type_input)
        form_layout.addRow("名称:", self.tax_name_input)
        form_layout.addRow("描述:", self.tax_description_input)
        form_layout.addRow("继承的TAXid (用于组合/同义词):", self.tax_parent_input)
        form_layout.addRow("分类ID:", self.tax_id_input)
        
        input_layout = QHBoxLayout()
        self.tax_generate_id_btn = QPushButton("生成ID")
        self.tax_save_btn = QPushButton("保存分类")
        self.tax_clear_btn = QPushButton("清空表单")
        
        input_layout.addWidget(self.tax_generate_id_btn)
        input_layout.addWidget(self.tax_save_btn)
        input_layout.addWidget(self.tax_clear_btn)
        
        input_group.setLayout(form_layout)
        
        # 按钮连接
        self.tax_generate_id_btn.clicked.connect(self.generate_taxonomy_id)
        self.tax_save_btn.clicked.connect(self.save_taxonomy)
        self.tax_clear_btn.clicked.connect(self.clear_taxonomy_form)
        
        # 表格显示
        self.tax_table = QTableWidget()
        self.tax_table.setColumnCount(6)
        self.tax_table.setHorizontalHeaderLabels(["分类ID", "名称", "级别", "类型", "文献ID", "操作"])
        
        layout.addWidget(input_group)
        layout.addLayout(input_layout)
        layout.addWidget(self.tax_table)
        
        tab.setLayout(layout)
        return tab

    def create_sample_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 输入区域
        input_group = QGroupBox("添加/编辑样本")
        form_layout = QFormLayout()
        
        self.smp_tax_id_input = QComboBox()
        self.smp_collector_input = QLineEdit()
        self.smp_latitude_input = QDoubleSpinBox()
        self.smp_latitude_input.setRange(-90, 90)
        self.smp_latitude_input.setDecimals(6)
        self.smp_longitude_input = QDoubleSpinBox()
        self.smp_longitude_input.setRange(-180, 180)
        self.smp_longitude_input.setDecimals(6)
        self.smp_id_input = QLineEdit()
        self.smp_id_input.setPlaceholderText("例如: SMP-xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.smp_description_input = QTextEdit()
        self.smp_description_input.setMaximumHeight(100)
        
        form_layout.addRow("继承的TAXid:", self.smp_tax_id_input)
        form_layout.addRow("采集者:", self.smp_collector_input)
        form_layout.addRow("纬度:", self.smp_latitude_input)
        form_layout.addRow("经度:", self.smp_longitude_input)
        form_layout.addRow("描述:", self.smp_description_input)
        form_layout.addRow("样本ID:", self.smp_id_input)
        
        input_layout = QHBoxLayout()
        self.smp_generate_id_btn = QPushButton("生成ID")
        self.smp_save_btn = QPushButton("保存样本")
        self.smp_clear_btn = QPushButton("清空表单")
        
        input_layout.addWidget(self.smp_generate_id_btn)
        input_layout.addWidget(self.smp_save_btn)
        input_layout.addWidget(self.smp_clear_btn)
        
        input_group.setLayout(form_layout)
        
        # 按钮连接
        self.smp_generate_id_btn.clicked.connect(self.generate_sample_id)
        self.smp_save_btn.clicked.connect(self.save_sample)
        self.smp_clear_btn.clicked.connect(self.clear_sample_form)
        
        # 表格显示
        self.smp_table = QTableWidget()
        self.smp_table.setColumnCount(6)
        self.smp_table.setHorizontalHeaderLabels(["样本ID", "分类ID", "采集者", "纬度", "经度", "操作"])
        
        layout.addWidget(input_group)
        layout.addLayout(input_layout)
        layout.addWidget(self.smp_table)
        
        tab.setLayout(layout)
        return tab

    def generate_literature_id(self):
        """生成文献ID"""
        unique_id = str(uuid.uuid4())
        self.lit_id_input.setText(f"LIT-{unique_id}")

    def generate_taxonomy_id(self):
        """生成分类ID"""
        unique_id = str(uuid.uuid4())
        self.tax_id_input.setText(f"TAX-{unique_id}")

    def generate_sample_id(self):
        """生成样本ID"""
        unique_id = str(uuid.uuid4())
        self.smp_id_input.setText(f"SMP-{unique_id}")

    def load_data(self):
        # 加载文献数据
        if os.path.exists("literature.json"):
            with open("literature.json", "r", encoding="utf-8") as f:
                self.literature_data = json.load(f)
        
        # 加载分类数据
        if os.path.exists("taxonomy.json"):
            with open("taxonomy.json", "r", encoding="utf-8") as f:
                self.taxonomy_data = json.load(f)
                
        # 加载样本数据
        if os.path.exists("sample.json"):
            with open("sample.json", "r", encoding="utf-8") as f:
                self.sample_data = json.load(f)
                
        self.refresh_all_tables()
        self.update_comboboxes()

    def save_data(self):
        # 保存文献数据
        with open("literature.json", "w", encoding="utf-8") as f:
            json.dump(self.literature_data, f, ensure_ascii=False, indent=2)
            
        # 保存分类数据
        with open("taxonomy.json", "w", encoding="utf-8") as f:
            json.dump(self.taxonomy_data, f, ensure_ascii=False, indent=2)
            
        # 保存样本数据
        with open("sample.json", "w", encoding="utf-8") as f:
            json.dump(self.sample_data, f, ensure_ascii=False, indent=2)

    def refresh_all_tables(self):
        self.refresh_literature_table()
        self.refresh_taxonomy_table()
        self.refresh_sample_table()

    def update_comboboxes(self):
        # 更新文献下拉框
        self.tax_lit_id_input.clear()
        for lit in self.literature_data:
            self.tax_lit_id_input.addItem(lit.get("id", "") + " - " + lit.get("title", ""), lit.get("id", ""))
            
        # 更新分类下拉框
        self.tax_parent_input.clear()
        self.smp_tax_id_input.clear()
        for tax in self.taxonomy_data:
            display_text = tax.get("id", "") + " - " + tax.get("name", "")
            self.tax_parent_input.addItem(display_text, tax.get("id", ""))
            self.smp_tax_id_input.addItem(display_text, tax.get("id", ""))

    def save_literature(self):
        lit_id = self.lit_id_input.text().strip()
        title = self.lit_title_input.text().strip()
        authors = self.lit_authors_input.text().strip()
        journal = self.lit_journal_input.text().strip()
        year = self.lit_year_input.text().strip()
        doi = self.lit_doi_input.text().strip()
        url = self.lit_url_input.text().strip()
        abstract = self.lit_abstract_input.toPlainText().strip()
        
        # 处理is_oa字段，确保正确转换为布尔值
        is_oa_text = self.lit_is_oa_input.text().strip().lower()
        is_oa = True if is_oa_text == 'true' else False if is_oa_text == 'false' else None
        
        if not lit_id or not title:
            QMessageBox.warning(self, "输入错误", "文献ID和标题不能为空！")
            return
            
        # 创建文献条目
        literature_entry = {
            "id": lit_id,
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "abstract": abstract
        }
        
        # 只有当is_oa有有效值时才添加到条目中
        if is_oa is not None:
            literature_entry["is_oa"] = is_oa
            
        # 检查是否已存在相同ID的文献
        existing_index = next((i for i, item in enumerate(self.literature_data) if item["id"] == lit_id), None)
        if existing_index is not None:
            self.literature_data[existing_index] = literature_entry
        else:
            self.literature_data.append(literature_entry)
            
        self.save_data()
        self.refresh_literature_table()
        self.update_comboboxes()
        self.clear_literature_form()
        QMessageBox.information(self, "成功", "文献保存成功！")

    def clear_literature_form(self):
        # 清空文献表单
        self.lit_id_input.clear()
        self.lit_title_input.clear()
        self.lit_authors_input.clear()
        self.lit_journal_input.clear()
        self.lit_year_input.clear()
        self.lit_doi_input.clear()
        self.lit_url_input.clear()
        self.lit_abstract_input.clear()
        self.lit_ris_input.clear()

    def load_literature_into_form(self, row):
        item = self.literature_data[row]
        self.lit_id_input.setText(item.get("id", ""))
        self.lit_title_input.setText(item.get("title", ""))
        self.lit_authors_input.setText(item.get("authors", ""))
        self.lit_journal_input.setText(item.get("journal", ""))
        self.lit_year_input.setText(item.get("year", ""))
        self.lit_doi_input.setText(item.get("doi", ""))
        self.lit_url_input.setText(item.get("url", ""))
        self.lit_abstract_input.setPlainText(item.get("abstract", ""))
        
        # 加载is_oa字段
        is_oa = item.get("is_oa")
        if is_oa is True:
            self.lit_is_oa_input.setText("true")
        elif is_oa is False:
            self.lit_is_oa_input.setText("false")
        else:
            self.lit_is_oa_input.setText("")

    def import_from_ris(self):
        ris_text = self.lit_ris_input.toPlainText().strip()
        if not ris_text:
            QMessageBox.warning(self, "输入错误", "RIS内容不能为空！")
            return
            
        # 解析RIS格式
        lit_data = self.parse_ris_format(ris_text)
        if lit_data:
            # 自动生成ID
            self.generate_literature_id()
            self.lit_title_input.setText(lit_data.get("title", ""))
            self.lit_authors_input.setText(lit_data.get("authors", ""))
            self.lit_journal_input.setText(lit_data.get("journal", ""))
            self.lit_year_input.setText(lit_data.get("year", ""))
            QMessageBox.information(self, "成功", "RIS解析成功！")
        else:
            QMessageBox.warning(self, "解析失败", "无法从RIS内容中提取有效信息！")

    def parse_ris_format(self, ris_text):
        # 简单的RIS格式解析
        lines = ris_text.split('\n')
        lit_data = {"title": "", "authors": "", "journal": "", "year": ""}
        
        for line in lines:
            if line.startswith("TI"):
                lit_data["title"] = line[6:].strip() if len(line) > 6 else ""
            elif line.startswith("AU"):
                if lit_data["authors"]:
                    lit_data["authors"] += "; " + line[6:].strip() if len(line) > 6 else ""
                else:
                    lit_data["authors"] = line[6:].strip() if len(line) > 6 else ""
            elif line.startswith("JO"):
                lit_data["journal"] = line[6:].strip() if len(line) > 6 else ""
            elif line.startswith("PY"):
                year_match = re.search(r'\d{4}', line)
                if year_match:
                    lit_data["year"] = year_match.group()
                    
        return lit_data

    def save_taxonomy(self):
        tax_id = self.tax_id_input.text().strip()
        name = self.tax_name_input.text().strip()
        level = self.tax_level_input.currentText()
        tax_type = self.tax_type_input.currentText()
        lit_id = self.tax_lit_id_input.currentData()
        parent_tax_id = self.tax_parent_input.currentData()
        description = self.tax_description_input.toPlainText().strip()
        
        if not tax_id or not name:
            QMessageBox.warning(self, "输入错误", "分类ID和名称不能为空！")
            return
            
        # 检查是否已存在相同ID的分类
        for i, tax in enumerate(self.taxonomy_data):
            if tax.get("id") == tax_id:
                # 更新现有分类
                self.taxonomy_data[i] = {
                    "id": tax_id,
                    "name": name,
                    "level": level,
                    "type": tax_type,
                    "lit_id": lit_id,
                    "parent_tax_id": parent_tax_id,
                    "description": description
                }
                break
        else:
            # 添加新分类
            self.taxonomy_data.append({
                "id": tax_id,
                "name": name,
                "level": level,
                "type": tax_type,
                "lit_id": lit_id,
                "parent_tax_id": parent_tax_id,
                "description": description
            })
            
        self.save_data()
        self.refresh_taxonomy_table()
        self.update_comboboxes()
        self.clear_taxonomy_form()
        QMessageBox.information(self, "成功", "分类保存成功！")

    def clear_taxonomy_form(self):
        # 清空分类表单
        self.tax_id_input.clear()
        self.tax_name_input.clear()
        self.tax_description_input.clear()

    def save_sample(self):
        smp_id = self.smp_id_input.text().strip()
        tax_id = self.smp_tax_id_input.currentData()
        collector = self.smp_collector_input.text().strip()
        latitude = self.smp_latitude_input.value()
        longitude = self.smp_longitude_input.value()
        description = self.smp_description_input.toPlainText().strip()
        
        if not smp_id or not tax_id:
            QMessageBox.warning(self, "输入错误", "样本ID和分类ID不能为空！")
            return
            
        # 检查是否已存在相同ID的样本
        for i, smp in enumerate(self.sample_data):
            if smp.get("id") == smp_id:
                # 更新现有样本
                self.sample_data[i] = {
                    "id": smp_id,
                    "tax_id": tax_id,
                    "collector": collector,
                    "latitude": latitude,
                    "longitude": longitude,
                    "description": description
                }
                break
        else:
            # 添加新样本
            self.sample_data.append({
                "id": smp_id,
                "tax_id": tax_id,
                "collector": collector,
                "latitude": latitude,
                "longitude": longitude,
                "description": description
            })
            
        self.save_data()
        self.refresh_sample_table()
        self.clear_sample_form()
        QMessageBox.information(self, "成功", "样本保存成功！")

    def clear_sample_form(self):
        # 清空样本表单
        self.smp_id_input.clear()
        self.smp_collector_input.clear()
        self.smp_latitude_input.setValue(0)
        self.smp_longitude_input.setValue(0)
        self.smp_description_input.clear()

    def refresh_literature_table(self):
        self.lit_table.setRowCount(len(self.literature_data))
        for row, lit in enumerate(self.literature_data):
            self.lit_table.setItem(row, 0, QTableWidgetItem(lit.get("id", "")))
            self.lit_table.setItem(row, 1, QTableWidgetItem(lit.get("title", "")))
            self.lit_table.setItem(row, 2, QTableWidgetItem(lit.get("authors", "")))
            self.lit_table.setItem(row, 3, QTableWidgetItem(lit.get("journal", "")))
            
            # 显示年份
            year_item = QTableWidgetItem(lit.get("year", ""))
            self.lit_table.setItem(row, 4, year_item)
            
            # 添加操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            edit_btn = QPushButton("编辑")
            delete_btn = QPushButton("删除")
            edit_btn.clicked.connect(lambda checked, l=lit: self.edit_literature(l))
            delete_btn.clicked.connect(lambda checked, lid=lit.get("id"): self.delete_literature(lid))
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            self.lit_table.setCellWidget(row, 5, btn_widget)
            
            # 添加操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            edit_btn = QPushButton("编辑")
            delete_btn = QPushButton("删除")
            edit_btn.clicked.connect(lambda checked, l=lit: self.edit_literature(l))
            delete_btn.clicked.connect(lambda checked, lid=lit.get("id"): self.delete_literature(lid))
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            self.lit_table.setCellWidget(row, 5, btn_widget)

    def refresh_taxonomy_table(self):
        self.tax_table.setRowCount(len(self.taxonomy_data))
        for row, tax in enumerate(self.taxonomy_data):
            self.tax_table.setItem(row, 0, QTableWidgetItem(tax.get("id", "")))
            self.tax_table.setItem(row, 1, QTableWidgetItem(tax.get("name", "")))
            self.tax_table.setItem(row, 2, QTableWidgetItem(tax.get("level", "")))
            self.tax_table.setItem(row, 3, QTableWidgetItem(tax.get("type", "")))
            self.tax_table.setItem(row, 4, QTableWidgetItem(tax.get("lit_id", "")))
            
            # 添加操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            edit_btn = QPushButton("编辑")
            delete_btn = QPushButton("删除")
            edit_btn.clicked.connect(lambda checked, t=tax: self.edit_taxonomy(t))
            delete_btn.clicked.connect(lambda checked, tid=tax.get("id"): self.delete_taxonomy(tid))
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            self.tax_table.setCellWidget(row, 5, btn_widget)

    def refresh_sample_table(self):
        self.smp_table.setRowCount(len(self.sample_data))
        for row, smp in enumerate(self.sample_data):
            self.smp_table.setItem(row, 0, QTableWidgetItem(smp.get("id", "")))
            self.smp_table.setItem(row, 1, QTableWidgetItem(smp.get("tax_id", "")))
            self.smp_table.setItem(row, 2, QTableWidgetItem(smp.get("collector", "")))
            self.smp_table.setItem(row, 3, QTableWidgetItem(str(smp.get("latitude", ""))))
            self.smp_table.setItem(row, 4, QTableWidgetItem(str(smp.get("longitude", ""))))
            
            # 添加操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            edit_btn = QPushButton("编辑")
            delete_btn = QPushButton("删除")
            edit_btn.clicked.connect(lambda checked, s=smp: self.edit_sample(s))
            delete_btn.clicked.connect(lambda checked, sid=smp.get("id"): self.delete_sample(sid))
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            self.smp_table.setCellWidget(row, 5, btn_widget)

    def edit_literature(self, literature):
        self.lit_id_input.setText(literature.get("id", ""))
        self.lit_title_input.setText(literature.get("title", ""))
        self.lit_authors_input.setText(literature.get("authors", ""))
        self.lit_journal_input.setText(literature.get("journal", ""))
        self.lit_year_input.setText(literature.get("year", ""))
        self.lit_doi_input.setText(literature.get("doi", ""))
        self.lit_url_input.setText(literature.get("url", ""))
        self.lit_abstract_input.setPlainText(literature.get("abstract", ""))
        
        # 设置is_oa字段
        is_oa = literature.get("is_oa")
        if is_oa is True:
            self.lit_is_oa_input.setText("true")
        elif is_oa is False:
            self.lit_is_oa_input.setText("false")
        else:
            self.lit_is_oa_input.clear()

    def delete_literature(self, lit_id):
        reply = QMessageBox.question(self, "确认删除", f"确定要删除文献 {lit_id} 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.literature_data = [lit for lit in self.literature_data if lit.get("id") != lit_id]
            self.save_data()
            self.refresh_literature_table()
            self.update_comboboxes()
            QMessageBox.information(self, "成功", "文献删除成功！")

    def edit_taxonomy(self, taxonomy):
        self.tax_id_input.setText(taxonomy.get("id", ""))
        self.tax_name_input.setText(taxonomy.get("name", ""))
        self.tax_description_input.setPlainText(taxonomy.get("description", ""))
        
        # 设置级别
        level_index = self.tax_level_input.findText(taxonomy.get("level", ""))
        if level_index >= 0:
            self.tax_level_input.setCurrentIndex(level_index)
            
        # 设置类型
        type_index = self.tax_type_input.findText(taxonomy.get("type", ""))
        if type_index >= 0:
            self.tax_type_input.setCurrentIndex(type_index)
            
        # 设置文献ID
        for i in range(self.tax_lit_id_input.count()):
            if self.tax_lit_id_input.itemData(i) == taxonomy.get("lit_id"):
                self.tax_lit_id_input.setCurrentIndex(i)
                break
                
        # 设置父分类ID
        for i in range(self.tax_parent_input.count()):
            if self.tax_parent_input.itemData(i) == taxonomy.get("parent_tax_id"):
                self.tax_parent_input.setCurrentIndex(i)
                break

    def delete_taxonomy(self, tax_id):
        reply = QMessageBox.question(self, "确认删除", f"确定要删除分类 {tax_id} 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.taxonomy_data = [tax for tax in self.taxonomy_data if tax.get("id") != tax_id]
            self.save_data()
            self.refresh_taxonomy_table()
            self.update_comboboxes()
            QMessageBox.information(self, "成功", "分类删除成功！")

    def edit_sample(self, sample):
        self.smp_id_input.setText(sample.get("id", ""))
        self.smp_collector_input.setText(sample.get("collector", ""))
        self.smp_latitude_input.setValue(float(sample.get("latitude", 0)))
        self.smp_longitude_input.setValue(float(sample.get("longitude", 0)))
        self.smp_description_input.setPlainText(sample.get("description", ""))
        
        # 设置分类ID
        for i in range(self.smp_tax_id_input.count()):
            if self.smp_tax_id_input.itemData(i) == sample.get("tax_id"):
                self.smp_tax_id_input.setCurrentIndex(i)
                break

    def delete_sample(self, smp_id):
        reply = QMessageBox.question(self, "确认删除", f"确定要删除样本 {smp_id} 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sample_data = [smp for smp in self.sample_data if smp.get("id") != smp_id]
            self.save_data()
            self.refresh_sample_table()
            QMessageBox.information(self, "成功", "样本删除成功！")


def main():
    app = QApplication(sys.argv)
    window = TaxonomyManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()