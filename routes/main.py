from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Form
from lib.converter import convert_from_pdf_to_text
from lib.connectS3 import get_s3_client
from config.env import get_env
from botocore.exceptions import ClientError
from lib.createBucket import create_bucket

router = APIRouter(prefix="/v1")

async def hello(name: str):
    return {"name": name, "message": "hello, world!"}

@router.get("/")
async def display():
    text = convert_from_pdf_to_text()
    return text

@router.post("/upload")
async def upload_pdf(pdf: UploadFile = File(...), query: str = Form(...), difficulty: str = Form(...)):
    return """
    This page intentionally left blank

Foreword
One of our favorite candies here in Denmark is Ga-Jol, whose strong licorice vapors are a
perfect complement to our damp and often chilly weather. Part of the charm of Ga-Jol to
us Danes is the wise or witty sayings printed on the ﬂap of every box top. I bought a twopack of the delicacy this morning and found that it bore this old Danish saw:
Ærlighed i små ting er ikke nogen lille ting.
“Honesty in small things is not a small thing.” It was a good omen consistent with what I
already wanted to say here. Small things matter. This is a book about humble concerns
whose value is nonetheless far from small.
God is in the details, said the architect Ludwig mies van der Rohe. This quote recalls
contemporary arguments about the role of architecture in software development, and particularly in the Agile world. Bob and I occasionally ﬁnd ourselves passionately engaged in
this dialogue. And yes, mies van der Rohe was attentive to utility and to the timeless forms
of building that underlie great architecture. On the other hand, he also personally selected
every doorknob for every house he designed. Why? Because small things matter.
In our ongoing “debate” on TDD, Bob and I have discovered that we agree that software architecture has an important place in development, though we likely have different
visions of exactly what that means. Such quibbles are relatively unimportant, however,
because we can accept for granted that responsible professionals give some time to thinking and planning at the outset of a project. The late-1990s notions of design driven only by
the tests and the code are long gone. Yet attentiveness to detail is an even more critical
foundation of professionalism than is any grand vision. First, it is through practice in the
small that professionals gain proﬁciency and trust for practice in the large. Second, the
smallest bit of sloppy construction, of the door that does not close tightly or the slightly
crooked tile on the ﬂoor, or even the messy desk, completely dispels the charm of the
larger whole. That is what clean code is about.
Still, architecture is just one metaphor for software development, and in particular for
that part of software that delivers the initial product in the same sense that an architect
delivers a pristine building. In these days of Scrum and Agile, the focus is on quickly
bringing product to market. We want the factory running at top speed to produce software.
These are human factories: thinking, feeling coders who are working from a product backlog or user story to create product. The manufacturing metaphor looms ever strong in such
thinking. The production aspects of Japanese auto manufacturing, of an assembly-line
world, inspire much of Scrum.
xix

xx

Foreword

Yet even in the auto industry, the bulk of the work lies not in manufacturing but in
maintenance—or its avoidance. In software, 80% or more of what we do is quaintly called
“maintenance”: the act of repair. Rather than embracing the typical Western focus on producing good software, we should be thinking more like home repairmen in the building
industry, or auto mechanics in the automotive ﬁeld. What does Japanese management have
to say about that?
In about 1951, a quality approach called Total Productive Maintenance (TPM) came
on the Japanese scene. Its focus is on maintenance rather than on production. One of the
major pillars of TPM is the set of so-called 5S principles. 5S is a set of disciplines—and
here I use the term “discipline” instructively. These 5S principles are in fact at the foundations of Lean—another buzzword on the Western scene, and an increasingly prominent
buzzword in software circles. These principles are not an option. As Uncle Bob relates in
his front matter, good software practice requires such discipline: focus, presence of mind,
and thinking. It is not always just about doing, about pushing the factory equipment to produce at the optimal velocity. The 5S philosophy comprises these concepts:

• Seiri, or organization (think “sort” in English). Knowing where things are—using
approaches such as suitable naming—is crucial. You think naming identiﬁers isn’t
important? Read on in the following chapters.
• Seiton, or tidiness (think “systematize” in English). There is an old American saying:
A place for everything, and everything in its place. A piece of code should be where
you expect to ﬁnd it—and, if not, you should re-factor to get it there.
• Seiso, or cleaning (think “shine” in English): Keep the workplace free of hanging
wires, grease, scraps, and waste. What do the authors here say about littering your
code with comments and commented-out code lines that capture history or wishes for
the future? Get rid of them.
• Seiketsu, or standardization: The group agrees about how to keep the workplace clean.
Do you think this book says anything about having a consistent coding style and set of
practices within the group? Where do those standards come from? Read on.
• Shutsuke, or discipline (self-discipline). This means having the discipline to follow the
practices and to frequently reﬂect on one’s work and be willing to change.
If you take up the challenge—yes, the challenge—of reading and applying this book,
you’ll come to understand and appreciate the last point. Here, we are ﬁnally driving to the
roots of responsible professionalism in a profession that should be concerned with the life
cycle of a product. As we maintain automobiles and other machines under TPM, breakdown maintenance—waiting for bugs to surface—is the exception. Instead, we go up a
level: inspect the machines every day and ﬁx wearing parts before they break, or do the
equivalent of the proverbial 10,000-mile oil change to forestall wear and tear. In code,
refactor mercilessly. You can improve yet one level further, as the TPM movement innovated over 50 years ago: build machines that are more maintainable in the ﬁrst place. Making your code readable is as important as making it executable. The ultimate practice,
introduced in TPM circles around 1960, is to focus on introducing entire new machines or

Foreword

xxi

replacing old ones. As Fred Brooks admonishes us, we should probably re-do major software chunks from scratch every seven years or so to sweep away creeping cruft. Perhaps
we should update Brooks’ time constant to an order of weeks, days or hours instead of
years. That’s where detail lies.
There is great power in detail, yet there is something humble and profound about this
approach to life, as we might stereotypically expect from any approach that claims Japanese roots. But this is not only an Eastern outlook on life; English and American folk wisdom are full of such admonishments. The Seiton quote from above ﬂowed from the pen of
an Ohio minister who literally viewed neatness “as a remedy for every degree of evil.”
How about Seiso? Cleanliness is next to godliness. As beautiful as a house is, a messy
desk robs it of its splendor. How about Shutsuke in these small matters? He who is faithful
in little is faithful in much. How about being eager to re-factor at the responsible time,
strengthening one’s position for subsequent “big” decisions, rather than putting it off? A
stitch in time saves nine. The early bird catches the worm. Don’t put off until tomorrow
what you can do today. (Such was the original sense of the phrase “the last responsible
moment” in Lean until it fell into the hands of software consultants.) How about calibrating the place of small, individual efforts in a grand whole? Mighty oaks from little acorns
grow. Or how about integrating simple preventive work into everyday life? An ounce of
prevention is worth a pound of cure. An apple a day keeps the doctor away. Clean code
honors the deep roots of wisdom beneath our broader culture, or our culture as it once was,
or should be, and can be with attentiveness to detail.
Even in the grand architectural literature we ﬁnd saws that hark back to these supposed details. Think of mies van der Rohe’s doorknobs. That’s seiri. That’s being attentive
to every variable name. You should name a variable using the same care with which you
name a ﬁrst-born child.
As every homeowner knows, such care and ongoing reﬁnement never come to an end.
The architect Christopher Alexander—father of patterns and pattern languages—views
every act of design itself as a small, local act of repair. And he views the craftsmanship of
ﬁne structure to be the sole purview of the architect; the larger forms can be left to patterns
and their application by the inhabitants. Design is ever ongoing not only as we add a new
room to a house, but as we are attentive to repainting, replacing worn carpets, or upgrading the kitchen sink. Most arts echo analogous sentiments. In our search for others who
ascribe God’s home as being in the details, we ﬁnd ourselves in the good company of the
19th century French author Gustav Flaubert. The French poet Paul Valery advises us that a
poem is never done and bears continual rework, and to stop working on it is abandonment.
Such preoccupation with detail is common to all endeavors of excellence. So maybe there
is little new here, but in reading this book you will be challenged to take up good disciplines that you long ago surrendered to apathy or a desire for spontaneity and just
“responding to change.”
Unfortunately, we usually don’t view such concerns as key cornerstones of the art of
programming. We abandon our code early, not because it is done, but because our value
system focuses more on outward appearance than on the substance of what we deliver.

xxii

Foreword

This inattentiveness costs us in the end: A bad penny always shows up. Research, neither in
industry nor in academia, humbles itself to the lowly station of keeping code clean. Back
in my days working in the Bell Labs Software Production Research organization (Production, indeed!) we had some back-of-the-envelope ﬁndings that suggested that consistent
indentation style was one of the most statistically signiﬁcant indicators of low bug density.
We want it to be that architecture or programming language or some other high notion
should be the cause of quality; as people whose supposed professionalism owes to the
mastery of tools and lofty design methods, we feel insulted by the value that those factoryﬂoor machines, the coders, add through the simple consistent application of an indentation
style. To quote my own book of 17 years ago, such style distinguishes excellence from
mere competence. The Japanese worldview understands the crucial value of the everyday
worker and, more so, of the systems of development that owe to the simple, everyday
actions of those workers. Quality is the result of a million selﬂess acts of care—not just of
any great method that descends from the heavens. That these acts are simple doesn’t mean
that they are simplistic, and it hardly means that they are easy. They are nonetheless the
fabric of greatness and, more so, of beauty, in any human endeavor. To ignore them is not
yet to be fully human.
Of course, I am still an advocate of thinking at broader scope, and particularly of the
value of architectural approaches rooted in deep domain knowledge and software usability.
The book isn’t about that—or, at least, it isn’t obviously about that. This book has a subtler
message whose profoundness should not be underappreciated. It ﬁts with the current saw
of the really code-based people like Peter Sommerlad, Kevlin Henney and Giovanni
Asproni. “The code is the design” and “Simple code” are their mantras. While we must
take care to remember that the interface is the program, and that its structures have much
to say about our program structure, it is crucial to continuously adopt the humble stance
that the design lives in the code. And while rework in the manufacturing metaphor leads to
cost, rework in design leads to value. We should view our code as the beautiful articulation
of noble efforts of design—design as a process, not a static endpoint. It’s in the code that
the architectural metrics of coupling and cohesion play out. If you listen to Larry Constantine describe coupling and cohesion, he speaks in terms of code—not lofty abstract concepts that one might ﬁnd in UML. Richard Gabriel advises us in his essay, “Abstraction
Descant” that abstraction is evil. Code is anti-evil, and clean code is perhaps divine.
Going back to my little box of Ga-Jol, I think it’s important to note that the Danish
wisdom advises us not just to pay attention to small things, but also to be honest in small
things. This means being honest to the code, honest to our colleagues about the state of our
code and, most of all, being honest with ourselves about our code. Did we Do our Best to
“leave the campground cleaner than we found it”? Did we re-factor our code before checking in? These are not peripheral concerns but concerns that lie squarely in the center of
Agile values. It is a recommended practice in Scrum that re-factoring be part of the concept of “Done.” Neither architecture nor clean code insist on perfection, only on honesty
and doing the best we can. To err is human; to forgive, divine. In Scrum, we make everything visible. We air our dirty laundry. We are honest about the state of our code because

Foreword

xxiii

code is never perfect. We become more fully human, more worthy of the divine, and closer
to that greatness in the details.
In our profession, we desperately need all the help we can get. If a clean shop ﬂoor
reduces accidents, and well-organized shop tools increase productivity, then I’m all for
them. As for this book, it is the best pragmatic application of Lean principles to software I
have ever seen in print. I expected no less from this practical little group of thinking individuals that has been striving together for years not only to become better, but also to gift
their knowledge to the industry in works such as you now ﬁnd in your hands. It leaves the
world a little better than I found it before Uncle Bob sent me the manuscript.
Having completed this exercise in lofty insights, I am off to clean my desk.
James O. Coplien
Mørdrup, Denmark

This page intentionally left blank

(c) 2008 Focus Shift

Introduction

Reproduced with the kind permission of Thom Holwerda.
http://www.osnews.com/story/19266/WTFs_m

Which door represents your code? Which door represents your team or your company?
Why are we in that room? Is this just a normal code review or have we found a stream of
horrible problems shortly after going live? Are we debugging in a panic, poring over code
that we thought worked? Are customers leaving in droves and managers breathing down

xxv

xxvi

Introduction

our necks? How can we make sure we wind up behind the right door when the going gets
tough? The answer is: craftsmanship.
There are two parts to learning craftsmanship: knowledge and work. You must gain
the knowledge of principles, patterns, practices, and heuristics that a craftsman knows, and
you must also grind that knowledge into your ﬁngers, eyes, and gut by working hard and
practicing.
I can teach you the physics of riding a bicycle. Indeed, the classical mathematics is
relatively straightforward. Gravity, friction, angular momentum, center of mass, and so
forth, can be demonstrated with less than a page full of equations. Given those formulae I
could prove to you that bicycle riding is practical and give you all the knowledge you
needed to make it work. And you’d still fall down the ﬁrst time you climbed on that bike.
Coding is no different. We could write down all the “feel good” principles of clean
code and then trust you to do the work (in other words, let you fall down when you get on
the bike), but then what kind of teachers would that make us, and what kind of student
would that make you?
No. That’s not the way this book is going to work.
Learning to write clean code is hard work. It requires more than just the knowledge of
principles and patterns. You must sweat over it. You must practice it yourself, and watch
yourself fail. You must watch others practice it and fail. You must see them stumble and
retrace their steps. You must see them agonize over decisions and see the price they pay for
making those decisions the wrong way.
Be prepared to work hard while reading this book. This is not a “feel good” book that
you can read on an airplane and ﬁnish before you land. This book will make you work, and
work hard. What kind of work will you be doing? You’ll be reading code—lots of code.
And you will be challenged to think about what’s right about that code and what’s wrong
with it. You’ll be asked to follow along as we take modules apart and put them back
together again. This will take time and effort; but we think it will be worth it.
We have divided this book into three parts. The ﬁrst several chapters describe the principles, patterns, and practices of writing clean code. There is quite a bit of code in these
chapters, and they will be challenging to read. They’ll prepare you for the second section
to come. If you put the book down after reading the ﬁrst section, good luck to you!
The second part of the book is the harder work. It consists of several case studies of
ever-increasing complexity. Each case study is an exercise in cleaning up some code—of
transforming code that has some problems into code that has fewer problems. The detail in
this section is intense. You will have to ﬂip back and forth between the narrative and the
code listings. You will have to analyze and understand the code we are working with and
walk through our reasoning for making each change we make. Set aside some time
because this should take you days.
The third part of this book is the payoff. It is a single chapter containing a list of heuristics and smells gathered while creating the case studies. As we walked through and
cleaned up the code in the case studies, we documented every reason for our actions as a

Introduction

xxvii

heuristic or smell. We tried to understand our own reactions to the code we were reading
and changing, and worked hard to capture why we felt what we felt and did what we did.
The result is a knowledge base that desribes the way we think when we write, read, and
clean code.
This knowledge base is of limited value if you don’t do the work of carefully reading
through the case studies in the second part of this book. In those case studies we have carefully annotated each change we made with forward references to the heuristics. These forward references appear in square brackets like this: [H22]. This lets you see the context in
which those heuristics were applied and written! It is not the heuristics themselves that are
so valuable, it is the relationship between those heuristics and the discrete decisions we
made while cleaning up the code in the case studies.
To further help you with those relationships, we have placed a cross-reference at the end
of the book that shows the page number for every forward reference. You can use it to look
up each place where a certain heuristic was applied.
If you read the ﬁrst and third sections and skip over the case studies, then you will
have read yet another “feel good” book about writing good software. But if you take the
time to work through the case studies, following every tiny step, every minute decision—if
you put yourself in our place, and force yourself to think along the same paths that we
thought, then you will gain a much richer understanding of those principles, patterns, practices, and heuristics. They won’t be “feel good” knowledge any more. They’ll have been
ground into your gut, ﬁngers, and heart. They’ll have become part of you in the same way
that a bicycle becomes an extension of your will when you have mastered how to ride it.

Acknowledgments
Artwork
Thank you to my two artists, Jeniffer Kohnke and Angela Brooks. Jennifer is responsible
for the stunning and creative pictures at the start of each chapter and also for the portraits
of Kent Beck, Ward Cunningham, Bjarne Stroustrup, Ron Jeffries, Grady Booch, Dave
Thomas, Michael Feathers, and myself.
Angela is responsible for the clever pictures that adorn the innards of each chapter.
She has done quite a few pictures for me over the years, including many of the inside pictures in Agile Software Develpment: Principles, Patterns, and Practices. She is also my
ﬁrstborn in whom I am well pleased.

This page intentionally left blank

On the Cover
The image on the cover is M104: The Sombrero Galaxy. M104 is located in Virgo and is
just under 30 million light-years from us. At it’s core is a supermassive black hole weighing in at about a billion solar masses.
Does the image remind you of the explosion of the Klingon power moon Praxis? I
vividly remember the scene in Star Trek VI that showed an equatorial ring of debris ﬂying
away from that explosion. Since that scene, the equatorial ring has been a common artifact
in sci-ﬁ movie explosions. It was even added to the explosion of Alderaan in later editions
of the ﬁrst Star Wars movie.
What caused this ring to form around M104? Why does it have such a huge central
bulge and such a bright and tiny nucleus? It looks to me as though the central black hole
lost its cool and blew a 30,000 light-year hole in the middle of the galaxy. Woe befell any
civilizations that might have been in the path of that cosmic disruption.
Supermassive black holes swallow whole stars for lunch, converting a sizeable fraction of their mass to energy. E = MC2 is leverage enough, but when M is a stellar mass:
Look out! How many stars fell headlong into that maw before the monster was satiated?
Could the size of the central void be a hint?
The image of M104 on the cover is a
combination of the famous visible light photograph from Hubble (right), and the recent
infrared image from the Spitzer orbiting
observatory (below, right). It’s the infrared
image that clearly shows us the ring nature
of the galaxy. In visible light we only see the
front edge of the ring in silhouette. The central bulge obscures the rest of the ring.
But in the infrared, the hot particles in
the ring shine through the central bulge. The
two images combined give us a view we’ve
not seen before and imply that long ago it
was a raging inferno of activity.

Cover image: © Spitzer Space Telescope

xxix

This page intentionally left blank

1
Clean Code

You are reading this book for two reasons. First, you are a programmer. Second, you want
to be a better programmer. Good. We need better programmers.

1

2

Chapter 1: Clean Code

This is a book about good programming. It is ﬁlled with code. We are going to look at
code from every different direction. We’ll look down at it from the top, up at it from the
bottom, and through it from the inside out. By the time we are done, we’re going to know a
lot about code. What’s more, we’ll be able to tell the difference between good code and bad
code. We’ll know how to write good code. And we’ll know how to transform bad code into
good code.

There Will Be Code
One might argue that a book about code is somehow behind the times—that code is no
longer the issue; that we should be concerned about models and requirements instead.
Indeed some have suggested that we are close to the end of code. That soon all code will
be generated instead of written. That programmers simply won’t be needed because business people will generate programs from speciﬁcations.
Nonsense! We will never be rid of code, because code represents the details of the
requirements. At some level those details cannot be ignored or abstracted; they have to be
speciﬁed. And specifying requirements in such detail that a machine can execute them is
programming. Such a speciﬁcation is code.
I expect that the level of abstraction of our languages will continue to increase. I
also expect that the number of domain-speciﬁc languages will continue to grow. This
will be a good thing. But it will not eliminate code. Indeed, all the speciﬁcations written
in these higher level and domain-speciﬁc language will be code! It will still need to
be rigorous, accurate, and so formal and detailed that a machine can understand and
execute it.
The folks who think that code will one day disappear are like mathematicians who
hope one day to discover a mathematics that does not have to be formal. They are hoping
that one day we will discover a way to create machines that can do what we want rather
than what we say. These machines will have to be able to understand us so well that they
can translate vaguely speciﬁed needs into perfectly executing programs that precisely meet
those needs.
This will never happen. Not even humans, with all their intuition and creativity,
have been able to create successful systems from the vague feelings of their customers.
Indeed, if the discipline of requirements speciﬁcation has taught us anything, it is that
well-speciﬁed requirements are as formal as code and can act as executable tests of that
code!
Remember that code is really the language in which we ultimately express the requirements. We may create languages that are closer to the requirements. We may create tools
that help us parse and assemble those requirements into formal structures. But we will
never eliminate necessary precision—so there will always be code.

Bad Code

3

Bad Code
I was recently reading the preface to Kent Beck’s
book Implementation Patterns.1 He says, “. . . this
book is based on a rather fragile premise: that
good code matters. . . .” A fragile premise? I disagree! I think that premise is one of the most
robust, supported, and overloaded of all the premises in our craft (and I think Kent knows it). We
know good code matters because we’ve had to
deal for so long with its lack.
I know of one company that, in the late 80s,
wrote a killer app. It was very popular, and lots of
professionals bought and used it. But then the
release cycles began to stretch. Bugs were not
repaired from one release to the next. Load times
grew and crashes increased. I remember the day I
shut the product down in frustration and never
used it again. The company went out of business
a short time after that.
Two decades later I met one of the early employees of that company and asked him
what had happened. The answer conﬁrmed my fears. They had rushed the product to
market and had made a huge mess in the code. As they added more and more features, the
code got worse and worse until they simply could not manage it any longer. It was the bad
code that brought the company down.
Have you ever been signiﬁcantly impeded by bad code? If you are a programmer of
any experience then you’ve felt this impediment many times. Indeed, we have a name for
it. We call it wading. We wade through bad code. We slog through a morass of tangled
brambles and hidden pitfalls. We struggle to ﬁnd our way, hoping for some hint, some
clue, of what is going on; but all we see is more and more senseless code.
Of course you have been impeded by bad code. So then—why did you write it?
Were you trying to go fast? Were you in a rush? Probably so. Perhaps you felt that you
didn’t have time to do a good job; that your boss would be angry with you if you took the
time to clean up your code. Perhaps you were just tired of working on this program and
wanted it to be over. Or maybe you looked at the backlog of other stuff that you had promised to get done and realized that you needed to slam this module together so you could
move on to the next. We’ve all done it.
We’ve all looked at the mess we’ve just made and then have chosen to leave it for
another day. We’ve all felt the relief of seeing our messy program work and deciding that a

1. [Beck07].

4

Chapter 1: Clean Code

working mess is better than nothing. We’ve all said we’d go back and clean it up later. Of
course, in those days we didn’t know LeBlanc’s law: Later equals never.

The Total Cost of Owning a Mess
If you have been a programmer for more than two or three years, you have probably been
signiﬁcantly slowed down by someone else’s messy code. If you have been a programmer
for longer than two or three years, you have probably been slowed down by messy code.
The degree of the slowdown can be signiﬁcant. Over the span of a year or two, teams that
were moving very fast at the beginning of a project can ﬁnd themselves moving at a snail’s
pace. Every change they make to the code breaks two or three other parts of the code. No
change is trivial. Every addition or modiﬁcation to the system requires that the tangles,
twists, and knots be “understood” so that more tangles, twists, and knots can be added.
Over time the mess becomes so big and so deep and so tall, they can not clean it up. There
is no way at all.
As the mess builds, the productivity of the team continues to decrease, asymptotically
approaching zero. As productivity decreases, management does the only thing they can;
they add more staff to the project in hopes of increasing productivity. But that new staff is
not versed in the design of the system. They don’t know the difference between a change
that matches the design intent and a change that thwarts the design intent. Furthermore,
they, and everyone else on the team, are under horriﬁc pressure to increase productivity. So
they all make more and more messes, driving the productivity ever further toward zero.
(See Figure 1-1.)

Figure 1-1
Productivity vs. time

The Total Cost of Owning a Mess

5

The Grand Redesign in the Sky
Eventually the team rebels. They inform management that they cannot continue to develop
in this odious code base. They demand a redesign. Management does not want to expend
the resources on a whole new redesign of the project, but they cannot deny that productivity is terrible. Eventually they bend to the demands of the developers and authorize the
grand redesign in the sky.
A new tiger team is selected. Everyone wants to be on this team because it’s a greenﬁeld project. They get to start over and create something truly beautiful. But only the best
and brightest are chosen for the tiger team. Everyone else must continue to maintain the
current system.
Now the two teams are in a race. The tiger team must build a new system that does
everything that the old system does. Not only that, they have to keep up with the changes
that are continuously being made to the old system. Management will not replace the old
system until the new system can do everything that the old system does.
This race can go on for a very long time. I’ve seen it take 10 years. And by the time it’s
done, the original members of the tiger team are long gone, and the current members are
demanding that the new system be redesigned because it’s such a mess.
If you have experienced even one small part of the story I just told, then you already
know that spending time keeping your code clean is not just cost effective; it’s a matter of
professional survival.

Attitude
Have you ever waded through a mess so grave that it took weeks to do what should have
taken hours? Have you seen what should have been a one-line change, made instead in
hundreds of different modules? These symptoms are all too common.
Why does this happen to code? Why does good code rot so quickly into bad code? We
have lots of explanations for it. We complain that the requirements changed in ways that
thwart the original design. We bemoan the schedules that were too tight to do things right.
We blather about stupid managers and intolerant customers and useless marketing types
and telephone sanitizers. But the fault, dear Dilbert, is not in our stars, but in ourselves.
We are unprofessional.
"""
