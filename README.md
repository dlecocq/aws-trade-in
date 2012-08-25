Amazon Trade-In Command-Line Tool
=================================
Make queries to [Amazon Trade-In](http://www.amazon.com/Trade-In/b?ie=UTF8&node=2242532011) from the command line. Amazon has a great app
for scanning books for trade-in, but for checking eligibility periodically,
it becomes rather tedious.

The Solution
============
The books that are eligible for Amazon Trade In vary over time. And what's
more, how much certain items are worth also seem to vary over time.

With that in mind, I wanted to be able to save a list of items I'm trying to
get rid of, and then periodically check in without having to scan a bunch of
books, DVDs and so forth every time.

Usage
=====
First, you'll need credentials. The trade-in value data is retrieved through 
the Product Advertising API, and the documentation [details the credentials
you need to access it](http://docs.amazonwebservices.com/AWSECommerceService/latest/DG/CHAP_GettingSetUp.html). They are:

    - API Access ID
    - API Secret Key
    - Associate ID

With those in hand, you can:

    sudo pip install aws-trade-in

This installs the command-line utility `aws-trade-in`, which can be invoked:

    aws-trade-in --access-id ... --secret-key ... --associates-id ... --dir books

The above command will recurse through the `books/` directory, looking for 
files, where each is expected to contain a list of bar code numbers (SKUs)
of books, dvds, etc. with one SKU per line:

    9780760724064
    9780786881857
    9780806961743
    9780896086289
    9780743284257
    9780452263499
    ...

Getting Bar Codes
-----------------
We made use of the [Bar-Code](http://itunes.apple.com/us/app/bar-code/id422314523?mt=8) app for iPhone since it can _email the lists of bar
codes you scan_. This made it easy to go through our books and dvds once, and
not have to type anything in ourselves.

Results
-------
It then provides a summary of which items are eligible, and if so, how much 
Amazon will give you. For example, with the number of books we have around the 
house that we're trying to slowly get rid of, we organize our books:

    books/
        bookshelf-1/
            shelf-0
            shelf-1
            shelf-2
            shelf-3
        hallway-bookshelf/
            ...

When the results are printed out, they're organized by the file they're from,
so that given the summary you can quickly find your books:

    Reading 16 skus in /..../books/bookself-1/shelf-0
        9780760724064: Not Eligible : Twentieth-Century Small Arms: ...
        9780786881857: Not Eligible : Don't Sweat the Small Stuff--a...
        9780806961743: Not Eligible : The Little Giant Book of Optic...
        9780896086289: Not Eligible : Feminism Is for Everybody: Pas...
        ...
    Reading 15 skus in /..../books/bookshelf-1/shelf-1
        ....
