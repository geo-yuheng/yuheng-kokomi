exception_status_code = {
    # System status
    "0x0000": {
        "en": "INFO: System is ready.\n",
        "zh": "信息：系统就绪。\n",
        "zh-MOE": "Kokomi就绪。\n",
    },
            
    "0x0001": {
        "en": "INFO: Define Overpass for Network successfully.\n",
        "zh": "信息：指定Overpass成功：\n  {name} {api}\n",
        "zh-MOE": "信息：已在海祇岛上建立珊瑚宫。（指定Overpass成功）：\n  {name} {api}\n",
    },
    
    "0x0010": {
        "en": "INFO: Searching in Overpass.\n",
        "zh": "信息：正在Overpass中搜索：",  # 下接http-request的地址
        "zh-MOE": "信息：Kokomi正在珊瑚宫（Overpass）翻箱倒柜：",
    },
    
    "0x0011": {
        "en": "INFO: Searching in Overpass ( {now} / {total} ):\n",
        "zh": "信息：正在Overpass中搜索（第 {now} 次/共 {total} 次）：",  # 下接http-request的地址
        "zh-MOE": "信息：Kokomi正在珊瑚宫（Overpass）翻箱倒柜（第 {now} 次/共 {total} 次）：",
    },
    
    "0x0012": {
        "en": "INFO: {number} {type}(s) have been found.\n",
        "zh": "信息：找到了 {number} 个 {type}。\n",
        "zh-MOE": "信息：Kokomi找到了 {number} 个 {type}。\n",
    },

    "0x1001": {
        "en": "WARN: Self-defined Overpass set.\n",
        "zh": "警告：你正在使用自定义的Overpass配置:\n  {name} {api}\n",
        "zh-MOE": "警示意义的：你正在使用自定义的珊瑚宫（Overpass）配置:\n  {name} {api}\n",
    },

    "0x2000": {
        "en": "ERROR: No Overpass info.\n",
        "zh": "错误：Overpass未指定。\n",
        "zh-MOE": "错误的：珊瑚宫（Overpass）未指定。\n",
    },
    
    "0x2001": {
        "en": "ERROR: Uncompleted Overpass set.\n",
        "zh": "错误：Overpass配置不完整。\n",
        "zh-MOE": "错误的：珊瑚宫（Overpass）配置不完整。\n",
    },
    
    "0x2002": {
        "en": "ERROR: Undefined Overpass preset.\n",
        "zh": "错误：没有定义的Overpass预设配置。\n",
        "zh-MOE": "错误的：没有定义的珊瑚宫（Overpass）预设配置。\n",
    },
    
    "0x2010": {
        "en": "ERROR: No info from Overpass.\n",
        "zh": "错误：Overpass没有回传任何信息。\n",
        "zh-MOE": "错误的：珊瑚宫（Overpass）没有回传任何信息。\n",
    },
    
    "0x2011": {
        "en": "",  # 超时
        "zh": "",
        "zh-MOE": "",
    },
    
    "0x201A": {
        "en": "ERROR: Undefined Feature type: {type}.\n",
        "zh": "错误：没有定义的要素类型：{type}。\n",
        "zh-MOE": "错误的：没有定义的锦囊（要素）类型：{type}。\n",
    },

    # Dataset
    "0x0100": {
        "en": "INFO: Dataset {set} is included.\n",  # include
        "zh": "信息：数据集"{set}"已加载。\n",
        "zh-MOE": "信息：「海染砗磲」"{set}"已装备。\n",
    },

    "0x1100": {
        "en": "WARN: Dataset with the same name {set} has been included and will be replaced.\n",  # include
        "zh": "警告：同名数据集"{set}"已存在，将被替换。",
        "zh-MOE": "警示意义的：同名「海染砗磲」"{set}"已存在，将被替换。",
    },
    
    "0x1114": {
        "en": "WARN: When there is id limitation in a Dataset, other limitations cannot function.\n",  # id
        "zh": "警告：使用id限定后，其他数据集条件无法生效。\n",
        "zh-MOE": "警示意义的：使用id限定后，其他「海染砗磲」条件无法生效。\n",
    },
    
    "0x11A0": {
        "en": "INFO: Dataset {set} uses data from an intersection of multiple Datasets.\n",  # convert
        "zh": "信息：所加载的数据集"{set}"使用了多个其他数据集的交集。\n",
        "zh-MOE": "信息：所装备的「海染砗磲」"{set}"使用了多个其他「海染砗磲」的交集。\n",
    },
    
    "0x11A1": {
        "en": "WARN: Bbox in set {set} is disabled due to it is not the main set in this query.\n",
        "zh": "警告：因为数据集"{set}"不是最外层语句，其界定框限制不生效。\n",
        "zh-MOE": "警示意义的：因为「海染砗磲」"{set}"不是最外层语句，其界定框限制不生效。\n",
    },

    "0x2104": {
        "en": "ERROR: Undefined key-value relation.\n",  # k_v
        "zh": "错误：未定义的键值关系。\n",
        "zh-MOE": "错误的：未定义的键值关系。\n",
    },
    
    "0x2105": {
        "en": "ERROR: Value needed except exist and !exist.\n",
        "zh": "错误：除exist、!exist条件外需要键的值。\n",
        "zh-MOE": "错误的：除exist、!exist条件外需要键的值。\n",
    },
    
    "0x2108": {
        "en": "ERROR: Not-included Dataset {set}.\n",  # around
        "zh": "错误：找不到数据集"{set}"。\n",
        "zh-MOE": "错误的：找不到「海染砗磲」"{set}"。\n",
    },
    
    "0x2109": {
        "en": "ERROR: Lat/lon-s not in pairs.\n",
        "zh": "错误：传入的点串线坐标[纬度1, 经度1, 纬度2, 经度2, ...]不成对。\n",
        "zh-MOE": "错误的：传入的点串线坐标[纬度1, 经度1, 纬度2, 经度2, ...]不成对。\n",
    },
    
    "0x210C": {
        "en": "ERROR: Not-included Dataset {set}.\n",  # set_from
        "zh": "错误：找不到数据集"{set}"。\n",
        "zh-MOE": "错误的：找不到「海染砗磲」"{set}"。\n",
    },
    
    "0x210D": {
        "en": "ERROR: Name list not made up with str.\n",
        "zh": "错误：传入名称列表包含非字符串元素。\n",
        "zh-MOE": "错误的：传入名称列表包含非字符串元素。\n",
    },
    
    "0x2110": {
        "en": "ERROR: Lat/lon-s not in pairs.\n",  # located_in
        "zh": "错误：传入的多边形坐标[纬度1, 经度1, 纬度2, 经度2, ...]不成对。\n",
        "zh-MOE": "错误的：传入的多边形坐标[纬度1, 经度1, 纬度2, 经度2, ...]不成对。\n",
    },
}

