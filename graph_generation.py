from tqdm_pickle import load_file
import pandas as pd
import copy
from collections import defaultdict
import typing
import graph_tool.all as gt
import numpy as np
import json
import os
import csv
import time
import traceback
from tqdm import tqdm
from typing import DefaultDict, List, Optional
import pickle
from moduleG import *
import moduleG
import imp
imp.reload(moduleG)

# reverse_map = defaultdict(lambda: {})


def formating_timestamp(timestamp: int) -> str:

    """Function: Change the timestamp to readable format 
    param:
        -timestamp: The timestamp
    """
    
    time_array = time.localtime(timestamp)
    tx_formal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return tx_formal_time


def add_TxNode_property(directed_graph):
    tx_hash = directed_graph.new_vertex_property("string")
    directed_graph.vp["tx_hash"] = tx_hash
    tx_inputs_count = directed_graph.new_vertex_property("int")
    directed_graph.vp["tx_inputs_count"] = tx_inputs_count
    tx_inputs_value = directed_graph.new_vertex_property("double")
    directed_graph.vp["tx_inputs_value"] = tx_inputs_value
    tx_outputs_count = directed_graph.new_vertex_property("int")
    directed_graph.vp["tx_outputs_count"] = tx_outputs_count
    tx_outputs_value = directed_graph.new_vertex_property("double")
    directed_graph.vp["tx_outputs_value"] = tx_outputs_value
    tx_block_height = directed_graph.new_vertex_property("int")
    directed_graph.vp["tx_block_height"] = tx_block_height
    tx_block_time = directed_graph.new_vertex_property("int")
    directed_graph.vp["tx_block_time"] = tx_block_time
    tx_fee = directed_graph.new_vertex_property("double")
    directed_graph.vp["tx_fee"] = tx_fee
    tx_size = directed_graph.new_vertex_property("int")
    directed_graph.vp["tx_size"] = tx_size


def add_AdsNode_property(directed_graph):
    ads_address = directed_graph.new_vertex_property("string")
    directed_graph.vp["address"] = ads_address
    ads_prev_type = directed_graph.new_vertex_property("string")
    directed_graph.vp["prev_type"] = ads_prev_type
    ads_next_type = directed_graph.new_vertex_property("string")
    directed_graph.vp["next_type"] = ads_next_type


def add_edge_property(directed_graph):
    edge_value = directed_graph.new_edge_property("double")
    directed_graph.ep["value"] = edge_value
    edge_time = directed_graph.new_edge_property("int")
    directed_graph.ep["time"] = edge_time


def add_TxNode_coinbase(directed_graph, hash: str, inputs_count: int,
                        outputs_count: int, outputs_value: float,
                        block_height: int, block_time: int, fee: float,
                        size: int):
    coinbase_node = directed_graph.add_vertex()
    moduleG.reverse_map["transaction_dict"][hash] = directed_graph.vertex_index[
        coinbase_node]
    directed_graph.vp["tx_hash"][coinbase_node] = hash
    directed_graph.vp["tx_inputs_count"][coinbase_node] = inputs_count
    directed_graph.vp["tx_outputs_count"][coinbase_node] = outputs_count
    directed_graph.vp["tx_outputs_value"][coinbase_node] = outputs_value
    directed_graph.vp["tx_block_height"][coinbase_node] = block_height
    directed_graph.vp["tx_block_time"][coinbase_node] = block_time
    directed_graph.vp["tx_fee"][coinbase_node] = fee
    directed_graph.vp["tx_size"][coinbase_node] = size


def add_TxNode(directed_graph, hash, inputs_count, inputs_value, outputs_count,
               outputs_value, block_height, block_time, fee, size):
    tx_node = directed_graph.add_vertex()
    moduleG.reverse_map["transaction_dict"][hash] = directed_graph.vertex_index[tx_node]
    directed_graph.vp["tx_hash"][tx_node] = hash
    directed_graph.vp["tx_inputs_count"][tx_node] = inputs_count
    directed_graph.vp["tx_inputs_value"][tx_node] = inputs_value
    directed_graph.vp["tx_outputs_count"][tx_node] = outputs_count
    directed_graph.vp["tx_outputs_value"][tx_node] = outputs_value
    directed_graph.vp["tx_block_height"][tx_node] = block_height
    directed_graph.vp["tx_block_time"][tx_node] = block_time
    directed_graph.vp["tx_fee"][tx_node] = fee
    directed_graph.vp["tx_size"][tx_node] = size


def add_inputs_AdsNode(directed_graph, prev_address, prev_type):
    if prev_address not in moduleG.reverse_map["account_dict"]:
        ads_inputs_node = directed_graph.add_vertex()
        moduleG.reverse_map["account_dict"][prev_address] = directed_graph.vertex_index[
            ads_inputs_node]
        directed_graph.vp["address"][ads_inputs_node] = prev_address
        directed_graph.vp["prev_type"][ads_inputs_node] = prev_type
    else:
        ads_index = moduleG.reverse_map["account_dict"][prev_address]
        if directed_graph.vp["prev_type"][ads_index] == '':
            directed_graph.vp["prev_type"][ads_index] = prev_type


def add_outputs_AdsNode(directed_graph, address, next_type):
    if address not in moduleG.reverse_map["account_dict"]:
        ads_outputs_node = directed_graph.add_vertex()
        moduleG.reverse_map["account_dict"][address] = directed_graph.vertex_index[
            ads_outputs_node]
        directed_graph.vp["address"][ads_outputs_node] = address
        directed_graph.vp["next_type"][ads_outputs_node] = next_type
    else:
        ads_index = moduleG.reverse_map["account_dict"][address]
        if directed_graph.vp["next_type"][ads_index] == '':
            directed_graph.vp["next_type"][ads_index] = next_type


