import requests
import os
import json
import time
import csv

path = r"C:\Users\l\Desktop"
os.chdir(path)
csvFile = open(r"C:\Users\l\Desktop\Python职位分析(上海).csv", "w")
writer = csv.writer(csvFile)
writer.writerow(("职位名称", "职位薪资", "职位优势", "公司全称", "公司福利", "工作地区"))
csvFile.close()

NO = 1  # 用于表示工作的序号
try:
    for page in range(1, 31, 1):
        print("开始爬取第%d页!" % page)

        url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Host': "www.lagou.com",
            'Origin': 'https:// www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=default&city=%E4%B8%8A%E6%B5%B7',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': None,
            'X-Requested-With': 'XMLHttpRequest'}  # 必要头文件
        data = {'first': 'true',
                'pn': '1',
                'kd': '数据分析'}  # 提交的表单数据

        if page != 1:
            data["pn"] = str(page)
            data["first"] = "false"

        html = requests.post(url, headers=header, data=data, params=params)
        json_result = html.json()

        positions = json_result['content']["positionResult"]["result"]
        if 1 <= NO <= 9:
            for each in positions:
                writer.writerow((each["positionName"], each["salary"], each["positionAdvantage"],
                                 each["companyFullName"], each["district"]))
                print("%d.职位名称:%s" % (NO, each["positionName"]))
                print("  职位薪资:%s" % each["salary"])
                print("  职位优势:%s" % each["positionAdvantage"])
                print("  公司全称:%s" % each["companyFullName"])
                print("  公司福利:%s" % each["companyLabelList"])
                print("  工作地区:%s" % each["district"])
                NO += 1
        elif 10 <= NO <= 99:
            for each in positions:
                writer.writerow((each["positionName"], each["salary"], each["positionAdvantage"],
                                 each["companyFullName"], each["district"]))
                print("%d.职位名称:%s" % (NO, each["positionName"]))
                print("   职位薪资:%s" % each["salary"])
                print("   职位优势:%s" % each["positionAdvantage"])
                print("   公司全称:%s" % each["companyFullName"])
                print("   公司福利:%s" % each["companyLabelList"])
                print("   工作地区:%s" % each["district"])
                NO += 1
        elif 100 <= NO <= 999:
            for each in positions:
                writer.writerow((each["positionName"], each["salary"], each["positionAdvantage"],
                                 each["companyFullName"], each["district"]))
                print("%d.职位名称:%s" % (NO, each["positionName"]))
                print("    职位薪资:%s" % each["salary"])
                print("    职位优势:%s" % each["positionAdvantage"])
                print("    公司全称:%s" % each["companyFullName"])
                print("    公司福利:%s" % each["companyLabelList"])
                print("    工作地区:%s" % each["district"])
                NO += 1

        content = json.dumps(positions, ensure_ascii=False)

        with open("content.json", "ab") as file:
            file.write(content.encode('utf-8'))
        file.close()

        if page != 30:
            print("第%d页爬取完毕!" % page)
            print("休眠30秒!\n")
            time.sleep(30)
        else:
            print("第%d页爬取完毕!" % page)
            print("爬取完毕!")

except:
    print("您的操作太频繁,请稍后再试!")
csvFile.close()
exit()
