# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

# r = requests.get("http://github.com")
# html = r.text.encode("utf-8")
# with open("text.html","wb") as f:
#     f.write(html)
#
# soup = BeautifulSoup(html,"html.parser")
# soup.prettify()
#
# # Getting all the links in the html
# # for each in soup.find_all("a"):
# #     print(each.get("href"))
#
# # soup = BeautifulSoup('<b class="boldest">Extremely bold</b>',"html.parser")

# # Accessing tag in the html = > a = anchor, b= bold,etc
# tag = soup.a
# print(tag)

# # Accessing attribute of the tag => Treat it as a dict
# # A tag may have any number of attributes. The tag <b id="boldest"> has an attribute “id” whose value is “boldest”.
# # You can access a tag’s attributes by treating the tag like a dictionary:
# print(tag["class"])
# print(tag["href"])

# # Adding attributes to the tag
# tag["test"] = "This is a test"
# print(tag["test"])

# # Accessing all the attributes of the tag by accessing the dictionary
# print(tag.attrs)

# # Multi-value attributes (E.g class, etc) => Each Dom object can have multiple classes
# #  Beautiful Soup presents the value(s) of a multi-valued attribute as a list:
# css_soup = BeautifulSoup("<p class='body'></p>","html.parser")
# print(css_soup.p["class"])
# css_soup2 = BeautifulSoup("<p class='body strikeout first'></p>","html.parser")
# print(css_soup2.p["class"])
#
# # If an attribute looks like it has more than one value, but it’s not a multi-valued attribute as defined by any
# # version of the HTML standard, Beautiful Soup will leave the attribute alone:
# id_soup = BeautifulSoup("<p id='my id'></p>","html.parser")
# print(id_soup.p["id"])
#
# # When you turn a tag back into a string, multiple attribute values are consolidated:
# rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>',"html.parser")
# print(rel_soup.a["rel"])
# rel_soup.a["rel"] = ["index","content","first"]
# print(rel_soup.a["rel"])

# # You can use `get_attribute_list to get a value that’s always a list, string, whether or not it’s a multi-valued atribute
# print(rel_soup.a.get_attribute_list("rel"))
# # If you parse a document as XML, there are no multi-valued attributes:
# xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
# xml_soup.p['class']

# Navigable Strings
# soup = BeautifulSoup('<b class="boldest">Extremely bold</b>',"html.parser")
# tag = soup.b
# # use string to access the text within a tag
# print(tag.string)
# print(type(tag.string))
# # You can convert a NavigableString to a Unicode string with unicode():
# # unicode_string = unicode(tag.string)
#
# # You can’t edit a string in place, but you can replace one string with another, using replace_with():
# tag.string.replace_with("Mildly bold")
# print(tag.string)

# # Comments and other special strings
# markup = "<b><!- Wassup y'all!! --></b>"
# soup = BeautifulSoup(markup,"html.parser")
# comment = soup.b.string
# print(comment)
# print(type(comment))
#
# # The Comment object is just a special type of NavigableString:
# # But when it appears as part of an HTML document, a Comment is displayed with special formatting:
# print(soup.b.prettify())

# Navigating the tree
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

# Navigating use tag name
# Use .head ot get the <head> tag, .title pt get the <title> tag , etc
print(soup.head)
print(soup.title)

# This code gets the FIRST <b> tag in body
print(soup.body.b)

# To get all the tags, we can use methods like find_all():
print(soup.find_all("a"))

# .contents AND .children
#A tag's children are available in a list called .contents
head_tag = soup.head
print(head_tag)
print(head_tag.contents)
print(head_tag.contents[0])
body_tag = soup.body
print(body_tag)
print(body_tag.contents)
print(body_tag.contents[1])

# # The html tag is a children of the BeautifulSoup object
# # A string does not have .contents because it can't contain anything
title_tag = head_tag.contents[0]
# text = title_tag.contents[0]
# print(text.contents)

# Instead of getting the children a a list, we can iterate over them using the .children generator
for child in body_tag.children:
    print("Child: " + str(child))

# .descendants
# The .contents and .children attributes only considers a tag's direct children
# The .descendants tag lets us iterate over all the tag's children recursively
# => direct children,children of direct children,etc

# title is the child of the head tag, while "The Dormouse's story" is the child of title
print(head_tag.contents)
# Iterating over all the descendants
for each in head_tag.descendants:
    print(each)
