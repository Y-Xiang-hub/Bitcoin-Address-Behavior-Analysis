'''This is the test implemented by networkx
   Some indicators here are in old version
'''

import json
import os
import time
import traceback

import networkx as nx
from typing import List, Optional
import matplotlib.pyplot as plt

# from pip install import Network
from sqlalchemy import null


def add_TxNode_coinbase(directed_graph, hash, input_count, outputs_count, outputs_value, block_height, block_time, fee,
                        size):
    directed_graph.add_node(hash, tx_input_count=input_count, tx_output_count=outputs_count,
                            tx_outputs_value=outputs_value,
                            tx_block_height=block_height, tx_block_time=block_time, tx_fee=fee, tx_size=size)


def add_TxNode(directed_graph, hash, input_count, input_value, outputs_count, outputs_value, block_height, block_time,
               fee, size):
    directed_graph.add_node(hash, tx_input_count=input_count, tx_input_value=input_value, tx_output_count=outputs_count,
                            tx_outputs_value=outputs_value, tx_block_height=block_height, tx_block_time=block_time,
                            tx_fee=fee, tx_size=size)


def add_input_AdsNode(directed_graph, prev_address, prev_type):
    directed_graph.add_node(prev_address, prev_type=prev_type)


def add_input_AdsEdge(directed_graph, AdsNode, TxNode, prev_value, block_time):
    directed_graph.add_edge(AdsNode, TxNode, in_value=prev_value, in_time=block_time)


def add_output_AdsNode(directed_graph, address, next_type):
    directed_graph.add_node(address, next_type=next_type)


def add_output_AdsEdge(directed_graph, TxNode, AdsNode, value, block_time):
    directed_graph.add_edge(TxNode, AdsNode, out_value=value, out_time=block_time)


def process_single_folder(directed_graph, path_folder):
    # function of reading one json file
    files_json = os.listdir(path_folder)
    flag_coinbase = True  # set it before the start of a folder loop
    for file in files_json:
        print(file)
        json_file = open(path_folder + "/" + file, 'r')
        json_content = json_file.read()
        json_dict = json.loads(json_content)

        for i in json_dict["data"]["list"]:

            # coinbase transaction
            if flag_coinbase is True:
                '''Tx node attribute

                '''

                tx_hash = i["hash"]
                tx_input_count = i["inputs_count"]
                tx_output_count = i["outputs_count"]
                tx_output_value = i["outputs_value"] / 100000000
                tx_block_height = i["block_height"]
                tx_time = i["block_time"]
                time_array = time.localtime(tx_time)
                tx_formal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                tx_fee = 0
                tx_size = i["size"]  # bytes

                add_TxNode_coinbase(directed_graph, tx_hash, tx_input_count, tx_output_count, tx_output_value,
                                    tx_block_height,
                                    tx_formal_time, tx_fee, tx_size)

                '''output node and edge attribute

                '''

                for j in i["outputs"]:
                    if j["type"] != "NULL_DATA":
                        output_address = j["addresses"][0]
                        output_type = j["type"]
                        add_input_AdsNode(directed_graph, output_address, output_type)

                        output_edge_value = j["value"] / 100000000
                        output_edge_time = tx_formal_time
                        add_output_AdsEdge(directed_graph, tx_hash, output_address, output_edge_value, output_edge_time)

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
                if "outputs_value" in i.keys():
                    tx_output_value = i["outputs_value"] / 100000000  # check if outputs_value exists
                    tx_block_height = i["block_height"]
                    tx_time = i["block_time"]
                    time_array = time.localtime(tx_time)
                    tx_formal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                    if "fee" in i.keys():
                        tx_fee = i["fee"] / 100000000
                        tx_size = i["size"]  # bytes
                    else:
                        tx_fee = 0
                        tx_size = i["size"]  # bytes
                    add_TxNode(directed_graph, tx_hash, tx_input_count, tx_input_value, tx_output_count,
                               tx_output_value,
                               tx_block_height, tx_formal_time, tx_fee, tx_size)

                else:
                    break
                '''input node and edge attribute

                '''

                for j in i["inputs"]:
                    input_address = j["prev_addresses"][0]
                    if "prev_type" in j.keys():
                        input_type = j["prev_type"]
                        add_input_AdsNode(directed_graph, input_address, input_type)
                        input_edge_value = j["prev_value"] / 100000000
                        input_edge_time = tx_formal_time
                        add_input_AdsEdge(directed_graph, input_address, tx_hash, input_edge_value, input_edge_time)
                    else:
                        continue

                '''output node and edge attribute

                '''

                for j in i["outputs"]:
                    if "type" in j.keys():
                        if j["type"] != "NULL_DATA":
                            output_address = j["addresses"][0]
                            output_type = j["type"]
                            add_output_AdsNode(directed_graph, output_address, output_type)

                            output_edge_value = j["value"] / 100000000
                            output_edge_time = tx_formal_time
                            add_output_AdsEdge(directed_graph, tx_hash, output_address, output_edge_value,
                                               output_edge_time)

                        else:
                            continue
                    else:
                        continue
        json_file.close()


def traverse_folder(directed_graph, start_num, end_num, folder_path):
    for num in range(start_num, end_num + 1):
        real_path = folder_path + str(num)
        print(num)
        process_single_folder(directed_graph, real_path)


def save_graph(graph_structure, save_graph_path):
    nx.write_gpickle(graph_structure, save_graph_path)
    '''
    # Gml .gml
    nx.write_gml(graph_structure, save_graph_path)
    # Gexf .gexf
    nx.write_gexf(graph_structure, save_graph_path)
    # Pickled .gpickle
    nx.write_gpickle(graph_structure, save_graph_path)
    # GraphML .graphml
    nx.write_graphml(graph_structure, save_graph_path)
    '''


def load_graph(load_graph_path):
    model = nx.read_gpickle(load_graph_path)

    '''
    model = nx.read_gml(load_graph_path)
    model = nx.read_gexf(load_graph_path)
    model = nx.read_gpickle(load_graph_path)
    model = nx.read_graphml(load_graph_path)
    '''

    return model


def combine_two_graphs(graph_a, graph_b):
    new_graph = nx.compose(graph_a, graph_b)
    return new_graph


def graph_density(graph):
    nodes_num = nx.number_of_nodes(graph)
    edges_num = nx.number_of_edges(graph)
    return edges_num / (nodes_num * (nodes_num - 1))


def average_degree(graph):
    num_edges = nx.number_of_edges(graph)
    num_nodes = nx.number_of_nodes(graph)
    return 2 * num_edges / num_nodes


if __name__ == '__main__':
    # build directed graph
    DG = nx.MultiDiGraph()

    # basic settings
    folder_path = os.getcwd().replace('\\','/') + path
    start_folder = 680000
    end_folder = 681999
    
    # execution
    traverse_folder(DG, start_folder, end_folder, folder_path)
    
    # save the graph
    save_path = os.getcwd().replace('\\', '/') + path 
    save_graph(DG, save_path + "BTC_" + str(start_folder) + "_" + str(end_folder) + ".gpickle")

    # load the graph
    load_path = save_path
    DH = load_graph(load_path + filename)
   
