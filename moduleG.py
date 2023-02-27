import math
import re
import time
from collections import defaultdict
from typing import Optional, Any
from graph_tool.topology import all_paths
import numpy as np
import graph_tool.all as gt

reverse_map = defaultdict(lambda: {})


"""
    Statistical Indicator
"""


def merge_same_node(nparray: np.array, is_in: bool=True):

    """Function: Merge the edge with the same input and output node
    param:
        -nparray: The edge with nparray format
        -is_in: Check if it is input edge (default to True)
                If it is true that is input edge
                Else, it is output edge
    """
    
    if is_in:
        flag = 0
        return np.array([[v, nparray[0][1], np.sum(nparray[nparray[:, flag]==v][:, 2])]for v in set(nparray[:, flag])])
    else:
        flag = 1
        return np.array([[nparray[0][0], v, np.sum(nparray[nparray[:, flag]==v][:, 2])]for v in set(nparray[:, flag])])


"""
    Pure Amount Indicator (PAI)
"""


def module_11311(graph: gt.Graph, address: str):
    
    """Compute the total input/output token amount
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    in_num, out_num = 0, 0
    address_index = reverse_map["account_dict"][address]
    in_edges = graph.get_in_edges(address_index, [graph.ep["value"]])
    out_edges = graph.get_out_edges(address_index, [graph.ep["value"]])

    for in_edge in in_edges:
        temp = in_edge[2]
        in_num += temp
    for out_edge in out_edges:
        temp = out_edge[2]
        out_num += temp
    return in_num, out_num


def module_11312(graph: gt.Graph, address: str):

    """Compute the difference of [input token amount] and [output token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    list_address = module_11311(graph, address)
    diff = list_address[1] - list_address[0]
    return diff


def module_11313(graph: gt.Graph, address: str):
    
    """Compute the ratio of [total input token amount] and [total output token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    list_address = module_11311(graph, address)
    ratio = (list_address[1] / list_address[0]) if list_address[0] else None  
    return ratio


def module_11314(graph: gt.Graph, address: str, flag_repeat: bool=True):

    """Compute the maximum/minimum value of the input/output token amount
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge 
    """
    
    address_index = reverse_map["account_dict"][address]
    in_edges = graph.get_in_edges(address_index, [graph.ep["value"]])
    out_edges = graph.get_out_edges(address_index, [graph.ep["value"]])
    if flag_repeat is not True:
        in_edges = merge_same_node(in_edges, is_in=True)
        out_edges = merge_same_node(out_edges, is_in=False)
    in_min = (np.min(in_edges, 0))[2] if in_edges.__len__() != 0 else 0
    in_max = (np.max(in_edges, 0))[2] if in_edges.__len__() != 0 else 0
    out_min = (np.min(out_edges, 0))[2] if out_edges.__len__() != 0 else 0
    out_max = (np.max(out_edges, 0))[2] if out_edges.__len__() != 0 else 0
    return in_min, in_max, out_min, out_max


def module_11315(graph: gt.Graph, address: str, flag_repeat: bool=True):
    
    """Compute the difference of the input/output [maximum token amount] and [minimum token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge 
    """
    
    num = module_11314(graph, address, flag_repeat)
    in_diff = num[1] - num[0]
    out_diff = num[3] - num[2]
    return in_diff, out_diff


def module_11316(graph: gt.Graph, address: str, flag_repeat: bool=True):
    
    """Compute the ratio of [input/output difference from module_11315] and [total input/output token amount] 
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge 
    """
    
    diff = module_11315(graph, address, flag_repeat=flag_repeat)
    num = module_11311(graph, address)
    in_ratio = None if num[0] == 0 else round(diff[0] / num[0], 6)
    out_ratio = None if num[1] == 0 else round(diff[1] / num[1], 6)
    return in_ratio, out_ratio


def module_11317(graph: gt.Graph, address: str, flag_repeat: bool=True):
    
    """Compute the standard deviation of the input/output/input and output token amount
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    address_index = reverse_map["account_dict"][address]
    in_edges = graph.get_in_edges(address_index, [graph.ep["value"]])
    out_edges = graph.get_out_edges(address_index, [graph.ep["value"]])
    if flag_repeat is not True:
        in_edges = merge_same_node(in_edges, is_in=True)
        out_edges = merge_same_node(out_edges, is_in=False)
        if in_edges.size > 0:
            if out_edges.size > 0:
                all_edges = np.append(in_edges, out_edges, axis=0)
            else:
                all_edges = in_edges
        else:
            all_edges = out_edges   
    else:
        all_edges = graph.get_all_edges(address_index, [graph.ep["value"]])
    in_std = (np.std(in_edges, axis=0))[2] if in_edges.any() else None
    out_std = (np.std(out_edges, axis=0))[2] if out_edges.any() else None
    all_std = (np.std(all_edges, axis=0))[2] if all_edges.any() else None
    return in_std, out_std, all_std


def module_1132(graph: gt.Graph, address: str, flag_repeat: bool=True):
    
    """Compute the ratio of [every input/output token amount] and [total input/output token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    num = module_11311(graph, address)
    address_index = reverse_map["account_dict"][address]
    in_stats, out_stats = {}, {}
    in_edges = graph.get_in_edges(address_index, [graph.ep["value"]])
    out_edges = graph.get_out_edges(address_index, [graph.ep["value"]])
    if flag_repeat is not True:
        in_edges = merge_same_node(in_edges, is_in=True)
        out_edges = merge_same_node(out_edges, is_in=False)
    for flag_in, in_edge in enumerate(in_edges):
        in_ratio = round(in_edge[2] / num[0], 5) if num[0] else None
        in_stats[flag_in] = in_edge[0], in_edge[1], in_edge[2], in_ratio
    for flag_out, out_edge in enumerate(out_edges):
        out_ratio = round(out_edge[2] / num[1], 5) if num[1] else None
        out_stats[flag_out] = out_edge[0], out_edge[1], out_edge[2], out_ratio
    in_ratio, out_ratio = [], []
    for stats in in_stats:
        in_ratio.append(in_stats[stats][3])
    for stats in out_stats:
        out_ratio.append(out_stats[stats][3])
    return in_ratio, out_ratio


def module_11321(graph: gt.Graph, address: str, flag_repeat: bool=True):

    """Compute the ratio of [input/output maximum/minimum token amount] and [total input/output token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    in_ratio,out_ratio = module_1132(graph, address, flag_repeat)
    return min(in_ratio) if in_ratio else None, max(in_ratio) if in_ratio else None, min(out_ratio) if out_ratio else None, max(out_ratio) if out_ratio else None


def module_11322(graph: gt.Graph, address: str, flag_repeat: bool=True):

    """Compute the standard deviation of the ratio of [input/output token amount] and [total input/output token amount]
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -flag_repeat: Check if preserving the repeat situation (default to True)
                      If it is true, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    in_ratio,out_ratio = module_1132(graph, address, flag_repeat)
    return np.std(in_ratio) if in_ratio else None, np.std(out_ratio) if out_ratio else None


"""
    Pure Degree Indicator (PDI)
"""


def module_1231(graph, address: str, drop_duplicated=False):
    
    """Obtain the in-degree/out-degree/total degree of the Bitcoin address
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -drop_duplicated: Check if preserving the repeat situation (default to False)
                      If it is False, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    if drop_duplicated:
        in_degree = [
            in_neighbor for in_neighbor in address_vertex.in_neighbors()
        ].__len__()
        out_degree = [
            out_neighbor for out_neighbor in address_vertex.out_neighbors()
        ].__len__()
        all_degree = [
            all_neighbor for all_neighbor in address_vertex.all_neighbors()
        ].__len__()
    else:
        in_degree = [in_edge
                     for in_edge in address_vertex.in_edges()].__len__()
        out_degree = [out_edge
                      for out_edge in address_vertex.out_edges()].__len__()
        all_degree = [all_edge
                      for all_edge in address_vertex.all_edges()].__len__()
    return in_degree, out_degree, all_degree


def module_12311(graph, address: str, drop_duplicated=False):

    """Compute the ratio of [in-degree/out-degree] and [the total degree]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -drop_duplicated: Check if preserving the repeat situation (default to False)
                      If it is False, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    in_degree, out_degree, all_degree = module_1231(graph, address,
                                                    drop_duplicated)
    return in_degree / all_degree if all_degree else None, out_degree / all_degree if all_degree else None


def module_12312(graph, address: str, drop_duplicated=False):
    
    """Compute the ratio of [in-degree] and [out-degree]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -drop_duplicated: Check if preserving the repeat situation (default to False)
                      If it is False, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    in_degree, out_degree, all_degree = module_1231(graph, address,
                                                    drop_duplicated)
    return in_degree / out_degree if out_degree else None


def module_12313(graph, address: str, drop_duplicated=False):
    
    """Compute the difference of [in-degree] and [out-degree]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -drop_duplicated: Check if preserving the repeat situation (default to False)
                      If it is False, preserving the repeat input and output edge  
                      Else, mergeing the repeat input and output edge
    """
    
    in_degree, out_degree, all_degree = module_1231(graph, address,
                                                    drop_duplicated)
    return in_degree - out_degree


"""
    Pure Time Indicator (PTI)
"""


def formating_timestamp(timestamp: int):

    """Function: Change the timestamp to readable format 
    param:
        -timestamp: The timestamp
    """
    
    time_array = time.localtime(timestamp)
    tx_formal_time = time.strftime("%Y%m%d", time_array)
    return tx_formal_time


def module_1311(graph: gt.Graph, address: str):
    
    """Obtain the life cycle of the Bitcoin address (i.e. the difference of the earliest active time and the latest active time, the basic unit is the solar day)
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    activate_times = [
        graph.ep['time'][edge] for edge in address_vertex.all_edges()
    ]
    earliest_activate_time, latest_activate_time = min(activate_times), max(
        activate_times)
    if earliest_activate_time // 86400 != latest_activate_time // 86400:
        if earliest_activate_time % 86400 < latest_activate_time % 86400:
            return math.ceil(
                (latest_activate_time - earliest_activate_time) / 86400)
        else:
            return math.ceil(
                (latest_activate_time - earliest_activate_time) / 86400) + 1
    else:
        return 1


def module_1312(graph: gt.Graph, address: str):
    
    """Obtain the active period of the Bitcoin address (if a Bitcoin address has at least one transaction record in a day, it is active on that day)
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """

    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    return list(
        set([
            formating_timestamp(graph.ep['time'][edge])
            for edge in address_vertex.all_edges()
        ])).__len__()


def module_13121(graph: gt.Graph, address: str):
    
    """Compute the ratio of [active period] and [life cycle] of the Bitcoin address
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    return module_1311(graph, address) / module_1312(
        graph, address) if module_1312(graph, address) else None


def module_1313(graph: gt.Graph, address: str):
    
    """Obtain the active times of the Bitcoin address in a solar day
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    activate_date = [
        formating_timestamp(graph.ep['time'][edge])
        for edge in address_vertex.all_edges()
    ]
    rs = {}
    for date in activate_date:
        if date in rs:
            rs[date] += 1
        else:
            rs[date] = 1
    return rs if rs.__len__() else None


def module_13131(graph: gt.Graph, address: str):
    
    """Compute the maximum/minimum/average value of the active times
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    active_times_count = module_1313(graph, address)
    values = list(active_times_count.values())
    return max(values) if values.__len__(
    ) else None, min(values) if values.__len__(
    ) else None, sum(values) / values.__len__() if values.__len__() else None


def module_13132(graph: gt.Graph, address: str):
    
    """Compute the difference of [maximum active times] and [minimum active times]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    active_times_count = module_1313(graph, address)
    values = list(active_times_count.values())
    return max(values) - min(values) if values else None


def module_13133(graph: gt.Graph, address: str):
    
    """Compute the standard deviation of the active times
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    active_times_count = module_1313(graph, address)
    values = list(active_times_count.values())
    return np.std(values) if values else None


def module_1314(graph: gt.Graph, address: str):
    
    """Obtain the time interval of every transaction of a Bitcoin address
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    activate_date = list(
        set([
            int(graph.ep['time'][edge]) for edge in address_vertex.all_edges()
        ]))
    activate_date.sort(reverse=False)
    return [(activate_date[date_index + 1] - activate_date[date_index]) / 86400
            for date_index in range(activate_date.__len__() - 1)
            ] if activate_date.__len__() > 1 else None


def module_13141(graph: gt.Graph, address: str):
    
    """Compute the maximum/minimum/average value of the time interval
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    intervals = module_1314(graph, address)
    return max(intervals) if intervals else None, min(intervals) if intervals else None, np.mean(
        intervals) if intervals else None


def module_13142(graph: gt.Graph, address: str):

    """Compute the difference of the [maximum time interval] and [minimum time interval]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    intervals = module_1314(graph, address)
    return max(intervals) - min(intervals) if intervals else None


"""
    Combination Indicator (CI)
"""


def module_14131(graph: gt.Graph, address: str):

    """Compute the ratio of the [total input/output token amount] and [in-degree/out-degree]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    input_sum, output_sum = module_11311(graph, address)
    in_degree, out_degree, all_degree = module_1231(graph, address)
    return input_sum / in_degree if in_degree else None, output_sum / out_degree if out_degree else None


def module_14132(graph: gt.Graph, address: str):

    """Compute the ratio of [difference of [input token amount] and [output token amount]] and [difference of [in-degree] and [out-degree]]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    if module_11312(graph, address) == 0:
        return 0;
    elif module_12313(graph, address) == 0:
        return None
    else:
        result = module_11312(graph, address) / module_12313(graph, address)
        return result


def module_14211(graph: gt.Graph, address: str):

    """Compute the total input/output token amount of the Bitcoin address on every active solar day
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = {}
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)
    for in_edge in address_vertex.in_edges():
        _time, input_value = formating_timestamp(
            graph.ep['time'][in_edge]), graph.ep['value'][in_edge]
        if _time in rs:
            rs[_time][0] += input_value
        else:
            rs[_time] = [input_value, 0]
    for out_edge in address_vertex.out_edges():
        _time, output_value = formating_timestamp(
            graph.ep['time'][out_edge]), graph.ep['value'][out_edge]
        if _time in rs:
            rs[_time][1] += output_value
        else:
            rs[_time] = [0, output_value]
    return rs


def module_142111(graph: gt.Graph, address: str):
    
    """Compute the average input/output token amount of the active solar days
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    sum_per_day = module_14211(graph, address)
    sum_input_value = sum([values[0] for values in list(sum_per_day.values())])
    sum_output_value = sum(
        [values[1] for values in list(sum_per_day.values())])
    return sum_input_value / sum_per_day.__len__(
    ), sum_output_value / sum_per_day.__len__()


def module_142112(graph: gt.Graph, address: str):

    """Compute the maximum/minimum input/output token amount of the active solar days
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    sum_per_day = module_14211(graph, address)
    max_input_value = max([values[0] for values in list(sum_per_day.values())])
    min_input_value = min([values[0] for values in list(sum_per_day.values())])
    max_output_value = max(
        [values[1] for values in list(sum_per_day.values())])
    min_output_value = min(
        [values[1] for values in list(sum_per_day.values())])
    return max_input_value, max_output_value, min_input_value, min_output_value


def module_14212(graph: gt.Graph, address: str):

    """Compute the ratio of [total input/output token amount] and [life cycle] of the Bitcoin address in every active solar day 
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    life_cycle = module_1311(graph, address)
    value_per_day = module_14211(graph, address)
    for key in value_per_day:
        value_per_day[key] = [
            value_per_day[key][0] / life_cycle,
            value_per_day[key][1] / life_cycle
        ]
    return value_per_day


def module_142121(graph: gt.Graph, address: str):

    """Compute the input/output average value from module_14212
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    temp = module_14212(graph, address)
    in_list, out_list = [], []
    for i in temp:
        in_list.append(temp[i][0])
        out_list.append(temp[i][1])
    return np.mean(in_list) if in_list else None, np.mean(out_list) if out_list else None


def module_142122(graph: gt.Graph, address: str):

    """Compute the input/output maximum/minimum value from module_14212
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    temp = module_14212(graph, address)
    in_list, out_list = [], []
    for i in temp:
        in_list.append(temp[i][0])
        out_list.append(temp[i][1])
    return np.min(in_list) if in_list else None, np.max(in_list) if in_list else None, np.min(out_list) if out_list else None, np.max(out_list) if out_list else None


def module_142123(graph: gt.Graph, address: str):

    """Compute the standard deviation of input/output value from module_14212
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    temp = module_14212(graph, address)
    in_list, out_list = [], []
    for i in temp:
        in_list.append(temp[i][0])
        out_list.append(temp[i][1])
    return np.std(in_list) if in_list else None, np.std(out_list) if out_list else None


def module_14213(graph: gt.Graph, address: str):

    """Compute the ratio of [change of total input/output token amount] and [time interval]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)

    in_degree_per_time = {}
    for in_edge in address_vertex.in_edges():
        if str(graph.ep['time'][in_edge]) in in_degree_per_time:
            in_degree_per_time[int(
                graph.ep['time'][in_edge])] += graph.ep['value'][in_edge]
        else:
            in_degree_per_time[int(
                graph.ep['time'][in_edge])] = graph.ep['value'][in_edge]
    in_degree_per_time = list(in_degree_per_time.items())
    in_degree_per_time.sort(key=lambda item: item[0], reverse=False)
    rs1 = [
        (in_degree_per_time[index+1][1]) /
        (in_degree_per_time[index+1][0] - in_degree_per_time[index][0]) * 86400
        for index in range(in_degree_per_time.__len__() - 1)]

    out_value_per_time = {}
    for out_edge in address_vertex.out_edges():
        if str(graph.ep['time'][out_edge]) in out_value_per_time:
            out_value_per_time[int(
                graph.ep['time'][out_edge])] += graph.ep['value'][out_edge]
        else:
            out_value_per_time[int(
                graph.ep['time'][out_edge])] = graph.ep['value'][out_edge]
    out_value_per_time = list(out_value_per_time.items())
    out_value_per_time.sort(key=lambda item: item[0], reverse=False)
    rs2 = [
        (out_value_per_time[index+1][1]) /
        (out_value_per_time[index+1][0] - out_value_per_time[index][0]) * 86400
        for index in range(out_value_per_time.__len__() - 1)]

    return rs1, rs2


def module_142131(graph: gt.Graph, address: str):
    
    """Compute the input/output average value from module_14213
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    t1, t2 = module_14213(graph, address)
    return np.mean(t1) if t1 else None, np.mean(t2) if t2 else None


def module_142132(graph: gt.Graph, address: str):

    """Compute the input/output maximum/minimum value from module_14213
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    t1, t2 = module_14213(graph, address)
    return np.min(t1) if t1 else None, np.max(t1) if t1 else None, np.min(t2) if t2 else None, np.max(t2) if t2 else None


def module_142133(graph: gt.Graph, address: str):

    """Compute the standard deviation of input/output value from module_14213
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """

    t1, t2 = module_14213(graph, address)
    return np.std(t1) if t1 else None, np.std(t2) if t2 else None


def module_14311(graph: gt.Graph, address: str):

    """Compute the total in-degree/out-degree/total degree in every active solar day
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = {}
    for in_edge in graph.vertex(
            reverse_map['account_dict'][address]).in_edges():
        _time = formating_timestamp(
            graph.ep['time'][in_edge])
        if _time in rs:
            rs[_time][0] += 1
            rs[_time][2] += 1
        else:
            rs[_time] = [1, 0, 1]
    for out_edge in graph.vertex(
            reverse_map['account_dict'][address]).out_edges():
        _time = formating_timestamp(
            graph.ep['time'][out_edge])
        if _time in rs:
            rs[_time][1] += 1
            rs[_time][2] += 1
        else:
            rs[_time] = [0, 1, 1]
    return rs


def module_143111(graph: gt.Graph, address: str):

    """Compute the total average in-degree/out-degree of each day in the solar active days
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    degree_per_day = module_14311(graph, address)
    in_degree_sum = sum(
        [degree[0] for degree in list(degree_per_day.values())])
    out_degree_sum = sum(
        [degree[1] for degree in list(degree_per_day.values())])
    return in_degree_sum / degree_per_day.__len__(
    ), out_degree_sum / degree_per_day.__len__()


def module_143112(graph: gt.Graph, address: str):

    """Compute the maximum/minimum in-degree/out-degree of each day in the solar active days
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    degree_per_day = module_14311(graph, address)
    max_in_degree = max(
        [degree[0] for degree in list(degree_per_day.values())])
    min_in_degree = min(
        [degree[0] for degree in list(degree_per_day.values())])
    max_out_degree = max(
        [degree[1] for degree in list(degree_per_day.values())])
    min_out_degree = min(
        [degree[1] for degree in list(degree_per_day.values())])
    return max_in_degree, max_out_degree, min_in_degree, min_out_degree


def module_14312(graph: gt.Graph, address: str):

    """Compute the ratio of [total in-degree/out-degree/total degree] of each day in active days and [life cycle] 
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    life_cycle = module_1311(graph, address)
    degree_per_active_day = module_14311(graph, address)
    for date in degree_per_active_day:
        degree_per_active_day[date][0] /= life_cycle
        degree_per_active_day[date][1] /= life_cycle
        degree_per_active_day[date][2] /= life_cycle
    return degree_per_active_day


def module_143121(graph: gt.Graph, address: str):

    """Compute the input/output/total average value from module_14312
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    degree = module_14312(graph, address)
    il, ol, al = [], [], []
    for i in degree:
        il.append(degree[i][0])
        ol.append(degree[i][1])
        al.append(degree[i][2])
    return np.mean(il), np.mean(ol), np.mean(al)


def module_143122(graph: gt.Graph, address: str):

    """Compute the input/output/total maximum/minimum value from module_14312
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    degree = module_14312(graph, address)
    il, ol, al = [], [], []
    for i in degree:
        il.append(degree[i][0])
        ol.append(degree[i][1])
        al.append(degree[i][2])
    return np.min(il) if il else None, np.max(il) if il else None, np.min(ol) if ol else None, np.max(ol) if ol else None, np.min(al) if al else None, np.max(al) if al else None
 

def module_143123(graph: gt.Graph, address: str):
    
    """Compute the standard deviation of input/output/total value from module_14312
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    degree = module_14312(graph, address)
    il, ol, al = [], [], []
    for i in degree:
        il.append(degree[i][0])
        ol.append(degree[i][1])
        al.append(degree[i][2])
    return np.std(il) if il else None, np.std(ol) if ol else None, np.std(al) if al else None
 

def module_14313(graph: gt.Graph, address: str):

    """Compute the ratio of [change of in-degreee/out-degree] and [time interval]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)

    in_degree_per_time = {}
    for in_edge in address_vertex.in_edges():
        if str(graph.ep['time'][in_edge]) in in_degree_per_time:
            in_degree_per_time[int(graph.ep['time'][in_edge])] += 1
        else:
            in_degree_per_time[int(graph.ep['time'][in_edge])] = 1
    in_degree_per_time = list(in_degree_per_time.items())
    in_degree_per_time.sort(key=lambda item: item[0], reverse=False)

    rs1 = [
        (in_degree_per_time[index+1][1]) /
        (in_degree_per_time[index+1][0] - in_degree_per_time[index][0]) * 86400
        for index in range(in_degree_per_time.__len__() - 1)
    ]

    out_degree_per_time = {}
    for out_edge in address_vertex.out_edges():
        if str(graph.ep['time'][out_edge]) in out_degree_per_time:
            out_degree_per_time[int(graph.ep['time'][out_edge])] += 1
        else:
            out_degree_per_time[int(graph.ep['time'][out_edge])] = 1
    out_degree_per_time = list(out_degree_per_time.items())
    out_degree_per_time.sort(key=lambda item: item[0], reverse=False)
    
    rs2 = [
        (out_degree_per_time[index+1][1]) /
        (out_degree_per_time[index+1][0] - out_degree_per_time[index][0]) * 86400
        for index in range(out_degree_per_time.__len__() - 1)
    ]

    return rs1, rs2


def module_143131(graph: gt.Graph, address: list):
    
    """Compute the average value from module_14313
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs1, rs2 = module_14313(graph, address)
    return np.mean(rs1) if rs1 else None, np.mean(rs2) if rs2 else None


def module_143132(graph: gt.Graph, address: list):

    """Compute the maximum/minimum value from module_14313
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs1, rs2 = module_14313(graph, address)
    return np.min(rs1) if rs1 else None, np.max(rs1) if rs1 else None, np.min(rs2) if rs2 else None, np.max(rs2) if rs2 else None


def module_143133(graph: gt.Graph, address: list):

    """Compute the standard deviation of value from module_14313
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs1, rs2 = module_14313(graph, address)
    return np.std(rs1) if rs1 else None, np.std(rs2) if rs2 else None
  

def module_14411(graph: gt.Graph, address: str):
    
    """Compute the ratio of the [ratio of [total input token amount] and [in-degree]] and [life cycle]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = {}
    life_cycle = module_1311(graph, address)
    value_per_day = module_14211(graph, address)
    degree_per_day = module_14311(graph, address)

    for date in value_per_day:
        rs[date] = value_per_day[date][0] / degree_per_day[date][0] / life_cycle if degree_per_day[date][0] else 0
    return rs


def module_144111(graph: gt.Graph, address: str):

    """Compute the average value from module_14411
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14411(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.mean(rs) if rs else None


def module_144112(graph: gt.Graph, address: str):
    
    """Compute the maximum/minimum value from module_14411
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14411(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.min(rs) if rs else None,np.max(rs) if rs else None


def module_144113(graph: gt.Graph, address: str):

    """Compute the standard deviation of value from module_14411
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14411(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.std(rs) if rs else None

     
def module_14412(graph: gt.Graph, address: str):
    
    """Compute the ratio of the [ratio of [total output token amount] and [out-degree]] and [life cycle]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = {}
    life_cycle = module_1311(graph, address)
    value_per_day = module_14211(graph, address)
    degree_per_day = module_14311(graph, address)
    for date in value_per_day:
        rs[date] = value_per_day[date][1] / degree_per_day[date][1] / life_cycle if degree_per_day[date][1]  else 0
    return rs 


def module_144121(graph: gt.Graph, address: str):

    """Compute the average value from module_14412
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14412(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.mean(rs) if rs else None


def module_144122(graph: gt.Graph, address: str):
    
    """Compute the maximum/minimum value from module_14412
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14412(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.min(rs) if rs else None, np.max(rs) if rs else None


def module_144123(graph: gt.Graph, address: str):

    """Compute the standard deviation of value from module_14412
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = []
    temp = module_14412(graph, address)
    for i in temp:
        rs.append(temp[i])
    return np.std(rs) if rs else None


def module_14413(graph, address: str):

    """Compute the ratio of [change of the ratio of [total input token amount] and [in-degree]] and [time interval]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)

    ratio_per_time = {}
    for in_edge in address_vertex.in_edges():
        if str(graph.ep['time'][in_edge]) in ratio_per_time:
            ratio_per_time[int(graph.ep['time'][in_edge])][0] += graph.ep['value'][in_edge]
            ratio_per_time[int(graph.ep['time'][in_edge])][1] += 1
        else:
            ratio_per_time[int(graph.ep['time'][in_edge])] = [
                (graph.ep['value'][in_edge]), 1
            ]
    ratio_per_time = list(ratio_per_time.items())
    ratio_per_time.sort(key=lambda item: item[0], reverse=False)
    for index in range(1, ratio_per_time.__len__()):
        ratio_per_time[index][1][0] += ratio_per_time[index-1][1][0]
        ratio_per_time[index][1][1] += ratio_per_time[index-1][1][1]

    rs = [
        ((ratio_per_time[index + 1][1][0] / ratio_per_time[index + 1][1][1]) -
         (ratio_per_time[index][1][0] / ratio_per_time[index][1][1])) /
        (int(ratio_per_time[index + 1][0]) - int(ratio_per_time[index][0]))
        for index in range(ratio_per_time.__len__() - 1)
    ]
    return rs


def module_144131(graph: gt.Graph, address: str):

    """Compute the average value from module_14413
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14413(graph, address)
    return np.mean(rs) if rs else None


def module_144132(graph: gt.Graph, address: str):

    """Compute the maximum/minimum value from module_14413
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14413(graph, address)
    return np.min(rs) if rs else None, np.max(rs) if rs else None


def module_144133(graph: gt.Graph, address: str):

    """Compute the standard deviation of value from module_14413
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14413(graph, address)
    return np.std(rs) if rs else None


def module_14414(graph, address: str):
    
    """Compute the ratio of [change of the ratio of [total output token amount] and [out-degree]] and [time interval]
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    address_index = reverse_map['account_dict'][address]
    address_vertex = graph.vertex(address_index)

    ratio_per_time = {}
    for out_edge in address_vertex.out_edges():
        if str(graph.ep['time'][out_edge]) in ratio_per_time:
            ratio_per_time[str(
                graph.ep['time'][out_edge])][0] += graph.ep['value'][out_edge]
            ratio_per_time[str(graph.ep['time'][out_edge])][1] += 1
        else:
            ratio_per_time[str(graph.ep['time'][out_edge])] = [
                (graph.ep['value'][out_edge]), 1
            ]
    ratio_per_time = list(ratio_per_time.items())
    ratio_per_time.sort(key=lambda item: item[0], reverse=False)
    for index in range(1, ratio_per_time.__len__()):
        ratio_per_time[index][1][0] += ratio_per_time[index-1][1][0]
        ratio_per_time[index][1][1] += ratio_per_time[index-1][1][1]
    try:
        rs = [
            ((ratio_per_time[index + 1][1][0] / ratio_per_time[index + 1][1][1]) -
             (ratio_per_time[index][1][0] / ratio_per_time[index][1][1])) /
            (int(ratio_per_time[index + 1][0]) - int(ratio_per_time[index][0]))
            for index in range(ratio_per_time.__len__() - 1)
        ]
    except:
        print(ratio_per_time)
        exit(0)
    return rs


def module_144141(graph: gt.Graph, address: str):

    """Compute the average value from module_14414
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14414(graph, address)
    return np.mean(rs) if rs else None


def module_144142(graph: gt.Graph, address: str):

    """Compute the maximum/minimum value from module_14414
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14414(graph, address)
    return np.min(rs) if rs else None, np.max(rs) if rs else None


def module_144143(graph: gt.Graph, address: str):

    """Compute the standard deviation of value from module_14414
    param:    
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
    """
    
    rs = module_14414(graph, address)
    return np.std(rs) if rs else None


def module_2111(graph: gt.Graph, address: str, n: int, flag_return_with_graph=False):

    """Function: k-hop subgraph generation
    param:
        -graph: The Bitcoin transaction graph
        -address: The Bitcoin address
        -n : The value of k in k-hop
        -flag_return_with_graph: Check if returing the subgraph (default to False)
                                 If it is True, returing the subgraph
                                 Else, no returning result
    return:
        -layers [dict]: {the number of layer:[index，...], ...}
        -gg [gt.Graph]: The returned subgraph
    """
    
    from collections import defaultdict
    
    addr_index = reverse_map["account_dict"][address]
    gv = gt.GraphView(graph, directed=False)
    u = gt.bfs_iterator(gv, gv.vertex(addr_index))
    dist = gv.new_vp("int")
    fil = graph.new_vp("bool")
    dist[gv.vertex(addr_index)] = 0
    layers = defaultdict(lambda: [])
    fil[graph.vertex(addr_index)] = True
    for i, e in enumerate(u):
        if dist[e.source()] >= n:
            break
        dist[e.target()] = dist[e.source()] + 1
        fil[graph.vertex(gv.vertex_index[e.target()])] = True
        layers[dist[e.target()]].append(gv.vertex_index[e.target()])
    if flag_return_with_graph:
        gg = gt.GraphView(graph, vfilt=fil)
        gt.graph_draw(gg)
        return layers, gg
    else:
        return layers


def module_221(graph: gt.Graph):

    """Compute the in-degree/out-degree/total degree of each node in the graph to calculate the average value and standard deviation of their degrees
    param:
        -graph: The Bitcoin transaction graph
    """
    
    average_degree_t = gt.vertex_average(graph, "total")
    average_degree_i = gt.vertex_average(graph, "in")
    average_degree_o = gt.vertex_average(graph, "out")
    return average_degree_t[0], average_degree_t[1], average_degree_i[0], average_degree_i[1], average_degree_o[0], average_degree_o[1]


def module_222(graph: gt.Graph):

    """Compute the distribution of in-degree/out-degree/total degree of the Bitcoin address in the graph
    param:
        -graph: The Bitcoin transaction graph
    return:
        -in_stats, out_stats, all_stats: [(key1,value1), (key2, value2), ...]
                                         Ascending order according to the key value
    """

    from collections import defaultdict
    
    in_stats, out_stats, all_stats = defaultdict(lambda:0), defaultdict(lambda:0), defaultdict(lambda:0)
    for v in graph.vertices():
        if graph.vp["address"][v]:
            in_stats[v.in_degree()] += 1
            out_stats[v.out_degree()] += 1
            all_stats[v.in_degree()+v.out_degree()] += 1
    return tuple(sorted(x.items()) for x in (in_stats, out_stats, all_stats))


def module_223(graph: gt.Graph):

    """Degree correlation (simplified Pearson degree correlation)
    param:
        -graph: The Bitcoin transaction graph
    """
    
    E_num = (graph.num_edges()) ** (-1)
    s1, s2, s3 = 0, 0, 0
    for s, t in graph.iter_edges():
        d = graph.get_total_degrees([s, t])
        s1 += d[0] * d[1]
        s2 += (d[0] + d[1]) / 2
        s3 += np.sum(np.square(d))
    up = E_num * s1 - (E_num * s2) ** 2
    down = E_num * s3 - (E_num * s2) ** 2
    return up / down


def module_224(graph: gt.Graph):

    """Betweenness
    param:
        -graph: The Bitcoin transaction graph
    """
    
    vp, ep = gt.betweenness(graph) 
    return vp[0]


def module_225(graph: gt.Graph):

    """The diameter and average path length
    param:
        -graph: The Bitcoin transaction graph
    """

    d = gt.shortest_distance(graph)
    dm = np.stack([d[i].a for i in graph.iter_vertices()])
    dm2 = dm[(0 < dm) & (dm < graph.num_vertices())]
    return dm2.mean(), dm2.max()


def module_226(graph: gt.Graph):

    """Local clustering coefficient 
    param:
        -graph: The Bitcoin transaction graph
    note:
        The result of this function is deleted after preprocess step due to all value of which is zero
    """
    
    def local_clustering(g,v):
        return sum(len([None for vj in v.all_neighbors() if g.edge(vi, vj)]) for vi in v.all_neighbors())
    return local_clustering(graph, graph.vertex(0))


def module_231(graph: gt.Graph, depth: int=3):

    """Extended clustering coefficient
    param:
        -graph: The Bitcoin transaction graph
        -depth : The depth of extended clustering coefficient
    note:
        The result of this function is deleted after preprocess step due to all value of which is zero
    """
    
    clust = gt.extended_clustering(graph, undirected=False, max_depth=depth)
    temp = map(lambda key: clust[key][0], range(depth))
    return list(temp)


def module_232(graph: gt.Graph):
    
    """Closeness centrality
    param:
        -graph: The Bitcoin transaction graph
    """
    
    import math
    
    cloness = gt.closeness(graph, source=0)
    return cloness if cloness.any() else None


def module_233(graph: gt.Graph):

    """PageRank
    param:
        -graph: The Bitcoin transaction graph
    """

    pr = gt.pagerank(graph)
    return pr[0]


def module_234(graph: gt.Graph):
    
    """Density
    param:
        -graph: The Bitcoin transaction graph
    """
    v_num = graph.num_vertices()
    e_num = set(tuple(x) for x in(graph.get_edges()).tolist()).__len__()
    return e_num / (v_num*(v_num-1))


def module_max_n(graph: gt.Graph, path_folder):

    """Function: Compute the maximum k value of k-hop subgraph
    
    """
    
    import pandas as pd
    from tqdm import tqdm
    
    try:
        data = pd.read_csv(path_folder, index_col="account")
        new_g = gt.GraphView(graph, directed=False)
        num = 0
        for index, rows in tqdm(data.iterrows()):
            num += 1
            if num > 100:
                data.to_csv(path_folder, mode = 'w')
                break
            index_n = reverse_map["account_dict"][index]

            dict = new_g.new_vp("int")
            u= gt.dfs_iterator(new_g, new_g.vertex(index_n))
            max = 0
            for i, e in enumerate(u):
                dict[e.target()] = dict[e.source()]+1
                if dict[e.target()] > max:
                    max = dict[e.target()]          
                rows["max_n"] = max
                if dict[e.target()] >= 4:
                    rows["max_n"] = "M"
                    break
        data.to_csv(path_folder, mode = 'w')
    except:
        print(index,"error")
