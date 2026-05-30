#!/usr/bin/env python3
"""Generate complete Cambridge IELTS 17 Tests 1-4 JSON data."""

import json
import os

OUT_DIR = "data/cambridge/cam17"
os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# READING PASSAGE TEXTS
# ============================================================

PASSAGE_TEXTS = {
    "t1_p1": (
        "In the first half of the 1800s, London's population grew at an astonishing rate, and the central "
        "area became increasingly congested. In addition, the expansion of the overground railway "
        "network resulted in more and more passengers arriving in the capital. However, in 1846, a Royal "
        "Commission decided that the railways should not be allowed to enter the City, the capital's "
        "historic and business centre. The result was that the overground railway stations formed a ring "
        "around the City. The area within consisted of poorly built, overcrowded slums and the streets were "
        "full of horse-drawn traffic. Crossing the City became a nightmare. It could take an hour and a half "
        "to travel 8 km by horse-drawn carriage or bus. Numerous schemes were proposed to resolve these "
        "problems, but few succeeded.\n\n"
        "Amongst the most vocal advocates for a solution to London's traffic problems was Charles "
        "Pearson, who worked as a solicitor for the City of London. He saw both social and economic "
        "advantages in building an underground railway that would link the overground railway stations "
        "together and clear London slums at the same time. His idea was to relocate the poor workers who "
        "lived in the inner-city slums to newly constructed suburbs, and to provide cheap rail travel for "
        "them to get to work. Pearson's ideas gained support amongst some businessmen and in 1851 he "
        "submitted a plan to Parliament. It was rejected, but coincided with a proposal from another group "
        "for an underground connecting line, which Parliament passed.\n\n"
        "The two groups merged and established the Metropolitan Railway Company in August 1854. The "
        "company's plan was to construct an underground railway line from the Great Western Railway's "
        "(GWR) station at Paddington to the edge of the City at Farringdon Street – a distance of almost "
        "5 km. The organisation had difficulty in raising the funding for such a radical and expensive "
        "scheme, not least because of the critical articles printed by the press. Objectors argued that the "
        "tunnels would collapse under the weight of traffic overhead, buildings would be shaken and "
        "passengers would be poisoned by the emissions from the train engines. However, Pearson and his "
        "partners persisted.\n\n"
        "The GWR, aware that the new line would finally enable them to run trains into the heart of "
        "the City, invested almost £250,000 in the scheme. Eventually, over a five-year period, £1m "
        "was raised. The chosen route ran beneath existing main roads to minimise the expense of "
        "demolishing buildings. Originally scheduled to be completed in 21 months, the construction of "
        "the underground line took three years. It was built just below street level using a technique known "
        "as 'cut and cover'. A trench about ten metres wide and six metres deep was dug, and the sides "
        "temporarily held up with timber beams. Brick walls were then constructed, and finally a brick "
        "arch was added to create a tunnel. A two-metre-deep layer of soil was laid on top of the tunnel "
        "and the road above rebuilt.\n\n"
        "The Metropolitan line, which opened on 10 January 1863, was the world's first underground "
        "railway. On its first day, almost 40,000 passengers were carried between Paddington and "
        "Farringdon, the journey taking about 18 minutes. By the end of the Metropolitan's first year of "
        "operation, 9.5 million journeys had been made.\n\n"
        "Even as the Metropolitan began operation, the first extensions to the line were being authorised; "
        "these were built over the next five years, reaching Moorgate in the east of London and "
        "Hammersmith in the west. The original plan was to pull the trains with steam locomotives, using "
        "firebricks in the boilers to provide steam, but these engines were never introduced. Instead, the "
        "line used specially designed locomotives that were fitted with water tanks in which steam could "
        "be condensed. However, smoke and fumes remained a problem, even though ventilation shafts "
        "were added to the tunnels.\n\n"
        "Despite the extension of the underground railway, by the 1880s, congestion on London's streets "
        "had become worse. The problem was partly that the existing underground lines formed a circuit "
        "around the centre of London and extended to the suburbs, but did not cross the capital's centre. "
        "The 'cut and cover' method of construction was not an option in this part of the capital. The only "
        "alternative was to tunnel deep underground.\n\n"
        "Although the technology to create these tunnels existed, steam locomotives could not be used in "
        "such a confined space. It wasn't until the development of a reliable electric motor, and a means of "
        "transferring power from the generator to a moving train, that the world's first deep-level electric "
        "railway, the City & South London, became possible. The line opened in 1890, and ran from the "
        "City to Stockwell, south of the River Thames. The trains were made up of three carriages and "
        "driven by electric engines. The carriages were narrow and had tiny windows just below the roof "
        "because it was thought that passengers would not want to look out at the tunnel walls. The line "
        "was not without its problems, mainly caused by an unreliable power supply. Although the City & "
        "South London Railway was a great technical achievement, it did not make a profit. Then, in 1900, "
        "the Central London Railway, known as the 'Tuppenny Tube', began operation using new electric "
        "locomotives. It was very popular and soon afterwards new railways and extensions were added to "
        "the growing tube network. By 1907, the heart of today's Underground system was in place."
    ),
    "t1_p2": (
        "A\nStadiums are among the oldest forms of urban architecture: vast stadiums where the public "
        "could watch sporting events were at the centre of western city life as far back as the ancient "
        "Greek and Roman Empires, well before the construction of the great medieval cathedrals and "
        "the grand 19th- and 20th-century railway stations which dominated urban skylines in later eras.\n\n"
        "Today, however, stadiums are regarded with growing scepticism. Construction costs can soar "
        "above £1 billion, and stadiums finished for major events such as the Olympic Games or the "
        "FIFA World Cup have notably fallen into disuse and disrepair.\n\n"
        "But this need not be the case. History shows that stadiums can drive urban development and "
        "adapt to the culture of every age. Even today, architects and planners are finding new ways "
        "to adapt the mono-functional sports arenas which became emblematic of modernisation "
        "during the 20th century.\n\n"
        "B\nThe amphitheatre of Arles in southwest France, with a capacity of 25,000 spectators, "
        "is perhaps the best example of just how versatile stadiums can be. Built by the Romans in "
        "90 AD, it became a fortress with four towers after the fifth century, and was then "
        "transformed into a village containing more than 200 houses. With the growing interest in "
        "conservation during the 19th century, it was converted back into an arena for the staging of "
        "bullfights, thereby returning the structure to its original use as a venue for public spectacles.\n\n"
        "Another example is the imposing arena of Verona in northern Italy, with space for 30,000 "
        "spectators, which was built 60 years before the Arles amphitheatre and 40 years before "
        "Rome's famous Colosseum. It has endured the centuries and is currently considered one of "
        "the world's prime sites for opera, thanks to its outstanding acoustics.\n\n"
        "C\nThe area in the centre of the Italian town of Lucca, known as the Piazza dell'Anfiteatro, "
        "is yet another impressive example of an amphitheatre becoming absorbed into the fabric "
        "of the city. The site evolved in a similar way to Arles and was progressively filled with "
        "buildings from the Middle Ages until the 19th century, variously used as houses, a salt depot "
        "and a prison. But rather than reverting to an arena, it became a market square, designed "
        "by Romanticist architect Lorenzo Nottolini. Today, the ruins of the amphitheatre remain "
        "embedded in the various shops and residences surrounding the public square.\n\n"
        "D\nThere are many similarities between modern stadiums and the ancient amphitheatres "
        "intended for games. But some of the flexibility was lost at the beginning of the 20th century, "
        "as stadiums were developed using new products such as steel and reinforced concrete, and "
        "made use of bright lights for night-time matches.\n\n"
        "Many such stadiums are situated in suburban areas, designed for sporting use only and "
        "surrounded by parking lots. These factors mean that they may not be as accessible to the "
        "general public, require more energy to run and contribute to urban heat.\n\n"
        "E\nBut many of today's most innovative architects see scope for the stadium to help improve the "
        "city. Among the current strategies, two seem to be having particular success: the stadium as "
        "an urban hub, and as a power plant.\n\n"
        "There's a growing trend for stadiums to be equipped with public spaces and services that "
        "serve a function beyond sport, such as hotels, retail outlets, conference centres, restaurants "
        "and bars, children's playgrounds and green space. Creating mixed-use developments such as "
        "this reinforces compactness and multi-functionality, making more efficient use of land and "
        "helping to regenerate urban spaces.\n\n"
        "This opens the space up to families and a wider cross-section of society, instead of catering "
        "only to sportspeople and supporters. There have been many examples of this in the UK: the "
        "mixed-use facilities at Wembley and Old Trafford have become a blueprint for many other "
        "stadiums in the world.\n\n"
        "F\nThe phenomenon of stadiums as power stations has arisen from the idea that energy "
        "problems can be overcome by integrating interconnected buildings by means of a smart grid, "
        "which is an electricity supply network that uses digital communications technology to detect "
        "and react to local changes in usage, without significant energy losses. Stadiums are ideal "
        "for these purposes, because their canopies have a large surface area for fitting photovoltaic "
        "panels and rise high enough (more than 40 metres) to make use of micro wind turbines.\n\n"
        "Freiburg Mage Solar Stadium in Germany is the first of a new wave of stadiums as power "
        "plants, which also includes the Amsterdam Arena and the Kaohsiung Stadium. The latter, "
        "inaugurated in 2009, has 8,844 photovoltaic panels producing up to 1.14 GWh of electricity "
        "annually. This reduces the annual output of carbon dioxide by 660 tons and supplies up "
        "to 80 percent of the surrounding area when the stadium is not in use. This is proof that a "
        "stadium can serve its city, and have a decidedly positive impact in terms of reduction of CO2 "
        "emissions.\n\n"
        "G\nSporting arenas have always been central to the life and culture of cities. In every era, the "
        "stadium has acquired new value and uses: from military fortress to residential village, public "
        "space to theatre and most recently a field for experimentation in advanced engineering. "
        "The stadium of today now brings together multiple functions, thus helping cities to create a "
        "sustainable future."
    ),
    "t1_p3": (
        "Anna Keay reviews Charles Spencer's book about the hunt for King Charles II "
        "during the English Civil War of the seventeenth century\n\n"
        "Charles Spencer's latest book, To Catch a King, tells us the story of the hunt for King "
        "Charles II in the six weeks after his resounding defeat at the Battle of Worcester in September "
        "1651. And what a story it is. After his father was executed by the Parliamentarians in 1649, "
        "the young Charles II sacrificed one of the very principles his father had died for and "
        "did a deal with the Scots, thereby accepting Presbyterianism as the national religion in "
        "return for being crowned King of Scots. His arrival in Edinburgh prompted the English "
        "Parliamentary army to invade Scotland in a pre-emptive strike. This was followed by a "
        "Scottish invasion of England. The two sides finally faced one another at Worcester in "
        "the west of England in 1651. After being comprehensively defeated on the meadows "
        "outside the city by the Parliamentarian army, the 21-year-old king found himself the subject "
        "of a national manhunt, with a huge sum offered for his capture. Over the following "
        "six weeks he managed, through a series of heart-poundingly close escapes, to evade the "
        "Parliamentarians before seeking refuge in France. For the next nine years, the penniless "
        "and defeated Charles wandered around Europe with only a small group of loyal supporters.\n\n"
        "Years later, after his restoration as king, the 50-year-old Charles II requested a meeting "
        "with the writer and diarist Samuel Pepys. His intention when asking Pepys to commit his "
        "story to paper was to ensure that this most extraordinary episode was never forgotten. "
        "Over two three-hour sittings, the king related to him in great detail his personal recollections "
        "of the six weeks he had spent as a fugitive. As the king and secretary settled down (a scene "
        "that is surely a gift for a future scriptwriter), Charles commenced his story: 'After the battle "
        "was so absolutely lost as to be beyond hope of recovery, I began to think of the best way of "
        "saving myself.'\n\n"
        "One of the joys of Spencer's book, a result not least of its use of Charles II's own narrative "
        "as well as those of his supporters, is just how close the reader gets to the action. The day-by-"
        "day retelling of the fugitives' doings provides delicious details: the cutting of the king's long "
        "hair with agricultural shears, the use of walnut leaves to dye his pale skin, and the day Charles "
        "spent lying on a branch of the great oak tree in Boscobel Wood as the Parliamentary soldiers "
        "scoured the forest floor below. Spencer draws out both the humour – such as the preposterous "
        "refusal of Charles's friend Henry Wilmot to adopt disguise on the grounds that it was "
        "beneath his dignity – and the emotional tension when the secret of the king's presence was "
        "cautiously revealed to his supporters.\n\n"
        "Charles's adventures after losing the Battle of Worcester hide the uncomfortable truth that "
        "whilst almost everyone in England had been appalled by the execution of his father, they "
        "had not welcomed the arrival of his son with the Scots army, but had instead firmly bolted "
        "their doors. This was partly because he rode at the head of what looked like a foreign invasion "
        "force and partly because, after almost a decade of civil war, people were desperate to avoid "
        "it beginning again. This makes it all the more interesting that Charles II himself loved the "
        "story so much ever after. As well as retelling it to anyone who would listen, causing eye-"
        "rolling among courtiers, he set in train a series of initiatives to memorialise it. There was to "
        "be a new order of chivalry, the Knights of the Royal Oak. A series of enormous oil paintings "
        "depicting the episode were produced, including a two-metre-wide canvas of Boscobel Wood "
        "and a set of six similarly enormous paintings of the king on the run. In 1660, Charles II "
        "commissioned the artist John Michael Wright to paint a flying squadron of cherubs carrying "
        "an oak tree to the heavens on the ceiling of his bedchamber. It is hard to imagine many other "
        "kings marking the lowest point in their life so enthusiastically, or indeed pulling off such an "
        "escape in the first place.\n\n"
        "Charles Spencer is the perfect person to pass the story on to a new generation. His "
        "pacey, readable prose steers deftly clear of modern idioms and elegantly brings to life the "
        "details of the great tale. He has even-handed sympathy for both the fugitive king and the "
        "fierce republican regime that hunted him, and he succeeds in his desire to explore far "
        "more of the background of the story than previous books on the subject have done. Indeed, "
        "the opening third of the book is about how Charles II found himself at Worcester in the first "
        "place, which for some will be reason alone to read To Catch a King.\n\n"
        "The tantalising question left, in the end, is that of what it all meant. Would Charles II have "
        "been a different king had these six weeks never happened? The days and nights spent in hiding "
        "must have affected him in some way. Did the need to assume disguises, to survive on wit and "
        "charm alone, to use trickery and subterfuge to escape from tight corners help form him? This "
        "is the one area where the book doesn't quite hit the mark. Instead its depiction of Charles II in "
        "his final years as an ineffective, pleasure-loving monarch doesn't do justice to the man (neither "
        "is it accurate), or to the complexity of his character. But this one niggle aside, To Catch a "
        "King is an excellent read, and those who come to it knowing little of the famous tale will find "
        "they have a treat in store."
    ),
    "t2_p1": (
        "In late 1946 or early 1947, three Bedouin teenagers were tending their goats and sheep "
        "near the ancient settlement of Qumran, located on the northwest shore of the Dead "
        "Sea in what is now known as the West Bank. One of these young shepherds tossed a "
        "rock into an opening on the side of a cliff and was surprised to hear a shattering sound. "
        "He and his companions later entered the cave and stumbled across a collection of "
        "large clay jars, seven of which contained scrolls with writing on them. The teenagers "
        "took the seven scrolls to a nearby town where they were sold for a small sum to a local "
        "antiquities dealer. Word of the find spread, and Bedouins and archaeologists eventually "
        "unearthed tens of thousands of additional scroll fragments from 10 nearby caves; "
        "together they make up between 800 and 900 manuscripts. It soon became clear that this "
        "was one of the greatest archaeological discoveries ever made.\n\n"
        "The origin of the Dead Sea Scrolls, which were written around 2,000 years ago between "
        "150 BCE and 70 CE, is still the subject of scholarly debate even today. According to the "
        "prevailing theory, they are the work of a population that inhabited the area until Roman "
        "troops destroyed the settlement around 70 CE. The area was known as Judea at that "
        "time, and the people are thought to have belonged to a group called the Essenes, a "
        "devout Jewish sect.\n\n"
        "The majority of the texts on the Dead Sea Scrolls are in Hebrew, with some fragments "
        "written in an ancient version of its alphabet thought to have fallen out of use in the fifth "
        "century BCE. But there are other languages as well. Some scrolls are in Aramaic, the "
        "language spoken by many inhabitants of the region from the sixth century BCE to the "
        "siege of Jerusalem in 70 CE. In addition, several texts feature translations of the Hebrew "
        "Bible into Greek.\n\n"
        "The Dead Sea Scrolls include fragments from every book of the Old Testament of the "
        "Bible except for the Book of Esther. The only entire book of the Hebrew Bible preserved "
        "among the manuscripts from Qumran is Isaiah; this copy, dated to the first century BCE, "
        "is considered the earliest biblical manuscript still in existence. Along with biblical texts, "
        "the scrolls include documents about sectarian regulations and religious writings that do "
        "not appear in the Old Testament.\n\n"
        "The writing on the Dead Sea Scrolls is mostly in black or occasionally red ink, and "
        "the scrolls themselves are nearly all made of either parchment (animal skin) or an "
        "early form of paper called 'papyrus'. The only exception is the scroll numbered 3Q15, "
        "which was created out of a combination of copper and tin. Known as the Copper "
        "Scroll, this curious document features letters chiselled onto metal – perhaps, as some "
        "have theorized, to better withstand the passage of time. One of the most intriguing "
        "manuscripts from Qumran, this is a sort of ancient treasure map that lists dozens of gold "
        "and silver caches. Using an unconventional vocabulary and odd spelling, it describes 64 "
        "underground hiding places that supposedly contain riches buried for safekeeping. None "
        "of these hoards have been recovered, possibly because the Romans pillaged Judea "
        "during the first century CE. According to various hypotheses, the treasure belonged to "
        "local people, or was rescued from the Second Temple before its destruction or never "
        "existed to begin with.\n\n"
        "Some of the Dead Sea Scrolls have been on interesting journeys. In 1948, a Syrian "
        "Orthodox archbishop known as Mar Samuel acquired four of the original seven scrolls "
        "from a Jerusalem shoemaker and part-time antiquity dealer, paying less than $100 "
        "for them. He then travelled to the United States and unsuccessfully offered them to a "
        "number of universities, including Yale. Finally, in 1954, he placed an advertisement in "
        "the business newspaper The Wall Street Journal – under the category 'Miscellaneous "
        "Items for Sale' – that read: 'Biblical Manuscripts dating back to at least 200 B.C. are for "
        "sale. This would be an ideal gift to an educational or religious institution by an individual "
        "or group.' Fortunately, Israeli archaeologist and statesman Yigael Yadin negotiated their "
        "purchase and brought the scrolls back to Jerusalem, where they remain to this day.\n\n"
        "In 2017, researchers from the University of Haifa restored and deciphered one of the last "
        "untranslated scrolls. The university's Eshbal Ratson and Jonathan Ben-Dov spent one "
        "year reassembling the 60 fragments that make up the scroll. Deciphered from a band "
        "of coded text on parchment, the find provides insight into the community of people who "
        "wrote it and the 364-day calendar they would have used. The scroll names celebrations "
        "that indicate shifts in seasons and details two yearly religious events known from "
        "another Dead Sea Scroll. Only one more known scroll remains untranslated."
    ),
    "t2_p2": (
        "A second attempt at domesticating the tomato\n\n"
        "A\nIt took at least 3,000 years for humans to learn how to domesticate the wild tomato "
        "and cultivate it for food. Now two separate teams in Brazil and China have done it all "
        "over again in less than three years. And they have done it better in some ways, as "
        "the re-domesticated tomatoes are more nutritious than the ones we eat at present.\n\n"
        "This approach relies on the revolutionary CRISPR genome editing technique, in "
        "which changes are deliberately made to the DNA of a living cell, allowing genetic "
        "material to be added, removed or altered. The technique could not only improve "
        "existing crops, but could also be used to turn thousands of wild plants into useful "
        "and appealing foods. In fact, a third team in the US has already begun to do this "
        "with a relative of the tomato called the groundcherry.\n\n"
        "This fast-track domestication could help make the world's food supply healthier and "
        "far more resistant to diseases, such as the rust fungus devastating wheat crops.\n\n"
        "'This could transform what we eat,' says Jorg Kudla at the University of Munster in "
        "Germany, a member of the Brazilian team. 'There are 50,000 edible plants in the "
        "world, but 90 percent of our energy comes from just 15 crops.'\n\n"
        "'We can now mimic the known domestication course of major crops like rice, maize, "
        "sorghum or others,' says Caixia Gao of the Chinese Academy of Sciences in Beijing. "
        "'Then we might try to domesticate plants that have never been domesticated.'\n\n"
        "B\nWild tomatoes, which are native to the Andes region in South America, produce "
        "pea-sized fruits. Over many generations, peoples such as the Aztecs and Incas "
        "transformed the plant by selecting and breeding plants with mutations in their "
        "genetic structure, which resulted in desirable traits such as larger fruit.\n\n"
        "But every time a single plant with a mutation is taken from a larger population for "
        "breeding, much genetic diversity is lost. And sometimes the desirable mutations "
        "come with less desirable traits. For instance, the tomato strains grown for "
        "supermarkets have lost much of their flavour.\n\n"
        "By comparing the genomes of modern plants to those of their wild relatives, "
        "biologists have been working out what genetic changes occurred as plants were "
        "domesticated. The teams in Brazil and China have now used this knowledge to "
        "reintroduce these changes from scratch while maintaining or even enhancing the "
        "desirable traits of wild strains.\n\n"
        "C\nKudla's team made six changes altogether. For instance, they tripled the size "
        "of fruit by editing a gene called FRUIT WEIGHT, and increased the number of "
        "tomatoes per truss by editing another called MULTIFLORA.\n\n"
        "While the historical domestication of tomatoes reduced levels of the red pigment "
        "lycopene – thought to have potential health benefits – the team in Brazil managed "
        "to boost it instead. The wild tomato has twice as much lycopene as cultivated ones; "
        "the newly domesticated one has five times as much.\n\n"
        "'They are quite tasty,' says Kudla. 'A little bit strong. And very aromatic.'\n\n"
        "The team in China re-domesticated several strains of wild tomatoes with desirable "
        "traits lost in domesticated tomatoes. In this way they managed to create a strain "
        "resistant to a common disease called bacterial spot race, which can devastate "
        "yields. They also created another strain that is more salt tolerant – and has higher "
        "levels of vitamin C.\n\n"
        "D\nMeanwhile, Joyce Van Eck at the Boyce Thompson Institute in New York state "
        "decided to use the same approach to domesticate the groundcherry or goldenberry "
        "(Physalis pruinosa) for the first time. This fruit looks similar to the closely related "
        "Cape gooseberry (Physalis peruviana).\n\n"
        "Groundcherries are already sold to a limited extent in the US but they are hard to "
        "produce because the plant has a sprawling growth habit and the small fruits fall "
        "off the branches when ripe. Van Eck's team has edited the plants to increase fruit "
        "size, make their growth more compact and to stop fruits dropping. 'There's potential "
        "for this to be a commercial crop,' says Van Eck. But she adds that taking the "
        "work further would be expensive because of the need to pay for a licence for the "
        "CRISPR technology and get regulatory approval.\n\n"
        "E\nThis approach could boost the use of many obscure plants, says Jonathan Jones "
        "of the Sainsbury Lab in the UK. But it will be hard for new foods to grow so popular "
        "with farmers and consumers that they become new staple crops, he thinks.\n\n"
        "The three teams already have their eye on other plants that could be 'catapulted "
        "into the mainstream', including foxtail, oat-grass and cowpea. By choosing wild "
        "plants that are drought or heat tolerant, says Gao, we could create crops that will "
        "thrive even as the planet warms.\n\n"
        "But Kudla didn't want to reveal which species were in his team's sights, because "
        "CRISPR has made the process so easy. 'Any one with the right skills could go to "
        "their lab and do this.'"
    ),
    "t2_p3": (
        "Insight or evolution?\n"
        "Two scientists consider the origins of discoveries and other innovative behavior\n\n"
        "Scientific discovery is popularly believed to result from the sheer genius of such intellectual "
        "stars as naturalist Charles Darwin and theoretical physicist Albert Einstein. Our view of such "
        "unique contributions to science often disregards the person's prior experience and the efforts of "
        "their lesser-known predecessors. Conventional wisdom also places great weight on insight in "
        "promoting breakthrough scientific achievements, as if ideas spontaneously pop into someone's "
        "head – fully formed and functional.\n\n"
        "There may be some limited truth to this view. However, we believe that it largely misrepresents "
        "the real nature of scientific discovery, as well as that of creativity and innovation in many other "
        "realms of human endeavor.\n\n"
        "Setting aside such greats as Darwin and Einstein – whose monumental contributions are duly "
        "celebrated – we suggest that innovation is more a process of trial and error, where two steps "
        "forward may sometimes come with one step back, as well as one or more steps to the right or "
        "left. This evolutionary view of human innovation undermines the notion of creative genius and "
        "recognizes the cumulative nature of scientific progress.\n\n"
        "Consider one unheralded scientist: John Nicholson, a mathematical physicist working in the "
        "1910s who postulated the existence of 'proto-elements' in outer space. By combining different "
        "numbers of weights of these proto-elements' atoms, Nicholson could recover the weights of all "
        "the elements in the then-known periodic table. These successes are all the more noteworthy given "
        "the fact that Nicholson was wrong about the presence of proto-elements: they do not actually "
        "exist. Yet, amid his often fanciful theories and wild speculations, Nicholson also proposed a novel "
        "theory about the structure of atoms. Niels Bohr, the Nobel prize-winning father of modern atomic "
        "theory, jumped off from this interesting idea to conceive his now-famous model of the atom.\n\n"
        "What are we to make of this story? One might simply conclude that science is a collective and "
        "cumulative enterprise. That may be true, but there may be a deeper insight to be gleaned. We "
        "propose that science is constantly evolving, much as species of animals do. In biological systems, "
        "organisms may display new characteristics that result from random genetic mutations. In the same "
        "way, random, arbitrary or accidental mutations of ideas may help pave the way for advances in "
        "science. If mutations prove beneficial, then the animal or the scientific theory will continue to "
        "thrive and perhaps reproduce.\n\n"
        "Support for this evolutionary view of behavioral innovation comes from many domains. Consider "
        "one example of an influential innovation in US horseracing. The so-called 'acey-deucy' stirrup "
        "placement, in which the rider's foot in his left stirrup is placed as much as 25 centimeters lower "
        "than the right, is believed to confer important speed advantages when turning on oval tracks. It "
        "was developed by a relatively unknown jockey named Jackie Westrope. Had Westrope conducted "
        "methodical investigations or examined extensive film records in a shrewd plan to outrun his "
        "rivals? Had he foreseen the speed advantage that would be conferred by riding acey-deucy? No. "
        "He suffered a leg injury, which left him unable to fully bend his left knee. His modification just "
        "happened to coincide with enhanced left-hand turning performance. This led to the rapid and "
        "widespread adoption of riding acey-deucy by many riders, a racing style which continues in "
        "today's thoroughbred racing.\n\n"
        "Plenty of other stories show that fresh advances can arise from error, misadventure, and also "
        "pure serendipity – a happy accident. For example, in the early 1970s, two employees of the "
        "company 3M each had a problem: Spencer Silver had a product – a glue which was only slightly "
        "sticky – and no use for it, while his colleague Art Fry was trying to figure out how to affix "
        "temporary bookmarks in his hymn book without damaging its pages. The solution to both these "
        "problems was the invention of the brilliantly simple yet phenomenally successful Post-It note. "
        "Such examples give lie to the claim that ingenious, designing minds are responsible for human "
        "creativity and invention. Far more banal and mechanical forces may be at work; forces that are "
        "fundamentally connected to the laws of science.\n\n"
        "The notions of insight, creativity and genius are often invoked, but they remain vague and of "
        "doubtful scientific utility, especially when one considers the diverse and enduring contributions of "
        "individuals such as Plato, Leonardo da Vinci, Shakespeare, Beethoven, Galileo, Newton, Kepler, "
        "Curie, Pasteur and Edison. These notions merely label rather than explain the evolution of human "
        "innovations. We need another approach, and there is a promising candidate.\n\n"
        "The Law of Effect was advanced by psychologist Edward Thorndike in 1898, some 40 years "
        "after Charles Darwin published his groundbreaking work on biological evolution, On the Origin "
        "of Species. This simple law holds that organisms tend to repeat successful behaviors and to "
        "refrain from performing unsuccessful ones. Just like Darwin's Law of Natural Selection, the Law "
        "of Effect involves an entirely mechanical process of variation and selection, without any end "
        "objective in sight.\n\n"
        "Of course, the origin of human innovation demands much further study. In particular, the "
        "provenance of the raw material on which the Law of Effect operates is not as clearly known as "
        "that of the genetic mutations on which the Law of Natural Selection operates. The generation of "
        "novel ideas and behaviors may not be entirely random, but constrained by prior successes and "
        "failures – of the current individual (such as Bohr) or of predecessors (such as Nicholson).\n\n"
        "The time seems right for abandoning the naive notions of intelligent design and genius, and for "
        "scientifically exploring the true origins of creative behavior."
    ),
    "t3_p1": (
        "The thylacine\n\n"
        "The extinct thylacine, also known as the Tasmanian tiger, was a marsupial that bore a superficial "
        "resemblance to a dog. Its most distinguishing feature was the 13–19 dark brown stripes over its "
        "back, beginning at the rear of the body and extending onto the tail. The thylacine's average nose-"
        "to-tail length for adult males was 162.6 cm, compared to 153.7 cm for females.\n\n"
        "The thylacine appeared to occupy most types of terrain except dense rainforest, with open "
        "eucalyptus forest thought to be its prime habitat. In terms of feeding, it was exclusively "
        "carnivorous, and its stomach was muscular with an ability to distend so that it could eat large "
        "amounts of food at one time, probably an adaptation to compensate for long periods when "
        "hunting was unsuccessful and food scarce. The thylacine was not a fast runner and probably "
        "caught its prey by exhausting it during a long pursuit. During long-distance chases, thylacines "
        "were likely to have relied more on scent than any other sense. They emerged to hunt during the "
        "evening, night and early morning and tended to retreat to the hills and forest for shelter during the "
        "day. Despite the common name 'tiger', the thylacine had a shy, nervous temperament. Although "
        "mainly nocturnal, it was sighted moving during the day and some individuals were even recorded "
        "basking in the sun.\n\n"
        "The thylacine had an extended breeding season from winter to spring, with indications that "
        "some breeding took place throughout the year. The thylacine, like all marsupials, was tiny and "
        "hairless when born. Newborns crawled into the pouch on the belly of their mother, and attached "
        "themselves to one of the four teats, remaining there for up to three months. When old enough to "
        "leave the pouch, the young stayed in a lair such as a deep rocky cave, well-hidden nest or hollow "
        "log, whilst the mother hunted.\n\n"
        "Approximately 4,000 years ago, the thylacine was widespread throughout New Guinea and most "
        "of mainland Australia, as well as the island of Tasmania. The most recent, well-dated occurrence "
        "of a thylacine on the mainland is a carbon-dated fossil from Murray Cave in Western Australia, "
        "which is around 3,100 years old. Its extinction coincided closely with the arrival of wild dogs "
        "called dingoes in Australia and a similar predator in New Guinea. Dingoes never reached "
        "Tasmania, and most scientists see this as the main reason for the thylacine's survival there.\n\n"
        "The dramatic decline of the thylacine in Tasmania, which began in the 1830s and continued for "
        "a century, is generally attributed to the relentless efforts of sheep farmers and bounty hunters "
        "with shotguns. While this determined campaign undoubtedly played a large part, it is likely that "
        "various other factors also contributed to the decline and eventual extinction of the species. These "
        "include competition with wild dogs introduced by European settlers, loss of habitat along with "
        "the disappearance of prey species, and a distemper-like disease which may also have affected "
        "the thylacine.\n\n"
        "There was only one successful attempt to breed a thylacine in captivity, at Melbourne Zoo in "
        "1899. This was despite the large numbers that went through some zoos, particularly London Zoo "
        "and Tasmania's Hobart Zoo. The famous naturalist John Gould foresaw the thylacine's demise "
        "when he published his Mammals of Australia between 1848 and 1863, writing, 'The numbers of "
        "this singular animal will speedily diminish, extermination will have its full sway, and it will then, "
        "like the wolf of England and Scotland, be recorded as an animal of the past.'\n\n"
        "However, there seems to have been little public pressure to preserve the thylacine, nor was much "
        "concern expressed by scientists at the decline of this species in the decades that followed. A "
        "notable exception was T.T. Flynn, Professor of Biology at the University of Tasmania. In 1914, "
        "he was sufficiently concerned about the scarcity of the thylacine to suggest that some should be "
        "captured and placed on a small island. But it was not until 1929, with the species on the very edge "
        "of extinction, that Tasmania's Animals and Birds Protection Board passed a motion protecting "
        "thylacines only for the month of December, which was thought to be their prime breeding season. "
        "The last known wild thylacine to be killed was shot by a farmer in the north-east of Tasmania "
        "in 1930, leaving just captive specimens. Official protection of the species by the Tasmanian "
        "government was introduced in July 1936, 59 days before the last known individual died in Hobart "
        "Zoo on 7th September, 1936.\n\n"
        "There have been numerous expeditions and searches for the thylacine over the years, none of "
        "which has produced definitive evidence that thylacines still exist. The species was declared extinct "
        "by the Tasmanian government in 1986."
    ),
    "t3_p2": (
        "Palm oil\n\n"
        "A\nPalm oil is an edible oil derived from the fruit of the African oil palm tree, and is currently "
        "the most consumed vegetable oil in the world. It's almost certainly in the soap we wash with "
        "in the morning, the sandwich we have for lunch, and the biscuits we snack on during the "
        "day. Why is palm oil so attractive for manufacturers? Primarily because its unique properties "
        "– such as remaining solid at room temperature – make it an ideal ingredient for long-term "
        "preservation, allowing many packaged foods on supermarket shelves to have 'best before' "
        "dates of months, even years, into the future.\n\n"
        "B\nMany farmers have seized the opportunity to maximise the planting of oil palm trees. "
        "Between 1990 and 2012, the global land area devoted to growing oil palm trees grew from "
        "6 to 17 million hectares, now accounting for around ten percent of total cropland in the "
        "entire world. From a mere two million tonnes of palm oil being produced annually globally "
        "50 years ago, there are now around 60 million tonnes produced every single year, a figure "
        "looking likely to double or even triple by the middle of the century.\n\n"
        "C\nHowever, there are multiple reasons why conservationists cite the rapid spread of oil palm "
        "plantations as a major concern. There are countless news stories of deforestation, habitat "
        "destruction and dwindling species populations, all as a direct result of land clearing to "
        "establish oil palm tree monoculture on an industrial scale, particularly in Malaysia and "
        "Indonesia. Endangered species – most famously the Sumatran orangutan, but also rhinos, "
        "elephants, tigers, and numerous other fauna – have suffered from the unstoppable spread of "
        "oil palm plantations.\n\n"
        "D\n'Palm oil is surely one of the greatest threats to global biodiversity,' declares Dr Farnon "
        "Ellwood of the University of the West of England, Bristol. 'Palm oil is replacing rainforest, "
        "and rainforest is where all the species are. That's a problem.' This has led to some radical "
        "questions among environmentalists, such as whether consumers should try to boycott palm "
        "oil entirely.\n\n"
        "Meanwhile Bhavani Shankar, Professor at London's School of Oriental and African Studies, "
        "argues, 'It's easy to say that palm oil is the enemy and we should be against it. It makes for "
        "a more dramatic story, and it's very intuitive. But given the complexity of the argument, I "
        "think a much more nuanced story is closer to the truth.'\n\n"
        "E\nOne response to the boycott movement has been the argument for the vital role palm "
        "oil plays in lifting many millions of people in the developing world out of poverty. Is it "
        "desirable to have palm oil boycotted, replaced, eliminated from the global supply chain, "
        "given how many low-income people in developing countries depend on it for their "
        "livelihoods? How best to strike a utilitarian balance between these competing factors has "
        "become a serious bone of contention.\n\n"
        "F\nEven the deforestation argument isn't as straightforward as it seems. Oil palm plantations "
        "produce at least four and potentially up to ten times more oil per hectare than soybean, "
        "rapeseed, sunflower or other competing oils. That immensely high yield – which is "
        "predominantly what makes it so profitable – is potentially also an ecological benefit. If ten "
        "times more palm oil can be produced from a patch of land than any competing oil, then ten "
        "times more land would need to be cleared in order to produce the same volume of oil from "
        "that competitor.\n\n"
        "As for the question of carbon emissions, the issue really depends on what oil palm trees are "
        "replacing. Crops vary in the degree to which they sequester carbon – in other words, the "
        "amount of carbon they capture from the atmosphere and store within the plant. The more "
        "carbon a plant sequesters, the more it reduces the effect of climate change. As Shankar "
        "explains: '[Palm oil production] actually sequesters more carbon in some ways than other "
        "alternatives. […] Of course, if you're cutting down virgin forest it's terrible – that's what's "
        "happening in Indonesia and Malaysia, it's been allowed to get out of hand. But if it's "
        "replacing rice, for example, it might actually sequester more carbon.'\n\n"
        "G\nThe industry is now regulated by a group called the Roundtable on Sustainable Palm Oil "
        "(RSPO), consisting of palm growers, retailers, product manufacturers, and other interested "
        "parties. Over the past decade or so, an agreement has gradually been reached regarding "
        "standards that producers of palm oil have to meet in order for their product to be regarded "
        "as officially 'sustainable'. The RSPO insists upon no virgin forest clearing, transparency and "
        "regular assessment of carbon stocks, among other criteria. Only once these requirements are "
        "fully satisfied is the oil allowed to be sold as certified sustainable palm oil (CSPO). Recent "
        "figures show that the RSPO now certifies around 12 million tonnes of palm oil annually, "
        "equivalent to roughly 21 percent of the world's total palm oil production.\n\n"
        "H\nThere is even hope that oil palm plantations might not need to be such sterile monocultures, "
        "or 'green deserts', as Ellwood describes them. New research at Ellwood's lab hints at one "
        "plant which might make all the difference. The bird's nest fern (Asplenium nidus) grows on "
        "trees in an epiphytic fashion (meaning it's dependent on the tree only for support, not for "
        "nutrients), and is native to many tropical regions, where as a keystone species it performs a "
        "vital ecological role. Ellwood believes that reintroducing the bird's nest fern into oil palm "
        "plantations could potentially allow these areas to recover their biodiversity, providing a "
        "home for all manner of species, from fungi and bacteria, to invertebrates such as insects, "
        "amphibians, reptiles and even mammals."
    ),
    "t3_p3": (
        "Building the Skyline: The Birth and Growth of Manhattan's Skyscrapers\n\n"
        "Katharine L. Shester reviews a book by Jason Barr about the development of New York City\n\n"
        "In Building the Skyline, Jason Barr takes the reader through a detailed history of New York "
        "City. The book combines geology, history, economics, and a lot of data to explain why business "
        "clusters developed where they did and how the early decisions of workers and firms shaped "
        "the skyline we see today. Building the Skyline is organized into two distinct parts. The first is "
        "primarily historical and addresses New York's settlement and growth from 1609 to 1900; the "
        "second deals primarily with the 20th century and is a compilation of chapters commenting "
        "on different aspects of New York's urban development. The tone and organization of the book "
        "changes somewhat between the first and second parts, as the latter chapters incorporate aspects of "
        "Barr's related research papers.\n\n"
        "Barr begins chapter one by taking the reader on a 'helicopter time-machine' ride – giving a "
        "fascinating account of how the New York landscape in 1609 might have looked from the sky. He "
        "then moves on to a subterranean walking tour of the city, indicating the location of rock and water "
        "below the subsoil, before taking the reader back to the surface. His love of the city comes through "
        "as he describes various fun facts about the location of the New York residence of early 19th-century "
        "vice-president Aaron Burr as well as a number of legends about the city.\n\n"
        "Chapters two and three take the reader up to the Civil War (1861–1865), with chapter two "
        "focusing on the early development of land and the implementation of a grid system in 1811. "
        "Chapter three focuses on land use before the Civil War. Both chapters are informative and well "
        "researched and set the stage for the economic analysis that comes later in the book. I would "
        "have liked Barr to expand upon his claim that existing tenements prevented skyscrapers in "
        "certain neighborhoods because 'likely no skyscraper developer was interested in performing the "
        "necessary \"slum clearance\"'. Later in the book, Barr makes the claim that the depth of bedrock "
        "was not a limiting factor for developers, as foundation costs were a small fraction of the cost of "
        "development. At first glance, it is not obvious why slum clearance would be limiting, while more "
        "expensive foundations would not.\n\n"
        "Chapter four focuses on immigration and the location of neighborhoods and tenements in the "
        "late 19th century. Barr identifies four primary immigrant enclaves and analyzes their locations "
        "in terms of the amenities available in the area. Most of these enclaves were located on the least "
        "valuable land, between the industries located on the waterfront and the wealthy neighborhoods "
        "bordering Central Park.\n\n"
        "Part two of the book begins with a discussion of the economics of skyscraper height. In chapter "
        "five, Barr distinguishes between engineering height, economic height, and developer height — "
        "where engineering height is the tallest building that can be safely made at a given time, economic "
        "height is the height that is most efficient from society's point of view, and developer height is the "
        "actual height chosen by the developer, who is attempting to maximize return on investment.\n\n"
        "Chapter five also has an interesting discussion of the technological advances that led to the "
        "construction of skyscrapers. For example, the introduction of iron and steel skeletal frames made "
        "thick, load-bearing walls unnecessary, expanding the usable square footage of buildings and "
        "increasing the use of windows and availability of natural light. Chapter six then presents data on "
        "building height throughout the 20th century and uses regression analysis to 'predict' building "
        "construction. While less technical than the research paper on which the chapter is based, it is "
        "probably more technical than would be preferred by a general audience.\n\n"
        "Chapter seven tackles the 'bedrock myth', the assumption that the absence of bedrock close to the "
        "surface between Downtown and Midtown New York is the reason for skyscrapers not being built "
        "between the two urban centers. Rather, Barr argues that while deeper bedrock does increase foundation "
        "costs, these costs were neither prohibitively high nor were they large compared to the overall cost "
        "of building a skyscraper. What I enjoyed the most about this chapter was Barr's discussion of how "
        "foundations are actually built. He describes the use of caissons, which enable workers to dig down "
        "for considerable distances, often below the water table, until they reach bedrock. Barr's thorough "
        "technological history discusses not only how caissons work, but also the dangers involved. While this "
        "chapter references empirical research papers, it is a relatively easy read.\n\n"
        "Chapters eight and nine focus on the birth of Midtown and the building boom of the 1920s. "
        "Chapter eight contains lengthy discussions of urban economic theory that may serve as a "
        "distraction to readers primarily interested in New York. However, they would be well-suited for "
        "undergraduates learning about the economics of cities. In the next chapter, Barr considers two of "
        "the primary explanations for the building boom of the 1920s — the first being exuberance, and "
        "the second being financing. He uses data to assess the viability of these two explanations and "
        "finds that supply and demand factors explain much of the development of the 1920s; though it "
        "enabled the boom, cheap credit was not, he argues, the primary cause.\n\n"
        "In the final chapter (chapter 10), Barr discusses another of his empirical papers that estimates "
        "Manhattan land values from the mid-19th century to the present day. The data work that went into "
        "these estimations is particularly impressive. Toward the end of the chapter, Barr assesses 'whether "
        "skyscrapers are a cause or an effect of high land values'. He finds that changes in land values "
        "predict future building height, but the reverse is not true. The book ends with an epilogue, in "
        "which Barr discusses the impact of climate change on the city and makes policy suggestions for "
        "New York going forward."
    ),
    "t4_p1": (
        "Bats to the rescue\n\n"
        "How Madagascar's bats are helping to save the rainforest\n\n"
        "There are few places in the world where relations between agriculture and conservation are more "
        "strained. Madagascar's forests are being converted to agricultural land at a rate of one percent "
        "every year. Much of this destruction is fuelled by the cultivation of the country's main staple "
        "crop: rice. And a key reason for this destruction is that insect pests are destroying vast quantities "
        "of what is grown by local subsistence farmers, leading them to clear forest to create new paddy "
        "fields. The result is devastating habitat and biodiversity loss on the island, but not all species "
        "are suffering. In fact, some of the island's insectivorous bats are currently thriving and this has "
        "important implications for farmers and conservationists alike.\n\n"
        "Enter University of Cambridge zoologist Ricardo Rocha. He's passionate about conservation, "
        "and bats. More specifically, he's interested in how bats are responding to human activity and "
        "deforestation in particular. Rocha's new study shows that several species of bats are giving "
        "Madagascar's rice farmers a vital pest control service by feasting on plagues of insects. And this, "
        "he believes, can ease the financial pressure on farmers to turn forest into fields.\n\n"
        "Bats comprise roughly one-fifth of all mammal species in Madagascar and thirty-six recorded bat "
        "species are native to the island, making it one of the most important regions for conservation of "
        "this animal group anywhere in the world.\n\n"
        "Co-leading an international team of scientists, Rocha found that several species of indigenous "
        "bats are taking advantage of habitat modification to hunt insects swarming above the country's "
        "rice fields. They include the Malagasy mouse-eared bat, Major's long-fingered bat, the Malagasy "
        "white-bellied free-tailed bat and Peters' wrinkle-lipped bat.\n\n"
        "'These winner species are providing a valuable free service to Madagascar as biological pest "
        "suppressors,' says Rocha. 'We found that six species of bat are preying on rice pests, including the "
        "paddy swarming caterpillar and grass webworm. The damage which these insects cause puts the "
        "island's farmers under huge financial pressure and that encourages deforestation.'\n\n"
        "The study, now published in the journal Agriculture, Ecosystems and Environment, set out to "
        "investigate the feeding activity of insectivorous bats in the farmland bordering the Ranomafana "
        "National Park in the southeast of the country.\n\n"
        "Rocha and his team used state-of-the-art ultrasonic recorders to record over a thousand bat "
        "'feeding buzzes' (echolocation sequences used by bats to target their prey) at 54 sites, in order "
        "to identify the favourite feeding spots of the bats. They next used DNA barcoding techniques to "
        "analyse droppings collected from bats at the different sites.\n\n"
        "The recordings revealed that bat activity over rice fields was much higher than it was in "
        "continuous forest – seven times higher over rice fields which were on flat ground, and sixteen "
        "times higher over fields on the sides of hills – leaving no doubt that the animals are preferentially "
        "foraging in these man-made ecosystems. The researchers suggest that the bats favour these fields "
        "because lack of water and nutrient run-off make these crops more susceptible to insect pest "
        "infestations. DNA analysis showed that all six species of bat had fed on economically important "
        "insect pests. While the findings indicated that rice farming benefits most from the bats, the "
        "scientists also found indications that the bats were consuming pests of other crops, including the "
        "black twig borer (which infests coffee plants), the sugarcane cicada, the macadamia nut-borer, and "
        "the sober tabby (a pest of citrus fruits).\n\n"
        "'The effectiveness of bats as pest controllers has already been proven in the USA and Catalonia,' "
        "said co-author James Kemp, from the University of Lisbon. 'But our study is the first to show this "
        "happening in Madagascar, where the stakes for both farmers and conservationists are so high.'\n\n"
        "Local people may have a further reason to be grateful to their bats. While the animal is often "
        "associated with spreading disease, Rocha and his team found evidence that Malagasy bats feed "
        "not just on crop pests but also on mosquitoes – carriers of malaria, Rift Valley fever virus and "
        "elephantiasis – as well as blackflies, which spread river blindness.\n\n"
        "Rocha points out that the relationship is complicated. When food is scarce, bats become a crucial "
        "source of protein for local people. Even the children will hunt them. And as well as roosting in "
        "trees, the bats sometimes roost in buildings, but are not welcomed there because they make them "
        "unclean. At the same time, however, they are associated with sacred caves and the ancestors, so "
        "they can be viewed as beings between worlds, which makes them very significant in the culture of "
        "the people. And one potential problem is that while these bats are benefiting from farming, at the "
        "same time deforestation is reducing the places where they can roost, which could have long-term "
        "effects on their numbers. Rocha says, 'With the right help, we hope that farmers can promote this "
        "mutually beneficial relationship by installing bat houses.'\n\n"
        "Rocha and his colleagues believe that maximising bat populations can help to boost crop yields "
        "and promote sustainable livelihoods. The team is now calling for further research to quantify this "
        "contribution. 'I'm very optimistic,' says Rocha. 'If we give nature a hand, we can speed up the "
        "process of regeneration.'"
    ),
    "t4_p2": (
        "Does education fuel economic growth?\n\n"
        "A\nOver the last decade, a huge database about the lives of southwest German villagers "
        "between 1600 and 1900 has been compiled by a team led by Professor Sheilagh Ogilvie "
        "at Cambridge University's Faculty of Economics. It includes court records, guild ledgers, "
        "parish registers, village censuses, tax lists and – the most recent addition – 9,000 handwritten "
        "inventories listing over a million personal possessions belonging to ordinary women and "
        "men across three centuries. Ogilvie, who discovered the inventories in the archives of two "
        "German communities 30 years ago, believes they may hold the answer to a conundrum that "
        "has long puzzled economists: the lack of evidence for a causal link between education and a "
        "country's economic growth.\n\n"
        "B\nAs Ogilvie explains, 'Education helps us to work more productively, invent better "
        "technology, and earn more … surely it must be critical for economic growth? But, if you "
        "look back through history, there's no evidence that having a high literacy rate made a "
        "country industrialise earlier.' Between 1600 and 1900, England had only mediocre literacy "
        "rates by European standards, yet its economy grew fast and it was the first country to "
        "industrialise. During this period, Germany and Scandinavia had excellent literacy rates, but "
        "their economies grew slowly and they industrialised late. 'Modern cross-country analyses "
        "have also struggled to find evidence that education causes economic growth, even though "
        "there is plenty of evidence that growth increases education,' she adds.\n\n"
        "C\nIn the handwritten inventories that Ogilvie is analysing are the belongings of women and "
        "men at marriage, remarriage and death. From badger skins to Bibles, sewing machines to "
        "scarlet bodices – the villagers' entire worldly goods are included. Inventories of agricultural "
        "equipment and craft tools reveal economic activities; ownership of books and education-"
        "related objects like pens and slates suggests how people learned. In addition, the tax lists "
        "included in the database record the value of farms, workshops, assets and debts; signatures "
        "and people's estimates of their age indicate literacy and numeracy levels; and court records "
        "reveal obstacles (such as the activities of the guilds) that stifled industry.\n\n"
        "Previous studies usually had just one way of linking education with economic growth – the "
        "presence of schools and printing presses, perhaps, or school enrolment, or the ability to "
        "sign names. According to Ogilvie, the database provides multiple indicators for the same "
        "individuals, making it possible to analyse links between literacy, numeracy, wealth, and "
        "industriousness, for individual women and men over the long term.\n\n"
        "D\nOgilvie and her team have been building the vast database of material possessions on top "
        "of their full demographic reconstruction of the people who lived in these two German "
        "communities. 'We can follow the same people – and their descendants – across 300 years "
        "of educational and economic change,' she says. Individual lives have unfolded before their "
        "eyes. Stories like that of the 24-year-olds Ana Regina and Magdalena Riethmüllerin, who "
        "were chastised in 1707 for reading books in church instead of listening to the sermon. 'This "
        "tells us they were continuing to develop their reading skills at least a decade after leaving "
        "school,' explains Ogilvie. The database also reveals the case of Juliana Schweickherdt, a "
        "50-year-old spinster living in the small Black Forest community of Wildberg, who was "
        "reprimanded in 1752 by the local weavers' guild for 'weaving cloth and combing wool, "
        "counter to the guild ordinance'. When Juliana continued taking jobs reserved for male guild "
        "members, she was summoned before the guild court and told to pay a fine equivalent to one "
        "third of a servant's annual wage. It was a small act of defiance by today's standards, but it "
        "reflects a time when laws in Germany and elsewhere regulated people's access to labour "
        "markets. The dominance of guilds not only prevented people from using their skills, but also "
        "held back even the simplest industrial innovation.\n\n"
        "E\nThe data-gathering phase of the project has been completed and now, according to Ogilvie, "
        "it is time 'to ask the big questions'. One way to look at whether education causes economic "
        "growth is to 'hold wealth constant'. This involves following the lives of different people with "
        "the same level of wealth over a period of time. If wealth is constant, it is possible to discover "
        "whether education was, for example, linked to the cultivation of new crops, or to the "
        "adoption of industrial innovations like sewing machines. The team will also ask what aspect "
        "of education helped people engage more with productive and innovative activities. Was it, "
        "for instance, literacy, numeracy, book ownership, years of schooling? Was there a threshold "
        "level – a tipping point – that needed to be reached to affect economic performance?\n\n"
        "F\nOgilvie hopes to start finding answers to these questions over the next few years. One "
        "thing is already clear, she says: the relationship between education and economic growth "
        "is far from straightforward. 'German-speaking central Europe is an excellent laboratory "
        "for testing theories of economic growth,' she explains. Between 1600 and 1900, literacy "
        "rates and book ownership were high and yet the region remained poor. It was also the case "
        "that local guilds and merchant associations were extremely powerful and legislated against "
        "anything that undermined their monopolies. In villages throughout the region, guilds "
        "blocked labour migration and resisted changes that might reduce their influence.\n\n"
        "'Early findings suggest that the potential benefits of education for the economy can be held "
        "back by other barriers, and this has implications for today,' says Ogilvie. 'Huge amounts "
        "are spent improving education in developing countries, but this spending can fail to deliver "
        "economic growth if restrictions block people – especially women and the poor – from using "
        "their education in economically productive ways. If economic institutions are poorly set up, "
        "for instance, education can't lead to growth.'"
    ),
    "t4_p3": (
        "Timur Gareyev – blindfold chess champion\n\n"
        "A\nNext month, a chess player named Timur Gareyev will take on nearly 50 opponents "
        "at once. But that is not the hard part. While his challengers will play the games as "
        "normal, Gareyev himself will be blindfolded. Even by world record standards, it "
        "sets a high bar for human performance. The 28-year-old already stands out in the "
        "rarefied world of blindfold chess. He has a fondness for bright clothes and unusual "
        "hairstyles, and he gets his kicks from the adventure sport of BASE jumping. He has "
        "already proved himself a strong chess player, too. In a 10-hour chess marathon in "
        "2013, Gareyev played 33 games in his head simultaneously. He won 29 and lost "
        "none. The skill has become his brand: he calls himself the Blindfold King.\n\n"
        "B\nBut Gareyev's prowess has drawn interest from beyond the chess-playing "
        "community. In the hope of understanding how he and others like him can perform "
        "such mental feats, researchers at the University of California in Los Angeles "
        "(UCLA) called him in for tests. They now have their first results. 'The ability to play "
        "a game of chess with your eyes closed is not a far reach for most accomplished "
        "players,' said Jesse Rissman, who runs a memory lab at UCLA. 'But the thing that's "
        "so remarkable about Timur and a few other individuals is the number of games they "
        "can keep active at once. To me it is simply astonishing.'\n\n"
        "C\nGareyev learned to play chess in his native Uzbekistan when he was six years old. "
        "Tutored by his grandfather, he entered his first tournament aged eight and soon "
        "became obsessed with competitions. At 16, he was crowned Asia's youngest ever "
        "chess grandmaster. He moved to the US soon after, and as a student helped his "
        "university win its first national chess championship. In 2013, Gareyev was ranked "
        "the third best chess player in the US.\n\n"
        "D\nTo the uninitiated, blindfold chess seems to call for superhuman skill. But displays "
        "of the feat go back centuries. The first recorded game in Europe was played in "
        "13th-century Florence. In 1947, the Argentinian grandmaster Miguel Najdorf played "
        "45 simultaneous games in his mind, winning 39 in the 24-hour session.\n\n"
        "E\nAccomplished players can develop the skill of playing blind even without realising "
        "it. The nature of the game is to run through possible moves in the mind to see "
        "how they play out. From this, regular players develop a memory for the patterns "
        "the pieces make, the defences and attacks. 'You recreate it in your mind,' said "
        "Gareyev. 'A lot of players are capable of doing what I'm doing.' The real mental "
        "challenge comes from playing multiple games at once in the head. Not only must "
        "the positions of each piece on every board be memorised, they must be recalled "
        "faithfully when needed, updated with each player's moves, and then reliably stored "
        "again, so the brain can move on to the next board. First moves can be tough to "
        "remember because they are fairly uninteresting. But the ends of games are taxing "
        "too, as exhaustion sets in. When Gareyev is tired, his recall can get patchy. He "
        "sometimes makes moves based on only a fragmented memory of the pieces' positions.\n\n"
        "F\nThe scientists first had Gareyev perform some standard memory tests. These "
        "assessed his ability to hold numbers, pictures and words in mind. One classic test "
        "measures how many numbers a person can repeat, both forwards and backwards, "
        "soon after hearing them. Most people manage about seven. 'He was not "
        "exceptional on any of these standard tests,' said Rissman. 'We didn't find anything "
        "other than playing chess that he seems to be supremely gifted at.' But next came "
        "the brain scans. With Gareyev lying down in the machine, Rissman looked at how "
        "well connected the various regions of the chess player's brain were. Though the "
        "results are tentative and as yet unpublished, the scans found much greater than "
        "average communication between parts of Gareyev's brain that make up what is "
        "called the frontoparietal control network. Of 63 people scanned alongside the chess "
        "player, only one or two scored more highly on the measure. 'You use this network in "
        "almost any complex task. It helps you to allocate attention, keep rules in mind, and "
        "work out whether you should be responding or not,' said Rissman.\n\n"
        "G\nIt was not the only hint of something special in Gareyev's brain. The scans also "
        "suggest that Gareyev's visual network is more highly connected to other brain parts "
        "than usual. Initial results suggest that the areas of his brain that process visual "
        "images – such as chess boards – may have stronger links to other brain regions, "
        "and so be more powerful than normal. While the analyses are not finalised yet, they "
        "may hold the first clues to Gareyev's extraordinary ability.\n\n"
        "H\nFor the world record attempt, Gareyev hopes to play 47 blindfold games at once in "
        "about 16 hours. He will need to win 80% to claim the title. 'I don't worry too much "
        "about the winning percentage, that's never been an issue for me,' he said. 'The "
        "most important part of blindfold chess for me is that I have found the one thing that "
        "I can fully dedicate myself to. I miss having an obsession.'"
    ),
}


