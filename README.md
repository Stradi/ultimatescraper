# Ultimate Scraper

This is the second version of the comic scraper. It is a complete rewrite of the original scraper writter in TypeScript, which can be found [here](https://www.github.com/Stradi/comic-scraper).

This project is mainly used in [UltimateComics](https://www.ultimatecomics.com).

## Features

The scraper scrapes websites, extracts comics and stores them in a database.

I am still working on more great features. Here are some of the features that I want to implement:

- [x] [ViewComics](https://viewcomics.me) support
- [ ] [ReadComicOnline](https://readcomiconline.li) support
- [ ] [ReadComicsOnline](https://readcomicsonline.ru) support
- [ ] [ComicExtra](https://comicextra.com) support
- [ ] Scrape single comic by providing name
- [x] Scrape single comic by providing URL
- [ ] Scrape all comics from a genre
- [ ] Scrape all comics from a publisher
- [ ] Scrape all comics from a author
- [ ] Remove watermark from images
- [ ] Upload scraped images to a cloud storage

## Installation

Since this is a Python project, you need to have Python installed on your system. You can download it [here](https://www.python.org/downloads/).

After you have installed Python, copy this repository to your computer and navigate to the directory.

The preferred way is to generate a Virtual Environment before installing dependencies via `pip`. You can learn more about Virtual Environment for Python in [here](https://docs.python.org/3/library/venv.html).

### Create a Virtual Environment using `venv`

While you are in the main directory of this repository, run the following command:

```bash
python -m venv venv
```

This will create a folder called `venv`. After creating virtual environment, you need to activate it. `venv` folder contains another folder called `Scripts`. In there you will find scripts to activate and deactivate virtual environment. You need to run the `activate` script according to your operating system.

#### Windows

For Windows, run the following command:

```bash
venv\Scripts\activate
```

If you are using Powershell, run the following command:

```powershell
venv\Scripts\Activate.ps1
```

#### Linux

For Linux, run the following command:

```bash
source venv/bin/activate
```

#### MacOS

For MacOS, run the following command:

```bash
source venv/bin/activate
```

### Installing Dependencies

After activating the virtual environment, you need to install the dependencies. You can do that by running the following command:

```bash
pip install -r requirements.txt
```

This will install all the required dependencies to your virtual environment.

## Usage

Before using the scraper, you need to fill some information in the `.env` file. The sample `.env` file is provided in the repository. You can copy it and rename it to `.env`.

### `.env` file

The `.env` file contains the following information:

- `HOST`: The host of the _MySQL_ database.
- `USER`: The username of the _MySQL_ database.
- `PASSWORD`: The password of the _MySQL_ database.
- `DATABASE`: The name of the _MySQL_ database.
- `SSL_CERT`: This is mainly for _PlanetScale_ database. It defaults to the file at `cacert.pem` located in the root directory of this repository. You can leave it empty if you are not using _PlanetScale_.

### Running the Scraper

To use the scraper, you need to run `Scrapy CLI` commands. You can learn more about Scrapy CLI in [here](https://docs.scrapy.org/en/latest/topics/commands.html).

For example, to run _ViewComics_ scraper, you need to run the following command:

```bash
python -m scrapy crawl ViewComics
```

This will scrape ViewComics website and save all the processed items in the database.
