# Basic Libraries
import re
import json
# External Libraries
from bs4 import BeautifulSoup


def clean_sentence_spellcheck(
        text: str,
        #regex: str = "([\(\)\{\}\@\#\*\-\"])",
        replace_price: bool = False,
        replace_number: bool = False,
        all_lowercase: bool = False
):
    """Function to clean a text"""
    # remove non printable characters
    review_text = text.encode('ascii', errors='ignore')

    # remove HTML
    review_text = BeautifulSoup(review_text, "lxml").get_text()

    # replace numeric price indicator
    if replace_price:
        review_text = re.sub('(\$[0-9]+(\.[0-9]*)?)', ' price_r ', review_text)

    # replace numbers
    if replace_number:
        review_text = re.sub('([0-9]+(\.[0-9]*)?)', ' number_r ', review_text)

    # replace price indicator $
    if replace_price:
        review_text = re.sub('(\$)', ' price_r ', review_text)

    # replace = with equals
    #review_text = review_text.replace("=", " equals ")

    # replace % with percent
    #review_text = review_text.replace("%", " percent ")

    # replace & with and
    # = review_text.replace("&", " and ")

    # replace + with plus
    review_text = review_text.replace("+", " plus ")

    # replace w/ with with
    review_text = review_text.replace("w/", " with ")

    # replace w/o with without
    review_text = review_text.replace("w/o", " without ")

    # clean using regex
    #review_text = re.sub(regex, " ", review_text)

    # replace ;
    review_text = re.sub('\;+', ' ; ', review_text)

    # replace :
    review_text = re.sub('\:+', ' : ', review_text)

    # replace ,
    review_text = re.sub('\,+', ' , ', review_text)

    # replace !
    review_text = re.sub('\!+', ' ! ', review_text)

    # replace ?
    review_text = re.sub('\?+', ' ? ', review_text)

    # replace repeated .
    review_text = re.sub('\.+', ' . ', review_text)

    # replace repeated .
    review_text = re.sub('\/+', ' / ', review_text)
    
    #without replacing using regex 
    # replace (
    review_text = re.sub('\(+', ' ( ', review_text)
    # replace )
    review_text = re.sub('\)+', ' ) ', review_text)
    # replace {
    review_text = re.sub('\{+', ' { ', review_text)
    # replace }
    review_text = re.sub('\}+', ' } ', review_text)
    # replace @
    review_text = re.sub('\@+', ' @ ', review_text)
    # replace #
    review_text = re.sub('\#+', ' # ', review_text)
    # replace *
    review_text = re.sub('\*+', ' * ', review_text)
    # replace -
    review_text = re.sub('\-+', ' - ', review_text)
    # replace "
    review_text = re.sub('\"+', ' " ', review_text)
    # replace =
    review_text = re.sub('\=+', ' = ', review_text)
    # replace %
    review_text = re.sub('\%+', ' % ', review_text)
    # replace &
    review_text = re.sub('\&+', ' & ', review_text)


    # convert to lower case
    if all_lowercase:
        review_text = review_text.lower()

    return ' '.join(review_text.split())


def clean_sentence_correct(
        text: str,
):
    """Function to clean a text"""
    # remove non printable characters
    review_text = text.encode('ascii', errors='ignore')

    # remove HTML
    review_text = BeautifulSoup(review_text, "lxml").get_text()

    # replace ;
    review_text = re.sub(' \;', ';', review_text)
    review_text = re.sub('\;+', ';', review_text)

    # replace :
    review_text = re.sub(r'(?<=\d) \: (?=\d)', ":", review_text)  # numbers
    review_text = re.sub(' \:', ':', review_text)
    review_text = re.sub('\:+', ':', review_text)

    # replace ,
    review_text = re.sub(' \,', ',', review_text)
    review_text = re.sub('\,+', ',', review_text)

    # replace !
    review_text = re.sub(' \!', '!', review_text)
    review_text = re.sub('\!+', '!', review_text)

    # replace ?
    review_text = re.sub(' \?', '?', review_text)
    review_text = re.sub('\?+', '?', review_text)
    
    #without replacing using regex 
    # replace (
    review_text = re.sub('\(+', '(', review_text)
    review_text = re.sub(' \(', '(', review_text)
    # replace )
    review_text = re.sub('\)+', ')', review_text)
    review_text = re.sub(' \)', ')', review_text)
    # replace {
    review_text = re.sub('\{+', '{', review_text)
    review_text = re.sub(' \{', '{', review_text)
    # replace }
    review_text = re.sub('\}+', '}', review_text)
    review_text = re.sub(' \}', '}', review_text)
    # replace @
    review_text = re.sub('\@+', '@', review_text)
    review_text = re.sub(' \@', '@', review_text)
    # replace #
    review_text = re.sub('\#+', '#', review_text)
    review_text = re.sub(' \#', '#', review_text)
    # replace *
    review_text = re.sub('\*+', '*', review_text)
    review_text = re.sub(' \*', '*', review_text)
    # replace -
    review_text = re.sub('\-+', '-', review_text)
    review_text = re.sub(' \-', '-', review_text)
    # replace "
    review_text = re.sub('\"+', '"', review_text)
    review_text = re.sub(' \"', '"', review_text)
    # replace =
    review_text = re.sub('\=+', '=', review_text)
    review_text = re.sub(' \=', '=', review_text)
    # replace %
    review_text = re.sub('\%+', '%', review_text)
    review_text = re.sub(' \%', '%', review_text)
    # replace &
    review_text = re.sub('\&+', '&', review_text)
    review_text = re.sub(' \&', '&', review_text)

    # replace repeated .
    review_text = re.sub('^\.', '', review_text)  # start
    review_text = re.sub(' \.$', '.', review_text)  # end
    review_text = re.sub(r'(?<=\d) \. (?=\d)', ".", review_text)  # numbers
    review_text = re.sub(r" \. ", ". ", review_text)  # sentence space
    review_text = re.sub(r"([a-zA-Z])\. ([a-zA-Z]) ?\.", "\\1.\\2.", review_text)  # abbreviations
    review_text = re.sub('\.+', '.', review_text)

    # replace repeated .
    review_text = re.sub(' / ', '/', review_text)

    # Replace single characters except i and a and numbers
    #review_text = re.sub(r'((?<= )[^iaIA0-9$;:,!?\.\'](?= |$))', " ", review_text)

    return ' '.join(review_text.split())
