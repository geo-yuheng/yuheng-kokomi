from typing import Union

import requests
import yuheng
from query_builder import QueryBuilder
from yuheng.method.network import get_endpoint_overpass

from .const import exception_status_code, get_message


class QueryClient:
    def __init__(self):
        self.energy = 50
        self.check_energy = 1
        self.directive_type = ["node", "way", "relation"]
        self.directive_dict = {"node": {}, "way": {}, "relation": {}}
        self.directive_text_temp = ""
        self.network_config = {"overpass_name": "", "overpass_api": ""}
        # overpass_name = Overpass_name, overpass_api = Overpass_api
        print(get_message("system.info.ready"))

    # 检查能量值
    def energy_check(self):
        if self.check_energy == 1 and self.energy <= 30:
            print("NOTICE: Now energy is low(", self.energy,
                  ") due to mass ERRORs.\n"
                  "    For not showing this message, please set check_energy as 0.\n"
                  "注意：发生的错误有点多，能量值较低。\n"
                  "    退订请设置check_energy为0。\n"
                  )

    # 恢复能量值
    def energy_restore(self):
        self.energy = self.energy + 4
        print("INFO: Energy value +4.\n")

    # 显示当前能量值
    def show_energy(self):
        print("INFO: Current energy value is", self.energy, ".\n")

    # 网络连接参数设置：指定查询的api参数。
    #   参数1为【预设名称，str】（"OSMde"、"OSMru"、"OGF"、"None"）：使用预设Overpass服务器配置，或不使用预设（"None"）；
    #   参数2为【自定名称，str】：参数1为"None"时，自定义Overpass服务器名称，默认为空；
    #   参数3为【自定API地址，str】：参数1为"None"时，自定义Overpass服务器API地址，填写至"interpreter?..."前，默认为空。
    # 返回int：
    #   【1】：成功使用预设配置；
    #   【0】：成功使用自定义配置；
    #   【-1】：使用了未定义的预设名称；
    #   【-2】：不完整的自定义配置。
    def network_config_set(self, preset: str, name: str = "", api: str = "") -> int:
        self.energy_check()
        network_config_list = {
            "OSMde": {
                "overpass_name": "OSMde",
                "overpass_api": get_endpoint_overpass(endpoint_name="osmde")
            },
            "OSMru": {
                "overpass_name": "OSMru",
                "overpass_api": get_endpoint_overpass(endpoint_name="osmru")
            },
            "OGF": {
                "overpass_name": "OGF",
                "overpass_api": get_endpoint_overpass(endpoint_name="ogf")
            }
        }
        if preset in network_config_list:
            self.network_config["overpass_name"] = network_config_list.get(preset)["overpass_name"]
            self.network_config["overpass_api"] = network_config_list.get(preset)["overpass_api"]
            print(get_message("system.info.overpass.defined", name=self.network_config["overpass_name"],
                                            api=self.network_config["overpass_api"]))
            self.energy = self.energy + 1
            return 1
        else:
            if preset == "None":
                if name != "" and api != "":
                    self.network_config["overpass_name"] = name
                    self.network_config["overpass_api"] = api
                    print(get_message("system.warn.overpass.custom", name=self.network_config["overpass_name"],
                                                api=self.network_config["overpass_api"]))
                    self.energy = self.energy + 0
                    return 0
                else:
                    print(get_message("system.error.overpass.incomplete"))
                    self.energy = self.energy - 2
                    return -2
            else:
                print(get_message("system.error.overpass.preset.undefined"))
                self.energy = self.energy - 1
                return -1

    # 查询要素：本次查询收到的报文将储存在临时变量（directive_text_temp）中，并调用get_directive_dict处理信息。
    #   参数1为【查询指令，str或QueryBuilder】：在Overpass查询的参数，默认为空str，其中：
    #       str：以"data="后开始，当然返回的报文也会告诉你不给东西查不到。
    #       QueryBuilder：传入一个查询构建器对象，并直接按照其中设置的条件查询
    #   参数2为【延时，int】：设置最大超时时长，默认为500。
    # 返回list，其中：
    #   第1项为int：总分割查询次数n；
    #   随后n项，每项均为int：每次查询结果：
    #   【2】：向Overpass成功地GET了报文；
    #   【-1】：Overpass没有传回任何消息，可能是网络连接原因；
    #   【-2】：Overpass api未指定。
    def query(self, query_info: Union[str, 'QueryBuilder'] = "", timeout: int = 500) -> list:
        self.energy_check()
        result_list = []
        if isinstance(query_info, str):
            print(get_message("system.info.overpass.searching"))
            result_list.append(1)
            result = self.get_content("data=[out:xml][timeout:" + str(timeout) + "];" + query_info + "out body;")
            result_list.append(result)
        else:
            query_list = query_info.convert()
            result_list.append(len(query_list))
            for x in range(len(query_list)):
                print(get_message("system.info.overpass.searching.progress", now=x+1, total=len(query_list)))
                result = self.get_content("data=[out:xml][timeout:" + str(timeout) + "];" + query_list[x] + "out body;")
                result_list.append(result)
        return result_list

    def get_content(self, query_info: str = ""):
        print(self.network_config["overpass_api"] + "interpreter?" + query_info, "\n")
        if self.network_config["overpass_api"] == "":
            print(get_message("system.error.overpass.missing"))
            self.energy = self.energy - 2
            return -2
        else:
            text_temp = requests.get(self.network_config["overpass_api"] + "interpreter?" + query_info).text
            if text_temp == "":
                print(get_message("system.error.overpass.noinfo"))
                self.energy = self.energy - 1
                return -1
            else:
                self.directive_text_temp = text_temp
                self.directive_dict["node"].update(self.get_directive_dict("node", text_temp))
                self.directive_dict["way"].update(self.get_directive_dict("way", text_temp))
                self.directive_dict["relation"].update(self.get_directive_dict("relation", text_temp))
                self.energy = self.energy + 2
                return 2

    # 要素报文分割：将指定类型每个要素的信息切开，放入dict中。
    #   参数1为【要素类型】（"node"、"way"、"relation"）：应当是点、线、关系的一种；
    #   参数2为【欲切割报文】：需要处理的报文，默认为空。
    # 返回dict，其中：
    #   {要素ID: {
    #       "type": 要素类型,
    #       "tag_dict": {键名: 值, ...},
    #       "member_dict": {成员类型 + ID: 角色, ...},
    #       "node_list": [ID1, ID2, ...],
    #       "text": 报文全文,
    #       "lon_lat": [经度, 纬度]
    #       },
    #   ...
    #   }。
    def get_directive_dict(self, directive_type: str, directive_text: str = ""):
        if directive_type in self.directive_type:
            directive_front = 0
            directive_behind = 0
            directive_found = 0
            directive_list = {}
            # 用behind作为start是说从上一个结束之后开始查下一个
            while directive_text.find("<" + directive_type, directive_behind) != -1:
                # 找报文开头结尾
                directive_front = directive_text.find("<" + directive_type, directive_behind)
                # 如果""/>"比"">"先来，那说明只有一行，结尾是"/>"（/>不取双引号"因为取id要用）
                if directive_text.find("/>", directive_front) < directive_text.find("\">", directive_front):
                    directive_behind = directive_text.find("/>", directive_front)
                else:  # 否则是很多行，结尾是"</" + directive_type + ">"
                    directive_behind = directive_text.find("</" + directive_type + ">", directive_front)
                dealt_text = directive_text[directive_front: directive_behind]
                directive_found = directive_found + 1

                # 找id
                id_front = dealt_text.find("id=\"") + 4
                id_behind = dealt_text.find("\"", id_front)
                directive_id = dealt_text[id_front:id_behind]
                # 点经纬度
                lon_lat_list = []
                if directive_type == "node":
                    lat_front = dealt_text.find("lat=\"") + 5
                    lat_behind = dealt_text.find("\"", lat_front)
                    directive_lat = dealt_text[lat_front:lat_behind]
                    lon_front = dealt_text.find("lon=\"") + 5
                    lon_behind = dealt_text.find("\"", lon_front)
                    directive_lon = dealt_text[lon_front:lon_behind]
                    lon_lat_list = [directive_lon, directive_lat]

                # 分割dealt_text
                line_front = 0
                line_behind = 0
                # line_found = 0
                tag_dict = {}
                member_dict = {}
                node_list = []
                while dealt_text.find(">\n", line_behind) != -1:
                    line_front = dealt_text.find(">\n", line_behind)
                    line_behind = dealt_text.find(">\n", line_front + 1)
                    line_text = dealt_text[line_front + 2:line_behind]
                    # print(line_text)
                    # line_found = line_found + 1

                    # 处理tag、member、nd
                    # TODO:可以使用directive_type判断？
                    if line_text.find("<tag") != -1:
                        line_key = line_text[
                                line_text.find("k=\"") + 3:line_text.find("\" ", line_text.find("k=\"") + 3)]
                        line_value = line_text[
                                    line_text.find("v=\"") + 3:line_text.find("\"/", line_text.find("k=\"") + 3)]
                        # print(line_key, line_value)
                        tag_dict.update({line_key: line_value})
                    if line_text.find("<member") != -1:
                        member_type = line_text[line_text.find("type=\"") + 6
                                                :line_text.find("\" ", line_text.find("type=\"") + 6)]
                        member_ref = line_text[line_text.find("ref=\"") + 5
                                            :line_text.find("\" ", line_text.find("ref=\"") + 5)]
                        member_role = line_text[line_text.find("role=\"") + 6
                                                :line_text.find("\"/", line_text.find("role=\"") + 6)]
                        # print(member_type, member_ref, member_role)
                        member_dict.update({member_type + member_ref: member_role})
                    if line_text.find("<nd") != -1:
                        node_ref = line_text[line_text.find("ref=\"") + 5
                                            :line_text.find("\"/", line_text.find("ref=\"") + 5)]
                        # print(node_ref)
                        node_list.append(node_ref)

                # 准备返回的dict的子项
                directive = {"type": directive_type,
                            "tag_dict": tag_dict,
                            "member_dict": member_dict,
                            "node_list": node_list,
                            "text": dealt_text,
                            "lon_lat": lon_lat_list
                            }
                directive_list.update({directive_id: directive})

            # 结束
            print(get_message("system.info.feature.found", number=directive_found, type=directive_type))
            self.energy = self.energy + 1
            return directive_list
        else:
            print(get_message("system.error.feature.type.undefined", type=directive_type))
            self.energy = self.energy - 1
            return {}