# BABD Construction and Analysis

*NOTE: WE WILL UPLOAD THE CORE CODE AFTER OUR PAPER IS ACCEPTED.*

This project is the source code of our dataset [BABD-13](https://www.kaggle.com/datasets/lemonx/babd13) on Kaggle. The research paper of this project can be found on [BABD: A Bitcoin Address Behavior Dataset for Address Behavior Pattern Analysis](https://arxiv.org/abs/2204.05746). If you find our work is helpful for your research, please consider citing it as:

    @article{xiang2022babd,
      title={BABD: A Bitcoin Address Behavior Dataset for Address Behavior Pattern Analysis},
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

 
## Data Collection
In the `data_collection folder`, `Bitcoin_Ledger_Reader_V3.1.py` is used for collecting Bitcoin ledger data from [BTC.com](https://btc.com/). And `labeled_data_API.py` is used for collecting Bitcoin labeled addresses from [WalletExplorer](https://www.walletexplorer.com/) that is completed by Qingqing Yang ([@Vinedou](https://github.com/Vinedou)) . Here we would like to thank [Aleš Janda](http://www.alesjanda.cz/) for his generous help.
 
## Graph Generation
To generate a Bitcoin transaction graph from raw Bitcoin ledger data, it is necessary to select the attributes needed for the following analysis steps first that can be found in `graph_generation.py`. Then we use `graph_generation.py` to generate the Bitcoin transaction graph that is implemented by [graph-tool](https://graph-tool.skewed.de/).

## Feature Extraction
In this process, we need to extract the required features from the generated Bitcoin transaction graph for the concrete labeled Bitcoin addresses. There are two kinds of features we are concerned about in this work that are **statistical features** and **local structural features**.

The methods to extract statistical features and structural features can be found in `moduleG.py`. Then, we run the code in `data_extraction.ipynb` to extract features. Specifically, we need to read the generated Bitcoin transaction graph first through the *read the graph* cell. After finishing reading the graph, we can compute the statistical features and local structural features respectively in different cells. The only difference between these two types of features is that we have to generate a subgraph before extracting local structural features. Besides, in order to accelerate the speed of feature extraction, we apply the parallel computing approach here.
 
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
- Yuexin Xiang wrote the original version of the Bitcoin ledger collection tool and graph initialization, and finished machine-learning-powered data analysis including but not limited to preprocessing.

## Contact Information
If you have any questions please feel free to contact me by e-mail yuexin.xiang@cug.edu.cn