# 新的消息结构，使用描述性键名
messages = {
    "system": {
        "info": {
            "ready": exception_status_code["0x0000"],
            "overpass": {
                "defined": exception_status_code["0x0001"],
                "searching": exception_status_code["0x0010"],
                "searching.progress": exception_status_code["0x0011"],
            },
            "feature": {
                "found": exception_status_code["0x0012"],
            },
        },
        "warn": {
            "overpass": {
                "custom": exception_status_code["0x1001"],
            },
        },
        "error": {
            "overpass": {
                "missing": exception_status_code["0x2000"],
                "incomplete": exception_status_code["0x2001"],
                "preset": {
                    "undefined": exception_status_code["0x2002"],
                },
                "noinfo": exception_status_code["0x2010"],
                "timeout": exception_status_code["0x2011"],
            },
            "feature": {
                "type": {
                    "undefined": exception_status_code["0x201A"],
                },
            },
        },
    },
    "dataset": {
        "info": {
            "included": exception_status_code["0x0100"],
            "intersection": exception_status_code["0x11A0"],
        },
        "warn": {
            "replaced": exception_status_code["0x1100"],
            "id_limitation": exception_status_code["0x1114"],
            "bbox_disabled": exception_status_code["0x11A1"],
        },
        "error": {
            "key_value": {
                "undefined": exception_status_code["0x2104"],
                "value_needed": exception_status_code["0x2105"],
            },
            "not_found": {
                "around": exception_status_code["0x2108"],
                "set_from": exception_status_code["0x210C"],
            },
            "coordinates": {
                "not_in_pairs": {
                    "points": exception_status_code["0x2109"],
                    "polygon": exception_status_code["0x2110"],
                },
            },
            "name_list": {
                "invalid": exception_status_code["0x210D"],
            },
        },
    },
}

