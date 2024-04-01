# BABD Construction and Analysis

This project provides the source code for building [BABD-13](https://www.kaggle.com/datasets/lemonx/babd13), which is accessible on Kaggle. The research paper, titled [BABD: A Bitcoin Address Behavior Dataset for Pattern Analysis](https://doi.org/10.1109/TIFS.2023.3347894), has been published in IEEE Transactions on Information Forensics and Security. If you find our work helpful for your research, please consider citing it as:

    @article{xiang2023babd,
      author={Xiang, Yuexin and Lei, Yuchen and Bao, Ding and Li, Tiantian and Yang, Qingqing and Liu, Wenmao and Ren, Wei and Choo, Kim-Kwang Raymond},
      journal={IEEE Transactions on Information Forensics and Security}, 
      title={BABD: A Bitcoin Address Behavior Dataset for Pattern Analysis}, 
      year={2024},
      volume={19},
      pages={2171-2185},
      doi={10.1109/TIFS.2023.3347894}
    }
    
If you have any questions please feel free to contact me by e-mail at Yuexin.Xiang@monash.edu.

## Contents

- [Data Collection](#data-collection)
- [Graph Generation](#graph-generation)
- [Feature Extraction](#feature-extraction)
- [Data Preprocess](#data-preprocess)
- [Data Analysis](#data-analysis)
- [Additional Notes](#additional-notes)
- [Credits](#credits)
- [Extended Research](#extended-research)
- [Appendix](#appendix)

 
## Data Collection
In the `data_collection` folder, `Bitcoin_Ledger_Reader_V3.1.py` is used for collecting Bitcoin ledger data from [BTC.com](https://btc.com/), also we share **partial Bitcoin ledger data** in JSON format from height 600,000 to 605,999 on our [Kaggle BABD-13](https://www.kaggle.com/datasets/lemonx/babd13) since the whole raw Bitcoin ledger data are too large. We also recommend using [BlockSci](https://github.com/citp/BlockSci) for raw Bitcoin ledger collection, the collected JSON format may be somewhat different from the format in this work but can be modified.

`labeled_data_API.py` is used for collecting Bitcoin addresses with labels from [WalletExplorer](https://www.walletexplorer.com/) that is completed by Qingqing Yang ([@Vinedou](https://github.com/Vinedou)). The collected labeled Bitcoin addresses are saved in .csv files (we named them `Bitcoin_Ads_type.csv` files for easier understanding) as shown in `data_collection` folder. The `Bitcoin_Ads_type.csv` files, including only Bitcoin addresses and their labels, are loaded in all *processing indicators* cells in `data_extraction.ipynb`.

Notably, we would like to thank [Aleš Janda](http://www.alesjanda.cz/) for his generous help in providing API.
 
## Graph Generation
To generate a Bitcoin transaction graph as we designed (shown in Fig. 1 in [our paper](https://doi.org/10.1109/TIFS.2023.3347894)) from Bitcoin ledger data in JSON format, we select several important attributes to construct the Bitcoin transaction graph which can be found in `graph_generation.py` implemented by [graph-tool](https://graph-tool.skewed.de/). 

In this step, we input continuous Bitcoin ledger data in JSON format (see JSON examples in [Kaggle BABD-13](https://www.kaggle.com/datasets/lemonx/babd13)) to generate the Bitcoin transaction graph consisting of two files `revmap.pkl` and `BitcoinGraph.gt`. These two files are loaded in the first cell of `data_extraction.ipynb` as the preparation before calculating the features of Bitcoin addresses with labels. 

## Feature Extraction
In this process, we extract the required features from the generated Bitcoin transaction graph for the concrete labeled Bitcoin addresses. There are two kinds of features we are concerned about in this work that are **statistical features** and **local structural features**. The methods to extract statistical and structural features can be found in `moduleG.py`. The primary difference between calculating these two types of features is that we generate a subgraph before extracting local structural features. To accelerate the speed of feature extraction, we apply the parallel computing approach here.

Next, we run the code in `data_extraction.ipynb` to extract features. First, we load the generated Bitcoin transaction graph (i.e., `revmap.pkl` and `BitcoinGraph.gt`) through the *read the graph* cell. After loading the whole graph, we input `Bitcoin_Ads_type.csv` files with only Bitcoin addresses and their corresponding labels (each type of Bitcoin address is stored in a different .csv file, we process each .csv file separately and generate the corresponding .csv file including all features) to further compute the statistical and local structural features in different *processing indicators* cells in `data_extraction.ipynb` (we recommend using cells noted *parallel computing* to calculate features for faster processing). 

## Data Preprocess
The results of the feature extraction module are stored in different .csv files based on different address types. For further analyzing the data, it is necessary to preprocess the current data by `functions_csv_preprocess.py` in the `preprocess_csv` folder. First, we separately preprocess each .csv file with different types of BItcoin addresses via steps 1 to 6. After that, we use step 7 to add number labels to different Bitcoin addresses to represent different types. Finally, in step 8, we merge all preprocessed .csv files to generate `BABD-13.csv` as shown in [our Kaggle](https://www.kaggle.com/datasets/lemonx/babd13).

## Data Analysis
We use the tools and models provided by [scikit-learn](https://scikit-learn.org/) and [xgboost](https://xgboost.ai/) to analyze and study our data, the code can be seen in `feature_selection.py` and `machine_learning.py` in `data_analysis` folder. The specific analysis of our dataset can be found in [our paper](https://doi.org/10.1109/TIFS.2023.3347894). 

Additionally, we also propose a method to divide the testing set and training set while considering the even assignment of strong label address and weak label address in `split_train_test.py` that is completed by Tiantian Li ([@oopshell](https://github.com/oopshell)).

## Additional Notes
In the `format` folder, `csv_format.yml` is the header of raw feature data .csv files, and `original_ledger_format.json` is an example of the Bitcoin ledger we use. In addition, `networkx_test_version.py` in the `networkx_test` folder is the testing code of our designed methods implemented by [NetworkX](https://networkx.org/) that can only be utilized for tests on small graphs.

## Credits
The project was mainly completed by Ding Bao ([@whbyaoi](https://github.com/whbyaoi)), Yuchen Lei ([@TooYoungTooSimp](https://github.com/TooYoungTooSimp)), and Yuexin Xiang ([@Y-Xiang-hub](https://github.com/Y-Xiang-hub)).

- Ding Bao finished most of the code for the metrics, both in terms of amount and complexity. Not only that, but he also wrote efficient crawlers to fulfill the need of building the dataset presented in the paper and examined the collected data in detail.
- Yuchen Lei authored the core module, directed parallelization improvements, fixed some bugs in the code, and proposed several helpful pieces of advice for machine-learning-based classification.
- Yuexin Xiang wrote the original version of the Bitcoin ledger collection tool and graph initialization and finished machine-learning-powered data analysis including but not limited to preprocessing.

## Extended Research
- Yang, Q., Xiang, Y., Liu, W., & Ren, W. (2022, December). [An Illicit Bitcoin Address Analysis Scheme Based on Subgraph Evolution](https://ieeexplore.ieee.org/abstract/document/10074805). In 2022 IEEE 24th Int Conf on High Performance Computing & Communications; 8th Int Conf on Data Science & Systems; 20th Int Conf on Smart City; 8th Int Conf on Dependability in Sensor, Cloud & Big Data Systems & Application (HPCC/DSS/SmartCity/DependSys) (pp. 679-686). IEEE. [[Data]](https://www.kaggle.com/datasets/lemonx/bitcoin-subgraph-evolution-data)
-  Xiang, Y., Li, T., & Li, Y. (2022, December). [Leveraging Subgraph Structure for Exploration and Analysis of Bitcoin Address](https://ieeexplore.ieee.org/abstract/document/10020980). In 2022 IEEE International Conference on Big Data (Big Data) (pp. 1957-1962). IEEE. [[Data]](https://www.kaggle.com/datasets/lemonx/basd8)
-  Bao, D., Ren, W., Xiang, Y., Liu, W., Zhu, T., Ren, Y., & Choo, K. K. R. (2023). [BTC-Shadow: An Analysis and Visualization System for Exposing Implicit Behaviors in Bitcoin Transaction Graphs](https://link.springer.com/article/10.1007/s11704-023-2531-0). Frontiers of Computer Science, 17(6), 1-3. [[Demo]](https://github.com/whbyaoi/BTCShadow)

## Appendix 
This part corresponds to Table II and Table III in the paper.

| Feature       | Description                                                                                    |
| --------------| ---------------------------------------------------------------------------------------------- |
| **`PAI`**     | The pure amount indicator                          |
| **`PAIa1`**   | The input/output token amount of an address node                       |
| `PAIa11-1`    | The total input token amount of an address node                              |
| `PAIa11-2`    | The total output token amount of an address node                           |
| `PAIa12`      | The difference between `PAIa11-1` and `PAIa11-2`                    |
| `PAIa13`      | The ratio of `PAIa11-1` to `PAIa11-2`                                   |
| `PAIa14-1`    | The minimum input token amount of an address node                       |
| `PAIa14-2`    | The maximum input token amount of an address node                        |
| `PAIa14-3`    | The minimum output token amount of an address node                       |
| `PAIa14-4`    | The maximum output token amount of an address node                          |
| `PAIa15-1`    | The difference between `PAIa14-2` and `PAIa14-1`                |
| `PAIa15-2`    | The difference between `PAIa14-4` and `PAIa14-3`                       |
| `PAIa16-1`    | The ratio of `PAIa15-1` to `PAIa14-2`                                           |
| `PAIa16-2`    | The ratio of `PAIa15-2` to `PAIa14-4`                                          |
| `PAIa17-1`    | The standard deviation of all input token amounts of an address node             |
| `PAIa17-2`    | The standard deviation of all output token amounts of an address node            |
| `PAIa17-3`    | The standard deviation of all input and output token amounts of an address node      |
| **`PAIa2`**   | The ratio of each input (output) token amount and `PAIa11-1` (`PAIa11-2`) token amount    |
| `PAIa21-1`    | The ratio of `PAIa14-1` to `PAIa11-1`                                                     |
| `PAIa21-2`    | The ratio of `PAIa14-2` to `PAIa11-1`                                            |
| `PAIa21-3`    | The ratio of `PAIa14-3` to `PAIa11-2`                                         |
| `PAIa21-4`    | The ratio of `PAIa14-4` to `PAIa11-2`                                         |
| `PAIa22-1`    | The standard deviation of the ratio of each input token amount and `PAIa11-1`                  |
| `PAIa22-2`    | The standard deviation of the ratio of each output token amount and `PAIa11-2`                 |
| **`PDI`**     | The pure degree indicator                                                                  |
| **`PDIa`**    | The degree of an address node                                                                  |
| `PDIa1-1`     | The in-degree of an address node                                                               |
| `PDIa1-2`     | The out-degree of an address node                                                              |
| `PDIa1-3`     | The total degree of an address node                                                            |
| `PDIa11-1`    | The ratio of `PDIa1-1` to `PDIa1-3`                                                            |
| `PDIa11-2`    | The ratio of `PDIa1-2` to `PDIa1-3`                                                            |
| `PDIa12`      | The ratio of `PDIa1-1` to `PDIa1-2`                                                            |
| `PDIa13`      | The difference between `PDIa1-1` and `PDIa1-2`                                                 |
| **`PTI`**     | The pure time indicator |
| **`PTIa1`**   | The lifecycle of an address node - the difference between the earliest and the latest active time |
| **`PTIa2`**   | The active period of an address node - the number of active days during the lifecycle          |
| `PTIa21`      | The ratio of `PTIa2` to `PTIa1`                                                                |
| **`PTIa3`**   | The number of active instances for each day in the active period of an address node            |
| `PTIa31-1`    | The maximum number of active instances of an address node                                      |
| `PTIa31-2`    | The minimum number of active instances of an address node                                      |
| `PTIa31-3`    | The average number of active instances of an address node                                      |
| `PTIa32`      | The difference between `PTIa31-1` and `PTIa31-2`                                               |
| `PTIa33`      | The standard deviation of the number of active instances of an address node                    |
| **`PTIa4`**   | Each transaction time interval for the address node in chronological order  |
| `PTIa41-1`    | The maximum transaction time interval of an address node      |
| `PTIa41-2`    | The minimum transaction time interval of an address node      |
| `PTIa41-3`    | The average transaction time interval of an address node      |
| `PTIa42`      | The difference between `PTIa41-1` and `PTIa41-2`    |
| `PTIa43`      | The standard deviation of the transaction time interval of an address node       |
| **`CI1`**     | **`PAI`** + **`PDI`** |
| `CI1a1-1`     | The ratio of `PAIa11-1` to `PDIa1-1`   |
| `CI1a1-2`     | The ratio of `PAIa11-2` to `PDIa1-2`   |
| `CI1a2`       | The ratio of `PAIa12` to `PDIa13`   |
| **`CI2`**     | **`PAI`** + **`PTI`**   |
| **`CI2a1`**   | The total input/output token amount for each active day   |
| `CI2a11-1`    | The average total input token amount for each day within the active days  |
| `CI2a11-2`    | The average total output token amount for each day within the active days  |
| `CI2a12-1`    | The maximum input token amount in a single day within the active days |
| `CI2a12-2`    | The maximum output token amount in a single day within the active days |
| `CI2a12-3`    | The minimum input token amount in a single day within the active days |
| `CI2a12-4`    | The minimum output token amount in a single day within the active days |
| **`CI2a2`**   | The ratio of `CI2a1` to `PTIa1` |
| `CI2a21-1`    | The average ratio of `CI2a2` (input) to `PTIa1` during the active days |
| `CI2a21-2`    | The average ratio of `CI2a2` (output) to `PTIa1` during the active days |
| `CI2a22-1`    | The minimum ratio of `CI2a2` (input) to `PTIa1` during the active days |
| `CI2a22-2`    | The maximum ratio of `CI2a2` (input) to `PTIa1` during the active days |
| `CI2a22-3`    | The minimum ratio of `CI2a2` (output) to `PTIa1` during the active days |
| `CI2a22-4`    | The maximum ratio of `CI2a2` (output) to `PTIa1` during the active days |
| `CI2a23-1`    | The standard deviation of the ratio of `CI2a2` (input) to `PTIa1` during the active days |
| `CI2a23-2`    | The standard deviation of the ratio of `CI2a2` (output) to `PTIa1` during the active days  |
| **`CI2a3`**   | The ratio of the change in the total input/output token amount to `PTIa4` |
| `CI2a31-1`    | The average ratio of the change in the total input token amount to `PTIa4` |
| `CI2a31-2`    | The average ratio of the change in the total output token amount to `PTIa4` |
| `CI2a32-1`    | The minimum ratio of the change in the total input token amount to `PTIa4` |
| `CI2a32-2`    | The maximum ratio of the change in the total input token amount to `PTIa4` |
| `CI2a32-3`    | The minimum ratio of the change in the total output token amount to `PTIa4` |
| `CI2a32-4`    | The maximum ratio of the change in the total output token amount to `PTIa4` |
| `CI2a33-1`    | The standard deviation of the ratio of the change in the total input token amount to `PTIa4` |
| `CI2a33-2`    | The standard deviation of the ratio of the change in the total output token amount to `PTIa4` |
| **`CI3`**     | **`PDI`** + **`PTI`**   |
| **`CI3a1`**   | The total in-degree/out-degree for each day within the active days     |
| `CI3a11-1`    | The average value of `CI3a1` (in-degree) within the active days |
| `CI3a11-2`    | The average value of `CI3a1` (out-degree) within the active days  |
| `CI3a12-1`    | The maximum value of `CI3a1` (in-degree) within the active days |
| `CI3a12-2`    | The maximum value of `CI3a1` (out-degree) within the active days|
| `CI3a12-3`    | The minimum value of `CI3a1` (in-degree) within the active days|
| `CI3a12-4`    | The minimum value of `CI3a1` (out-degree) within the active days|
| **`CI3a2`**   | The ratio of total in-degree/out-degree/total degree for each day to `PTIa1`  |
| `CI3a21-1`    | The average value of `CI3a2` (in-degree) |
| `CI3a21-2`    | The average value of `CI3a2` (out-degree) |
| `CI3a21-3`    | The average value of `CI3a2` (total degree) |
| `CI3a22-1`    | The minimum value of `CI3a2` (in-degree) |
| `CI3a22-2`    | The maximum value of `CI3a2` (in-degree)|
| `CI3a22-3`    | The minimum value of `CI3a2` (out-degree) |
| `CI3a22-4`    | The maximum value of `CI3a2` (out-degree) |
| `CI3a22-5`    | The minimum value of `CI3a2` (total degree)  |
| `CI3a22-6`    | The maximum value of `CI3a2` (total degree)   |
| `CI3a23-1`    | The standard deviation of `CI3a2` (in-degree) |
| `CI3a23-2`    | The standard deviation of `CI3a2` (out-degree) |
| `CI3a23-3`    | The standard deviation of `CI3a2` (total degree) |
| **`CI3a3`**   | The ratio of the change in in-degree/out-degree to `PTIa4` |
| `CI3a31-1`    | The average value of `CI3a3` (in-degree)|
| `CI3a31-2`    | The average value of `CI3a3` (out-degree) |
| `CI3a32-1`    | The minimum value of `CI3a3` (in-degree) |
| `CI3a32-2`    | The maximum value of `CI3a3` (in-degree)  |
| `CI3a32-3`    | The minimum value of `CI3a3` (out-degree) |
| `CI3a32-4`    | The maximum value of `CI3a3` (out-degree)   |
| `CI3a33-1`    | The standard deviation of `CI3a3` (in-degree)  |
| `CI3a33-2`    | The standard deviation of `CI3a3` (out-degree) |
| **`CI4`**     | **`PAI`** + **`PDI`** + **`PTI`**   |
| **`CI4a1`**   | The ratio of `CI1a1-1` to `PTIa1` |
| `CI4a11`      | The average value of `CI4a1` |
| `CI4a12-1`    | The minimum value of `CI4a1` |
| `CI4a12-2`    | The maximum value of `CI4a1` |
| `CI4a13`      | The standard deviation of `CI4a1` |
| **`CI4a2`**   | The ratio of `CI1a1-2` to `PTIa1` |
| `CI4a21`      | The average value of `CI4a2` |
| `CI4a22-1`    | The minimum value of `CI4a2` |
| `CI4a22-2`    | The maximum value of `CI4a2` |
| `CI4a23`      | The standard deviation of `CI4a2` |
| **`CI4a3`**   | The ratio of the value change between the total input token amount and in-degree to `PTIa4` | 
| `CI4a31`      | The average value of `CI4a3` |
| `CI4a32-1`    | The minimum value of `CI4a3` |
| `CI4a32-2`    | The maximum value of `CI4a3` |
| `CI4a33`      | The standard deviation of `CI4a3` |
| **`CI4a4`**   | The ratio of the value change between the total output token amount and out-degree to `PTIa4` | 
| `CI4a41`      | The average value of `CI4a4` |
| `CI4a42-1`    | The minimum value of `CI4a4` |
| `CI4a42-2`    | The maximum value of `CI4a4` |
| `CI4a43`      | The standard deviation of `CI4a4` |
| **`S1`**      | The average degree                                                                             |
| `S1-1`        | The average in-degree                                                                          |
| `S1-2`        | The standard deviation of `S1-1`                                                               |
| `S1-3`        | The average out-degree                                                                         |
| `S1-4`        | The standard deviation of `S1-3`                                                               |
| `S1-5`        | The average total degree                                                                       |
| `S1-6`        | The standard deviation of `S1-5`                                                               |
| **`S2`**      | The degree distribution                                                                        |
| `S2-1`        | The maximum in-degree of the subgraph                                                          |
| `S2-2`        | The maximum out-degree of the subgraph                                                         |
| `S2-3`        | The maximum total degree of the subgraph                                                       |
| **`S3`**      | The Pearson correlation coefficient                                                            |
| **`S4`**      | The betweenness centrality                                                                     |
| **`S5`**      | The average path                                                                               |
| **`S6`**      | The maximum diameter                                                                           |
| **`S7`**      | The closeness centrality                                                                       |
| **`S8`**      | The PageRank                                                                                   |
| **`S9`**      | The density                                                                                    |

*Note: In* `BABD-13`*, we recalculated some features by merging identical edges in the Bitcoin graph, adding these new features such as PAIa11-R1 instead of just using PAIa11-1 to the dataset.*
