web-crawler:
This project is created to crawl those hyperlinks for definitions in a wikipedia page. In order to reduce running time, only five links 
will be randomly selected in each page.
In the first layer, crawl the target page and randomly get 5 hyperlinks;
In the second layer, crawl the 5 parent hyperlinks and randomly get 5 child hyperlinks from each, which is 25 hyperlinks;
In the next layer, do the same thing. And this can keep going on and on.
