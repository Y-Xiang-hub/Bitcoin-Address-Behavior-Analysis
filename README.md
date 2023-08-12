![image](https://github.com/Y-Xiang-hub/Bitcoin-Address-Behavior-Analysis/assets/57489506/231a57ec-e998-4233-8c7a-f8a23d490299)# BABD Construction and Analysis

*NOTE: WE WILL UPLOAD A COMPLETE APPENDIX AFTER OUR PAPER IS ACCEPTED.*

This project is the source code of our dataset [BABD-13](https://www.kaggle.com/datasets/lemonx/babd13) on Kaggle. The research paper of this project can be found on [BABD: A Bitcoin Address Behavior Dataset for Pattern Analysis](https://arxiv.org/abs/2204.05746). If you find our work helpful for your research, please consider citing it as:

    @article{xiang2022babd,
      title={BABD: A Bitcoin Address Behavior Dataset for Pattern Analysis},
      author={Xiang, Yuexin and Lei, Yuchen and Bao, Ding and Ren, Wei and Li, Tiantian and Yang, Qingqing and Liu, Wenmao and Zhu, Tianqing and Choo, Kim-Kwang Raymond},
      journal={arXiv preprint arXiv:2204.05746},
      year={2022}
    }
    
## Contents

- [Data Collection](#data-collection)
- [Graph Generation](#graph-generation)
- [Feature Extraction](#feature-extraction)
- [Data Preprocess](#data-preprocess)
- [Data Analysis](#data-analysis)
- [Additional Notes](#additional-notes)
- [Credits](#credits)
- [Contact Information](#contact-information)
- [Appendix](#appendix)

 
## Data Collection
In the `data_collection folder`, `Bitcoin_Ledger_Reader_V3.1.py` is used for collecting Bitcoin ledger data from [BTC.com](https://btc.com/). And `labeled_data_API.py` is used for collecting Bitcoin labeled addresses from [WalletExplorer](https://www.walletexplorer.com/) that is completed by Qingqing Yang ([@Vinedou](https://github.com/Vinedou)). Here we would like to thank [Aleš Janda](http://www.alesjanda.cz/) for his generous help.
 
## Graph Generation
To generate a Bitcoin transaction graph from raw Bitcoin ledger data, it is necessary to select the attributes needed for the following analysis steps first which can be found in `graph_generation.py`. Then we use `graph_generation.py` to generate the Bitcoin transaction graph that is implemented by [graph-tool](https://graph-tool.skewed.de/).

## Feature Extraction
In this process, we need to extract the required features from the generated Bitcoin transaction graph for the concrete labeled Bitcoin addresses. There are two kinds of features we are concerned about in this work that are **statistical features** and **local structural features**.

The methods to extract statistical features and structural features can be found in `moduleG.py`. Then, we run the code in `data_extraction.ipynb` to extract features. Specifically, we need to read the generated Bitcoin transaction graph first through the *read the graph* cell. After reading the graph, we can compute the statistical and local structural features in different cells. The only difference between these two types of features is that we have to generate a subgraph before extracting local structural features. Besides, in order to accelerate the speed of feature extraction, we apply the parallel computing approach here.
 
## Data Preprocess
The results of the feature extraction module are stored in .csv files. However, for further analyzing the data, it is necessary to preprocess the current data by `functions_csv_preprocess.py` in the `preprocess_csv` folder.

## Data Analysis
We use the tools and models provided by [scikit-learn](https://scikit-learn.org/) and [xgboost](https://xgboost.ai/) to analyze and study our data, the code can be seen in `feature_selection.py` and `machine_learning.py` in `data_analysis` folder. The specific analysis of our dataset can be found in our [paper](https://arxiv.org/abs/2204.05746). Additionally, we also propose a method to divide the testing set and training set while considering the even assignment of strong label address and weak label address in `split_train_test.py` that is completed by Tiantian Li ([@oopshell](https://github.com/oopshell)).

## Additional Notes
In the `format` folder, `csv_format.yml` is the header of raw feature data .csv files, and `original_ledger_format.json` is an example of the Bitcoin ledger we use. In addition, `networkx_test_version.py` in the `networkx_test` folder is the testing code of our designed methods implemented by [NetworkX](https://networkx.org/) that can only utilize for tests on small graphs.

## Credits
The project was mainly completed by Ding Bao ([@whbyaoi](https://github.com/whbyaoi)), Yuchen Lei ([@TooYoungTooSimp](https://github.com/TooYoungTooSimp)), and Yuexin Xiang ([@Y-Xiang-hub](https://github.com/Y-Xiang-hub)).

- Ding Bao finished most of the code for the metrics, both in terms of amount and complexity. Not only that, but he also wrote efficient crawlers to fulfill the need of building the dataset presented in the paper and examined the collected data in detail.
- Yuchen Lei authored the core module, directed parallelization improvements, fixed some bugs in the code, and proposed several helpful pieces of advice for machine-learning-based classification.
- Yuexin Xiang wrote the original version of the Bitcoin ledger collection tool and graph initialization and finished machine-learning-powered data analysis including but not limited to preprocessing.

## Contact Information
If you have any questions please feel free to contact me by e-mail at yuexin.xiang@cug.edu.cn

## Appendix 
| Feature       | Description                                                                                    |
| --------------| ---------------------------------------------------------------------------------------------- |
| **`PAI`** | The pure amount indicator                          |
| **`PAIa1`** | The input/output token amount of an address node                       |
| `PAIa11-1`  | The total input token amount of an address node                              |
| `PAIa11-2`  | The total output token amount of an address node                           |
| `PAIa12`     | The difference between `PAIa11-1` and `PAIa11-2`                    |
| `PAIa13`    | The ratio of `PAIa11-1` to `PAIa11-2`                                   |
| `PAIa14-1`  | The minimum input token amount of an address node                       |
| `PAIa14-2`   | The maximum input token amount of an address node                        |
| `PAIa14-3`   | The minimum output token amount of an address node                       |
| `PAIa14-4`   | The maximum output token amount of an address node                          |
| `PAIa15-1`   | The difference between `PAIa14-2` and `PAIa14-1`                |
| `PAIa15-2`    | The difference between `PAIa14-4` and `PAIa14-3`                       |
| `PAIa16-1`    | The ratio of `PAIa15-1` to `PAIa14-2`.                                           |
| `PAIa16-2`    | The ratio of `PAIa15-2` to `PAIa14-4`.                                          |
| `PAIa17-1`    | The standard deviation of all input token amounts of an address node.             |
| `PAIa17-2`    | The standard deviation of all output token amounts of an address node.            |
| `PAIa17-3`    | The standard deviation of all input and output token amounts of an address node.      |
| **`PAIa2`**   | The ratio of each input (output) token amount and `PAIa11-1` (`PAIa11-2`) token amount    |
| `PAIa21-1`    | The ratio of `PAIa14-1` to `PAIa11-1`                                                     |
| `PAIa21-2`    | The ratio of `PAIa14-2` to `PAIa11-1`                                            |
| `PAIa21-3`    | The ratio of `PAIa14-3` to `PAIa11-2`                                         |
| `PAIa21-4`    | The ratio of `PAIa14-4` to `PAIa11-2`                                         |
| `PAIa22-1`    | The standard deviation of the ratio of each input token amount and `PAIa11-1`                  |
| `PAIa22-2`    | The standard deviation of the ratio of each output token amount and `PAIa11-2`                 |
| **`PDIa`**    | The degree of an address node                                                                  |
| `PDIa1-1`     | The in-degree of an address node                                                               |
| `PDIa1-2`     | The out-degree of an address node                                                              |
| `PDIa1-3`     | The total degree of an address node                                                            |
| `PDIa11-1`    | The ratio of `PDIa1-1` to `PDIa1-3`                                                            |
| `PDIa11-2`    | The ratio of `PDIa1-2` to `PDIa1-3`                                                            |
| `PDIa12`      | The ratio of `PDIa1-1` to `PDIa1-2`                                                            |
| `PDIa13`      | The difference between `PDIa1-1` and `PDIa1-2`                                                 |
| **`PTIa1`**   | The lifecycle of an address node - the difference between the earliest and the latest active time |
| **`PTIa2`**   | The active period of an address node - the number of active days during the lifecycle          |
| `PTIa21`      | The ratio of `PTIa2` to `PTIa1`                                                                |
| **`PTIa3`**   | The number of active instances for each day in the active period of an address node            |
| `PTIa31-1`    | The maximum number of active instances of an address node                                      |
| `PTIa31-2`    | The minimum number of active instances of an address node                                      |
| `PTIa31-3`    | The average number of active instances of an address node                                      |
| `PTIa32`      | The difference between `PTIa31-1` and `PTIa31-2`                                               |
| `PTIa33`      | The standard deviation of the number of active instances of an address node                    |
| **`PTIa4`**   |   Each transaction time interval for the address node in chronological order  |
| `PTIa41-1`    | The maximum transaction time interval of an address node      |
| `PTIa41-2`    | The minimum transaction time interval of an address node      |
| `PTIa41-3`    | The average transaction time interval of an address node      |
| `PTIa42`    | The difference between `PTIa41-1` and `PTIa41-2`    |
| `PTIa43`    | The standard deviation of the transaction time interval of an address node       |
| **`CI1a`**| **`PAI`** + **`PDI`** |

| **`...`**| ...  |
| `...`    |  ...   |


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