def add_inputs_AdsEdge(directed_graph, AdsNode, TxNode, prev_value,
                       block_time):
    Ads_index = moduleG.reverse_map["account_dict"][AdsNode]
    Tx_index = moduleG.reverse_map["transaction_dict"][TxNode]
    new_edge = directed_graph.add_edge(directed_graph.vertex(Ads_index),
                                       directed_graph.vertex(Tx_index))
    directed_graph.ep["value"][new_edge] = prev_value
    directed_graph.ep["time"][new_edge] = block_time


def add_outputs_AdsEdge(directed_graph, TxNode, AdsNode, value, block_time):
    Tx_index = moduleG.reverse_map["transaction_dict"][TxNode]
    Ads_index = moduleG.reverse_map["account_dict"][AdsNode]
    new_edge = directed_graph.add_edge(directed_graph.vertex(Tx_index),
                                       directed_graph.vertex(Ads_index))
    directed_graph.ep["value"][new_edge] = value
    directed_graph.ep["time"][new_edge] = block_time


def process_single_folder(directed_graph, path_folder):
    files_json = os.listdir(path_folder)
    flag_coinbase = True  # set it before the start of a folder loop

    for file in files_json:
        json_file = open(path_folder + "/" + file, 'r')
        json_content = json_file.read()
        json_dict = json.loads(json_content)
        try:
            for index, i in enumerate(json_dict["data"]["list"]):

                # coinbase transaction
                if 'is_coinbase' in i and i['is_coinbase']:
                
                    '''Tx node attribute
                    
                    '''

                    tx_hash = i["hash"]
                    tx_input_count = i["inputs_count"]
                    tx_output_count = i["outputs_count"]
                    tx_output_value = i["outputs_value"] / 100000000
                    tx_block_height = i["block_height"]
                    tx_formal_time = i["block_time"]
                    tx_fee = 0
                    tx_size = i["size"]  # bytes
                    add_TxNode_coinbase(directed_graph, tx_hash,
                                        tx_input_count, tx_output_count,
                                        tx_output_value, tx_block_height,
                                        tx_formal_time, tx_fee, tx_size)
                                        
                    '''Output node and edge attribute
                    
                    '''

                    for j in i["outputs"]:
                        if j["type"] != "NULL_DATA":
                            output_address = j["addresses"][0]
                            output_type = j["type"]
                            add_inputs_AdsNode(directed_graph, output_address,
                                               output_type)

                            output_edge_value = j["value"] / 100000000
                            output_edge_time = tx_formal_time
                            add_outputs_AdsEdge(directed_graph, tx_hash,
                                                output_address,
                                                output_edge_value,
                                                output_edge_time)

                        else:
                            continue
                    flag_coinbase = False

                # general transaction
                else:
                
                    '''Tx node attribute
                    
                    '''

                    tx_hash = i["hash"]
                    tx_input_count = i["inputs_count"]
                    tx_input_value = i["inputs_value"] / 100000000
                    tx_output_count = i["outputs_count"]
                    if "outputs_value" in i:
                        tx_output_value = i[
                            "outputs_value"] / 100000000  # check if outputs_value exists
                        tx_block_height = i["block_height"]
                        tx_formal_time = i["block_time"]
                        if "fee" in i:
                            tx_fee = i["fee"] / 100000000
                            tx_size = i["size"]  # bytes
                        else:
                            tx_fee = 0
                            tx_size = i["size"]  # bytes
                        add_TxNode(directed_graph, tx_hash, tx_input_count,
                                   tx_input_value, tx_output_count,
                                   tx_output_value, tx_block_height,
                                   tx_formal_time, tx_fee, tx_size)

                    else:
                        break
                        
                    '''Input node and edge attribute
                    
                    '''
                 
                    for j in i["inputs"]:
                        input_address = j["prev_addresses"][0]
                        if "prev_type" in j:
                            input_type = j["prev_type"]
                            add_inputs_AdsNode(directed_graph, input_address,
                                               input_type)
                            input_edge_value = j["prev_value"] / 100000000
                            input_edge_time = tx_formal_time
                            add_inputs_AdsEdge(directed_graph, input_address,
                                               tx_hash, input_edge_value,
                                               input_edge_time)
                        else:
                            continue
                            
                    '''Output node and edge attribute
                    
                    '''

                    for j in i["outputs"]:
                        if "type" in j:
                            if j["type"] != "NULL_DATA":
                                output_address = j["addresses"][0]
                                output_type = j["type"]
                                add_outputs_AdsNode(directed_graph,
                                                    output_address,
                                                    output_type)

                                output_edge_value = j["value"] / 100000000
                                output_edge_time = tx_formal_time
                                add_outputs_AdsEdge(directed_graph, tx_hash,
                                                    output_address,
                                                    output_edge_value,
                                                    output_edge_time)

                            else:
                                continue
                        else:
                            continue
        except:
            print("Error File：{}".format(path_folder + "/" + file))
            print(file)
            print(i["hash"])
            exstr = traceback.format_exc()
            print(exstr)
            continue
        json_file.close()


def traverse_folder(directed_graph, start_num, end_num, folder_path):
    for num in tqdm(range(start_num, end_num + 1)):
        real_path = folder_path + str(num)
        process_single_folder(directed_graph, real_path)


if __name__ == '__main__':
    graph = gt.Graph()
    add_TxNode_property(graph)
    add_AdsNode_property(graph)
    add_edge_property(graph)
    folder_path = os.getcwd().replace('\\', '/') + '/data/json_data/'
    start_folder = 585000
    end_folder = 685000
    traverse_folder(graph, start_folder, end_folder, folder_path)
    with open("revmap.pkl","wb") as f:
        pickle.dump(moduleG.reverse_map,f)
    graph.save("BitcoinGraph.gt")
