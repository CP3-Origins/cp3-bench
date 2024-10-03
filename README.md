# Python for CP3 Bench

This benchmark tool easily allows users to easily run a dataset across multiple symbolic
regression algorithms or methods. The supported algorithms are mentioned in the credits section.

## Gettings started

We offer two methods for using cp3-bench:

1. Manual installation on Ubuntu
2. Automated installation with Docker

First we go through the manual steps and then introduce the automated installation with docker.
The advantage of doing the manual installation is that you do not need docker, but you will 
need admin privileges and ensure that your `pyenv` is configured correctly and initialized. The advantage of Docker
is that we ensure that everything is correctly setup out of the box.

## Manual installation

This sections how you would install cp3-bench on a Ubuntu. It is key to the **success** of this procedure
that you correctly install and initialize `pyenv` and the virtual environments.

### Prerequisites

**NOTE**: This tool currently runs only on Ubuntu. However, some algorithms may work on 
other operating systems. For Windows users we recommend running Windows Subsystems for 
Linux (WSL) and you may consider using the Docker installation. For this to work you also need admin privileges.

To run this bench you need Ubunuty 22.04 or newer, Python 3.10 or newer, `pip`, and [pyenv](https://github.com/pyenv/pyenv). 
On Ubuntu the `pyenv` dependencies can  be installed by: 
```shell
sudo apt update
sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

`pyenv` can then be installed using:
```shell
curl https://pyenv.run | bash
```
**Note:** Remember to set pyenv to PATH otherwise this package will not work correctly. 
This can be done doing something like:

```shell
WARNING: seems you still have not added 'pyenv' to the load path.

Load pyenv automatically by adding
the following to ~/.bashrc:

export PATH="$HOME/.pyenv/bin:$PATH"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
You can check the version selected using:

```shell
pyenv versions
```

### Installation steps

To install cp3-bench start by cloning the repository with SSH:

```shell
git clone git@github.com:CP3-Origins/cp3-bench.git
```

or with HTTPS:

```shell
git clone https://github.com/CP3-Origins/cp3-bench.git
```

Then install the Python dependencies:
```shell
pip install -r requirements.txt
```

To install all benchmark methods:

```shell
python bench/install.py
```
Optional flags: `--methods` and `--reinstall`. Use `--help` for details.

The first flag allows you to select what methods you want to install, default is to install all methods.
The second flag allows you  to reinstall a method which can be useful if the install went wrong,
possible due to `pyenv` being improbably configured.

The status of the installation can be found in the `STATUS.md` file in the `bench` folder.
This will help give an overview over which packages are installed, and details on what 
install steps have failed, in case a method failed to install correctly.

Before using the package ensure `pyenv` is initialized, which can be done by these commands:

```shell
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

docker build . -t cp3-bench --build-arg METHODS=ffx
docker run -it cp3-bench

## Automated installation

This section explains how to get started with cp3-bench using Docker. If you want to learn more check out 
this [101 tutorial](https://www.docker.com/101-tutorial/). This technology allows for the creation of an image
which is setup with all necessities for using cp3-bench - abstracting away the installation steps.

### Prerequisites

This installation method requires Docker which can be run on all common operating systems such as macOS, Ubuntu, Windows (via WSL). The installation steps for Docker can be found [here](https://docs.docker.com/engine/install/).

### Installation steps

To install cp3-bench with Docker you first need to build the image. This can be done with the build command:

```shell
docker build . -t cp3-bench
```

**Note:** that this uses the tag flag `-t` to name the build `cp3-bench` which is a convinient way to label different builds. You can name it as you want or in principle leave out the tag.

The default is to install all cp3-bench with all methods, but we allow for a build argument to select a subset
of methods to be installed using the following command:

```shell
docker build . -t cp3-bench --build-arg METHODS=ffx,gpg
```
Here you can set `METHODS` equal to the comma separated list of methods you want to install. This `build` command creates the image of fully functional system with all dependencies set and it will take some time to
complete. Note that this image will be +10 GB in size for a full build. 

To use the image you created with build you simply run:

```shell
docker run -it cp3-bench
```

This is will spin up a container based on your image and mount your terminal to that of the container. You can type `exit` (maybe a few times) to leave the container. In this container you install other methods if needed or run benchmarks as you feel like.

## Usage of the package

This package is intended to be used as a benchmark engine which is called by another script.
After installing the scripts you need, it is intended that you call the `bench/evalute_dataset.py`
with valid path to a `.csv` file with a column named `target` which is the expected output value,
and all other columns are assumed to be input parameters.

In `tests/utils` there is a short example `.csv` file used for testing which specifies the expected 
file format. 

Alternatively, you can interact with it directly via CLI like:

```shell
python bench/evaluate_dataset.py --data_path <path_to_dataset>
```
Optional flag: `--methods`. This flag selects which models to use, default is all.

This has the primary limitation that you cannot run multiple datasets at once.

If you want to tune the parameters of the models, you can do that by going to `bench/methods` and
from here navigate to the algorithm for a given model and change the parameters in the constructor
of the `procedure.py` file.

The results of the benchmark can be found in the results folder, which will be generated after the 
first run.

## Troubleshooting

There are a few known issues that could cause errors related to `pyenv`, which is a
key element of this benchmark tool.

- If you get failures relating to installation, initialization of virtual environments,
and creation of the environments, then check that `pyenv` is correctly installed.
- If you get `ImportModelError` in the tests, it might be because you have not set
  paths correctly for `pyenv` or initialized `pyenv`.

## Contribution

We invite the community to further develop this codebase. You can either work on improvements of the 
framework as mentioned in the list below:

- [ ] Ensure that all classes have the `output_format` function, and that they all output the expression

  in the same style.
  - [ ] Enable a unified simplification procedure e.g. using SymPy to simplify the equation and allow 
    for a SymPy compatible output.
  - [ ] Allow the algorithm to report the MSE from the final output expression as an option.
- [ ] Add new algorithms.
- [ ] Fix Genetic Programming limitations on the DSO and uDSR algorithms.
- [ ] Improve the implementation of AI-Feynman including improving the multi-core capabilities.
- [ ] Improve hyperparameter tuning.
- [ ] Make a template for adding new algorithms.

All improvements are to be done via a pull request to the main branch. This will then be reviewed 
by the code owners.

If you add new algorithms they must pass the general tests. 
Remember to update the tests if you change the functioning of parts of the code base to ensure 
that the functionality of the update is also covered. General tests can be found in the `tests` folder
and tests for the symbolic algorithm is set in the algorithm folder.

You can report bugs and suggestions via email or create an issue where you describe the problem or
suggestion.

# Citation

If you want to use `cp3-bench` please cite:
```
@misc{thing2024cp3bench,
      title={cp3-bench: A tool for benchmarking symbolic regression algorithms tested with cosmology}, 
      author={Mattias E. Thing and Sofie M. Koksbang},
      year={2024},
      eprint={2406.15531},
      archivePrefix={arXiv},
      primaryClass={astro-ph.IM},
      url={https://arxiv.org/abs/2406.15531}, 
}
```

# Credits

This packages builds on the work of many authors who have created various of different
machine learning symbolic regression models. In this section we link to the 
different authors of the packages we use. Currently, we have implemented:

- ITEA
  - Name: Interaction-Transformation Evolutionary Algorithm
  - [GitHub link](https://github.com/folivetti/ITEA/)
  - .bibtex:
    ```
    @article{10.1162/evco_a_00285,
        author = {de Franca, F. O. and Aldeia, G. S. I.},
        title = "{Interaction-Transformation Evolutionary Algorithm for Symbolic Regression}",
        journal = {Evolutionary Computation},
        pages = {1-25},
        year = {2020},
        month = {12},    
        issn = {1063-6560},
        doi = {10.1162/evco_a_00285},
        url = {https://doi.org/10.1162/evco\_a\_00285},
        eprint = {https://direct.mit.edu/evco/article-pdf/doi/10.1162/evco\_a\_00285/1888497/evco\_a\_00285.pdf},
    }
    ```
- QLattice
  - Name: QLattice Clinical Omics
  - [GitHub link](https://github.com/abzu-ai/QLattice-clinical-omics)
  - .bibtex:
    ```
    @article{10.1093/bioinformatics/btac405,
        author = {Christensen, Niels Johan and Demharter, Samuel and Machado, Meera and Pedersen, Lykke and Salvatore, Marco and Stentoft-Hansen, Valdemar and Iglesias, Miquel Triana},
        title = "{Identifying interactions in omics data for clinical biomarker discovery using symbolic regression}",
        journal = {Bioinformatics},
        volume = {38},
        number = {15},
        pages = {3749-3758},
        year = {2022},
        month = {06},  issn = {1367-4803},
        doi = {10.1093/bioinformatics/btac405},
        url = {https://doi.org/10.1093/bioinformatics/btac405},
        eprint = {https://academic.oup.com/bioinformatics/article-pdf/38/15/3749/49884306/btac405.pdf},
    }
    ```
- GPZGD
  - name: gpzgd
  - [GitHub link](http://github.com/grantdick/gpzgd)
  - .bibtex:
    ```
    @inproceedings{10.1145/3377930.3390237,
        author = {Dick, Grant and Owen, Caitlin A. and Whigham, Peter A.},
        title = {Feature Standardisation and Coefficient Optimisation for Effective Symbolic Regression},
        year = {2020},
        isbn = {9781450371285},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3377930.3390237},
        doi = {10.1145/3377930.3390237},
        abstract = {Symbolic regression is a common application of genetic programming where model structure and corresponding parameters are evolved in unison. In the majority of work exploring symbolic regression, features are used directly without acknowledgement of their relative scale or unit. This paper extends recent work on the importance of standardisation of features when conducting symbolic regression. Specifically, z-score standardisation of input features is applied to both inputs and response to ensure that evolution explores a model space with zero mean and unit variance. This paper demonstrates that standardisation allows a simpler function set to be used without increasing bias. Additionally, it is demonstrated that standardisation can significantly improve the performance of coefficient optimisation through gradient descent to produce accurate models. Through analysis of several benchmark data sets, we demonstrate that feature standardisation enables simple but effective approaches that are comparable in performance to the state-of-the-art in symbolic regression.},
        booktitle = {Proceedings of the 2020 Genetic and Evolutionary Computation Conference},
        pages = {306–314},
        numpages = {9},
        keywords = {feature standardisation, genetic programming, symbolic regression, gradient descent},
        location = {Canc\'{u}n, Mexico},
        series = {GECCO '20}
    }
    ```
- GeneticEngine
  - Name: Genetic Engine
  - [GitHub link](http://github.com/alcides/GeneticEngine)
  - .bibtex:
    ```
    @inproceedings{espada2022data,
       author={Guilherme Espada and Leon Ingelse and Paulo Canelas and Pedro Barbosa and Alcides Fonseca},
       editor    = {Bernhard Scholz and Yukiyoshi Kameyama},
       title = {Datatypes as a More Ergonomic Frontend for Grammar-Guided Genetic Programming},
       booktitle = {{GPCE} '22: Concepts and Experiences, Auckland, NZ, December 6 - 7, 2022},
       pages     = {1},
       publisher = {{ACM}},
       year      = {2022},
    }
    ```
- PySR
  - Name: PySR 
  - [GitHub link](https://github.com/MilesCranmer/PySR)
  - .bibtex:
    ```
    @misc{cranmer2023interpretable,
       title={Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl}, 
       author={Miles Cranmer},
       year={2023},
       eprint={2305.01582},
       archivePrefix={arXiv},
       primaryClass={astro-ph.IM}
    }
    ```
- DSO
  - Name: Deep Symbolic Optimization
  - [GitHub link](https://github.com/dso-org/deep-symbolic-optimization)
  - .bibtex:
    ```
    @inproceedings{petersen2021deep,
       title={Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients},
       author={Petersen, Brenden K and Landajuela, Mikel and Mundhenk, T Nathan and Santiago, Claudio P and Kim, Soo K and Kim, Joanne T},
       booktitle={Proc. of the International Conference on Learning Representations},
       year={2021}
    }
    @inproceedings{mundhenk2021seeding,
      title={Symbolic Regression via Neural-Guided Genetic Programming Population Seeding},
      author={T. Nathan Mundhenk and Mikel Landajuela and Ruben Glatt and Claudio P. Santiago and Daniel M. Faissol and Brenden K. Petersen},
      booktitle={Advances in Neural Information Processing Systems},
      year={2021}
    }
    ```
- uDSR
  - Name: Unified Deep Symbolic Regression
  - [GitHub link](https://github.com/dso-org/deep-symbolic-optimization)
  - .bibtex:
    ```
    @inproceedings{petersen2021deep,
       title={Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients},
       author={Petersen, Brenden K and Landajuela, Mikel and Mundhenk, T Nathan and Santiago, Claudio P and Kim, Soo K and Kim, Joanne T},
       booktitle={Proc. of the International Conference on Learning Representations},
       year={2021}
    }
    @inproceedings{landajuela2022unified,
       title={A Unified Framework for Deep Symbolic Regression},
       author={Mikel Landajuela and Chak Lee and Jiachen Yang and Ruben Glatt and Claudio P. Santiago and Ignacio Aravena and Terrell N. Mundhenk and Garrett Mulcahy and Brenden K. Petersen},
       booktitle={Advances in Neural Information Processing Systems},
       year={2022}
    }
    ```
- FFX
  - Name: Fast Function Extraction
  - [GitHub link](https://github.com/natekupp/ffx/tree/master)
  - .bibtex:
    ```
    @inbook{McConaghy2011,
       author="McConaghy, Trent",
       editor="Riolo, Rick and Vladislavleva, Ekaterina and Moore, Jason H.",
       title="FFX: Fast, Scalable, Deterministic Symbolic Regression Technology",
       bookTitle="Genetic Programming Theory and Practice IX",
       year="2011",
       publisher="Springer New York",
       address="New York, NY",
       pages="235--260",
       isbn="978-1-4614-1770-5",
       doi="10.1007/978-1-4614-1770-5_13",
       url="https://doi.org/10.1007/978-1-4614-1770-5_13"
    }
    ```
- DSR
  - Name: Deep symbolic regression
  - [GitHub link](https://github.com/lacava/deep-symbolic-regression)
  - .bibtex:
    ```
    @inproceedings{petersen2021deep,
       title={Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients},
       author={Brenden K Petersen and Mikel Landajuela Larma and Terrell N. Mundhenk and Claudio Prata Santiago and Soo Kyung Kim and Joanne Taery Kim},
       booktitle={International Conference on Learning Representations},
       year={2021},
       url={https://openreview.net/forum?id=m5Qsh0kBQG}
    }
    ```
- AI-Feynman
  - Name: AI-Feynman
  - [GitHub link](https://github.com/lacava/AI-Feynman/)
  - .bibtex:
    ```
    @article{udrescu2020ai,
       title={AI Feynman: A physics-inspired method for symbolic regression},
       author={Udrescu, Silviu-Marian and Tegmark, Max},
       journal={Science Advances},
       volume={6},
       number={16},
       pages={eaay2631},
       year={2020},
       publisher={American Association for the Advancement of Science}
    }
    @article{udrescu2020ai,
       title={AI Feynman 2.0: Pareto-optimal symbolic regression exploiting graph modularity},
       author={Udrescu, Silviu-Marian and Tan, Andrew and Feng, Jiahai and Neto, Orisvaldo and Wu, Tailin and Tegmark, Max},
       journal={arXiv preprint arXiv:2006.10782},
       year={2020}
    }
    ```
- GPG
  - Name: gpg
  - [GitHub link](https://github.com/marcovirgolin/gpg)
  - .bibtex:
    ```
    @article{virgolin2021improving,
      title={Improving model-based genetic programming for symbolic regression of small expressions},
      author={Virgolin, Marco and Alderliesten, Tanja and Witteveen, Cees and Bosman, Peter A. N.},
      journal={Evolutionary Computation},
      volume={29},
      number={2},
      pages={211--237},
      year={2021},
      publisher={MIT Press}
    }
    ```

- Operon
  - Name: Operon
  - [GitHub link](https://github.com/heal-research/pyoperon/)
  - .bibtex:
    ```
    @inproceedings{10.1145/3377929.3398099,
        author = {Burlacu, Bogdan and Kronberger, Gabriel and Kommenda, Michael},
        title = {Operon C++: An Efficient Genetic Programming Framework for Symbolic Regression},
        year = {2020},
        isbn = {9781450371278},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3377929.3398099},
        doi = {10.1145/3377929.3398099},
        booktitle = {Proceedings of the 2020 Genetic and Evolutionary Computation Conference Companion},
        pages = {1562–1570},
        numpages = {9},
        keywords = {symbolic regression, genetic programming, C++},
        location = {Canc\'{u}n, Mexico},
        series = {GECCO '20}
    }
    ```

This work is inspired by and uses a limited number of features from [SRBench](https://github.com/cavalab/srbench/):
```
@misc{lacava2021contemporary,
   title={Contemporary Symbolic Regression Methods and their Relative Performance}, 
   author={William La Cava and Patryk Orzechowski and Bogdan Burlacu and Fabrício Olivetti de França and Marco Virgolin and Ying Jin and Michael Kommenda and Jason H. Moore},
   year={2021},
   eprint={2107.14351},
   archivePrefix={arXiv},
   primaryClass={cs.NE}
}
```