# 消息代码到消息键的映射
code_to_key = {
    "0x0000": "system.info.ready",
    "0x0001": "system.info.overpass.defined",
    "0x0010": "system.info.overpass.searching",
    "0x0011": "system.info.overpass.searching.progress",
    "0x0012": "system.info.feature.found",
    "0x1001": "system.warn.overpass.custom",
    "0x2000": "system.error.overpass.missing",
    "0x2001": "system.error.overpass.incomplete",
    "0x2002": "system.error.overpass.preset.undefined",
    "0x2010": "system.error.overpass.noinfo",
    "0x2011": "system.error.overpass.timeout",
    "0x201A": "system.error.feature.type.undefined",
    "0x0100": "dataset.info.included",
    "0x1100": "dataset.warn.replaced",
    "0x1114": "dataset.warn.id_limitation",
    "0x11A0": "dataset.info.intersection",
    "0x11A1": "dataset.warn.bbox_disabled",
    "0x2104": "dataset.error.key_value.undefined",
    "0x2105": "dataset.error.key_value.value_needed",
    "0x2108": "dataset.error.not_found.around",
    "0x2109": "dataset.error.coordinates.not_in_pairs.points",
    "0x210C": "dataset.error.not_found.set_from",
    "0x210D": "dataset.error.name_list.invalid",
    "0x2110": "dataset.error.coordinates.not_in_pairs.polygon",
}

def get_message(key, lang="en", **kwargs):
    """
    根据消息键获取消息
    
    参数:
        key (str): 消息键，例如 "system.info.ready"
        lang (str): 语言代码，默认为 "en"，可选值: "en", "zh", "zh-MOE"
        **kwargs: 格式化消息的参数
        
    返回:
        str: 格式化后的消息
    """
    keys = key.split(".")
    current = messages
    for k in keys:
        if k in current:
            current = current[k]
        else:
            return f"Message key not found: {key}"
    
    if isinstance(current, dict) and lang in current:
        message = current[lang]
        if kwargs:
            try:
                return message.format(**kwargs)
            except KeyError as e:
                return f"Missing format parameter: {e} for message: {message}"
        return message
    elif isinstance(current, str):
        # 向后兼容旧格式
        if kwargs:
            try:
                return current.format(**kwargs)
            except KeyError as e:
                return f"Missing format parameter: {e} for message: {current}"
        return current
    else:
        return f"Invalid message format for key: {key}"

def get_message_by_code(code, lang="en", **kwargs):
    """
    根据状态码获取消息
    
    参数:
        code (str): 状态码，例如 "0x0000"
        lang (str): 语言代码，默认为 "en"，可选值: "en", "zh", "zh-MOE"
        **kwargs: 格式化消息的参数
        
    返回:
        str: 格式化后的消息
    """
    if code in code_to_key:
        return get_message(code_to_key[code], lang, **kwargs)
    elif code in exception_status_code:
        # 向后兼容旧格式
        message = exception_status_code[code]
        if isinstance(message, dict) and lang in message:
            message = message[lang]
        if kwargs:
            try:
                return message.format(**kwargs)
            except KeyError as e:
                return f"Missing format parameter: {e} for message: {message}"
        return message
    else:
        return f"Unknown status code: {code}"