import copy
from typing import Union

from .const import exception_status_code

# 要按照type.A(other_condition)[k_v](if)->.B;>;的顺序和结构去整理
# TODO:不需要改变输入输出集时只需要一句话，需要怎么判断？


# 查询构建器：构建查询要素的条件，条件取上名称后就代表符合该条件的要素集。
class QueryBuilder:
    def __init__(self, nwr_type: str):
        self.__include_dict = {}
        self.__from_query_builder_list = (
            []
        )  # or列表，列表元素若是列表，则其为and
        self.__main_type = nwr_type
        self.__kv_dict = {}
        self.__around_dict = {}
        self.__global_bbox_list = []  # 南、西、北、东
        self.__id_dict = {}
        self.__recurse_dict = {}
        self.__located_in_list = []

    # 键值关系限制语句：限定查询主体的key与value。
    #   参数1为【限定键，str】：限定必须出现或有对应值要求的键；
    #   参数2为【限制关系，str】（"exist"、"!exist"、"="、"!="、"=!="、"v-reg"、"!v-reg"、"kv-reg"、"v-Aa_no_care"）：限定键值之间的关系；
    #   参数3为【限定值，str】：对限定键的值的要求，默认为空str
    # 返回QueryBuilder：
    #   如果成功，则返回已经追加限制语句的QueryBuilder；否则原样不动地返回。
    def key_value(
        self, key: str, relation: str, value: str = ""
    ) -> "QueryBuilder":
        relation_list = [
            "exist",
            "!exist",
            "=",
            "!=",
            "=!=",
            "v-reg",
            "!v-reg",
            "kv-reg",
            "v-Aa_no_care",
        ]
        # 存在key（value可不填）、不存在key、存在key且对应value匹配、存在key但对应value不匹配或不存在key、必须存在key但对应value不匹配，
        # v可含正则表达式、v可含正则表达式但不匹配、kv皆可含正则表达式，v可含正则表达式且不分大小写
        if relation in relation_list:
            if relation not in ["exist", "!exist"] and value == "":
                print(exception_status_code[0x2105])
                return self
            else:
                self.__kv_dict.update(
                    {key: {"value": value, "relation": relation}}
                )
                return self
        else:
            print(exception_status_code[0x2104])
            return self

    # 周边检索：查询特定要素周边指定半径的内容。
    #   参数1为【中心要素，str或list】：检索周边的圆心：
    #       str：中心要素集的名称，将检索其中各要素周边指定半径的内容；
    #       list：由一串经纬度对组成的偶数项列表，形如[纬度1, 经度1, 纬度2, 经度2, ...]，表示各经纬度对组成的点构成的线段，将检索其周边指定半径的内容，其中：
    #           第2n-1项为float、int或str：第n个点的纬度；
    #           第2n项为float、int或str：第n个点的经度；
    #   参数2为【半径，int】：周边检索的半径，单位为米；
    # 返回QueryBuilder：
    #   如果成功，则返回已经追加限制语句的QueryBuilder；否则原样不动地返回。
    def around(self, set_point: Union[str, list], r: int) -> "QueryBuilder":
        # 要素集合
        if isinstance(set_point, str):
            if (set_point not in self.__include_dict) and (set_point != "_"):
                print(exception_status_code[0x2108].format(set=set_point))
            else:
                self.__around_dict = {set_point: r}
        # 点串线
        else:
            if len(set_point) % 2 != 0:
                print(exception_status_code[0x2109])
            else:
                self.__around_dict = {r: set_point}
        return self

    # 从查询构建器提取：从满足其他查询构建器的内容中进一步查询。
    #   参数1为【中心要素，str或list】：查询构建器：
    #       str：或查询（并集），单次使用本方法时输入一个集合，通过连续使用数次本方法达到从多个查询构建器的并集提取；
    #       list：和查询（交集），由数个查询构建器名称组成的列表，列表内的查询构建器需要同时满足，呈交集；
    #             输入的列表与其他使用本方法输入的查询构建器呈并集，其中：
    #           每一项均为str：需要同时满足的查询构建器名称；
    # 返回QueryBuilder：
    #   如果成功，则返回已经追加限制语句的QueryBuilder；否则原样不动地返回。
    def set_from(self, set_name: Union[str, list]) -> "QueryBuilder":
        if isinstance(set_name, str):
            if (set_name in self.__include_dict) or (set_name == "_"):
                self.__from_query_builder_list.append(set_name)
            else:
                print(exception_status_code[0x210C].format(set=set_name))
        else:
            and_list = []
            for x in set_name:
                if isinstance(x, str):
                    if (x in self.__include_dict) or (x == "_"):
                        and_list.append(x)
                    else:
                        print(
                            exception_status_code[0x210C].format(set=set_name)
                        )
                else:
                    print(exception_status_code[0x210D])
            if len(and_list) > 0:
                self.__from_query_builder_list.append(and_list)
        return self

    def set_bbox(
        self, E: float, S: float, W: float, N: float
    ) -> "QueryBuilder":
        self.__global_bbox_list = [S, W, N, E]
        return self

    def extend(
        self, direction: str, set_name: str = "_"
    ) -> "QueryBuilder":  # recurse
        self.__recurse_dict.update({set_name: direction})
        return self

    def id(
        self, directive_id: Union[int, str, list], id_opreation: str = "="
    ) -> "QueryBuilder":
        if isinstance(directive_id, list):
            for x in range(len(directive_id)):
                self.__id_dict.update({str(directive_id[x]): id_opreation})
        else:
            self.__id_dict.update({str(directive_id): id_opreation})
        print(exception_status_code[0x1114])
        return self

    # 在多边形中（poly）
    def located_in(self, poly_list: list) -> "QueryBuilder":
        if len(poly_list) % 2 != 0:
            print(exception_status_code[0x2110])
        else:
            self.__located_in_list = poly_list
        return self

    def include_query_builder(
        self, set_name: str, the_set: "QueryBuilder"
    ) -> "QueryBuilder":
        if set_name in self.__include_dict:
            print(exception_status_code[0x1100].format(set=set_name))
        self.__include_dict.update({set_name: the_set})
        print(exception_status_code[0x0100].format(set=set_name))
        return self

    # TODO:判断要几个查询，并把要查询的内容返回出去，以便外部查询，step=已经进行了几步，不重复执行
    def how_many_query(self, step: int = 0) -> list:
        # TODO:添加flag_dict以便本地筛选
        query_list = []
        # id是否需要多次查询：如果又有等号也有><，则><部分不索引id，下载完后交给客户端筛选
        if step == 0:
            if self.__id_dict:
                id_eq = []
                id_big = []
                id_sml = []  # 不能连等
                for directive_id in self.__id_dict:
                    match self.__id_dict[directive_id]:
                        case "=":
                            id_eq.append(directive_id)
                        case ">":
                            id_big.append(directive_id)
                        case "<":
                            id_sml.append(directive_id)
                        case _:
                            id_eq.append(directive_id)
                if len(id_eq) > 0:
                    sub_query_builder_eq = copy.deepcopy(self)
                    new_id_dict = {}
                    for x in id_eq:
                        new_id_dict.update({x: "="})
                    sub_query_builder_eq.__id_dict = new_id_dict
                    query_list.extend(sub_query_builder_eq.how_many_query(1))
                if len(id_big) > 0:
                    sub_query_builder_big = copy.deepcopy(self)
                    new_id_dict = {}
                    for x in id_big:
                        new_id_dict.update({x: ">"})
                    sub_query_builder_big.__id_dict = new_id_dict
                    query_list.extend(sub_query_builder_big.how_many_query(1))
                if len(id_sml) > 0:
                    sub_query_builder_sml = copy.deepcopy(self)
                    new_id_dict = {}
                    for x in id_sml:
                        new_id_dict.update({x: "<"})
                    sub_query_builder_sml.__id_dict = new_id_dict
                    query_list.extend(sub_query_builder_sml.how_many_query(1))
                # print("第0步完成")
            else:
                query_list.extend(self.how_many_query(1))
        # set_from：长度>1就要拆开
        if step == 1:
            if len(self.__from_query_builder_list) > 1:
                # and交集要合成一个query，or每个自己分别query：[A, B, [C,D]] = A ∪ B ∪ (C ∩ D)
                for from_query_builder in self.__from_query_builder_list:
                    sub_query_builder_from = copy.deepcopy(self)
                    sub_query_builder_from.__from_query_builder_list = [
                        from_query_builder
                    ]
                    query_list.extend(sub_query_builder_from.how_many_query(2))
            else:
                query_list.extend(self.how_many_query(2))
                # print("第1步完成")
        if step == 2:  # 目前是最后一步
            query_list.append(self)
        return query_list

    # 仅在输出时指定的要素集名称（"...->.set_name"）；有引用的情况下，输出本查询构建器时可在声明引用阶段一层一层往回带；
    # 输出QL语句列表
    def convert(
        self, set_name: str = "", if_main: bool = True, outputed_list=None
    ) -> list:
        # 如果这个是主语句，最外层的，那么outputed列表应该清空
        if outputed_list is None:
            outputed_list = []
        result = ""
        # 预先处理引用
        # TODO:引用部分能不能只输出后面用了的？
        include_info = ""
        outputed = outputed_list
        for include in self.__include_dict:
            # 先把引用的"...->.set_name;"输出了，后使用set_name时名称就是一致的，然后内容也对的上（递归）
            # 如果事先已经打印了，就不重复打印，防止A->B;A,B->C中打印两次A
            if include not in outputed:
                # TODO:converted_list = ...；暂时先全部放一起，前置条件要不要分开怎么分开再想想
                for x in self.__include_dict[include].convert(
                    include, False, outputed
                ):
                    include_info += x
                # 合并how_many_query()至convert前：result += self.__include_dict[include].convert(include, False, outputed)
                outputed.append(include)
                # print("INFO: QueryBuilder " + include + " is printed.\n信息：所装备的查询构建器"" + include + ""已打印。\n")
        # 正式数据开始：先how_many_query()确定要几次查询
        query_list = self.how_many_query()
        result_list = []
        for each_query in query_list:
            # 每次都重置为只有include信息的，否则原来写在上面for循环之后只执行一次的话输出的内容会重复：
            # 就像这样：第一次查询include_info;node.A["name"]; 第二次include_info;node.A["name"];node.B["name"];
            result = include_info
            # 类型
            result += each_query.__main_type
            # id（使用「=」限制）
            # TODO：如果又有等号也有>< -> 这里不处理了，交给客户端本地筛选，预留flag位
            if each_query.__id_dict:
                id_info = ""
                eq_id_list = []
                for directive_id in each_query.__id_dict:
                    if each_query.__id_dict[directive_id] == "=":
                        eq_id_list.append(directive_id)
                if len(eq_id_list) > 0:
                    id_info = "(id:"
                    for x in range(len(eq_id_list) - 1):
                        id_info += str(eq_id_list[x]) + ","
                    id_info += str(eq_id_list[-1]) + ")"
                result += id_info
                # 有id限制时其他无法生效，直接处理集合并结束
                if set_name != "":
                    result += "->." + set_name
                result += ";"
                result_list.append(result)
                continue
            # .from_other_set
            if each_query.__from_query_builder_list:
                for from_query_builder in each_query.__from_query_builder_list:
                    if isinstance(from_query_builder, str):
                        result += "." + from_query_builder
                    else:
                        if len(from_query_builder) > 1:
                            print(
                                exception_status_code[0x11A0].format(
                                    set=(
                                        set_name
                                        if set_name != ""
                                        else "default"
                                    )
                                )
                            )
                        for x in from_query_builder:
                            result += "." + x
            # around
            if each_query.__around_dict:
                around_info = ""
                for around in each_query.__around_dict:
                    # 要素集{set_point: r}；点串线{r: set_point}
                    if isinstance(around, str):
                        around_info += (
                            "(around."
                            + around
                            + ":"
                            + str(each_query.__around_dict[around])
                            + ")"
                        )
                    else:
                        around_info += "(around" + ":" + str(around)
                        for point in each_query.__around_dict[around]:
                            around_info += "," + str(point)
                        around_info += ")"
                result += around_info
            # poly
            if each_query.__located_in_list:
                poly_info = '(poly:"'
                for x in range(len(each_query.__located_in_list) - 1):
                    poly_info += str(each_query.__located_in_list[x]) + " "
                poly_info += (
                    str(
                        each_query.__located_in_list[
                            len(each_query.__located_in_list) - 1
                        ]
                    )
                    + '")'
                )
            # k_v
            limit_info = ""
            for key in each_query.__kv_dict:
                value = each_query.__kv_dict[key].get("value")
                match each_query.__kv_dict[key].get("relation"):
                    case "exist":  # 存在key（value可不填）
                        now_info = '["' + key + '"]'
                    case "!exist":  # 不存在key
                        now_info = '[!"' + key + '"]'
                    case "=":  # 存在key且对应value匹配
                        now_info = '["' + key + '"' + '="' + value + '"]'
                    case "!=":  # 存在key但对应value不匹配 或 不存在key
                        now_info = '["' + key + '"' + '!="' + value + '"]'
                    case "=!=":  # 必须存在key但对应value不匹配
                        now_info = (
                            '["' + key + '"]["' + key + '"!="' + value + '"]'
                        )
                    case "v-reg":  # v可含正则表达式
                        now_info = '["' + key + '"~"' + value + '"]'
                    case "!v-reg":  # v可含正则表达式但不匹配
                        now_info = '["' + key + '"!~"' + value + '"]'
                    case "kv-reg":  # kv皆可含正则表达式
                        now_info = '[~"' + key + '"~"' + value + '"]'
                    case "v-Aa_no_care":  # v可含正则表达式且不分大小写
                        now_info = '[~"' + key + '"~"' + value + '",i]'
                    case _:
                        now_info = ""
                limit_info += now_info
            result += limit_info
            # 全局界定框
            if each_query.__global_bbox_list:
                if not if_main:
                    # TODO:这个判断需要吗？
                    print(exception_status_code[0x11A1].format(set_name))
                else:
                    bbox_info = "(bbox:"
                    for x in range(3):
                        bbox_info += (
                            str(each_query.__global_bbox_list[x]) + ","
                        )
                    bbox_info += str(each_query.__global_bbox_list[3]) + ")"
                    result += bbox_info
            # ->.set
            if set_name != "":
                result += "->." + set_name
            result += ";"
            # extend(recurse)
            recurse_info = ""
            if self.__recurse_dict:
                for recurse in self.__recurse_dict:
                    recurse_info += (
                        "." + recurse + self.__recurse_dict[recurse] + ";"
                    )
            result += recurse_info
            # 结束
            result_list.append(result)
        return result_list