# The <head> tag has only one child, but it has two descendants: the <title> tag and the <title> tag’s child.
# The BeautifulSoup object only has one direct child (the <html> tag), but it has a whole lot of descendants:
print(len(list(soup.children)))
print(len(list(soup.descendants)))

# .string
# If a tag only has 1 child, and the child is a NavigableString,the child is made available as .string
print(title_tag)
print(title_tag.string)
# If a tag only child is another tag,and THAT tag has a .string, then the parent tag is made available as .string
print(head_tag)
print(head_tag.string)
# If a tag contains more than 1 thing, .string does not know what ot do so it returns None
print(soup.html.string)


# .strings AND .stripped_strings
# If there is more than 1 thing in a tag, we can still look at the strings using the .strings generator
print(".strings and .stripped_strings")
print(".strings")
for string in soup.strings:
    print(repr(string))
# .stripped_strings removes all excess whitespace
# =>E.g Strings consisting solely of whitespace & whitespace at beg and end of strings are removed
print(".stripped_strings")
for string in soup.stripped_strings:
    print(repr(string))

# .parent
print(".parent")
# .parent goes 1 level up => parent of <title> is <head>
print(title_tag.parent)
# parent of a top level tag like the <html> tag is the BeautifulSoup object itself
print(type(soup.html.parent))
# parent of the BeautifulSoup object is none
print(soup.parent)
# .parents

# You can iterate over all of an element’s parents with .parents.
# This example uses .parents to travel from an <a> tag buried deep within the document, to the very top of the document
print(".parents")
link = soup.a
print(link)
for parent in link.parents:
    if parent is None:
        print(parent)
    else:
        print("This is the parent : " + parent.name)
        print(parent)

# Going sideways
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>","html.parser")
print("Going sideways - siblings")
print(sibling_soup.prettify())

# .next_sibling and .previous_sibling is used to navigate between page elements on the same level of the parse tree
# next sibling of <b> is <c>
print(sibling_soup.b.next_sibling)
# previous sibling of <c> is <b>
print(sibling_soup.c.previous_sibling)
# <b> has no previous sibling because nothing comes before it
print(sibling_soup.b.previous_sibling)
# <c> has no next sibling because nothing comes after it
print(sibling_soup.c.next_sibling)
# text 1 & text 2 are not siblings because they do not share the same parent
print(sibling_soup.b.string.next_sibling)
print(sibling_soup.c.string.previous_sibling)

# In real documents, the .next_sibling or .previous_sibling of a tag will usually be a string containing whitespace.
# next sibling of link is not the next <a> tag but the comma and newline
print(repr(link.next_sibling))

# We can iterate over all the siblings with .next_siblings OR .previous_siblings
print(".next siblings iteration")
for sibling in link.next_siblings:
    print(repr(sibling))

# Going back and forth
# <html><head><title>The Dormouse's story</title></head>
# <p class="title"><b>The Dormouse's story</b></p>
# An HTML parser takes this string of characters and turns it into a series of events: “open an <html> tag”,
# “open a <head> tag”, “open a <title> tag”, “add a string”, “close the <title> tag”, “open a <p> tag”, and so on.
    # Beautiful Soup offers tools for reconstructing the initial parse of the document.

# The .next element points to whatever was parsed immediately afterwards.
# It might be the same thing as .next_sibling but is usually drastically different
last_a_tag = soup.find("a", id="link3")
print(".next element")
print(last_a_tag) ## => <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
# Item returned by next_sibling is  # => '; and they lived at the bottom of a well.'
print(last_a_tag.next_sibling)
# But the element parsed immediately afterwards is Tillie
# That’s because in the original markup, the word “Tillie” appeared before that semicolon.
# The parser encountered an <a> tag, then the word “Tillie”, then the closing </a> tag, then the semicolon and
# rest of the sentence. The semicolon is on the same level as the <a> tag, but the word “Tillie” was encountered first.
print(last_a_tag.next_element) # => Tillie
# previous_element is the opposite of next_element
print(last_a_tag.previous_element)

# .next_elements AND .previous_elements iterates through all the next and previous elements respectively
for each in last_a_tag.previous_elements:
    print(repr(each))

# Searching the tree

# Filters that can be passed into .find and .find_all
# 1. String
# Pass a string to a search method and Beautiful Soup will perform a match against that exact string.
# This code finds all the <b> tags in the document:
# NOTE:If you pass in a byte string, Beautiful Soup will assume the string is encoded as UTF-8.
# You can avoid this by passing in a Unicode string instead.
print("\n\nSearching the tree \n\n")
print(soup.find_all("a"))

