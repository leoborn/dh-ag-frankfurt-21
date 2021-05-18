# dh-ag-frankfurt-21

This is the repository for the Python scripts used in the DH AG at the Institute for Japanese Studies at Frankfurt University (summer 2021).

The code assumes you have installed Python and have access to some kind of command-line environment (Terminal, iTerm, Windows PowerShell, Git Bash Shell etc.), where the following commands work:

* ```python --version```
* ```pip --version```

If these commands are recognized and executed, you're good to go!

## Preliminaries

Before running the scripts, you need to install some additional dependencies.
The required packages for all sessions are listed in _all\_requirements.txt_.
To install them, open a terminal and go to this repository's directory and run ```pip install -r all_requirements.txt```.

Note that each sub-directory for the more advanced sessions (**./scraping** and **./twitter**) also contains a _requirements.txt_ file each.
This is simply to delineate which additional libraries are used for which specific task.
For the purpose of the sessions, you only need to use the _all\_requirements.txt_ file.

We will provide all scripts as pure Pyton scripts (.py extension) as well as Jupyter notebooks (.ipynb extension), if possible.
This is to ensure that you understand how all scripts work step-by-step by using Jupyter notebooks, but also to enable you to run them as standalone programs using Python. 

The introductory script is only available as a Jupyter notebook since it only contains examples that do not constitute a standalone program.
The multi-page scraping script is only avalaible as a Python file for the reasons outlined below.
We will explore this script by reading the comments accompanying the code.

## Structure

The introductory script is in the root of this repository (the same as this file, _README.md_).
Since a full introduction into all basic concepts of Python is out of the scope of these sessions, we will focus only on the concepts and methods relevant for our specific tasks.
As stated above, each specific task we will explore, web scraping and twitter analysis, has its own sub-directory containing the relevant scripts.

### **./scraping**

We will explore two scenarios for web scraping: single-page scraping and multi-page scraping.
The former is concerned with just retrieving the information contained on one web page and will use the library _BeautifulSoup_.
The latter will demonstrate how to iterate through a web resource that contains links to other web pages; for this purpose, we use the _scrapy_ library.

Since _scrapy_ requires us to write a self-contained scraper, we cannot easily demonstrate its inner workings using Jupyter notebooks.
Therefore, the _scrapy_ script is commented extensively and we will thus explore the script following the comments before running it.

Lastly, while _scrapy_ scripts can be run in two ways, once using the ```scrapy``` command on the command-line and once as part of a standard Python script that is invoked using ```python```,
we will only present the latter form.