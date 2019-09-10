#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import os
import re
import xlsxwriter
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from wand.image import Image
from wand.color import Color
import io


def main():

    data_path = './data'
    temp_path = './temp'
    result_path = './results'
    result_filename = './result.xlsx'

    # 每个人的发票处理
    write_list = []
    for subdir in os.listdir(data_path):

        has_bill = False
        has_route = False
        flag = False

        subdir_path = os.path.join(data_path, subdir)

        # 检查文件夹
        tmp_sub_path = subdir_path.replace('data', 'temp')
        if not os.path.exists(tmp_sub_path):
            os.mkdir(tmp_sub_path)

        tmp_sub_path = subdir_path.replace('data', 'results')
        if not os.path.exists(tmp_sub_path):
            os.mkdir(tmp_sub_path)

        filename_list = []
        for filename in os.listdir(subdir_path):
            pdf_path = os.path.join(data_path, subdir, filename)
            filename_list.append(pdf_path)

            if ('发票' and '.pdf') in filename:
                has_bill = True
            if ('行程' and '.pdf') in filename:
                has_route = True

        if (not has_bill) or (not has_route):
            print(f'{subdir} 提交数据不完整或格式错误')
            continue

        bill_price, route_price = 0, 0
        route_price_list = []
        for filename in filename_list:
            text = parse_pdf(filename)
            if '发票' in filename:
                bill_price = extract_bill(text)

            elif '行程' in filename:
                price = extract_route(text)
                route_price_list.append(price)

        route_price = sum(route_price_list)
        if bill_price == route_price:
            flag = True

        print(f'{subdir} {bill_price} {route_price} {flag}')

        flag_str = '是' if flag else '否'
        data_str = '是'
        write_list.append([subdir, bill_price, route_price, flag_str, data_str])

        # 保存图片
        print(filename_list)
        save_pic(filename_list)

    write_excel(result_filename, write_list)

def save_pic(filename_list):

    for filepath in filename_list:
        result_filepath = filepath.replace('data', 'results').replace('.pdf', '.jpeg')

        pdf_bytes = io.BytesIO()
        img = Image(file=pdf_bytes)
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        img.save(filename=result_filepath)
        img.destroy()

# 写excel
def write_excel(result_filename, write_list):
    workbook = xlsxwriter.Workbook(result_filename)
    worksheet = workbook.add_worksheet()

    format = workbook.add_format()  # 定义format格式对象
    # format.set_bg_color('red')
    # format.set_border(1)  # 定义format对象单元格边框加粗（1个像素）的格式
    # format_title = workbook.add_format()  # 定义format_title格式对象
    # format_title.set_border(1)  # 定义format_title对象单元格边框加粗（1个像素）的格式
    # format_title.set_bg_color('#cccccc')  # 定义format_title对象单元格背景颜色为'#cccccc'的格式

    title = [U'姓名', U'发票价格', U'行程单价格', U'是否一致', U'数据规范']
    worksheet.write_row('A1', title)

    row_num = 2
    for k,v in enumerate(write_list):
        row = 'A' + str(row_num)
        data = v
        row_format = format
        if v[3] != '是':
            row_format.set_bg_color('red')
        worksheet.write_row(row, data, row_format)
        row_num += 1

    workbook.close()

# 解析文件
def parse_pdf(path):
    with open(path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        extracted_text = ''
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    extracted_text += lt_obj.get_text()

        return extracted_text

    # with open(output_path, "w", encoding="utf-8") as f:
    #     f.write(extracted_text)

def extract_bill(text):
    total_price = re.findall('小写）([\s\S]+?)销', text)[0]
    total_price = str(total_price).strip('\n').strip(' ').strip('￥')
    return float(total_price)

def extract_route(text):
    total_price = re.findall('合计(.*)元', text)[0]
    total_price = str(total_price).strip('\n').strip(' ').strip('￥')
    return float(total_price)


# 格式化发票内容
# 内容分区
def split_block(text):
    text_line = text.split("\n")
    # 第一步：分区：[公共头,购买方,销售方，公共域]
    header = []
    buyer = []
    saler = []
    body = []
    index = 0
    while index < len(text_line):
        if not text_line[index] == "购":
            header.append(re.sub(r"\s+", "", text_line[index]))
            index += 1
            continue
        else:
            break
    while index < len(text_line):
        if not text_line[index] == "项目名称":
            if text_line[index] == "购" or text_line[index] == "买" or text_line[index] == "方":
                index += 1
                continue
            if re.sub(r"\s+", "", text_line[index]) == "地址、" and re.sub(
                    r"\s+", "", text_line[index + 1]) == "电话:":
                buyer.append(
                    re.sub(r"\s+", "",
                           text_line[index] + text_line[index + 1]))
                index += 2
                continue
            buyer.append(re.sub(r"\s+", "", text_line[index]))
            index += 1
            continue
        else:
            break
    while index < len(text_line):
        if not re.sub(r"\s+", "", text_line[index]) == "名称:":
            body.append(re.sub(r"\s+", "", text_line[index]))
            index += 1
            continue
        else:
            break
    while index < len(text_line):
        if re.sub(r"\s+", "", text_line[index]) == "地址、" and re.sub(
                r"\s+", "", text_line[index + 1]) == "电话:":
            saler.append(
                re.sub(r"\s+", "", text_line[index] + text_line[index + 1]))
            index += 2
            continue
        saler.append(re.sub(r"\s+", "", text_line[index]))
        index += 1
        continue
    return header, buyer, body, saler

if __name__ == '__main__':
    main()