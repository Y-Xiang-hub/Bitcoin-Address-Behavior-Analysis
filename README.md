# BABD Construction and Analysis

*NOTE: WE WILL UPLOAD A COMPLETE APPENDIX AFTER OUR PAPER IS ACCEPTED.*

This project is the source code of our dataset [BABD-13](https://www.kaggle.com/datasets/lemonx/babd13) on Kaggle. The research paper of this project can be found on [BABD: A Bitcoin Address Behavior Dataset for Pattern Analysis](https://arxiv.org/abs/2204.05746). If you find our work is helpful for your research, please consider citing it as:

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
The results of the feature extraction module are stored in .csv files. However, for further analyzing the data, it is necessary to preprocess the current data by `functions_csv_preprocess.py` in `preprocess_csv` folder.

## Data Analysis
We use the tools and models provided by [scikit-learn](https://scikit-learn.org/) and [xgboost](https://xgboost.ai/) to analyze and study our data, the code can be seen in `feature_selection.py` and `machine_learning.py` in `data_analysis` folder. The specific analysis of our dataset can be found in our [paper](https://arxiv.org/abs/2204.05746). Additionally, we also propose a method to divide the testing set and training set while considering the even assignment of strong label address and weak label address in `split_train_test.py` that is completed by Tiantian Li ([@oopshell](https://github.com/oopshell)).

## Additional Notes
In `format` folder, `csv_format.yml` is the header of raw feature data .csv files and `original_ledger_format.json` is an example of the Bitcoin ledger we use. In addition, `networkx_test_version.py` in `networkx_test` folder is the testing code of our designed methods implemented by [NetworkX](https://networkx.org/) that can only utilize for tests on small graphs.

## Credits
The project was mainly completed by Ding Bao ([@whbyaoi](https://github.com/whbyaoi)), Yuchen Lei ([@TooYoungTooSimp](https://github.com/TooYoungTooSimp)), and Yuexin Xiang ([@Y-Xiang-hub](https://github.com/Y-Xiang-hub)).

- Ding Bao finished most of the code for the metrics, both in terms of amount and complexity. Not only that, but he also wrote efficient crawlers to fulfill the need of building the dataset presented in the paper and examined the collected data in detail.
- Yuchen Lei authored the core module, directed parallelization improvements, fixed some bugs in the code, and proposed several helpful pieces of advice for machine-learning-based classification.
- Yuexin Xiang wrote the original version of the Bitcoin ledger collection tool and graph initialization and finished machine-learning-powered data analysis including but not limited to preprocessing.

## Contact Information
If you have any questions please feel free to contact me by e-mail at yuexin.xiang@cug.edu.cn

## Appendix (Partial)
| Feature       | Description                                                                                    |
| --------------| ---------------------------------------------------------------------------------------------- |
| **`PAIa1`**   | The input/output token amount of an address node.                                              |
| `PAIa11-1`    | The total input token amount of an address node.                                               |
| `PAIa11-2`    | The total output token amount of an address node.                                              |
| `PAIa12`      | The difference of `PAIa11-1` and `PAIa11-2`.                                                   |
| `PAIa13`      | The ratio of `PAIa11-1` and `PAIa11-2`.                                                        |
| `PAIa14-1`    | The minimum input token amount of an address node.                                             |
| `PAIa14-2`    | The maximum input token amount of an address node.                                             |
| `PAIa14-3`    | The minimum output token amount of an address node.                                            |
| `PAIa14-4`    | The maximum output token amount of an address node.                                            |
| `PAIa15-1`    | The difference of `PAIa14-2` and `PAIa14-1`.                                                   |
| `PAIa15-2`    | The difference of `PAIa14-4` and `PAIa14-3`.                                                   |
| `PAIa16-1`    | The ratio of `PAIa15-1` and `PAIa14-2`.                                                        |
| `PAIa16-2`    | The ratio of `PAIa15-2` and `PAIa14-4`.                                                        |
| `PAIa17-1`    | The standard deviation of all input token amounts of an address node.                          |
| `PAIa17-2`    | The standard deviation of all output token amounts of an address node.                         |
| `PAIa17-3`    | The standard deviation of all input and output token amounts of an address node.               |
| **`PAIa2`**   | The ratio of each input (output) token amount and `PAIa11-1` (`PAIa11-2`) token amount         |
| `PAIa21-1`    | The ratio of `PAIa14-1` and `PAIa11-1`                                                         |
| `PAIa21-2`    | The ratio of `PAIa14-2` and `PAIa11-1`                                                         |
| `PAIa21-3`    | The ratio of `PAIa14-3` and `PAIa11-2`                                                         |
| `PAIa21-4`    | The ratio of `PAIa14-4` and `PAIa11-2`                                                         |
| `PAIa22-1`    | The standard deviation of the ratio of each input token amount and `PAIa11-1`                  |
| `PAIa22-2`    | The standard deviation of the ratio of each output token amount and `PAIa11-2`                 |
| **`PDIa`**    | The degree of an address node                                                                  |
| `PDIa1-1`     | The in-degree of an address node                                                               |
| `PDIa1-2`     | The out-degree of an address node                                                              |
| `PDIa1-3`     | The total degree of an address node                                                            |
| `PDIa11-1`    | The ratio of `PDIa1-1` and `PDIa1-3`                                                           |
| `PDIa11-2`    | The ratio of `PDIa1-2` and `PDIa1-3`                                                           |
| `PDIa11-3`    | The ratio of `PDIa1-1` and `PDIa1-2`                                                           |
| `PDIa11-4`    | The difference of `PDIa1-1` and `PDIa1-2`                                                      |
| ...     | ...                                                         |