# 2.Regular expression
# This code finds all the tags whose names start with b E.g <body> and <b>
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

# 3.A list
# If a list is passed in, BeautifulSoup will return matches against ANY item in the list
print(soup.find_all(["a","b","p"]))

# 4. True
# The value True makes BeautifulSoup matches everything it can.
# This code finds all the tags in the html but none of the text strings
print("\n\nTrue\n\n")
print(soup.find_all(True))

# 5.A Function
# define a function that takes an element as its only argument.
# The function should return True if the argument matches, and False otherwise.

def has_class_but_no_tag(tag):
    return tag.has_attr("class") and not tag.has_attr("id")
print("\n\nFunction\n\n")
print(soup.find_all(has_class_but_no_tag))

# If you pass in a function to filter on a specific attribute like href, the argument passed into the function will
# be the attribute value, not the whole tag. Here’s a function that finds all a tags whose href attribute does not
# match a regular expression:
def not_lacie(href):
    return href and not re.compile("lacie").search(href)
print("HREF => NOT LACIE")
print(soup.find_all(href=not_lacie))

# Function that returns true if a tag is surrounded by string
def surrounded_by_strings(tag):
    return (isinstance(tag.next_element,NavigableString) and isinstance(tag.previous_element,NavigableString))
print("\n\nSurrounded by strings\n\n")
for tag in soup.find_all(surrounded_by_strings):
    print(tag.name)

# Search Methods
# find_all(name, attrs, recursive, string, limit, **kwargs)
# The find_all() method looks through a tag’s descendants and retrieves all descendants that match your filters.

# name argument
# Pass in a value for name and you’ll tell Beautiful Soup to only consider tags with certain names.
# Text strings will be ignored, as will tags whose names that don’t match.
# Values for name can be a string,list,function,regex or the value True

print(soup.find_all("title")) #Prints the title tag

# keywords arguments
# any arguments that are not recognised will be turned into a filter for one of a tag's attributes
# This code below filters based on a tag's id attribute
print(soup.find_all(id="link1"))
# passing in the href attribute will filter against a tag's href attribute
print(soup.find_all(href="http://example.com/lacie"))

# attributes can be filtered based on strings,lists,functions or the value True
# This code below filters and returns all tags whose id attribute has a value regardless of what value it is
print(soup.find_all(id=True))

# we can filter multiple attibutes at once by passing in more than one keyword argument
print(soup.find_all(href="http://example.com/lacie",id="link2"))
# some attributes, like the data-* attributes in HTML 5, have names that can’t be used as the names of keyword arguments:
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>',"html.parser")
# print(data_soup.find_all(data-foo="value")) # => Does not work
# You can use these attributes in searches by putting them into a dictionary and passing the dictionary into find_all() as the attrs argument:
print(data_soup.find_all(attrs={"data-foo" : "value"}))

# Searching by CSS class => use the keyword class_ as class is a reserved keyword in python
print("SEARCHING BY CSS CLASS")
print(soup.find_all(class_="sister"))
# We can pass class_ a string,list,function or the value True
print(soup.find_all(class_=re.compile("itl")))
print(soup.find_all(class_=True))
def has_six_chars(css_class):
    return css_class is not None and len(css_class) == 6
print(soup.find_all(class_=has_six_chars))

# CSS classes can have multiple values for its class attributes

css_soup = BeautifulSoup('<p class="body strikeout"></p>',"html.parser")
# When we search for a ag that matches a certain CSS class we're matching against ANY of the class
print(css_soup.find_all("p", class_="strikeout"))
print(css_soup.find_all("p", class_="body"))
# We can also search for the exact string attribute of the class
print(css_soup.find_all(class_="body strikeout"))
# however, the order cannot be mixed up
print(css_soup.find_all(class_="strikeout body"))
# If you want to search for tags that match two or more CSS classes, you should use a CSS selector:
print(css_soup.select("p.strikeout.body"))

# The string argument
# With string you can search for strings instead of tags. As with name and the keyword arguments,
# you can pass in a string, a regular expression, a list, a function, or the value True.
print("THE STRING ARGUMENT")
print(soup.find_all(string="Elsie"))
# finding the parent of the string matched
for each in soup.find_all(string="Elsie"):
    print("Parent:" + str(each.parent))
