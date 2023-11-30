import os
import smtplib, ssl
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
load_dotenv()

port = 465  # For SSL
# APP PASSWORD FROM YOUR GOOGLE ACCOUNT
app_pass = os.getenv('APP_PASS')
sender_email = os.getenv('SENDER_EMAIL')
# vvvvvv ENTER RECEIVER EMAILS BELOW vvvvvv
receiver_emails = ["example1@gmail.com", "example2@gmail.com"]
subject_lines = ["It's a new week!", "Here's an excellent start to your week!", "It's grind time!", "A new week, A new me!", "Did someone say Monday?", "Your weekly dose of motivation!", "The weekend is over, and the hustle is on!", "Time to change the world!"]

# API for getting the background
def getImage():
    random_page = random.randint(1, 10)
    # API KEY FROM PIXABAY
    API_key = os.getenv('API_KEY')
    response = requests.get(f"https://pixabay.com/api/?key={API_key}&q=wallpaper&per_page=50&page={random_page}&min_width=1500")
    response = response.json()
    random_imageNmber = random.randint(0, 49)
    background = response["hits"][random_imageNmber]["largeImageURL"]
    img = Image.open(requests.get(background, stream=True).raw)
    return img

# defining the text_wrap function
def text_wrap(text, font, max_width):
        """Wrap text base on specified width.
        This is to enable text of width more than the image width to be display
        nicely.
        @params:
            text: str
                text to wrap
            font: obj
                font of the text
            max_width: int
                width to split the text with
        @return
            lines: list[str]
                list of sub-strings
        """
        lines = []

        # If the text width is smaller than the image width, then no need to split
        # just add it to the line list and return
        if font.getlength(text)  <= max_width:
            lines.append(text)
        else:
            #split the line by spaces to get words
            words = text.split(' ')
            i = 0
            # append every word to a line while its width is shorter than the image width
            while i < len(words):
                line = ''
                while i < len(words) and font.getlength(line + words[i]) <= max_width:
                    line = line + words[i]+ " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

# EDITING THE TEXT OVER THE IMAGE
def writeText(x1, y1, text1):
    x, y = x1, y1
    fillcolor = "white"
    shadowcolor = "black"
    text = text1
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Regular.ttf", 90)
    # This is to add a black outline on the text for easier reading
    draw.text((x-2, y), text, font=font, fill=shadowcolor)
    draw.text((x+2, y), text, font=font, fill=shadowcolor)
    draw.text((x, y-2), text, font=font, fill=shadowcolor)
    draw.text((x, y+2), text, font=font, fill=shadowcolor)
    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x, y), text, font=font, fill=fillcolor)

# API for getting the quote + author
responseQuote = requests.get("https://zenquotes.io/api/random")
responseQuote = responseQuote.json()

quote = "\"" + responseQuote[0]["q"] + "\""
author = "- " + responseQuote[0]["a"]


# ---- FINAL PROCEDURE FOR IMAGE ----
try:
    # Setting dimensions for textwrap
    img = getImage()
    width = 1500
    img_w = img.size[0]
    img_h = img.size[1]
    wpercent = (width/float(img_w))
    hsize = int((float(img_h)*float(wpercent)))
    img = img.resize((width,hsize), Image.Resampling.LANCZOS)
    lines = text_wrap(quote, ImageFont.truetype("Roboto-Regular.ttf", 90), 1300)
    y = 100
    # PRINT OUT EACH LINE TO INCORPORATE TEXTWRAP
    for line in lines:
        writeText(100, y, line) # Text lines for the quote
        y += 100

    writeText(100, (y + 150), author) # Text for the author
    img.save("MotivationalQuote.png")
except:
    img = getImage()
    width = 1500
    img_w = img.size[0]
    img_h = img.size[1]
    wpercent = (width/float(img_w))
    hsize = int((float(img_h)*float(wpercent)))
    img = img.resize((width,hsize), Image.Resampling.LANCZOS)
    lines = text_wrap(quote, ImageFont.truetype("Roboto-Regular.ttf", 90), 1400)
    y = 100
    for line in lines:
        writeText(100, y, line) # Text lines for the quote
        y += 100

    writeText(100, (y + 150), author) # Text for the author
    img.save("MotivationalQuote.png")

# Iterate through receiver emails and send a seperate email for each
for email in receiver_emails:
    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = random.choice(subject_lines)
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content("""\
    This is a message sent by MondayMotivationalMail! An attachment of a motivational quote is included, provided by ZenQuotes API and Pixabay API.
    """)

    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    quote_cid = make_msgid()
    msg.add_alternative("""\
    <html>
    <head></head>
    <body>
        <p>This Monday's Motivational Quote:</p>
        <br/>
        <img src="cid:{quote_cid}" />
        <br/>
        <p>Background images provided by <a href="https://pixabay.com/">Pixabay API</a></p>
        <p>Inspirational quotes provided by <a href="https://zenquotes.io/" target="_blank">ZenQuotes API</a></p>
    </body>
    </html>
    """.format(quote_cid=quote_cid[1:-1]), subtype='html')
    # note that we needed to peel the <> off the msgid for use in the html.

    # Now add the related image to the html part.
    with open("MotivationalQuote.png", 'rb') as img:
        msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                        cid=quote_cid)

    # Send the message via local SMTP server.
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, app_pass)
        # Send email here
        server.send_message(msg)
