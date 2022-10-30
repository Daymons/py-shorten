# py-shorten, a lightweight and easy to setup URL shortener.
py-shortener is a very lightweight Flask URL shortener, coming in at just 1.27KB, or 38 lines of code (+ database).  
It's best suitable for people who want a URL shortener that can run out of the box, as it only needs one line of setup.

# How do I set it up?
Easy. You just need to edit one line located in the `app.py`, this being `baseurl`. This is the URL you want the users to  
see when they shorten a link. For example, if you have the domain `short.it`, your `baseurl` line should look like this:  
`baseurl = "https://short.it"`. To run it, you first need to install the requirements with `pip install -r requirements.txt`.  
When this finishes, you can run the server with `python app.py`

# Contact
If you have any doubts, you can always [send me an email](mailto:me@daymons.xyz) or message me on Discord @ Daymons#7593