# Passing in a list
print(soup.find_all(string=["Tillie","Elsie","Lacie"]))

# Passing in a regex
print(soup.find_all(string=re.compile("Dormouse")))
# Passing in a function
def is_the_only_string_within_a_tag(s):
    # Return true if this string is the only childof its parent tag
    return(s == s.parent.string)
print(soup.find_all(string=is_the_only_string_within_a_tag))
# Although string is for finding strings, you can combine it with arguments that find tags:
# Beautiful Soup will find all tags whose .string matches your value for string.
# This code finds the <a> tags whose .string is “Elsie”:
print(soup.find_all("a",string="Elsie"))

# The limit argument
# There are three links in the soup, but this code only finds the first two:
print(soup.find_all("a",limit=2))

# The recursive argument
# When we call mytag.find_all(), BeautifulSoup examines all the descendants of mytag.If we want to only examine the
# direct descendants, we set recursive=False
print("RECURSIVE ARGUMENT")
print(soup.html.find_all("a"))
print(soup.html.find_all("a",recursive=False))
# NOTE: find_all() and find() are the only methods that support the recursive argument

# Calling a tag is like calling find_all
# The following lines of code are equivalent
print(soup.find_all("a"))
print(soup("a"))
# The following lines of code are also equivalent
print(soup.title.find_all(string=True))
print(soup.title(string=True))

# .find()
# .find_all() and .find() are nearly equivalent with the difference being:
# 1.find_all() returns a list containing the results while find() returns the result
# 2.if find_all() finds nothing, it returns an empty list while find() returns None
print(soup.find("title"))
print(soup.find("nosuchtag"))

# .parent and .parents()
# These are similiar to find() and find_all() except they work in different directions
# E.g find() & find_all() works downwards, looking through descendants while parent() & parents() work upwards
# looking through parents
print(".parent() and .parents()")
a_string = soup.find(string="Lacie")
print(a_string)
print(a_string.find_parents("a"))
print(a_string.find_parent("p"))
print(a_string.find_parents("p", class_="title"))

# .find_next_siblings() & .find_next_sibling()
# These methods use .next_siblings to iterate over the rest of an element’s siblings in the tree.
# The find_next_siblings() method returns all the siblings that match, and find_next_sibling() only returns the first
first_link = soup.a
print(".find_next_sibling() & .find_next_siblings()")
print(first_link)
print(first_link.find_next_siblings("a"))
first_story_paragraph = soup.p
print(first_story_paragraph)
print(first_story_paragraph.find_next_sibling("p"))

# .find_previous_sibling() & .find_previous_siblings()
# Same as .find_next_sibling() & .find_next_siblings() but works in the opposite direction


# .find_all_next() & .find_next()
# These methods use .next_elements to iterate over whatever tags and strings that come after it in the document.
# The find_all_next() method returns all matches, and find_next() only returns the first match:
print(first_link.find_all_next(string=True))
print(first_link.find_next("p"))
# Note:In the first example, the string “Elsie” showed up, even though it was contained within the <a> tag we started
# from. In the second example, the last <p> tag in the document showed up, even though it’s not in the same part of
# the tree as the <a> tag we started from. For these methods, all that matters is that an element match the filter,
# and show up later in the document than the starting element.

# .find_previous() & .find_all_previous()
# same as .find_next() & .find_all_next() but works in the opposite direction

# CSS Selectors
# BeautifulSoup supports the most commonly used CSS Selectors,just pass a sting into the .select() method of a
# BeautifulSoup object or the Tag object itself
print("CSS Selectors")
# We can find tags
print(soup.select("title"))
print(soup.select("p:nth-of-type(3)"))
# Find tags beneath other tags
print(soup.select("head title"))
print(soup.select("body a"))
# Find tage DIRECTLY beneath other tags
print(soup.select("p > a:nth-of-type(2)"))
print(soup.select("p > a"))
print(soup.select("html > head > title"))
# find the siblings of tags
print(soup.select("#link1 ~ .sister"))
print(soup.select("#link1 + .sister"))
# Find tags by CSS class
print(soup.select(".sister"))
print(soup.select("[class~=sister]"))
# Find tags by ID
print(soup.select("#link1"))
# Find tags that match any selector by a list of selectors
print(soup.select("#link1,#link3"))
# Test for the existence of an attribute
print(soup.select("a[href]"))
# Find tags by attribute value
