# ODU-REU Summer Research
This repository contains all of my work from the 2023 Summer REU program at Old Dominion University. During this time I worked with ODU faculty and members of VMASC to develop a large language model that could be used to ascertain Russian 
disinformation from articles pertaining to the Russia v. Ukraine War. I recieved advising under the wonderful Erika Frydenlund alongside my inspiring research partner Iryna Zhuchenko.

I had roughly two months to work on this project with things shifting into gear about a month in once Iryna and I decided to go forward with plans of developing a language model. We gathered 100 articles from [EU vs. Disinfo](https://euvsdisinfo.eu/disinformation-cases/),
manually classified and translated each article, and compiled it into a dataset. Our model was tested and trained with Spacy. Article text was gathered using a "universal" web crawler I designed for pulling text; it was inefficient and required manual cleaning.

You may find other files in this repository that pertain to some early Twitter bot development I was going to conduct, as well as web crawlers and data cleaning I did to assist my lab mates. Sorry for the mess, it was a busy summer!

### Credits
**Advisor:** [Erika Frydenlund](https://www.linkedin.com/in/efrydenlund/)

**Research Partner:** [Iryna Zhuchenko](https://www.linkedin.com/in/iryna-zhuchenko-0a6135265/)

**Team Lead:** [Jose Padilla](https://www.linkedin.com/in/jose-j-padilla-1624224a/)

**Graduate Student:** [Joseph Martinez](https://www.linkedin.com/in/josephmars/)

**Graduate Student:** [Brian Llinas](https://www.linkedin.com/in/brian-jesus-llinas-marimon/)

## Results
![Most common Disinfo words](/Disinfo_Words.png)

![Most common Proinfo words](/Proinfo_Words.png)

Our model was able to achieve [53% accuracy](https://github.com/adammartin13/ODU-REU/blob/main/Test%20100%20examples.txt), albeit riddled with many errors, and even then isn't great when considering that the model is merely saying "Yes/No" to if a given article
is disinformation given the articles text as input. I believe this is largely due to my poor implementation of the Spacy tokenizer, as not only are stop words not removed, but some symbols are still making it through to the testing/training set.
## Approach
Articles were gathered from the [EU vs. Disinfo](https://euvsdisinfo.eu/disinformation-cases/) database and added to [our own](https://github.com/adammartin13/ODU-REU/blob/main/Disinformation_Training_Data.csv), which was then passed through our 
[web scraper](https://github.com/adammartin13/ODU-REU/blob/main/article_crawler.py). I didn't have time to iron out custom scrapers for each website we pulled from, so this was a quicker approach while we manually removed excess HTML/JS after. 

The text was then [translated](https://github.com/adammartin13/ODU-REU/blob/main/translator.py) via Google Translator, which was validated by Iryna who was fluent in Russian, before tokenized for Spacy's model. You can find the scripts for the
[tokenization](https://github.com/adammartin13/ODU-REU/blob/main/spacyPreTraining.py), [training](https://github.com/adammartin13/ODU-REU/blob/main/spacyTraining.py), and [testing](https://github.com/adammartin13/ODU-REU/blob/main/spacyTest.py).
## Data
Our pre-balanced [data](https://github.com/adammartin13/ODU-REU/blob/main/Disinformation_Training_Data.csv) consisted of links to articles, flags for specific content of the article, and the translated article text. These flags were largely unused due to the time constraints of
the project, but were based on common tropes Iryna and I found when reading through articles. The flag used for categorizing our text was the disinformation flag, which we labeled based on where the article was coming from.
## Conclusions
This project was not only a matter of trying to learn how to put an LLM together, but actually doing so while also gathering the data for it over the course of roughly a month. Since my time at ODU I've continued to work on my research with Iryna and we hit
the ground running with going about new ways for training a new model. More data, more thorough research into our articles, more article collection and scraping automation, building our own tokenization tools, trying different model approaches, etc.. Working
with Iryna and the VMASC team inspired me to keep working on this project, and this repository acts as a reminder of where it started, what I managed to do in so little time, and how far I've improved.
## ODU VMASC Team
![VMASC Team](/VMASC.jpeg)

This was one of the greatest team projects I've ever worked on. I look back fondly at the time I've spent with everyone in the office and wish everyone the best. It was an innovative, challenging, friendly, and honest atmosphere that I hope to make proud
through my future iterations of this project and all other work I conduct in the future.