# ============================================================
# READING TESTS DATA
# ============================================================

def build_reading():
    """Build all 4 tests of reading data."""
    tests = []

    # --- TEST 1 ---
    tests.append({
        "id": "cam17_test1",
        "testNumber": 1,
        "passages": [
            {
                "id": "cam17_t1_p1", "title": "The development of the London underground railway",
                "text": PASSAGE_TEXTS["t1_p1"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t1_r_q1", "type": "notes_completion", "question": "The 1. _____ of London increased rapidly between 1800 and 1850", "options": [], "correctAnswer": "population"},
                    {"id": "cam17_t1_r_q2", "type": "notes_completion", "question": "Building the railway would make it possible to move people to better housing in the 2. _____", "options": [], "correctAnswer": "suburbs"},
                    {"id": "cam17_t1_r_q3", "type": "notes_completion", "question": "A number of 3. _____ agreed with Pearson's idea", "options": [], "correctAnswer": "businessmen"},
                    {"id": "cam17_t1_r_q4", "type": "notes_completion", "question": "The company initially had problems getting the 4. _____ needed for the project", "options": [], "correctAnswer": "funding"},
                    {"id": "cam17_t1_r_q5", "type": "notes_completion", "question": "Negative articles about the project appeared in the 5. _____", "options": [], "correctAnswer": "press"},
                    {"id": "cam17_t1_r_q6", "type": "notes_completion", "question": "With the completion of the brick arch, the tunnel was covered with 6. _____", "options": [], "correctAnswer": "soil"},
                    {"id": "cam17_t1_r_q7", "type": "tfng", "question": "Other countries had built underground railways before the Metropolitan line opened.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t1_r_q8", "type": "tfng", "question": "More people than predicted travelled on the Metropolitan line on the first day.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t1_r_q9", "type": "tfng", "question": "The use of ventilation shafts failed to prevent pollution in the tunnels.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t1_r_q10", "type": "tfng", "question": "A different approach from the 'cut and cover' technique was required in London's central area.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t1_r_q11", "type": "tfng", "question": "The windows on City & South London trains were at eye level.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t1_r_q12", "type": "tfng", "question": "The City & South London Railway was a financial success.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t1_r_q13", "type": "tfng", "question": "Trains on the 'Tuppenny Tube' nearly always ran on time.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                ]
            },
            {
                "id": "cam17_t1_p2", "title": "Stadiums: past, present and future",
                "text": PASSAGE_TEXTS["t1_p2"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t1_r_q14", "type": "matching_info", "question": "a mention of negative attitudes towards stadium building projects (Section)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "A"},
                    {"id": "cam17_t1_r_q15", "type": "matching_info", "question": "figures demonstrating the environmental benefits of a certain stadium (Section)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "F"},
                    {"id": "cam17_t1_r_q16", "type": "matching_info", "question": "examples of the wide range of facilities available at some new stadiums (Section)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "E"},
                    {"id": "cam17_t1_r_q17", "type": "matching_info", "question": "reference to the disadvantages of the stadiums built during a certain era (Section)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "D"},
                    {"id": "cam17_t1_r_q18", "type": "summary_completion", "question": "The amphitheatre of Arles was converted first into a 18. _____", "options": [], "correctAnswer": "fortress"},
                    {"id": "cam17_t1_r_q19", "type": "summary_completion", "question": "then into an arena where spectators could watch 19. _____", "options": [], "correctAnswer": "bullfights"},
                    {"id": "cam17_t1_r_q20", "type": "summary_completion", "question": "the arena in Verona is famous today as a venue where 20. _____ is performed", "options": [], "correctAnswer": "opera"},
                    {"id": "cam17_t1_r_q21", "type": "summary_completion", "question": "Lucca's amphitheatre was used for storage of 21. _____", "options": [], "correctAnswer": "salt"},
                    {"id": "cam17_t1_r_q22", "type": "summary_completion", "question": "It is now a market square with 22. _____ and homes incorporated", "options": [], "correctAnswer": "shops"},
                    {"id": "cam17_t1_r_q23", "type": "multiple_choice_multi", "question": "Which TWO negative features of 20th-century stadiums vs ancient amphitheatres?", "options": ["A. less imaginatively designed", "B. less spacious", "C. less convenient locations", "D. less versatile", "E. less durable materials"], "correctAnswer": "C,D"},
                    {"id": "cam17_t1_r_q24", "type": "multiple_choice_multi", "question": "Q23 second option", "options": ["A. less imaginatively designed", "B. less spacious", "C. less convenient locations", "D. less versatile", "E. less durable materials"], "correctAnswer": "C,D"},
                    {"id": "cam17_t1_r_q25", "type": "multiple_choice_multi", "question": "Which TWO advantages of modern stadium design?", "options": ["A. improved amenities for sports", "B. bringing community life to cities", "C. facilitating solar/wind research", "D. enabling reduced electricity consumption", "E. providing sites for renewable power"], "correctAnswer": "B,E"},
                    {"id": "cam17_t1_r_q26", "type": "multiple_choice_multi", "question": "Q25 second option", "options": ["A. improved amenities for sports", "B. bringing community life to cities", "C. facilitating solar/wind research", "D. enabling reduced electricity consumption", "E. providing sites for renewable power"], "correctAnswer": "B,E"},
                ]
            },
            {
                "id": "cam17_t1_p3", "title": "To catch a king",
                "text": PASSAGE_TEXTS["t1_p3"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t1_r_q27", "type": "matching_sentence", "question": "Charles II formed a 27. _____ with the Scots", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "H"},
                    {"id": "cam17_t1_r_q28", "type": "matching_sentence", "question": "he abandoned an important 28. _____ held by his father", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "J"},
                    {"id": "cam17_t1_r_q29", "type": "matching_sentence", "question": "The battle led to a 29. _____ for the Parliamentarians", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "F"},
                    {"id": "cam17_t1_r_q30", "type": "matching_sentence", "question": "A 30. _____ was offered for Charles's capture", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "B"},
                    {"id": "cam17_t1_r_q31", "type": "matching_sentence", "question": "he eventually reached the 31. _____ of continental Europe", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "D"},
                    {"id": "cam17_t1_r_q32", "type": "ynng", "question": "Charles chose Pepys for the task because he considered him to be trustworthy.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t1_r_q33", "type": "ynng", "question": "Charles's personal recollection of the escape lacked sufficient detail.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t1_r_q34", "type": "ynng", "question": "Charles indicated to Pepys that he had planned his escape before the battle.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t1_r_q35", "type": "ynng", "question": "The inclusion of Charles's account is a positive aspect of the book.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
                    {"id": "cam17_t1_r_q36", "type": "multiple_choice", "question": "What is the reviewer's main purpose in the first paragraph?", "options": ["A. to describe the Battle of Worcester", "B. to give an account of circumstances leading to Charles II's escape", "C. to provide details of Parliamentarians' political views", "D. to compare Charles II's beliefs with those of his father"], "correctAnswer": "B"},
                    {"id": "cam17_t1_r_q37", "type": "multiple_choice", "question": "Why does the reviewer include examples of the fugitives' behaviour in the third paragraph?", "options": ["A. to explain how close Charles came to losing his life", "B. to suggest supporters were badly prepared", "C. to illustrate how events of the six weeks are brought to life", "D. to argue certain aspects are not as well known"], "correctAnswer": "C"},
                    {"id": "cam17_t1_r_q38", "type": "multiple_choice", "question": "What point does the reviewer make about Charles II in the fourth paragraph?", "options": ["A. He chose to celebrate what was essentially a defeat.", "B. He misunderstood the motives of his opponents.", "C. He aimed to restore people's faith in the monarchy.", "D. He was driven by a desire to be popular."], "correctAnswer": "A"},
                    {"id": "cam17_t1_r_q39", "type": "multiple_choice", "question": "What does the reviewer say about Charles Spencer in the fifth paragraph?", "options": ["A. His decision to write the book is a surprise.", "B. He takes an unbiased approach to the subject matter.", "C. His descriptions would be better with more detail.", "D. He chooses language suitable for a 21st-century audience."], "correctAnswer": "B"},
                    {"id": "cam17_t1_r_q40", "type": "multiple_choice", "question": "When the reviewer says the book 'doesn't quite hit the mark', she is making the point that", "options": ["A. it overlooks the impact on ordinary people.", "B. it lacks analysis of prevalent views on monarchy.", "C. it omits references to Charles II's deceit in hiding.", "D. it fails to address whether Charles II's experiences had a lasting influence."], "correctAnswer": "D"},
                ]
            }
        ]
    })

    # --- TEST 2 ---
    tests.append({
        "id": "cam17_test2",
        "testNumber": 2,
        "passages": [
            {
                "id": "cam17_t2_p1", "title": "The Dead Sea Scrolls",
                "text": PASSAGE_TEXTS["t2_p1"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t2_r_q1", "type": "notes_completion", "question": "heard a noise of breaking when one teenager threw a 1. _____", "options": [], "correctAnswer": "rock"},
                    {"id": "cam17_t2_r_q2", "type": "notes_completion", "question": "teenagers went into the 2. _____ and found containers", "options": [], "correctAnswer": "cave"},
                    {"id": "cam17_t2_r_q3", "type": "notes_completion", "question": "made of 3. _____", "options": [], "correctAnswer": "clay"},
                    {"id": "cam17_t2_r_q4", "type": "notes_completion", "question": "thought to have been written by group known as the 4. _____", "options": [], "correctAnswer": "Essenes"},
                    {"id": "cam17_t2_r_q5", "type": "notes_completion", "question": "written mainly in the 5. _____ language", "options": [], "correctAnswer": "Hebrew"},
                    {"id": "cam17_t2_r_q6", "type": "tfng", "question": "The Bedouin teenagers who found the scrolls were disappointed by how little money they received.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t2_r_q7", "type": "tfng", "question": "There is agreement among academics about the origin of the Dead Sea Scrolls.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t2_r_q8", "type": "tfng", "question": "Most of the books of the Bible written on the scrolls are incomplete.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t2_r_q9", "type": "tfng", "question": "The information on the Copper Scroll is written in an unusual way.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t2_r_q10", "type": "tfng", "question": "Mar Samuel was given some of the scrolls as a gift.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t2_r_q11", "type": "tfng", "question": "In the early 1950s, a number of US educational establishments were keen to buy scrolls from Mar Samuel.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t2_r_q12", "type": "tfng", "question": "The scroll pieced together in 2017 contains information about annual occasions in the Qumran area 2,000 years ago.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t2_r_q13", "type": "tfng", "question": "Academics at the University of Haifa are currently researching how to decipher the final scroll.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                ]
            },
            {
                "id": "cam17_t2_p2", "title": "A second attempt at domesticating the tomato",
                "text": PASSAGE_TEXTS["t2_p2"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t2_r_q14", "type": "matching_info", "question": "a reference to a type of tomato that can resist a dangerous infection (Section)", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C"},
                    {"id": "cam17_t2_r_q15", "type": "matching_info", "question": "an explanation of how problems can arise from focusing only on a certain type of tomato plant (Section)", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B"},
                    {"id": "cam17_t2_r_q16", "type": "matching_info", "question": "a number of examples of plants that are not cultivated at present but could be useful as food sources (Section)", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "E"},
                    {"id": "cam17_t2_r_q17", "type": "matching_info", "question": "a comparison between the early domestication of the tomato and more recent research (Section)", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q18", "type": "matching_info", "question": "a personal reaction to the flavour of a tomato that has been genetically edited (Section)", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C"},
                    {"id": "cam17_t2_r_q19", "type": "matching_names", "question": "Domestication of certain plants could allow them to adapt to future environmental challenges.", "options": ["A. Jorg Kudla", "B. Caixia Gao", "C. Joyce Van Eck", "D. Jonathan Jones"], "correctAnswer": "B"},
                    {"id": "cam17_t2_r_q20", "type": "matching_names", "question": "The idea of growing and eating unusual plants may not be accepted on a large scale.", "options": ["A. Jorg Kudla", "B. Caixia Gao", "C. Joyce Van Eck", "D. Jonathan Jones"], "correctAnswer": "D"},
                    {"id": "cam17_t2_r_q21", "type": "matching_names", "question": "It is not advisable for the future direction of certain research to be made public.", "options": ["A. Jorg Kudla", "B. Caixia Gao", "C. Joyce Van Eck", "D. Jonathan Jones"], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q22", "type": "matching_names", "question": "Present efforts to domesticate one wild fruit are limited by the costs involved.", "options": ["A. Jorg Kudla", "B. Caixia Gao", "C. Joyce Van Eck", "D. Jonathan Jones"], "correctAnswer": "C"},
                    {"id": "cam17_t2_r_q23", "type": "matching_names", "question": "Humans only make use of a small proportion of the plant food available on Earth.", "options": ["A. Jorg Kudla", "B. Caixia Gao", "C. Joyce Van Eck", "D. Jonathan Jones"], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q24", "type": "sentence_completion", "question": "An undesirable trait such as loss of 24. _____ may be caused by a mutation in a tomato gene.", "options": [], "correctAnswer": "flavour / flavor"},
                    {"id": "cam17_t2_r_q25", "type": "sentence_completion", "question": "By modifying one gene, researchers made the tomato three times its original 25. _____", "options": [], "correctAnswer": "size"},
                    {"id": "cam17_t2_r_q26", "type": "sentence_completion", "question": "A type of tomato which was not badly affected by 26. _____, and was rich in vitamin C.", "options": [], "correctAnswer": "salt"},
                ]
            },
            {
                "id": "cam17_t2_p3", "title": "Insight or evolution?",
                "text": PASSAGE_TEXTS["t2_p3"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t2_r_q27", "type": "multiple_choice", "question": "The purpose of the first paragraph is to", "options": ["A. defend particular ideas.", "B. compare certain beliefs.", "C. disprove a widely held view.", "D. outline a common assumption."], "correctAnswer": "D"},
                    {"id": "cam17_t2_r_q28", "type": "multiple_choice", "question": "What are the writers doing in the second paragraph?", "options": ["A. criticising an opinion", "B. justifying a standpoint", "C. explaining an approach", "D. supporting an argument"], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q29", "type": "multiple_choice", "question": "In the third paragraph, what do the writers suggest about Darwin and Einstein?", "options": ["A. They represent an exception to a general rule.", "B. Their way of working has been misunderstood.", "C. They are an ideal which others should aspire to.", "D. Their achievements deserve greater recognition."], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q30", "type": "multiple_choice", "question": "John Nicholson is an example of a person whose idea", "options": ["A. established his reputation as an influential scientist.", "B. was only fully understood at a later point in history.", "C. laid the foundations for someone else's breakthrough.", "D. initially met with scepticism from the scientific community."], "correctAnswer": "C"},
                    {"id": "cam17_t2_r_q31", "type": "multiple_choice", "question": "What is the key point of interest about the 'acey-deucy' stirrup placement?", "options": ["A. the simple reason why it was invented", "B. the enthusiasm with which it was adopted", "C. the research that went into its development", "D. the cleverness of the person who first used it"], "correctAnswer": "A"},
                    {"id": "cam17_t2_r_q32", "type": "ynng", "question": "Acknowledging people such as Plato or da Vinci as geniuses will help us understand the process by which great minds create new ideas.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t2_r_q33", "type": "ynng", "question": "The Law of Effect was discovered at a time when psychologists were seeking a scientific reason why creativity occurs.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t2_r_q34", "type": "ynng", "question": "The Law of Effect states that no planning is involved in the behaviour of organisms.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
                    {"id": "cam17_t2_r_q35", "type": "ynng", "question": "The Law of Effect sets out clear explanations about the sources of new ideas and behaviours.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t2_r_q36", "type": "ynng", "question": "Many scientists are now turning away from the notion of intelligent design and genius.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t2_r_q37", "type": "matching_sentence", "question": "The traditional view: breakthroughs happen when a single great mind has sudden 37. _____", "options": ["A. invention", "B. goals", "C. compromise", "D. mistakes", "E. luck", "F. inspiration", "G. experiments"], "correctAnswer": "F"},
                    {"id": "cam17_t2_r_q38", "type": "matching_sentence", "question": "this process involves 38. _____, such as Nicholson's theory about proto-elements.", "options": ["A. invention", "B. goals", "C. compromise", "D. mistakes", "E. luck", "F. inspiration", "G. experiments"], "correctAnswer": "D"},
                    {"id": "cam17_t2_r_q39", "type": "matching_sentence", "question": "there is also often an element of 39. _____, e.g., the coincidence of ideas leading to the Post-It note.", "options": ["A. invention", "B. goals", "C. compromise", "D. mistakes", "E. luck", "F. inspiration", "G. experiments"], "correctAnswer": "E"},
                    {"id": "cam17_t2_r_q40", "type": "matching_sentence", "question": "there may be no clear 40. _____ involved, but merely a process of variation and selection.", "options": ["A. invention", "B. goals", "C. compromise", "D. mistakes", "E. luck", "F. inspiration", "G. experiments"], "correctAnswer": "B"},
                ]
            }
        ]
    })

    # --- TEST 3 ---
    tests.append({
        "id": "cam17_test3",
        "testNumber": 3,
        "passages": [
            {
                "id": "cam17_t3_p1", "title": "The thylacine",
                "text": PASSAGE_TEXTS["t3_p1"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t3_r_q1", "type": "notes_completion", "question": "ate an entirely 1. _____ diet", "options": [], "correctAnswer": "carnivorous"},
                    {"id": "cam17_t3_r_q2", "type": "notes_completion", "question": "probably depended mainly on 2. _____ when hunting", "options": [], "correctAnswer": "scent"},
                    {"id": "cam17_t3_r_q3", "type": "notes_completion", "question": "young spent first months of life inside its mother's 3. _____", "options": [], "correctAnswer": "pouch"},
                    {"id": "cam17_t3_r_q4", "type": "notes_completion", "question": "last evidence in mainland Australia is a 3,100-year-old 4. _____", "options": [], "correctAnswer": "fossil"},
                    {"id": "cam17_t3_r_q5", "type": "notes_completion", "question": "reduction in 5. _____ and available sources of food were partly responsible for decline in Tasmania", "options": [], "correctAnswer": "habitat"},
                    {"id": "cam17_t3_r_q6", "type": "tfng", "question": "Significant numbers of thylacines were killed by humans from the 1830s onwards.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t3_r_q7", "type": "tfng", "question": "Several thylacines were born in zoos during the late 1800s.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t3_r_q8", "type": "tfng", "question": "John Gould's prediction about the thylacine surprised some biologists.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t3_r_q9", "type": "tfng", "question": "In the early 1900s, many scientists became worried about the possible extinction of the thylacine.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t3_r_q10", "type": "tfng", "question": "T. T. Flynn's proposal to rehome captive thylacines on an island proved to be impractical.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t3_r_q11", "type": "tfng", "question": "There were still reasonable numbers of thylacines in existence when a piece of legislation protecting the species during their breeding season was passed.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t3_r_q12", "type": "tfng", "question": "From 1930 to 1936, the only known living thylacines were all in captivity.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t3_r_q13", "type": "tfng", "question": "Attempts to find living thylacines are now rarely made.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                ]
            },
            {
                "id": "cam17_t3_p2", "title": "Palm oil",
                "text": PASSAGE_TEXTS["t3_p2"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t3_r_q14", "type": "matching_info", "question": "examples of a range of potential environmental advantages of oil palm tree cultivation (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "F"},
                    {"id": "cam17_t3_r_q15", "type": "matching_info", "question": "description of an organisation which controls the environmental impact of palm oil production (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "G"},
                    {"id": "cam17_t3_r_q16", "type": "matching_info", "question": "examples of the widespread global use of palm oil (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "A"},
                    {"id": "cam17_t3_r_q17", "type": "matching_info", "question": "reference to a particular species which could benefit the ecosystem of oil palm plantations (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "H"},
                    {"id": "cam17_t3_r_q18", "type": "matching_info", "question": "figures illustrating the rapid expansion of the palm oil industry (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "B"},
                    {"id": "cam17_t3_r_q19", "type": "matching_info", "question": "an economic justification for not opposing the palm oil industry (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "E"},
                    {"id": "cam17_t3_r_q20", "type": "matching_info", "question": "examples of creatures badly affected by the establishment of oil palm plantations (Section)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "C"},
                    {"id": "cam17_t3_r_q21", "type": "multiple_choice_multi", "question": "Which TWO statements are made about the RSPO?", "options": ["A. Its membership has grown steadily.", "B. It demands that certified producers be open and honest.", "C. It took several years to establish its criteria.", "D. Its regulations are stricter than other industries.", "E. It was formed at the request of environmentalists."], "correctAnswer": "B,C"},
                    {"id": "cam17_t3_r_q22", "type": "multiple_choice_multi", "question": "Q21 second option", "options": ["A. Its membership has grown steadily.", "B. It demands that certified producers be open and honest.", "C. It took several years to establish its criteria.", "D. Its regulations are stricter than other industries.", "E. It was formed at the request of environmentalists."], "correctAnswer": "B,C"},
                    {"id": "cam17_t3_r_q23", "type": "sentence_completion", "question": "One advantage of palm oil for manufacturers is that it stays 23. _____ even when not refrigerated.", "options": [], "correctAnswer": "solid"},
                    {"id": "cam17_t3_r_q24", "type": "sentence_completion", "question": "The 24. _____ is the best known of the animals suffering habitat loss as a result of the spread of oil palm plantations.", "options": [], "correctAnswer": "Sumatran orangutan"},
                    {"id": "cam17_t3_r_q25", "type": "sentence_completion", "question": "As one of its criteria, the RSPO insists that growers check 25. _____ on a routine basis.", "options": [], "correctAnswer": "carbon stocks"},
                    {"id": "cam17_t3_r_q26", "type": "sentence_completion", "question": "Ellwood and his researchers are looking into whether the bird's nest fern could restore 26. _____ in areas where oil palm trees are grown.", "options": [], "correctAnswer": "biodiversity"},
                ]
            },
            {
                "id": "cam17_t3_p3", "title": "Building the Skyline: The Birth and Growth of Manhattan's Skyscrapers",
                "text": PASSAGE_TEXTS["t3_p3"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t3_r_q27", "type": "multiple_choice", "question": "What point does Shester make about Barr's book in the first paragraph?", "options": ["A. It gives a highly original explanation for urban development.", "B. Elements of Barr's research papers are incorporated throughout the book.", "C. Other books on the subject have taken a different approach.", "D. It covers a range of factors that affected the development of New York."], "correctAnswer": "D"},
                    {"id": "cam17_t3_r_q28", "type": "multiple_choice", "question": "How does Shester respond to the information in the book about tenements?", "options": ["A. She describes the reasons for Barr's interest.", "B. She indicates a potential problem with Barr's analysis.", "C. She compares Barr's conclusion with that of other writers.", "D. She provides details about the sources Barr used for his research."], "correctAnswer": "B"},
                    {"id": "cam17_t3_r_q29", "type": "multiple_choice", "question": "What does Shester say about chapter six of the book?", "options": ["A. It contains conflicting data.", "B. It focuses too much on possible trends.", "C. It is too specialised for most readers.", "D. It draws on research that is out of date."], "correctAnswer": "C"},
                    {"id": "cam17_t3_r_q30", "type": "multiple_choice", "question": "What does Shester suggest about the chapters focusing on the 1920s building boom?", "options": ["A. The information should have been organised differently.", "B. More facts are needed about the way construction was financed.", "C. The explanation that is given for the building boom is unlikely.", "D. Some parts will have limited appeal to certain people."], "correctAnswer": "D"},
                    {"id": "cam17_t3_r_q31", "type": "multiple_choice", "question": "What impresses Shester the most about the chapter on land values?", "options": ["A. the broad time period that is covered", "B. the interesting questions that Barr asks", "C. the nature of the research into the topic", "D. the recommendations Barr makes for the future"], "correctAnswer": "C"},
                    {"id": "cam17_t3_r_q32", "type": "ynng", "question": "The description in the first chapter of how New York probably looked from the air in the early 1600s lacks interest.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t3_r_q33", "type": "ynng", "question": "Chapters two and three prepare the reader well for material yet to come.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
                    {"id": "cam17_t3_r_q34", "type": "ynng", "question": "The biggest problem for many nineteenth-century New York immigrant neighbourhoods was a lack of amenities.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t3_r_q35", "type": "ynng", "question": "In the nineteenth century, New York's immigrant neighbourhoods tended to concentrate around the harbour.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
                    {"id": "cam17_t3_r_q36", "type": "matching_sentence", "question": "why skyscrapers are absent from 36. _____", "options": ["A. development plans", "B. deep excavations", "C. great distance", "D. excessive expense", "E. impossible tasks", "F. associated risks", "G. water level", "H. specific areas", "I. total expenditure", "J. construction guidelines"], "correctAnswer": "H"},
                    {"id": "cam17_t3_r_q37", "type": "matching_sentence", "question": "this cannot be regarded as 37. _____", "options": ["A. development plans", "B. deep excavations", "C. great distance", "D. excessive expense", "E. impossible tasks", "F. associated risks", "G. water level", "H. specific areas", "I. total expenditure", "J. construction guidelines"], "correctAnswer": "D"},
                    {"id": "cam17_t3_r_q38", "type": "matching_sentence", "question": "especially when compared to 38. _____", "options": ["A. development plans", "B. deep excavations", "C. great distance", "D. excessive expense", "E. impossible tasks", "F. associated risks", "G. water level", "H. specific areas", "I. total expenditure", "J. construction guidelines"], "correctAnswer": "I"},
                    {"id": "cam17_t3_r_q39", "type": "matching_sentence", "question": "how 39. _____ are made possible by the use of caissons", "options": ["A. development plans", "B. deep excavations", "C. great distance", "D. excessive expense", "E. impossible tasks", "F. associated risks", "G. water level", "H. specific areas", "I. total expenditure", "J. construction guidelines"], "correctAnswer": "B"},
                    {"id": "cam17_t3_r_q40", "type": "matching_sentence", "question": "but he also discusses their 40. _____", "options": ["A. development plans", "B. deep excavations", "C. great distance", "D. excessive expense", "E. impossible tasks", "F. associated risks", "G. water level", "H. specific areas", "I. total expenditure", "J. construction guidelines"], "correctAnswer": "F"},
                ]
            }
        ]
    })

    # --- TEST 4 ---
    tests.append({
        "id": "cam17_test4",
        "testNumber": 4,
        "passages": [
            {
                "id": "cam17_t4_p1", "title": "Bats to the rescue",
                "text": PASSAGE_TEXTS["t4_p1"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t4_r_q1", "type": "tfng", "question": "Many Madagascan forests are being destroyed by attacks from insects.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t4_r_q2", "type": "tfng", "question": "Loss of habitat has badly affected insectivorous bats in Madagascar.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t4_r_q3", "type": "tfng", "question": "Ricardo Rocha has carried out studies of bats in different parts of the world.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t4_r_q4", "type": "tfng", "question": "Habitat modification has resulted in indigenous bats in Madagascar becoming useful to farmers.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t4_r_q5", "type": "tfng", "question": "The Malagasy mouse-eared bat is more common than other indigenous bat species in Madagascar.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t4_r_q6", "type": "tfng", "question": "Bats may feed on paddy swarming caterpillars and grass webworms.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t4_r_q7", "type": "notes_completion", "question": "DNA analysis of bat 7. _____", "options": [], "correctAnswer": "droppings"},
                    {"id": "cam17_t4_r_q8", "type": "notes_completion", "question": "ate pests of rice, 8. _____, sugarcane, nuts and fruit", "options": [], "correctAnswer": "coffee"},
                    {"id": "cam17_t4_r_q9", "type": "notes_completion", "question": "prevent the spread of disease by eating 9. _____ and blackflies", "options": [], "correctAnswer": "mosquitoes"},
                    {"id": "cam17_t4_r_q10", "type": "notes_completion", "question": "they provide food rich in 10. _____", "options": [], "correctAnswer": "protein"},
                    {"id": "cam17_t4_r_q11", "type": "notes_completion", "question": "the buildings where they roost become 11. _____", "options": [], "correctAnswer": "unclean"},
                    {"id": "cam17_t4_r_q12", "type": "notes_completion", "question": "they play an important role in local 12. _____", "options": [], "correctAnswer": "culture"},
                    {"id": "cam17_t4_r_q13", "type": "notes_completion", "question": "farmers should provide special 13. _____ to support the bat population", "options": [], "correctAnswer": "houses"},
                ]
            },
            {
                "id": "cam17_t4_p2", "title": "Does education fuel economic growth?",
                "text": PASSAGE_TEXTS["t4_p2"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t4_r_q14", "type": "matching_info", "question": "an explanation of the need for research to focus on individuals with a fairly consistent income (Section)", "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": "E"},
                    {"id": "cam17_t4_r_q15", "type": "matching_info", "question": "examples of the sources the database has been compiled from (Section)", "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": "A"},
                    {"id": "cam17_t4_r_q16", "type": "matching_info", "question": "an account of one individual's refusal to obey an order (Section)", "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": "D"},
                    {"id": "cam17_t4_r_q17", "type": "matching_info", "question": "a reference to a region being particularly suited to research into the link between education and economic growth (Section)", "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": "F"},
                    {"id": "cam17_t4_r_q18", "type": "matching_info", "question": "examples of the items included in a list of personal possessions (Section)", "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": "C"},
                    {"id": "cam17_t4_r_q19", "type": "summary_completion", "question": "lives of individuals, as well as those of their 19. _____, over a 300-year period", "options": [], "correctAnswer": "descendants"},
                    {"id": "cam17_t4_r_q20", "type": "summary_completion", "question": "were reprimanded for reading while they should have been listening to a 20. _____", "options": [], "correctAnswer": "sermon"},
                    {"id": "cam17_t4_r_q21", "type": "summary_completion", "question": "she was later given a 21. _____", "options": [], "correctAnswer": "fine"},
                    {"id": "cam17_t4_r_q22", "type": "summary_completion", "question": "how the guilds could prevent 22. _____ and stop skilled people from working", "options": [], "correctAnswer": "innovation"},
                    {"id": "cam17_t4_r_q23", "type": "multiple_choice_multi", "question": "Which TWO statements does the writer make about literacy rates in Section B?", "options": ["A. Very little research has been done into the link.", "B. Literacy rates in Germany between 1600 and 1900 were very good.", "C. There is strong evidence that high literacy rates result in economic growth.", "D. England is a good example of how high literacy helped a country industrialise.", "E. Economic growth can help to improve literacy rates."], "correctAnswer": "B,E"},
                    {"id": "cam17_t4_r_q24", "type": "multiple_choice_multi", "question": "Q23 second option", "options": ["A. Very little research has been done into the link.", "B. Literacy rates in Germany between 1600 and 1900 were very good.", "C. There is strong evidence that high literacy rates result in economic growth.", "D. England is a good example of how high literacy helped a country industrialise.", "E. Economic growth can help to improve literacy rates."], "correctAnswer": "B,E"},
                    {"id": "cam17_t4_r_q25", "type": "multiple_choice_multi", "question": "Which TWO statements about guilds in Section F?", "options": ["A. They helped young people to learn a skill.", "B. They were opposed to people moving to an area for work.", "C. They kept better records than elsewhere.", "D. They opposed practices that threatened their control.", "E. They predominantly consisted of wealthy merchants."], "correctAnswer": "B,D"},
                    {"id": "cam17_t4_r_q26", "type": "multiple_choice_multi", "question": "Q25 second option", "options": ["A. They helped young people to learn a skill.", "B. They were opposed to people moving to an area for work.", "C. They kept better records than elsewhere.", "D. They opposed practices that threatened their control.", "E. They predominantly consisted of wealthy merchants."], "correctAnswer": "B,D"},
                ]
            },
            {
                "id": "cam17_t4_p3", "title": "Timur Gareyev – blindfold chess champion",
                "text": PASSAGE_TEXTS["t4_p3"], "timeRecommended": 20,
                "questions": [
                    {"id": "cam17_t4_r_q27", "type": "matching_info", "question": "a reference to earlier examples of blindfold chess (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "D"},
                    {"id": "cam17_t4_r_q28", "type": "matching_info", "question": "an outline of what blindfold chess involves (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "E"},
                    {"id": "cam17_t4_r_q29", "type": "matching_info", "question": "a claim that Gareyev's skill is limited to chess (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "F"},
                    {"id": "cam17_t4_r_q30", "type": "matching_info", "question": "why Gareyev's skill is of interest to scientists (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "B"},
                    {"id": "cam17_t4_r_q31", "type": "matching_info", "question": "an outline of Gareyev's priorities (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "H"},
                    {"id": "cam17_t4_r_q32", "type": "matching_info", "question": "a reason why the last part of a game may be difficult (Paragraph)", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": "E"},
                    {"id": "cam17_t4_r_q33", "type": "tfng", "question": "In the forthcoming games, all the participants will be blindfolded.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
                    {"id": "cam17_t4_r_q34", "type": "tfng", "question": "Gareyev has won competitions in BASE jumping.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t4_r_q35", "type": "tfng", "question": "UCLA is the first university to carry out research into blindfold chess players.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
                    {"id": "cam17_t4_r_q36", "type": "tfng", "question": "Good chess players are likely to be able to play blindfold chess.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
                    {"id": "cam17_t4_r_q37", "type": "summary_completion", "question": "tested Gareyev's 37. _____; e.g., recall a string of numbers in order and reverse", "options": [], "correctAnswer": "memory"},
                    {"id": "cam17_t4_r_q38", "type": "summary_completion", "question": "recall a string of 38. _____ in order and in reverse order", "options": [], "correctAnswer": "numbers"},
                    {"id": "cam17_t4_r_q39", "type": "summary_completion", "question": "scans showed an unusual amount of 39. _____ within the areas concerned with directing attention", "options": [], "correctAnswer": "communication"},
                    {"id": "cam17_t4_r_q40", "type": "summary_completion", "question": "unusual strength in the parts of his brain that deal with 40. _____ input", "options": [], "correctAnswer": "visual"},
                ]
            }
        ]
    })

    return tests


# ============================================================
# LISTENING TESTS DATA
# ============================================================

def build_listening():
    """Build all 4 tests of listening data."""
    tests = []

    # --- TEST 1 ---
    tests.append({
        "id": "cam17_test1",
        "testNumber": 1,
        "parts": [
            {
                "id": "cam17_t1_l_p1", "title": "Buckworth Conservation Group",
                "audioFile": "cam17_s1.mp3",
                "questions": [
                    {"id": "cam17_t1_l_q1", "type": "form_completion", "question": "making sure the beach does not have 1. _____ on it", "options": [], "correctAnswer": "litter"},
                    {"id": "cam17_t1_l_q2", "type": "form_completion", "question": "no 2. _____", "options": [], "correctAnswer": "dogs"},
                    {"id": "cam17_t1_l_q3", "type": "form_completion", "question": "next task is taking action to attract 3. _____ to the place", "options": [], "correctAnswer": "insects"},
                    {"id": "cam17_t1_l_q4", "type": "form_completion", "question": "identifying types of 4. _____", "options": [], "correctAnswer": "butterflies"},
                    {"id": "cam17_t1_l_q5", "type": "form_completion", "question": "building a new 5. _____", "options": [], "correctAnswer": "wall"},
                    {"id": "cam17_t1_l_q6", "type": "form_completion", "question": "walk across the sands and reach the 6. _____", "options": [], "correctAnswer": "island"},
                    {"id": "cam17_t1_l_q7", "type": "form_completion", "question": "wear appropriate 7. _____", "options": [], "correctAnswer": "boots"},
                    {"id": "cam17_t1_l_q8", "type": "form_completion", "question": "suitable for 8. _____ to participate in", "options": [], "correctAnswer": "beginners"},
                    {"id": "cam17_t1_l_q9", "type": "form_completion", "question": "making 9. _____ out of wood", "options": [], "correctAnswer": "spoons"},
                    {"id": "cam17_t1_l_q10", "type": "form_completion", "question": "cost of session (no camping): 10. £ _____", "options": [], "correctAnswer": "35 / thirty five"},
                ]
            },
            {
                "id": "cam17_t1_l_p2", "title": "Boat trip round Tasmania",
                "audioFile": "cam17_s2.mp3",
                "questions": [
                    {"id": "cam17_t1_l_q11", "type": "multiple_choice", "question": "What is the maximum number of people who can stand on each side of the boat?", "options": ["A. 9", "B. 15", "C. 18"], "correctAnswer": "A"},
                    {"id": "cam17_t1_l_q12", "type": "multiple_choice", "question": "What colour are the tour boats?", "options": ["A. dark red", "B. jet black", "C. light green"], "correctAnswer": "C"},
                    {"id": "cam17_t1_l_q13", "type": "multiple_choice", "question": "Which lunchbox is suitable for someone who doesn't eat meat or fish?", "options": ["A. Lunchbox 1", "B. Lunchbox 2", "C. Lunchbox 3"], "correctAnswer": "B"},
                    {"id": "cam17_t1_l_q14", "type": "multiple_choice", "question": "What should people do with their litter?", "options": ["A. take it home", "B. hand it to a member of staff", "C. put it in the bins provided on the boat"], "correctAnswer": "B"},
                    {"id": "cam17_t1_l_q15", "type": "multiple_choice_multi", "question": "Which TWO features of the lighthouse does Lou mention?", "options": ["A. why it was built", "B. who built it", "C. how long it took to build", "D. who staffed it", "E. what it was built with"], "correctAnswer": "A,D"},
                    {"id": "cam17_t1_l_q16", "type": "multiple_choice_multi", "question": "Q15 second option", "options": ["A. why it was built", "B. who built it", "C. how long it took to build", "D. who staffed it", "E. what it was built with"], "correctAnswer": "A,D"},
                    {"id": "cam17_t1_l_q17", "type": "multiple_choice_multi", "question": "Which TWO types of creature might come close to the boat?", "options": ["A. sea eagles", "B. fur seals", "C. dolphins", "D. whales", "E. penguins"], "correctAnswer": "B,C"},
                    {"id": "cam17_t1_l_q18", "type": "multiple_choice_multi", "question": "Q17 second option", "options": ["A. sea eagles", "B. fur seals", "C. dolphins", "D. whales", "E. penguins"], "correctAnswer": "B,C"},
                    {"id": "cam17_t1_l_q19", "type": "multiple_choice_multi", "question": "Which TWO points does Lou make about the caves?", "options": ["A. Only large tourist boats can visit them.", "B. The entrances are often blocked.", "C. It is too dangerous for individuals.", "D. Someone will explain what is inside them.", "E. They cannot be reached on foot."], "correctAnswer": "D,E"},
                    {"id": "cam17_t1_l_q20", "type": "multiple_choice_multi", "question": "Q19 second option", "options": ["A. Only large tourist boats can visit them.", "B. The entrances are often blocked.", "C. It is too dangerous for individuals.", "D. Someone will explain what is inside them.", "E. They cannot be reached on foot."], "correctAnswer": "D,E"},
                ]
            },
            {
                "id": "cam17_t1_l_p3", "title": "Work experience for veterinary science students",
                "audioFile": "cam17_s3.mp3",
                "questions": [
                    {"id": "cam17_t1_l_q21", "type": "multiple_choice", "question": "What problem did both Diana and Tim have when arranging their work experience?", "options": ["A. making initial contact with suitable farms", "B. organising transport to and from the farm", "C. finding a placement for the required length of time"], "correctAnswer": "A"},
                    {"id": "cam17_t1_l_q22", "type": "multiple_choice", "question": "Tim was pleased to be able to help", "options": ["A. a lamb that had a broken leg.", "B. a sheep that was having difficulty giving birth.", "C. a newly born lamb that was having trouble feeding."], "correctAnswer": "B"},
                    {"id": "cam17_t1_l_q23", "type": "multiple_choice", "question": "Diana says the sheep on her farm", "options": ["A. were of various different varieties.", "B. were mainly reared for their meat.", "C. had better quality wool than sheep on the hills."], "correctAnswer": "B"},
                    {"id": "cam17_t1_l_q24", "type": "multiple_choice", "question": "What did the students learn about adding supplements to chicken feed?", "options": ["A. These should only be given if specially needed.", "B. It is worth paying extra for the most effective ones.", "C. The amount given at one time should be limited."], "correctAnswer": "A"},
                    {"id": "cam17_t1_l_q25", "type": "multiple_choice", "question": "What happened when Diana was working with dairy cows?", "options": ["A. She identified some cows incorrectly.", "B. She accidentally threw some milk away.", "C. She made a mistake when storing milk."], "correctAnswer": "C"},
                    {"id": "cam17_t1_l_q26", "type": "multiple_choice", "question": "What did both farmers mention about vets and farming?", "options": ["A. Vets are failing to cope with some aspects of animal health.", "B. There needs to be a fundamental change in the training of vets.", "C. Some jobs could be done by the farmer rather than by a vet."], "correctAnswer": "C"},
                    {"id": "cam17_t1_l_q27", "type": "matching", "question": "Medical terminology — what opinion?", "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading difficult.", "E. Tim was shocked at something he learned.", "F. They were both surprised how little is known."], "correctAnswer": "A"},
                    {"id": "cam17_t1_l_q28", "type": "matching", "question": "Diet and nutrition — what opinion?", "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading difficult.", "E. Tim was shocked at something he learned.", "F. They were both surprised how little is known."], "correctAnswer": "E"},
                    {"id": "cam17_t1_l_q29", "type": "matching", "question": "Animal disease — what opinion?", "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading difficult.", "E. Tim was shocked at something he learned.", "F. They were both surprised how little is known."], "correctAnswer": "F"},
                    {"id": "cam17_t1_l_q30", "type": "matching", "question": "Wildlife medication — what opinion?", "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading difficult.", "E. Tim was shocked at something he learned.", "F. They were both surprised how little is known."], "correctAnswer": "C"},
                ]
            },
            {
                "id": "cam17_t1_l_p4", "title": "Labyrinths",
                "audioFile": "cam17_s4.mp3",
                "questions": [
                    {"id": "cam17_t1_l_q31", "type": "form_completion", "question": "Mazes are a type of 31. _____", "options": [], "correctAnswer": "puzzle"},
                    {"id": "cam17_t1_l_q32", "type": "form_completion", "question": "32. _____ is needed to navigate through a maze", "options": [], "correctAnswer": "logic"},
                    {"id": "cam17_t1_l_q33", "type": "form_completion", "question": "the word 'maze' is derived from a word meaning a feeling of 33. _____", "options": [], "correctAnswer": "confusion"},
                    {"id": "cam17_t1_l_q34", "type": "form_completion", "question": "they have frequently been used in 34. _____ and prayer", "options": [], "correctAnswer": "meditation"},
                    {"id": "cam17_t1_l_q35", "type": "form_completion", "question": "Ancient carvings on 35. _____ have been found across many cultures", "options": [], "correctAnswer": "stone"},
                    {"id": "cam17_t1_l_q36", "type": "form_completion", "question": "Ancient Greeks used the symbol on 36. _____", "options": [], "correctAnswer": "coins"},
                    {"id": "cam17_t1_l_q37", "type": "form_completion", "question": "The largest surviving example of a turf labyrinth once had a big 37. _____ at its centre", "options": [], "correctAnswer": "tree"},
                    {"id": "cam17_t1_l_q38", "type": "form_completion", "question": "walking a maze can reduce a person's 38. _____ rate", "options": [], "correctAnswer": "breathing"},
                    {"id": "cam17_t1_l_q39", "type": "form_completion", "question": "patients who can't walk can use 'finger labyrinths' made from 39. _____", "options": [], "correctAnswer": "paper"},
                    {"id": "cam17_t1_l_q40", "type": "form_completion", "question": "Alzheimer's sufferers experience less 40. _____", "options": [], "correctAnswer": "anxiety"},
                ]
            },
        ]
    })

    # --- TEST 2 ---
    tests.append({
        "id": "cam17_test2",
        "testNumber": 2,
        "parts": [
            {
                "id": "cam17_t2_l_p1", "title": "Opportunities for voluntary work in Southoe village",
                "audioFile": "cam17_s5.mp3",
                "questions": [
                    {"id": "cam17_t2_l_q1", "type": "form_completion", "question": "Help with 1. _____ books (times to be arranged)", "options": [], "correctAnswer": "collecting"},
                    {"id": "cam17_t2_l_q2", "type": "form_completion", "question": "Help needed to keep 2. _____ of books up to date", "options": [], "correctAnswer": "records"},
                    {"id": "cam17_t2_l_q3", "type": "form_completion", "question": "Library is in the 3. _____ Room in the village hall", "options": [], "correctAnswer": "West"},
                    {"id": "cam17_t2_l_q4", "type": "form_completion", "question": "Help by providing 4. _____", "options": [], "correctAnswer": "transport"},
                    {"id": "cam17_t2_l_q5", "type": "form_completion", "question": "Help with hobbies such as 5. _____", "options": [], "correctAnswer": "art"},
                    {"id": "cam17_t2_l_q6", "type": "form_completion", "question": "Taking Mrs Carroll to 6. _____", "options": [], "correctAnswer": "hospital"},
                    {"id": "cam17_t2_l_q7", "type": "form_completion", "question": "Work in the 7. _____ at Mr Selsbury's house", "options": [], "correctAnswer": "garden"},
                    {"id": "cam17_t2_l_q8", "type": "form_completion", "question": "19 Oct event: 8. _____ at Village hall", "options": [], "correctAnswer": "quiz"},
                    {"id": "cam17_t2_l_q9", "type": "form_completion", "question": "18 Nov dance: checking 9. _____", "options": [], "correctAnswer": "tickets"},
                    {"id": "cam17_t2_l_q10", "type": "form_completion", "question": "31 Dec New Year's Eve party: designing the 10. _____", "options": [], "correctAnswer": "poster"},
                ]
            },
            {
                "id": "cam17_t2_l_p2", "title": "Oniton Hall",
                "audioFile": "cam17_s6.mp3",
                "questions": [
                    {"id": "cam17_t2_l_q11", "type": "multiple_choice", "question": "Many past owners made changes to", "options": ["A. the gardens.", "B. the house.", "C. the farm."], "correctAnswer": "B"},
                    {"id": "cam17_t2_l_q12", "type": "multiple_choice", "question": "Sir Edward Downes built Oniton Hall because he wanted", "options": ["A. a place for discussing politics.", "B. a place to display his wealth.", "C. a place for artists and writers."], "correctAnswer": "C"},
                    {"id": "cam17_t2_l_q13", "type": "multiple_choice", "question": "Visitors can learn about the work of servants from", "options": ["A. audio guides.", "B. photographs.", "C. people in costume."], "correctAnswer": "C"},
                    {"id": "cam17_t2_l_q14", "type": "multiple_choice", "question": "What is new for children at Oniton Hall?", "options": ["A. clothes for dressing up", "B. mini tractors", "C. the adventure playground"], "correctAnswer": "B"},
                    {"id": "cam17_t2_l_q15", "type": "matching", "question": "dairy — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "D"},
                    {"id": "cam17_t2_l_q16", "type": "matching", "question": "large barn — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "C"},
                    {"id": "cam17_t2_l_q17", "type": "matching", "question": "small barn — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "G"},
                    {"id": "cam17_t2_l_q18", "type": "matching", "question": "stables — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "A"},
                    {"id": "cam17_t2_l_q19", "type": "matching", "question": "shed — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "E"},
                    {"id": "cam17_t2_l_q20", "type": "matching", "question": "parkland — which activity?", "options": ["A. shopping", "B. watching cows being milked", "C. seeing old farming equipment", "D. eating and drinking", "E. starting a trip", "F. seeing rare breeds of animals", "G. helping to look after animals", "H. using farming tools"], "correctAnswer": "F"},
                ]
            },
            {
                "id": "cam17_t2_l_p3", "title": "Romeo and Juliet theatre review",
                "audioFile": "cam17_s7.mp3",
                "questions": [
                    {"id": "cam17_t2_l_q21", "type": "multiple_choice_multi", "question": "Which TWO things do the students agree they need to include in their reviews?", "options": ["A. analysis of the text", "B. a summary of the plot", "C. a description of the theatre", "D. a personal reaction", "E. a reference to particular scenes"], "correctAnswer": "D,E"},
                    {"id": "cam17_t2_l_q22", "type": "multiple_choice_multi", "question": "Q21 second option", "options": ["A. analysis of the text", "B. a summary of the plot", "C. a description of the theatre", "D. a personal reaction", "E. a reference to particular scenes"], "correctAnswer": "D,E"},
                    {"id": "cam17_t2_l_q23", "type": "matching", "question": "the set — which opinion?", "options": ["A. They both expected this to be more traditional.", "B. They both thought this was original.", "C. They agree this created the right atmosphere.", "D. They agree this was a major strength.", "E. They were both disappointed by this.", "F. They disagree about why this was an issue.", "G. They disagree about how this could be improved."], "correctAnswer": "D"},
                    {"id": "cam17_t2_l_q24", "type": "matching", "question": "the lighting — which opinion?", "options": ["A. expected more traditional", "B. thought this was original", "C. created the right atmosphere", "D. was a major strength", "E. both disappointed", "F. disagree why an issue", "G. disagree how to improve"], "correctAnswer": "C"},
                    {"id": "cam17_t2_l_q25", "type": "matching", "question": "the costume design — which opinion?", "options": ["A. expected more traditional", "B. thought this was original", "C. created the right atmosphere", "D. was a major strength", "E. both disappointed", "F. disagree why an issue", "G. disagree how to improve"], "correctAnswer": "A"},
                    {"id": "cam17_t2_l_q26", "type": "matching", "question": "the music — which opinion?", "options": ["A. expected more traditional", "B. thought this was original", "C. created the right atmosphere", "D. was a major strength", "E. both disappointed", "F. disagree why an issue", "G. disagree how to improve"], "correctAnswer": "E"},
                    {"id": "cam17_t2_l_q27", "type": "matching", "question": "the actors' delivery — which opinion?", "options": ["A. expected more traditional", "B. thought this was original", "C. created the right atmosphere", "D. was a major strength", "E. both disappointed", "F. disagree why an issue", "G. disagree how to improve"], "correctAnswer": "F"},
                    {"id": "cam17_t2_l_q28", "type": "multiple_choice", "question": "The students think Romeo and Juliet is still relevant for young people because", "options": ["A. it illustrates how easily conflict can start.", "B. it deals with problems that families experience.", "C. it teaches them about relationships."], "correctAnswer": "B"},
                    {"id": "cam17_t2_l_q29", "type": "multiple_choice", "question": "The students found watching Romeo and Juliet in another language", "options": ["A. frustrating.", "B. demanding.", "C. moving."], "correctAnswer": "C"},
                    {"id": "cam17_t2_l_q30", "type": "multiple_choice", "question": "Why do the students think Shakespeare's plays have such international appeal?", "options": ["A. The stories are exciting.", "B. There are recognisable characters.", "C. They can be interpreted in many ways."], "correctAnswer": "C"},
                ]
            },
            {
                "id": "cam17_t2_l_p4", "title": "The impact of digital technology on the Icelandic language",
                "audioFile": "cam17_s8.mp3",
                "questions": [
                    {"id": "cam17_t2_l_q31", "type": "form_completion", "question": "has approximately 31. _____ speakers", "options": [], "correctAnswer": "321,000"},
                    {"id": "cam17_t2_l_q32", "type": "form_completion", "question": "has a 32. _____ that is still growing", "options": [], "correctAnswer": "vocabulary"},
                    {"id": "cam17_t2_l_q33", "type": "form_completion", "question": "has its own words for computer-based concepts, such as web browser and 33. _____", "options": [], "correctAnswer": "podcast"},
                    {"id": "cam17_t2_l_q34", "type": "form_completion", "question": "are big users of digital technology, such as 34. _____", "options": [], "correctAnswer": "smartphones"},
                    {"id": "cam17_t2_l_q35", "type": "form_completion", "question": "are becoming 35. _____ very quickly", "options": [], "correctAnswer": "bilingual"},
                    {"id": "cam17_t2_l_q36", "type": "form_completion", "question": "are having discussions using only English while they are in the 36. _____ at school", "options": [], "correctAnswer": "playground"},
                    {"id": "cam17_t2_l_q37", "type": "form_completion", "question": "are better able to identify the content of a 37. _____ in English than Icelandic", "options": [], "correctAnswer": "picture"},
                    {"id": "cam17_t2_l_q38", "type": "form_completion", "question": "write very little in Icelandic because of how complicated its 38. _____ is", "options": [], "correctAnswer": "grammar"},
                    {"id": "cam17_t2_l_q39", "type": "form_completion", "question": "is worried that young Icelanders may lose their 39. _____ as Icelanders", "options": [], "correctAnswer": "identity"},
                    {"id": "cam17_t2_l_q40", "type": "form_completion", "question": "is worried about children not being 40. _____ in either Icelandic or English", "options": [], "correctAnswer": "fluent"},
                ]
            },
        ]
    })

    # --- TEST 3 ---
    tests.append({
        "id": "cam17_test3",
        "testNumber": 3,
        "parts": [
            {
                "id": "cam17_t3_l_p1", "title": "Advice on surfing holidays",
                "audioFile": "cam17_s9.mp3",
                "questions": [
                    {"id": "cam17_t3_l_q1", "type": "form_completion", "question": "Recommends surfing for 1. _____ holidays in the summer", "options": [], "correctAnswer": "family"},
                    {"id": "cam17_t3_l_q2", "type": "form_completion", "question": "Need to be quite 2. _____", "options": [], "correctAnswer": "fit"},
                    {"id": "cam17_t3_l_q3", "type": "form_completion", "question": "Lahinch has some good quality 3. _____ and surf schools", "options": [], "correctAnswer": "hotels"},
                    {"id": "cam17_t3_l_q4", "type": "form_completion", "question": "Good surf school at 4. _____ beach", "options": [], "correctAnswer": "Carrowniskey"},
                    {"id": "cam17_t3_l_q5", "type": "form_completion", "question": "Surf camp lasts for one 5. _____", "options": [], "correctAnswer": "week"},
                    {"id": "cam17_t3_l_q6", "type": "form_completion", "question": "Can also explore the local 6. _____ by kayak", "options": [], "correctAnswer": "bay"},
                    {"id": "cam17_t3_l_q7", "type": "form_completion", "question": "Best month to go: 7. _____", "options": [], "correctAnswer": "September"},
                    {"id": "cam17_t3_l_q8", "type": "form_completion", "question": "Average temperature in summer: approx. 8. _____ degrees", "options": [], "correctAnswer": "19 / nineteen"},
                    {"id": "cam17_t3_l_q9", "type": "form_completion", "question": "Wetsuit and surfboard: 9. _____ euros per day", "options": [], "correctAnswer": "30 / thirty"},
                    {"id": "cam17_t3_l_q10", "type": "form_completion", "question": "Also advisable to hire 10. _____ for warmth", "options": [], "correctAnswer": "boots"},
                ]
            },
            {
                "id": "cam17_t3_l_p2", "title": "Extended hours childcare service",
                "audioFile": "cam17_s10.mp3",
                "questions": [
                    {"id": "cam17_t3_l_q11", "type": "multiple_choice_multi", "question": "Which TWO facts are given about the school's extended hours childcare service?", "options": ["A. It started recently.", "B. More children attend after school than before school.", "C. An average of 50 children attend in the mornings.", "D. A child cannot attend both sessions.", "E. The maximum number of children who can attend is 70."], "correctAnswer": "B,E"},
                    {"id": "cam17_t3_l_q12", "type": "multiple_choice_multi", "question": "Q11 second option", "options": ["A. It started recently.", "B. More children attend after school than before school.", "C. An average of 50 children attend in the mornings.", "D. A child cannot attend both sessions.", "E. The maximum number of children who can attend is 70."], "correctAnswer": "B,E"},
                    {"id": "cam17_t3_l_q13", "type": "multiple_choice", "question": "How much does childcare cost for a complete afternoon session per child?", "options": ["A. £3.50", "B. £5.70", "C. £7.20"], "correctAnswer": "C"},
                    {"id": "cam17_t3_l_q14", "type": "multiple_choice", "question": "What does the manager say about food?", "options": ["A. Children with allergies should bring their own food.", "B. Children may bring healthy snacks with them.", "C. Children are given a proper meal at 5 p.m."], "correctAnswer": "C"},
                    {"id": "cam17_t3_l_q15", "type": "multiple_choice", "question": "What is different about arrangements in the school holidays?", "options": ["A. Children from other schools can attend.", "B. Older children can attend.", "C. A greater number of children can attend."], "correctAnswer": "A"},
                    {"id": "cam17_t3_l_q16", "type": "matching", "question": "Spanish — what information?", "options": ["A. has limited availability", "B. is no longer available", "C. is for over 8s only", "D. requires help from parents", "E. involves an additional fee", "F. is a new activity", "G. was requested by children"], "correctAnswer": "E"},
                    {"id": "cam17_t3_l_q17", "type": "matching", "question": "Music — what information?", "options": ["A. has limited availability", "B. is no longer available", "C. is for over 8s only", "D. requires help from parents", "E. involves an additional fee", "F. is a new activity", "G. was requested by children"], "correctAnswer": "D"},
                    {"id": "cam17_t3_l_q18", "type": "matching", "question": "Painting — what information?", "options": ["A. has limited availability", "B. is no longer available", "C. is for over 8s only", "D. requires help from parents", "E. involves an additional fee", "F. is a new activity", "G. was requested by children"], "correctAnswer": "G"},
                    {"id": "cam17_t3_l_q19", "type": "matching", "question": "Yoga — what information?", "options": ["A. has limited availability", "B. is no longer available", "C. is for over 8s only", "D. requires help from parents", "E. involves an additional fee", "F. is a new activity", "G. was requested by children"], "correctAnswer": "F"},
                    {"id": "cam17_t3_l_q20", "type": "matching", "question": "Cooking — what information?", "options": ["A. has limited availability", "B. is no longer available", "C. is for over 8s only", "D. requires help from parents", "E. involves an additional fee", "F. is a new activity", "G. was requested by children"], "correctAnswer": "C"},
                ]
            },
            {
                "id": "cam17_t3_l_p3", "title": "Holly's Work Placement Tutorial",
                "audioFile": "cam17_s11.mp3",
                "questions": [
                    {"id": "cam17_t3_l_q21", "type": "multiple_choice", "question": "Holly has chosen the Orion Stadium placement because", "options": ["A. it involves children.", "B. it is outdoors.", "C. it sounds like fun."], "correctAnswer": "B"},
                    {"id": "cam17_t3_l_q22", "type": "multiple_choice", "question": "Which aspect of safety does Dr Green emphasise most?", "options": ["A. ensuring children stay in the stadium", "B. checking the equipment children will use", "C. removing obstacles in changing rooms"], "correctAnswer": "A"},
                    {"id": "cam17_t3_l_q23", "type": "multiple_choice", "question": "What does Dr Green say about the spectators?", "options": ["A. They can be hard to manage.", "B. They make useful volunteers.", "C. They shouldn't take photographs."], "correctAnswer": "A"},
                    {"id": "cam17_t3_l_q24", "type": "multiple_choice", "question": "What has affected the schedule in the past?", "options": ["A. bad weather", "B. an injury", "C. extra time"], "correctAnswer": "B"},
                    {"id": "cam17_t3_l_q25", "type": "matching", "question": "Communication — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "C"},
                    {"id": "cam17_t3_l_q26", "type": "matching", "question": "Organisation — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "A"},
                    {"id": "cam17_t3_l_q27", "type": "matching", "question": "Time management — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "D"},
                    {"id": "cam17_t3_l_q28", "type": "matching", "question": "Creativity — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "B"},
                    {"id": "cam17_t3_l_q29", "type": "matching", "question": "Leadership — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "F"},
                    {"id": "cam17_t3_l_q30", "type": "matching", "question": "Networking — important aspect?", "options": ["A. being flexible", "B. focusing on details", "C. having a smart appearance", "D. hiding your emotions", "E. relying on experts", "F. trusting your own views", "G. doing one thing at a time", "H. thinking of the future"], "correctAnswer": "H"},
                ]
            },
            {
                "id": "cam17_t3_l_p4", "title": "Bird Migration Theory",
                "audioFile": "cam17_s12.mp3",
                "questions": [
                    {"id": "cam17_t3_l_q31", "type": "form_completion", "question": "It was believed that birds hibernated underwater or buried themselves in 31. _____", "options": [], "correctAnswer": "mud"},
                    {"id": "cam17_t3_l_q32", "type": "form_completion", "question": "he observed that redstarts experience the loss of 32. _____ and thought they then turned into robins", "options": [], "correctAnswer": "feathers"},
                    {"id": "cam17_t3_l_q33", "type": "form_completion", "question": "the two species of birds had a similar 33. _____", "options": [], "correctAnswer": "shape"},
                    {"id": "cam17_t3_l_q34", "type": "form_completion", "question": "Charles Morton popularised the idea that birds fly to the 34. _____ in winter", "options": [], "correctAnswer": "moon"},
                    {"id": "cam17_t3_l_q35", "type": "form_completion", "question": "a stork was killed in Germany which had an African spear in its 35. _____", "options": [], "correctAnswer": "neck"},
                    {"id": "cam17_t3_l_q36", "type": "form_completion", "question": "previously there had been no 36. _____ that storks migrate to Africa", "options": [], "correctAnswer": "evidence"},
                    {"id": "cam17_t3_l_q37", "type": "form_completion", "question": "Little was known about the 37. _____ and journeys of migrating birds until ringing was established", "options": [], "correctAnswer": "destinations"},
                    {"id": "cam17_t3_l_q38", "type": "form_completion", "question": "they were considered incapable of travelling across huge 38. _____", "options": [], "correctAnswer": "oceans"},
                    {"id": "cam17_t3_l_q39", "type": "form_completion", "question": "Ringing depended on what is called the 39. _____ of dead birds", "options": [], "correctAnswer": "recovery"},
                    {"id": "cam17_t3_l_q40", "type": "form_completion", "question": "In 1931, the first 40. _____ to show the migration of European birds was printed", "options": [], "correctAnswer": "atlas"},
                ]
            },
        ]
    })

    # --- TEST 4 ---
    tests.append({
        "id": "cam17_test4",
        "testNumber": 4,
        "parts": [
            {
                "id": "cam17_t4_l_p1", "title": "Easy Life Cleaning Services",
                "audioFile": "cam17_s13.mp3",
                "questions": [
                    {"id": "cam17_t4_l_q1", "type": "form_completion", "question": "Cleaning the 1. _____ throughout the apartment", "options": [], "correctAnswer": "floor(s)"},
                    {"id": "cam17_t4_l_q2", "type": "form_completion", "question": "Every week: Cleaning the 2. _____", "options": [], "correctAnswer": "fridge"},
                    {"id": "cam17_t4_l_q3", "type": "form_completion", "question": "Ironing clothes – 3. _____ only", "options": [], "correctAnswer": "shirts"},
                    {"id": "cam17_t4_l_q4", "type": "form_completion", "question": "Every month: Cleaning all the 4. _____ from the inside", "options": [], "correctAnswer": "windows"},
                    {"id": "cam17_t4_l_q5", "type": "form_completion", "question": "Washing down the 5. _____", "options": [], "correctAnswer": "balcony"},
                    {"id": "cam17_t4_l_q6", "type": "form_completion", "question": "They can organise a plumber or an 6. _____ if necessary", "options": [], "correctAnswer": "electrician"},
                    {"id": "cam17_t4_l_q7", "type": "form_completion", "question": "special cleaning service for customers allergic to 7. _____", "options": [], "correctAnswer": "dust"},
                    {"id": "cam17_t4_l_q8", "type": "form_completion", "question": "all cleaners have a background check carried out by the 8. _____", "options": [], "correctAnswer": "police"},
                    {"id": "cam17_t4_l_q9", "type": "form_completion", "question": "All cleaners are given 9. _____ for two weeks", "options": [], "correctAnswer": "training"},
                    {"id": "cam17_t4_l_q10", "type": "form_completion", "question": "Customers send a 10. _____ after each visit", "options": [], "correctAnswer": "review"},
                ]
            },
            {
                "id": "cam17_t4_l_p2", "title": "Hotel staff retention",
                "audioFile": "cam17_s14.mp3",
                "questions": [
                    {"id": "cam17_t4_l_q11", "type": "multiple_choice", "question": "Many hotel managers are unaware that their staff often leave because of", "options": ["A. a lack of training.", "B. long hours.", "C. low pay."], "correctAnswer": "A"},
                    {"id": "cam17_t4_l_q12", "type": "multiple_choice", "question": "What is the impact of high staff turnover on managers?", "options": ["A. an increased workload", "B. low morale", "C. an inability to meet targets"], "correctAnswer": "A"},
                    {"id": "cam17_t4_l_q13", "type": "multiple_choice", "question": "What mistake should managers always avoid?", "options": ["A. failing to treat staff equally", "B. reorganising shifts without warning", "C. neglecting to have enough staff during busy periods"], "correctAnswer": "A"},
                    {"id": "cam17_t4_l_q14", "type": "multiple_choice", "question": "What unexpected benefit did Dunwich Hotel notice after improving staff retention rates?", "options": ["A. a fall in customer complaints", "B. an increase in loyalty club membership", "C. a rise in spending per customer"], "correctAnswer": "C"},
                    {"id": "cam17_t4_l_q15", "type": "matching", "question": "The Sun Club — which way of reducing staff turnover?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "A"},
                    {"id": "cam17_t4_l_q16", "type": "matching", "question": "The Portland — which way?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "C"},
                    {"id": "cam17_t4_l_q17", "type": "matching", "question": "Bluewater Hotels — which way?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "B"},
                    {"id": "cam17_t4_l_q18", "type": "matching", "question": "Pentlow Hotels — which way?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "C"},
                    {"id": "cam17_t4_l_q19", "type": "matching", "question": "Green Planet — which way?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "B"},
                    {"id": "cam17_t4_l_q20", "type": "matching", "question": "The Amesbury — which way?", "options": ["A. improving relationships and teamwork", "B. offering incentives and financial benefits", "C. providing career opportunities"], "correctAnswer": "A"},
                ]
            },
            {
                "id": "cam17_t4_l_p3", "title": "History of sporting equipment",
                "audioFile": "cam17_s15.mp3",
                "questions": [
                    {"id": "cam17_t4_l_q21", "type": "multiple_choice_multi", "question": "Which TWO points do Thomas and Jeanne make about Thomas's sporting activities at school?", "options": ["A. He should have felt more positive.", "B. The training was too challenging.", "C. He could have worked harder at them.", "D. His parents were disappointed in him.", "E. His fellow students admired him."], "correctAnswer": "C,E"},
                    {"id": "cam17_t4_l_q22", "type": "multiple_choice_multi", "question": "Q21 second option", "options": ["A. He should have felt more positive.", "B. The training was too challenging.", "C. He could have worked harder at them.", "D. His parents were disappointed in him.", "E. His fellow students admired him."], "correctAnswer": "C,E"},
                    {"id": "cam17_t4_l_q23", "type": "multiple_choice_multi", "question": "Which TWO feelings did Thomas experience when he was in Kenya?", "options": ["A. disbelief", "B. relief", "C. stress", "D. gratitude", "E. homesickness"], "correctAnswer": "A,D"},
                    {"id": "cam17_t4_l_q24", "type": "multiple_choice_multi", "question": "Q23 second option", "options": ["A. disbelief", "B. relief", "C. stress", "D. gratitude", "E. homesickness"], "correctAnswer": "A,D"},
                    {"id": "cam17_t4_l_q25", "type": "matching", "question": "the table tennis bat — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "B"},
                    {"id": "cam17_t4_l_q26", "type": "matching", "question": "the cricket helmet — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "F"},
                    {"id": "cam17_t4_l_q27", "type": "matching", "question": "the cycle helmet — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "A"},
                    {"id": "cam17_t4_l_q28", "type": "matching", "question": "the golf club — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "D"},
                    {"id": "cam17_t4_l_q29", "type": "matching", "question": "the hockey stick — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "C"},
                    {"id": "cam17_t4_l_q30", "type": "matching", "question": "the football — what comment?", "options": ["A. could cause excessive sweating", "B. material was mass produced for another purpose", "C. people often needed to make their own", "D. often had to be replaced", "E. material was expensive", "F. was unpopular among spectators", "G. caused injuries", "H. no one using it liked it at first"], "correctAnswer": "G"},
                ]
            },
            {
                "id": "cam17_t4_l_p4", "title": "Maple syrup",
                "audioFile": "cam17_s16.mp3",
                "questions": [
                    {"id": "cam17_t4_l_q31", "type": "form_completion", "question": "colour described as 31. _____", "options": [], "correctAnswer": "golden"},
                    {"id": "cam17_t4_l_q32", "type": "form_completion", "question": "very 32. _____ compared to refined sugar", "options": [], "correctAnswer": "healthy"},
                    {"id": "cam17_t4_l_q33", "type": "form_completion", "question": "best growing conditions and 33. _____ are in Canada and North America", "options": [], "correctAnswer": "climate"},
                    {"id": "cam17_t4_l_q34", "type": "form_completion", "question": "used hot 34. _____ to heat the sap", "options": [], "correctAnswer": "rock(s)"},
                    {"id": "cam17_t4_l_q35", "type": "form_completion", "question": "Tree trunks may not have the correct 35. _____ until they have been growing for 40 years", "options": [], "correctAnswer": "diameter"},
                    {"id": "cam17_t4_l_q36", "type": "form_completion", "question": "A tap is drilled into the trunk and a 36. _____ carries the sap into a bucket", "options": [], "correctAnswer": "tube"},
                    {"id": "cam17_t4_l_q37", "type": "form_completion", "question": "Large pans of sap called evaporators are heated by means of a 37. _____", "options": [], "correctAnswer": "fire"},
                    {"id": "cam17_t4_l_q38", "type": "form_completion", "question": "A lot of 38. _____ is produced during the evaporation process", "options": [], "correctAnswer": "steam"},
                    {"id": "cam17_t4_l_q39", "type": "form_completion", "question": "'Sugar sand' is removed because it makes the syrup look 39. _____ and affects the taste", "options": [], "correctAnswer": "cloudy"},
                    {"id": "cam17_t4_l_q40", "type": "form_completion", "question": "A huge quantity of sap is needed to make a 40. _____ of maple syrup", "options": [], "correctAnswer": "litre / liter"},
                ]
            },
        ]
    })

    return tests


# ============================================================
# SAVE FUNCTIONS
# ============================================================

def save_flat_reading(tests):
    """Save reading.json with Test 1 data as the primary flat structure."""
    t = tests[0]
    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Academic Reading",
        "tests": tests,
        # Flat structure for backward compatibility with app
        "totalQuestions": sum(len(p["questions"]) for p in t["passages"]),
        "passages": t["passages"]
    }


def save_flat_listening(tests):
    """Save listening.json with Test 1 data as the primary flat structure."""
    t = tests[0]
    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Listening",
        "tests": tests,
        "totalQuestions": sum(len(p["questions"]) for p in t["parts"]),
        "sections": t["parts"]
    }


def save_by_test(tests, module):
    """Save each test to its own JSON file."""
    for t in tests:
        test_num = t["testNumber"]
        path = f"{OUT_DIR}/{module}_test{test_num}.json"
        write_json(path, t)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# WRITING TESTS DATA
# ============================================================

def build_writing():
    tests = []
    tests.append({
        "id": "cam17_test1", "testNumber": 1,
        "task1": {
            "title": "Norbiton industrial area maps comparison",
            "instruction": "The two maps below show road access to a city hospital in 2007 and in 2010. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "wordLimit": 150, "timeRecommended": 20,
            "type": "map_comparison"
        },
        "task2": {
            "title": "Taking risks in professional and personal lives",
            "instruction": "It is important for people to take risks, both in their professional lives and their personal lives. Do you think the advantages of taking risks outweigh the disadvantages?",
            "wordLimit": 250, "timeRecommended": 40,
            "type": "opinion_essay"
        }
    })
    tests.append({
        "id": "cam17_test2", "testNumber": 2,
        "task1": {
            "title": "Police budget 2017-2018 in one area of Britain",
            "instruction": "The table and charts below give information on the police budget for 2017 and 2018 in one area of Britain. The table shows where the money came from and the charts show how it was distributed. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "wordLimit": 150, "timeRecommended": 20,
            "type": "table_and_charts"
        },
        "task2": {
            "title": "Children spending hours on smartphones",
            "instruction": "Some children spend hours every day on their smartphones. Why is this the case? Do you think this is a positive or a negative development?",
            "wordLimit": 250, "timeRecommended": 40,
            "type": "opinion_essay"
        }
    })
    tests.append({
        "id": "cam17_test3", "testNumber": 3,
        "task1": {
            "title": "Average weekly spending by families in 1968 and 2018",
            "instruction": "The chart below gives information about how families in one country spent their weekly income in 1968 and in 2018. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "wordLimit": 150, "timeRecommended": 20,
            "type": "bar_chart"
        },
        "task2": {
            "title": "Professionals working in the country where they trained",
            "instruction": "Some people believe that professionals, such as doctors and engineers, should be required to work in the country where they did their training. Others believe they should be free to work in another country if they wish. Discuss both these views and give your own opinion.",
            "wordLimit": 250, "timeRecommended": 40,
            "type": "discussion_essay"
        }
    })
    tests.append({
        "id": "cam17_test4", "testNumber": 4,
        "task1": {
            "title": "Number of shop closures and openings 2011-2018",
            "instruction": "The graph below shows the number of shops that closed and the number of new shops that opened in one country between 2011 and 2018. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "wordLimit": 150, "timeRecommended": 20,
            "type": "line_graph"
        },
        "task2": {
            "title": "Alternative medicines and treatments instead of doctors",
            "instruction": "Nowadays, a growing number of people with health problems are trying alternative medicines and treatments instead of visiting their usual doctor. Do you think this is a positive or a negative development?",
            "wordLimit": 250, "timeRecommended": 40,
            "type": "opinion_essay"
        }
    })
    return tests


# ============================================================
# SPEAKING TESTS DATA
# ============================================================

def build_speaking():
    tests = []
    tests.append({
        "id": "cam17_test1", "testNumber": 1,
        "part1": {
            "topic": "History",
            "questions": [
                "Did you study history when you were at school? [Why/Why not?]",
                "How often do you watch TV programmes about history? [Why/Why not?]",
                "Have you ever visited a museum to learn about history? [Why/Why not?]",
                "Do you think history is important? [Why/Why not?]"
            ]
        },
        "part2": {
            "title": "Describe a neighbourhood you lived in when you were a child",
            "prompts": ["where the neighbourhood was", "what kind of people lived there", "what it was like to live there", "explain how you felt about living in this neighbourhood when you were a child"]
        },
        "part3": {
            "topics": [
                {"topic": "Neighbours", "questions": [
                    "What sort of problems can people have with their neighbours?",
                    "How can neighbours be helpful to each other?",
                    "How can people get along well with their neighbours?"
                ]},
                {"topic": "Facilities in cities", "questions": [
                    "What facilities do newly built cities provide for people?",
                    "Should all new buildings in a city look the same?",
                    "To what extent do you think tourism affects the facilities in a city?"
                ]}
            ]
        }
    })
    tests.append({
        "id": "cam17_test2", "testNumber": 2,
        "part1": {
            "topic": "Reading",
            "questions": [
                "Did you have a favourite book when you were a child? [Why/Why not?]",
                "How much reading do you do for your work/studies? [Why/Why not?]",
                "What kinds of books do you read for pleasure? [Why/Why not?]",
                "Do you prefer to read a newspaper or a magazine online, or to buy a copy? [Why?]"
            ]
        },
        "part2": {
            "title": "Describe a big city you would like to visit",
            "prompts": ["which big city you would like to visit", "how you would travel there", "what you would do there", "explain why you would like to visit this big city"]
        },
        "part3": {
            "topics": [
                {"topic": "Visiting cities on holiday", "questions": [
                    "What are the most interesting things to do while visiting cities on holiday?",
                    "Why can it be expensive to visit cities on holiday?",
                    "Do you think it is better to visit cities alone or in a group with friends?"
                ]},
                {"topic": "The growth of cities", "questions": [
                    "Why have cities increased in size in recent years?",
                    "What are the challenges created by ever-growing cities?",
                    "In what ways do you think cities of the future will be different to cities today?"
                ]}
            ]
        }
    })
    tests.append({
        "id": "cam17_test3", "testNumber": 3,
        "part1": {
            "topic": "Drinks",
            "questions": [
                "What do you like to drink with your dinner? [Why?]",
                "Do you drink a lot of water every day? [Why/Why not?]",
                "Do you prefer drinking tea or coffee? [Why?]",
                "If people visit you in your home, what do you usually offer them to drink? [Why/Why not?]"
            ]
        },
        "part2": {
            "title": "Describe a monument (e.g., a statue or sculpture) that you like",
            "prompts": ["what this monument is", "where this monument is", "what it looks like", "explain why you like this monument"]
        },
        "part3": {
            "topics": [
                {"topic": "Public monuments", "questions": [
                    "What kinds of monuments do tourists in your country enjoy visiting?",
                    "Why do you think there are often statues of famous people in public places?",
                    "Do you agree that old monuments and buildings should always be preserved?"
                ]},
                {"topic": "Architecture", "questions": [
                    "Why is architecture such a popular university subject?",
                    "In what ways has the design of homes changed in recent years?",
                    "To what extent does the design of buildings affect people's moods?"
                ]}
            ]
        }
    })
    tests.append({
        "id": "cam17_test4", "testNumber": 4,
        "part1": {
            "topic": "Maps",
            "questions": [
                "Do you think it's better to use a paper map or a map on your phone? [Why?]",
                "When was the last time you needed to use a map? [Why/Why not?]",
                "If you visit a new city, do you always use a map to find your way around? [Why/Why not?]",
                "In general, do you find it easy to read maps? [Why/Why not?]"
            ]
        },
        "part2": {
            "title": "Describe an occasion when you had to do something in a hurry",
            "prompts": ["what you had to do", "why you had to do this in a hurry", "how well you did this", "explain how you felt about having to do this in a hurry"]
        },
        "part3": {
            "topics": [
                {"topic": "Arriving late", "questions": [
                    "Do you think it's OK to arrive late when meeting a friend?",
                    "What should happen to people who arrive late for work?",
                    "Can you suggest how people can make sure they don't arrive late?"
                ]},
                {"topic": "Managing study time", "questions": [
                    "Is it better to study for long periods or in shorter blocks of time?",
                    "What are the likely effects of students not managing their study time well?",
                    "How important is it for students to have enough leisure time?"
                ]}
            ]
        }
    })
    return tests


def main():
    reading_tests = build_reading()
    listening_tests = build_listening()
    writing_tests = build_writing()
    speaking_tests = build_speaking()

    # Save full combined files
    reading_data = save_flat_reading(reading_tests)
    listening_data = save_flat_listening(listening_tests)

    with open(f"{OUT_DIR}/reading.json", 'w', encoding='utf-8') as f:
        json.dump(reading_data, f, ensure_ascii=False, indent=2)

    with open(f"{OUT_DIR}/listening.json", 'w', encoding='utf-8') as f:
        json.dump(listening_data, f, ensure_ascii=False, indent=2)

    # Save writing and speaking
    write_json(f"{OUT_DIR}/writing.json", {"id": "cam17", "title": "Cambridge IELTS 17 Writing", "tasks": writing_tests})
    write_json(f"{OUT_DIR}/speaking.json", {"id": "cam17", "title": "Cambridge IELTS 17 Speaking", "tests": speaking_tests})

    # Also save per-test files for flexibility
    save_by_test(reading_tests, "reading")
    save_by_test(listening_tests, "listening")
    save_by_test(writing_tests, "writing")
    save_by_test(speaking_tests, "speaking")

    # Report
    for i, t in enumerate(reading_tests, 1):
        total_r = sum(len(p["questions"]) for p in t["passages"])
        chars = sum(len(p["text"]) for p in t["passages"])
        print(f"  Test {i} Reading: {len(t['passages'])} passages, {total_r} questions, {chars} chars text")

    for i, t in enumerate(listening_tests, 1):
        total_l = sum(len(p["questions"]) for p in t["parts"])
        print(f"  Test {i} Listening: {len(t['parts'])} parts, {total_l} questions")
        for j, p in enumerate(t["parts"], 1):
            print(f"    Part {j}: {p['title']} ({len(p['questions'])}Q) -> {p['audioFile']}")

    for i, t in enumerate(writing_tests, 1):
        print(f"  Test {i} Writing: Task 1 - {t['task1']['title'][:60]}...")

    for i, t in enumerate(speaking_tests, 1):
        print(f"  Test {i} Speaking: Part 2 - {t['part2']['title'][:60]}...")

    print(f"\n  Total: {len(reading_tests)} reading + {len(listening_tests)} listening + {len(writing_tests)} writing + {len(speaking_tests)} speaking")
    print(f"  Output: {OUT_DIR}/")


if __name__ == "__main__":
    main()
