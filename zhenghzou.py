import requests
from lxml import etree
import re
import openpyxl
import time


class ChangchunErshoufangInformation(object):
    def __init__(self):
        self.url = f"https://zz.ke.com/ershoufang/zhengdongxinqu/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        #todo  新增信息：
        self.proxies = [
            {'http': 'http://proxy1.example.com:1234', 'https': 'https://proxy1.example.com:1234'},
            {'http': 'http://proxy2.example.com:5678', 'https': 'https://proxy2.example.com:5678'},
        ]

    def beike_information(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet["A1"].value = "小区名称"
        sheet["B1"].value = "总价"
        sheet["C1"].value = "元/平米"
        sheet["D1"].value = "房屋面积"
        # sheet["E1"].value = "小区名称"
        sheet["F1"].value = "所在区域"
        sheet["G1"].value = "房屋类型"
        sheet["H1"].value = "房屋楼层"
        sheet["I1"].value = "抵押信息"
        sheet["J1"].value = "交易权属"
        sheet["K1"].value = "房屋用途"
        sheet["L1"].value = "产权所属"
        sheet["M1"].value = "房屋买房年限"
        sheet["N1"].value = "是否配备电梯"
        sheet["O1"].value = "供暖方式"
        sheet["P1"].value = "梯户比"
        sheet["Q1"].value = "建筑结构"
        sheet["R1"].value = "房屋朝向"
        sheet["S1"].value = "装修情况"
        sheet["T1"].value = "建筑类型"
        sheet["U1"].value = "户型结构"
        sheet["V1"].value = "建成年代"

        column = 2
        for page in range(1, 2):
            print(f"正在获取第{page}页数据.")

            ershoufang_result_src = []
            # time.sleep(3)

            resp = requests.get(self.url + f"pg{page}/", headers=self.header)
            main_tree = etree.HTML(resp.text)

            #TODO 获取当前页的所有房源信息
            house_url_list = main_tree.xpath("/html/body/div[1]/div[4]/div[1]/div[4]/ul//div[1]/div[1]/a/@href")

            for src in house_url_list:
                ershoufang = src[18:28]
                if ershoufang == "ershoufang":  #TODO 将不是二手的信息 过滤掉
                    ershoufang_result_src.append(src)
                else:
                    continue
            print(f"第{page}页共有{len(ershoufang_result_src)}个数据.")


            #TODO 针对每个房源获取相应的信息
            for href in ershoufang_result_src:
                time.sleep(3)
                resp_two = requests.get(href)
                tree_two = etree.HTML(resp_two.text)

                #TODO  1. 获取房源标题名称
                title_l = tree_two.xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h1/@title")
                title = title_l[0]

                #TODO  2. 获取房源总价
                price_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div/span[1]/text()")
                price = price_l[0] + "万"


                # TODO  3. 获取房源单价
                mean_price_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span/text()")
                mean_price = mean_price_l[0] + "元/平米"

                #TODO 4. 房屋面积
                acreage_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[3]/div[3]/div[1]/text()")
                acreage = acreage_l[0]

                #TODO 5. 小区名称
                xiaoqu_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[4]/div[1]/a[1]/text()")
                xiaoqu = xiaoqu_l[0]

                #TODO 6. 房屋所在区域
                area_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[4]/div[2]/span[2]/a[1]/text()")
                area = area_l[0]


                #TODO 7. 房屋户型
                house_type_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[1]/text()")
                house_type = ""
                for i in house_type_l:
                    house_type = str(house_type) + str(i)
                house_type = re.sub('\s+', '', house_type).strip()


                print(house_type_l,'ssss')



                #TODO 8. 所在楼层
                house_flor_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[5]/text()")
                house_flor = ""
                for i in house_flor_l:
                    house_flor = str(house_flor) + str(i)
                house_flor = re.sub('\s+', '', house_flor).strip()



                #TODO 9. 抵押信息
                house_pledge_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/ul/li[7]/span[1]/text()")
                house_pledge = ""
                for i in house_pledge_l:
                    house_pledge = str(house_pledge) + str(i)
                house_pledge = re.sub('\s+', '', house_pledge).strip()
                # house_pledge = "None"

                #TODO 10. 交易权属
                house_power = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/ul/li[2]/text()")
                # house_power =  house_power_l[0]
                #
                # #TODO 11. 房屋用途
                house_use = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/ul/li[4]/text()")
                # house_use = house_use_l[0]



                # #TODO  =============================新增============
                #
                #TODO 12. 产权所属
                ower_use_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/ul/li[6]/span/text()")
                # ower_use_l = ower_use_l[0]

                #TODO 13. 房屋年限  是否满五
                house_time_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/ul/li[5]/text()")
                # house_time_l = house_time_l[0]


                #TODO 14. 是否配备电梯
                house_elevator_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[12]/span/text()")
                # house_elevator_l = house_elevator_l[0]

                #TODO 15. 供暖方式  .....
                house_heating_method_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[11]/span/text()")
                house_heating_method_l = house_heating_method_l[0]


                #TODO 16. 梯户比
                house_ladder_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[10]/span/text()")
                house_ladder_l = house_ladder_l[0]

                #TODO 17. 建筑结构
                building_structure_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[8]/span/text()")
                building_structure_l = building_structure_l[0]

                # #TODO 18. 房屋朝向
                house_orientation_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[7]/text()")
                # house_orientation_l = re.sub('\s+', '', house_orientation_l[0]).strip()
                print(house_orientation_l)
                house_orientation_l = house_orientation_l[0].strip()


                #TODO 19. 装修情况
                house_condition_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[9]/span/text()")
                # print(house_condition_l)
                house_condition_l = house_condition_l[0]


                #TODO 20. 建筑类型
                house_type_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[4]/span/text()")
                house_type_l = house_type_l[0]

                #TODO 21. 户型结构
                house_structure_l = tree_two.xpath("/html/body/div[1]/div[5]/div[2]/div/div/div[1]/div[2]/ul/li[3]/span/text()")
                house_structure_l = house_structure_l[0]

                #TODO 22. 建成年代
                house_Date_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[3]/div[3]/div[2]/text()")
                house_Date_l = house_Date_l[0]


                for cow in "ABCDEFGHIJKLMNOPQRSTUV":
                    cell_name = str(cow) + str(column)
                    if cow == "A":
                        pass
                        # sheet[cell_name].value = xiaoqu
                    elif cow == "B":
                        sheet[cell_name].value = price
                    elif cow == "C":
                        sheet[cell_name].value = mean_price
                    elif cow == "D":
                        sheet[cell_name].value = acreage
                    elif cow == "E":
                        sheet[cell_name].value = xiaoqu
                    elif cow == "F":
                        sheet[cell_name].value = area
                    elif cow == "G":
                        sheet[cell_name].value = house_type
                    elif cow == "H":
                        sheet[cell_name].value = house_flor
                    elif cow == "I":
                        sheet[cell_name].value = house_pledge

                    elif cow == "J":
                        sheet[cell_name].value = house_power
                    elif cow == "K":
                        sheet[cell_name].value = house_use
                    elif cow == "L":
                        sheet[cell_name].value = ower_use_l


                    elif cow == "M":
                        sheet[cell_name].value = house_time_l

                    elif cow == "N":
                        sheet[cell_name].value = house_elevator_l

                    elif cow == "O":
                        sheet[cell_name].value = house_heating_method_l
                    elif cow == "P":
                        sheet[cell_name].value = house_ladder_l


                    elif cow == "Q":
                        sheet[cell_name].value = building_structure_l

                    elif cow == "R":
                        sheet[cell_name].value = house_orientation_l
                    elif cow == "S":
                        sheet[cell_name].value = house_condition_l
                    elif cow == "T":
                        sheet[cell_name].value = house_type_l
                    elif cow == "U":
                        sheet[cell_name].value = house_structure_l
                    elif cow == "V":
                        sheet[cell_name].value = house_Date_l


                print(f"已经获取{column - 1}个数据")
                column += 1
            wb.save("./郑东新区_贝壳网二手房数据集_1-100页.xlsx")
            time.sleep(2)
        print("Done.")


if __name__ == '__main__':
    ChangchunErshoufangInformation().beike_information()
