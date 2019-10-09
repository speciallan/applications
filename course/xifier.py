#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import os

def main():
    str1 = '岗位职责：\n\
1.协助负责员工全生命周期的HR运营管理，包括入离职协调沟通，劳动关系管理等，为公司所有员工提供对应服务，并建立SSC良好的服务口碑；\n\
2.维护SSC基础数据及员工信息，通过对数据管理的不断优化，为业务部门提供数据支持，辅助业务管理者诊断组织问题；\n\
3.组织人力行政各模块梳理并优化各项制度流程，编制相应SOP并推动执行，形成体系化、高效率的业务流程执行体系；\n\
4.推动SSC服务的线上化流程化，并负责eHR等办公系统的运营管理，收集需求，推动系统优化进程。\n\
\n\
任职要求：\n\
1.本科及以上学历，人力资源管理专业或具有同类实习经验者优先考虑；\n\
2.热爱人力资源行业，具备优秀的沟通能力和组织协调能力；\n\
3.具备基础HR运营知识，能够针对不同的情境提供相应的HR政策及规定的支持，具备较强的数据分析与逻辑思考能力；\n\
4.在SSC搭建过程中，愿意和团队成员一起承接最基础的操作工作，一边执行一边建设；\n\
5.熟悉劳动法、社保及个税政策者优先考虑。'



    print(ord('😁'))

    print(chr(128513+1))
    exit()

    t = os.getcwd()
    print(t)
    cur = '/'.join(sys.argv[0].split('/')[0:-1])
    os.chdir(cur)

    f = open('data.txt', 'r', encoding='utf-8')
    str1 = f.read()
    f.close()

    dict1 = {}
    # set1 = set()

    num = 1
    # for i in str1:
        # dict1[i] = num
        # set1.add(i)

    for i in str1:
        if i not in dict1.keys():
            dict1[i] = str(num).rjust(8, '0')
            num += 1

    print(dict1)

    print('编码:')
    ma = ''
    for i in str1:
        ma += str(dict1[i])

    dict2 = {str(v):k for k,v in dict1.items()}
    print('解码:')
    jiema = ''

    ma2 = []
    for i in range(0, len(ma), 8):
        ma2.append(ma[i:i+8])

    print(ma2)
    for i in ma2:
        # print(dict2[i])
        jiema += dict2[i]
    print(jiema)

    xifier = open('xifier.txt', 'w', encoding='utf-8')
    xifier.write(ma + jiema)
    xifier.close()



    # {'重': 6, '庆': 7, '大': 3, '学': 4, '在': 5}


if __name__ == '__main__':
    main()
