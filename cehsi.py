import requests
from lxml import etree
from lxml import html
import re
import openpyxl
import time


class ChangchunErshoufangInformation(object):
    def __init__(self):
        self.url = f"https://zz.ke.com/ershoufang/zhengzhoujingjijishukaifaqu/"
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
        sheet["E1"].value = "小区位置"
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
        sheet["W1"].value = "挂牌时间"
        sheet["X1"].value = "上次交易时间"
        sheet["Y1"].value = "小区介绍"
        sheet["Z1"].value = "周边配套"
        # sheet["a1"].value = "地理位置"

        column = 2

        for page in range(1, 101):
            print(f"正在获取第{page}页数据.")


            # time.sleep(3)

            resp = requests.get(self.url + f"pg{page}/", headers=self.header)

            main_tree = etree.HTML(resp.text)

            #TODO 获取当前页的所有房源信息
            house_url_list = main_tree.xpath("/html/body/div[1]/div[4]/div[1]/div[4]/ul//div[1]/div[1]/a/@href")


            ershoufang_result_src = []
            for src in house_url_list:
                ershoufang = src[18:28]
                if ershoufang == "ershoufang":  #TODO 将不是二手的信息 过滤掉
                    ershoufang_result_src.append(src)
                else:
                    continue
            print(f"第{page}页共有{len(ershoufang_result_src)}个数据.")


            #TODO 针对每个房源获取相应的信息
            for href in ershoufang_result_src:

                resp_two = requests.get(href)
                # tree_two = etree.HTML(resp_two.text)
                content = resp_two.content
                tree_two = html.fromstring(content)

                #TODO  1. 获取房源标题名称
                # title_l = tree_two.xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h1/@title")
                # title = title_l[0]

                #TODO  2. 获取房源总价
                price_l = tree_two.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[2]/div[2]/div/span[1]/text()')
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
                house_type_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()')
                house_type = ""
                for i in house_type_l:
                    house_type = str(house_type) + str(i)
                house_type = re.sub('\s+', '', house_type).strip()


                #TODO 8. 所在楼层
                house_flor_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()')
                house_flor = ""
                for i in house_flor_l:
                    house_flor = str(house_flor) + str(i)
                house_flor = re.sub('\s+', '', house_flor).strip()




                #TODO 9. 抵押信息
                house_pledge_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()')
                house_pledge = ""
                for i in house_pledge_l:
                    house_pledge = str(house_pledge) + str(i)
                house_pledge = re.sub('\s+', '', house_pledge).strip()
                # house_pledge = "None"





                #TODO 10. 交易权属
                house_power_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/text()')
                house_power =  ""
                for i in house_power_l:
                    house_power = str(house_power) + str(i)
                house_power = re.sub('\s+', '', house_power).strip()



                # #TODO 11. 房屋用途
                house_use_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/text()')
                house_use = ""
                for i in house_use_l:
                    house_use = str(house_use) + str(i)
                house_use = re.sub('\s+', '', house_use).strip()

                # #TODO  =============================新增==========================
                #TODO 12. 产权所属
                ower_use_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[6]/text()')
                ower_use = ""
                # ower_use_l = ower_use_l[0]
                for i in ower_use_l:
                    ower_use = str(ower_use) + str(i)
                ower_use = re.sub('\s+', '', ower_use).strip()


                #TODO 13. 房屋年限  是否满五
                house_time_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/text()')
                house_time = ""
                # house_time_l = house_time_l[0]
                for i in house_time_l:
                    house_time = str(house_time) + str(i)
                house_time = re.sub('\s+', '', house_time).strip()



                #TODO 14. 是否配备电梯
                house_elevator_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[12]/text()')
                house_elevator_ = ""
                for i in house_elevator_l:
                    house_elevator_ = str(house_elevator_) + str(i)
                house_elevator_ = re.sub('\s+', '', house_elevator_).strip()


                #TODO 15. 供暖方式  .....
                house_heating_method_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()')
                house_heating_method = ""
                for i in house_heating_method_l:
                    house_heating_method = str(house_heating_method) + str(i)
                house_heating_method = re.sub('\s+', '', house_heating_method).strip()


                #TODO 16. 梯户比
                house_ladder_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[10]/text()')
                house_ladder = ''
                for i in house_ladder_l:
                    house_ladder = str(house_ladder) + str(i)
                house_ladder = re.sub('\s+', '', house_ladder).strip()

                #TODO 17. 建筑结构
                building_structure_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[8]/text()')
                building_structure = ""
                for i in building_structure_l:
                    building_structure = str(building_structure) + str(i)
                building_structure = re.sub('\s+', '', building_structure).strip()

                # #TODO 18. 房屋朝向
                house_orientation_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[7]/text()')
                house_orientation = ''
                for i in house_orientation_l:
                    house_orientation = str(house_orientation) + str(i)
                house_orientation = re.sub('\s+', '', house_orientation).strip()

                #TODO 19. 装修情况
                house_condition_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()')
                # print(house_condition_l)
                house_condition = ""
                for i in house_condition_l:
                    house_condition = str(house_condition) + str(i)
                house_condition = re.sub('\s+', '', house_condition).strip()

                #TODO 20. 建筑类型
                building_type_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[4]/text()')
                building_type = ""
                for i in building_type_l:
                    building_type = str(building_type) + str(i)
                building_type = re.sub('\s+', '', building_type).strip()


                #TODO 21. 户型结构
                house_structure_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()')
                house_structure = ""
                for i in house_structure_l:
                    house_structure = str(house_structure) + str(i)
                house_structure = re.sub('\s+', '', house_structure).strip()

                #TODO 22. 建成年代
                house_Date_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[3]/div[3]/div[2]/text()")
                house_Date = ""
                for i in house_Date_l:
                    house_Date = str(house_Date) + str(i)
                house_Date = re.sub('\s+', '', house_Date).strip()


                #TODO 23. 挂牌时间
                Listing_time_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/text()')
                Listing_time = ""
                for i in Listing_time_l:
                    Listing_time = str(Listing_time) + str(i)
                Listing_time = re.sub('\s+', '', Listing_time).strip()


                #TODO 24. 上次交易时间
                Last_transaction_l = tree_two.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/text()')
                Last_transaction = ""
                for i in Last_transaction_l:
                    Last_transaction = str(Last_transaction) + str(i)
                Last_transaction = re.sub('\s+', '', Last_transaction).strip()


                #TODO 25. 小区介绍
                Community_introduction_l = tree_two.xpath('/html/body/div[1]/div[5]/div[3]/div[1]/div/div[3]/div[2]/text()')
                Community_introduction = ""
                for i in Community_introduction_l:
                    Community_introduction = str(Community_introduction) + str(i)
                Community_introduction = re.sub('\s+', '', Community_introduction).strip()

                #TODO 26. 周边配套
                Peripheral_facilities_l = tree_two.xpath('/html/body/div[1]/div[5]/div[3]/div[1]/div/div[5]/div[2]/text()')
                Peripheral_facilities = ""
                for i in Peripheral_facilities_l:
                    Peripheral_facilities = str(Peripheral_facilities) + str(i)
                Peripheral_facilities = re.sub('\s+', '', Peripheral_facilities).strip()

                #TODO 27. 小区位置
                Cell_location_l = tree_two.xpath('//*[@id="resblockCardContainer"]/div/div[1]/a/@href')
                Cell_location = ""
                for i in Cell_location_l:
                    Cell_location = str(Cell_location) + str(i)
                Cell_location = re.sub('\s+', '', Cell_location).strip()

                resp_two_ = requests.get(Cell_location)
                # tree_two = etree.HTML(resp_two.text)
                content = resp_two_.content
                respTwo = html.fromstring(content)

                Cell_location_ll = respTwo.xpath('//*[@id="beike"]/div[1]/div[2]/div[2]/div/div/div[1]/div/text()')
                cell_location = ""
                for i in Cell_location_ll:
                    cell_location = str(cell_location) + str(i)
                cell_location = re.sub('\s+', '', cell_location).strip()


                for cow in "ABCDEFGHIJKLMNOPQRSTUVWXYZa":
                    cell_name = str(cow) + str(column)
                    if cow == "A":
                        sheet[cell_name].value = xiaoqu
                    elif cow == "B":
                        sheet[cell_name].value = price
                    elif cow == "C":
                        sheet[cell_name].value = mean_price
                    elif cow == "D":
                        sheet[cell_name].value = acreage
                    elif cow == "E":
                        sheet[cell_name].value = cell_location
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
                        sheet[cell_name].value = ower_use

                    elif cow == "M":
                        sheet[cell_name].value = house_time

                    elif cow == "N":
                        if house_elevator_:
                            sheet[cell_name].value = house_elevator_
                        else:
                            sheet[cell_name].value = "没有"
                    elif cow == "O":
                        sheet[cell_name].value = house_heating_method
                    elif cow == "P":
                        sheet[cell_name].value = house_ladder

                    elif cow == "Q":
                        sheet[cell_name].value = building_structure

                    elif cow == "R":
                        sheet[cell_name].value = house_orientation
                    elif cow == "S":
                        sheet[cell_name].value = house_condition
                    elif cow == "T":
                        sheet[cell_name].value = building_type
                    elif cow == "U":
                        sheet[cell_name].value = house_structure
                    elif cow == "V":
                        sheet[cell_name].value = house_Date
                    elif cow == "W":
                        sheet[cell_name].value = Listing_time
                    elif cow == "X":
                        sheet[cell_name].value = Last_transaction
                    elif cow == "Y":
                        sheet[cell_name].value = Community_introduction
                    elif cow == "Z":
                        sheet[cell_name].value = Peripheral_facilities


                print(f"已经获取{column - 1}个数据")
                column += 1
            wb.save("./经开区_贝壳网二手房数据集_1-100页.xlsx")
            time.sleep(1)
        print("Done.")



if __name__ == '__main__':

    ChangchunErshoufangInformation().beike_information()



