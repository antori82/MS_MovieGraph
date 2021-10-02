
<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">MS Movie Graph</h3>

  <p align="center">
    Building a large graph database with Python and Neo4j.
    <br />
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about">About</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The MS Movie Graph is a large Neo4j database including some of the largest resources available on the Internet concerning the Movies domain. Since we cannot re-distribute these resources, we provide the code to assemble the database once these are obtained from the official sources. Thjis version covers IMDB, Wikidata and Movielens.


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/antori82/MS_MovieGraph.git
   ```
2. Download the IMDB data at https://www.imdb.com/interfaces/ and put them in a folder named "IMDB"
3. Download the Movielens dataset and put it in a folder named "Movielens"
4. Run the tsvProcess.py script to pre-process the IMDB data
5. Set up the Neo4j connection variables and run the CreateDatabase.py script to import the IMDB data
6. Run the ImportAwards.py script to import data concering awards from Wikidata
7. Run the Import MovielensRatings.py script to import Movielens data
8. Run the ImportWikiNames.py script to import, from Wikidata, alternative names of the movies rated in Movielens





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT 
## Contact

#Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

#Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)
-->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
