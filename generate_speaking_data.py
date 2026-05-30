#!/usr/bin/env python3
"""Generate 28 Cambridge IELTS speaking test JSON files (cam14-cam20, 4 tests each).
cam14-16: real topics from web search. cam17-20: AI-generated reasonable IELTS topics."""

import json
import os

DATA_DIR = "data/speaking"
os.makedirs(DATA_DIR, exist_ok=True)

SPEAKING_TESTS = {

# ==================== cam14 - Real topics ====================

"cam14_test1": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "What do you enjoy most about your work or studies?"},
        {"question": "What kind of books do you like to read?", "followUp": "Do you prefer reading physical books or e-books?"},
        {"question": "How often do you read for pleasure?", "followUp": "Has your reading habit changed over the years?"},
        {"question": "Did you enjoy reading when you were a child?", "followUp": "What was your favourite book as a child?"}
    ],
    "part2": {
        "cueCard": "Describe a book that you enjoyed reading because you had to think a lot.",
        "bulletPoints": [
            "what the book was",
            "why you decided to read it",
            "what it was about",
            "and explain why you enjoyed reading it because you had to think a lot"
        ],
        "followUpQuestions": [
            "Do you think reading is still important in the digital age?",
            "What kinds of books are most popular in your country?",
            "How do you think reading habits will change in the future?",
            "Is it better to read for information or for pleasure?"
        ],
        "preparationTime": 60
    }
},

"cam14_test2": {
    "part1": [
        {"question": "Do you like your home?", "followUp": "What is your favourite room in your home?"},
        {"question": "What kind of housing do you live in?", "followUp": "Would you prefer to live in a house or an apartment?"},
        {"question": "Do you enjoy shopping?", "followUp": "What do you usually buy when you go shopping?"},
        {"question": "Have you ever bought something for your home online?", "followUp": "Do you prefer shopping online or in physical stores?"}
    ],
    "part2": {
        "cueCard": "Describe something you liked very much which you bought for your home.",
        "bulletPoints": [
            "what you bought",
            "where you bought it from",
            "why you chose this particular thing",
            "and explain why you liked it so much"
        ],
        "followUpQuestions": [
            "Why do people like to decorate their homes?",
            "How has home decoration changed in your country over the years?",
            "Do you think people spend too much money on things for their home?",
            "Is the design of a home more important than its functionality?"
        ],
        "preparationTime": 60
    }
},

"cam14_test3": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "What subjects do/did you study?"},
        {"question": "What do you find most challenging about your work or studies?", "followUp": "How do you usually overcome difficult tasks?"},
        {"question": "Do you set goals for yourself?", "followUp": "How do you keep yourself motivated?"},
        {"question": "Have you ever had to work as part of a team?", "followUp": "What makes a team successful?"}
    ],
    "part2": {
        "cueCard": "Describe a very difficult task that you succeeded in doing as part of your work or studies.",
        "bulletPoints": [
            "what the task was",
            "why it was difficult",
            "how you completed it",
            "and explain how you felt when you had successfully completed the task"
        ],
        "followUpQuestions": [
            "Do you think difficult tasks are good for people's development?",
            "How do employers or teachers help people deal with challenging tasks?",
            "Is it better to work on difficult tasks alone or in a team?",
            "What skills are most important for overcoming challenges?"
        ],
        "preparationTime": 60
    }
},

"cam14_test4": {
    "part1": [
        {"question": "How often do you use the internet?", "followUp": "What do you mainly use the internet for?"},
        {"question": "Do you enjoy online shopping?", "followUp": "What was the last thing you bought online?"},
        {"question": "What kinds of websites do you visit most frequently?", "followUp": "How do you decide if a website is trustworthy?"},
        {"question": "Do you prefer buying things online or in physical stores?", "followUp": "What are the advantages of shopping online?"}
    ],
    "part2": {
        "cueCard": "Describe a website you have bought something from.",
        "bulletPoints": [
            "what the website was",
            "what you bought from it",
            "why you chose to buy from this website",
            "and explain whether you were satisfied with the experience"
        ],
        "followUpQuestions": [
            "How has online shopping changed the way people shop?",
            "What are the disadvantages of shopping online?",
            "Do you think physical stores will disappear in the future?",
            "How can online retailers improve the customer experience?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam15 - Real topics ====================

"cam15_test1": {
    "part1": [
        {"question": "Do you enjoy travelling?", "followUp": "What is your favourite type of holiday?"},
        {"question": "How often do you stay in hotels?", "followUp": "What do you look for when choosing a hotel?"},
        {"question": "What is the most important thing for you when you travel?", "followUp": "Do you prefer luxury or budget accommodation?"},
        {"question": "Have you ever had a bad experience in a hotel?", "followUp": "What would you do if you were unhappy with your hotel room?"}
    ],
    "part2": {
        "cueCard": "Describe a hotel that you know.",
        "bulletPoints": [
            "where the hotel is",
            "what the hotel looks like",
            "what facilities it has",
            "and explain whether you would recommend this hotel to others"
        ],
        "followUpQuestions": [
            "What makes a hotel a good place to stay?",
            "How has the hotel industry changed in recent years?",
            "Do you prefer staying in a hotel or other types of accommodation?",
            "How can hotels attract more customers?"
        ],
        "preparationTime": 60
    }
},

"cam15_test2": {
    "part1": [
        {"question": "How often do you use the internet?", "followUp": "What do you mainly use the internet for?"},
        {"question": "Do you enjoy online shopping?", "followUp": "What was the last thing you bought online?"},
        {"question": "What kinds of websites do you visit most frequently?", "followUp": "How do you decide if a website is trustworthy?"},
        {"question": "Do you prefer buying things online or in physical stores?", "followUp": "What are the advantages of shopping online?"}
    ],
    "part2": {
        "cueCard": "Describe a website that you bought something from.",
        "bulletPoints": [
            "what the website was",
            "what you bought from it",
            "why you chose to buy from this website",
            "and explain whether you were satisfied with the experience"
        ],
        "followUpQuestions": [
            "How has e-commerce changed the retail industry?",
            "What are the risks of online shopping?",
            "Do you think online shopping is good for the environment?",
            "What will online shopping be like in the future?"
        ],
        "preparationTime": 60
    }
},

"cam15_test3": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "What do you hope to achieve in your career?"},
        {"question": "Who do you admire most in your life?", "followUp": "What qualities do you think make someone admirable?"},
        {"question": "Do you follow any famous business people?", "followUp": "What can we learn from successful business people?"},
        {"question": "Do you think it is important to have role models?", "followUp": "How do role models influence young people?"}
    ],
    "part2": {
        "cueCard": "Describe a business person you admire.",
        "bulletPoints": [
            "who this person is",
            "what business they are in",
            "what you know about their career",
            "and explain why you admire this person"
        ],
        "followUpQuestions": [
            "What qualities does a person need to succeed in business?",
            "How important is education for business success?",
            "Do you think business people have a responsibility to society?",
            "How has the role of business leaders changed in recent years?"
        ],
        "preparationTime": 60
    }
},

"cam15_test4": {
    "part1": [
        {"question": "Do you enjoy watching TV?", "followUp": "What kinds of TV programs do you like?"},
        {"question": "How much time do you spend watching TV?", "followUp": "Do you prefer watching TV alone or with others?"},
        {"question": "Are there any science programs you find interesting?", "followUp": "How do TV programs help people learn about science?"},
        {"question": "Has the way you watch TV changed in recent years?", "followUp": "Do you use streaming services or traditional TV?"}
    ],
    "part2": {
        "cueCard": "Describe an interesting TV programme you watched about a science topic.",
        "bulletPoints": [
            "what the programme was about",
            "when you watched it",
            "why you decided to watch it",
            "and explain why you found it interesting"
        ],
        "followUpQuestions": [
            "Why do you think science programmes are popular?",
            "Should schools use TV programmes to teach science?",
            "How has television changed the way people learn about science?",
            "Do you think people trust the science presented on TV?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam16 - Real topics ====================

"cam16_test1": {
    "part1": [
        {"question": "Do you like travelling?", "followUp": "What is your favourite place you have visited?"},
        {"question": "What kinds of tourist attractions do you enjoy?", "followUp": "Do you prefer natural attractions or historical sites?"},
        {"question": "Have you been to any famous tourist attractions recently?", "followUp": "What made it memorable?"},
        {"question": "Is tourism popular in your country?", "followUp": "Where do most tourists go in your country?"}
    ],
    "part2": {
        "cueCard": "Describe a tourist attraction you enjoyed visiting.",
        "bulletPoints": [
            "what the attraction was",
            "when you went there",
            "who you went with",
            "and explain why you enjoyed visiting it"
        ],
        "followUpQuestions": [
            "How does tourism affect local communities?",
            "What can governments do to promote tourism?",
            "Do you think tourism has more positive or negative effects?",
            "How has tourism changed in the last few decades?"
        ],
        "preparationTime": 60
    }
},

"cam16_test2": {
    "part1": [
        {"question": "How often do you read reviews before buying something?", "followUp": "What kind of reviews do you usually read?"},
        {"question": "Do you write reviews yourself?", "followUp": "What motivates people to write reviews?"},
        {"question": "How do you decide whether a product is good?", "followUp": "Do you trust online reviews?"},
        {"question": "Have you ever been disappointed by a product with good reviews?", "followUp": "How do you deal with a disappointing purchase?"}
    ],
    "part2": {
        "cueCard": "Describe a review you read about a product or service.",
        "bulletPoints": [
            "what the product or service was",
            "where you read the review",
            "what the review said",
            "and explain whether the review influenced your decision"
        ],
        "followUpQuestions": [
            "Why are online reviews so popular?",
            "Do you think companies should respond to negative reviews?",
            "How reliable are online reviews in your opinion?",
            "What impact do reviews have on businesses?"
        ],
        "preparationTime": 60
    }
},

"cam16_test3": {
    "part1": [
        {"question": "Do you like shopping for luxury items?", "followUp": "What do you consider a luxury item?"},
        {"question": "Do you ever save money for expensive things?", "followUp": "How do you decide whether something is worth the price?"},
        {"question": "Are there any brands you particularly like?", "followUp": "Why do people buy branded products?"},
        {"question": "Do you think expensive things are always of better quality?", "followUp": "What makes a product worth its high price?"}
    ],
    "part2": {
        "cueCard": "Describe a luxury item you would like to own in the future.",
        "bulletPoints": [
            "what the item is",
            "what it looks like",
            "why you would like to own it",
            "and explain how you would feel if you owned it"
        ],
        "followUpQuestions": [
            "Why do some people spend a lot of money on luxury goods?",
            "Do you think the desire for luxury goods is a positive or negative thing?",
            "How has the market for luxury goods changed over time?",
            "Should luxury goods be taxed more heavily?"
        ],
        "preparationTime": 60
    }
},

"cam16_test4": {
    "part1": [
        {"question": "How often do you use technology?", "followUp": "What device do you use most frequently?"},
        {"question": "Is there any technology you used to use but no longer do?", "followUp": "Why did you stop using it?"},
        {"question": "How has technology changed your daily life?", "followUp": "Do you think people rely too much on technology?"},
        {"question": "What new technology do you find most exciting?", "followUp": "Is there any technology you would like to try?"}
    ],
    "part2": {
        "cueCard": "Describe some technology that you decided to stop using.",
        "bulletPoints": [
            "what the technology was",
            "when and why you started using it",
            "why you decided to stop using it",
            "and explain how your life has changed since you stopped using it"
        ],
        "followUpQuestions": [
            "Do you think people are becoming too dependent on technology?",
            "What older technologies are making a comeback?",
            "How can people reduce their screen time?",
            "Is it better to adopt new technology quickly or wait?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam17 - AI-generated reasonable topics ====================

"cam17_test1": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "What do you enjoy most about your daily routine?"},
        {"question": "Do you like to plan things in advance?", "followUp": "What kinds of things do you usually plan?"},
        {"question": "How do you usually spend your weekends?", "followUp": "Would you prefer to have more free time or more money?"},
        {"question": "Do you enjoy cooking?", "followUp": "What is your favourite dish to prepare?"}
    ],
    "part2": {
        "cueCard": "Describe a time when you had to make a difficult decision.",
        "bulletPoints": [
            "what the decision was",
            "why it was difficult to make",
            "what the result of your decision was",
            "and explain how you felt after making this decision"
        ],
        "followUpQuestions": [
            "Do you think young people find it harder to make decisions than older people?",
            "How can parents help their children learn to make good decisions?",
            "Should important decisions be made alone or with the help of others?",
            "Do you think technology helps people make better decisions?"
        ],
        "preparationTime": 60
    }
},

"cam17_test2": {
    "part1": [
        {"question": "Do you live in a city or a village?", "followUp": "What do you like most about where you live?"},
        {"question": "How do you usually get around?", "followUp": "What is the public transport like in your area?"},
        {"question": "Do you enjoy walking?", "followUp": "Where do you like to go for a walk?"},
        {"question": "How important is exercise to you?", "followUp": "What kind of exercise do you do regularly?"}
    ],
    "part2": {
        "cueCard": "Describe a place in your hometown that has changed a lot.",
        "bulletPoints": [
            "what place it is",
            "what it used to be like",
            "how it has changed",
            "and explain whether you think the changes are positive or negative"
        ],
        "followUpQuestions": [
            "Why do cities change so quickly?",
            "Do you think it is important to preserve historical buildings?",
            "How can city planners balance development and preservation?",
            "What will cities look like in 50 years?"
        ],
        "preparationTime": 60
    }
},

"cam17_test3": {
    "part1": [
        {"question": "What do you do for a living?", "followUp": "How did you choose your career path?"},
        {"question": "Do you like learning new things?", "followUp": "What is the most recent skill you have learned?"},
        {"question": "How do you prefer to learn new information?", "followUp": "Do you think schools prepare students well for the future?"},
        {"question": "Do you enjoy working with other people?", "followUp": "What makes a good colleague or classmate?"}
    ],
    "part2": {
        "cueCard": "Describe a skill that you would like to learn in the future.",
        "bulletPoints": [
            "what skill it is",
            "how you would learn it",
            "why you want to learn this skill",
            "and explain how this skill might be useful in your life"
        ],
        "followUpQuestions": [
            "What skills do you think will be most important in the future?",
            "Should practical skills be taught more in schools?",
            "How has the internet changed the way people learn new skills?",
            "Is it better to learn a wide range of skills or to specialise in one area?"
        ],
        "preparationTime": 60
    }
},

"cam17_test4": {
    "part1": [
        {"question": "Do you like to keep in touch with friends and family?", "followUp": "How do you usually communicate with them?"},
        {"question": "Has social media changed the way you communicate?", "followUp": "What are the advantages of social media?"},
        {"question": "Do you prefer calling or texting?", "followUp": "In what situations is it better to call rather than text?"},
        {"question": "How often do you meet friends in person?", "followUp": "What do you usually do when you meet up with friends?"}
    ],
    "part2": {
        "cueCard": "Describe a person you know who has an interesting job.",
        "bulletPoints": [
            "who this person is",
            "what job they do",
            "how they got into this job",
            "and explain why you think their job is interesting"
        ],
        "followUpQuestions": [
            "What jobs are most respected in your country?",
            "How do young people choose their careers these days?",
            "Do you think job satisfaction is more important than a high salary?",
            "How is the job market changing with new technology?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam18 - AI-generated reasonable topics ====================

"cam18_test1": {
    "part1": [
        {"question": "Where did you grow up?", "followUp": "What did you enjoy most about your childhood?"},
        {"question": "How has your neighbourhood changed since you were young?", "followUp": "Would you like to live in the same area when you are older?"},
        {"question": "Do you enjoy spending time outdoors?", "followUp": "What outdoor activities do you like?"},
        {"question": "Do you think it is important for children to spend time in nature?", "followUp": "How can parents encourage children to play outside more?"}
    ],
    "part2": {
        "cueCard": "Describe a childhood memory that is important to you.",
        "bulletPoints": [
            "what the memory is",
            "how old you were at the time",
            "who was with you",
            "and explain why this memory is so important to you"
        ],
        "followUpQuestions": [
            "Why do some childhood memories stay with us forever?",
            "How has childhood changed compared to your parents' generation?",
            "Do you think children today are under too much pressure?",
            "What role do grandparents play in children's lives?"
        ],
        "preparationTime": 60
    }
},

"cam18_test2": {
    "part1": [
        {"question": "Do you like to keep fit?", "followUp": "What do you do to stay healthy?"},
        {"question": "How important is a healthy diet to you?", "followUp": "Have your eating habits changed over time?"},
        {"question": "Do you cook your own meals?", "followUp": "Where do you usually buy your food?"},
        {"question": "What kind of food is popular in your country?", "followUp": "Do you think traditional food is being replaced by fast food?"}
    ],
    "part2": {
        "cueCard": "Describe a healthy habit that you have developed.",
        "bulletPoints": [
            "what the habit is",
            "when you started doing it",
            "why you decided to develop this habit",
            "and explain how this habit has benefited your life"
        ],
        "followUpQuestions": [
            "Why do many people find it difficult to maintain healthy habits?",
            "What role should the government play in promoting public health?",
            "How has the health and fitness industry changed in recent years?",
            "Do you think people in the future will be healthier than people today?"
        ],
        "preparationTime": 60
    }
},

"cam18_test3": {
    "part1": [
        {"question": "Do you like watching films?", "followUp": "What kind of films do you prefer?"},
        {"question": "How often do you go to the cinema?", "followUp": "Do you prefer watching films at home or in a cinema?"},
        {"question": "Do you have a favourite actor or director?", "followUp": "What makes a film great in your opinion?"},
        {"question": "Are foreign films popular in your country?", "followUp": "Do you enjoy films from other cultures?"}
    ],
    "part2": {
        "cueCard": "Describe a film that left a strong impression on you.",
        "bulletPoints": [
            "what film it was",
            "when and where you watched it",
            "what the film was about",
            "and explain why it left such a strong impression on you"
        ],
        "followUpQuestions": [
            "How do films influence society?",
            "Do you think the film industry will survive the rise of streaming services?",
            "Should films be used to educate people about social issues?",
            "How has film-making technology changed the viewing experience?"
        ],
        "preparationTime": 60
    }
},

"cam18_test4": {
    "part1": [
        {"question": "How often do you listen to music?", "followUp": "What kind of music do you enjoy?"},
        {"question": "Do you play any musical instruments?", "followUp": "Would you like to learn to play an instrument?"},
        {"question": "Do you prefer listening to music alone or with others?", "followUp": "Has your taste in music changed over the years?"},
        {"question": "How do you discover new music?", "followUp": "Do you go to live music events?"}
    ],
    "part2": {
        "cueCard": "Describe a song or piece of music that is meaningful to you.",
        "bulletPoints": [
            "what the song or piece of music is",
            "when you first heard it",
            "what it is about",
            "and explain why it is meaningful to you"
        ],
        "followUpQuestions": [
            "Why is music so important in people's lives?",
            "How has the music industry changed with the internet?",
            "Do you think music should be taught more in schools?",
            "Is traditional music in your country being lost?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam19 - AI-generated reasonable topics ====================

"cam19_test1": {
    "part1": [
        {"question": "Do you live in a house or an apartment?", "followUp": "What do you like most about your home?"},
        {"question": "What is your neighbourhood like?", "followUp": "What facilities are available near your home?"},
        {"question": "Do you get on well with your neighbours?", "followUp": "How important is it to have good neighbours?"},
        {"question": "Would you like to move to a different area in the future?", "followUp": "What would your ideal home look like?"}
    ],
    "part2": {
        "cueCard": "Describe a house or apartment that you would like to live in.",
        "bulletPoints": [
            "what it would look like",
            "where it would be located",
            "who you would live with",
            "and explain why you would like to live there"
        ],
        "followUpQuestions": [
            "How has housing design changed in your country?",
            "What are the advantages and disadvantages of living in a big city?",
            "Do you think the government should provide affordable housing?",
            "How will housing change in the future?"
        ],
        "preparationTime": 60
    }
},

"cam19_test2": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "How do you balance work/study and personal life?"},
        {"question": "What do you like to do to relax?", "followUp": "How important is it to take breaks during the day?"},
        {"question": "Do you have any hobbies?", "followUp": "How did you get interested in your hobby?"},
        {"question": "How do you usually spend your free time on weekdays?", "followUp": "Do you wish you had more free time?"}
    ],
    "part2": {
        "cueCard": "Describe a hobby or activity that helps you relax.",
        "bulletPoints": [
            "what the hobby or activity is",
            "how often you do it",
            "where and when you do it",
            "and explain why you find it relaxing"
        ],
        "followUpQuestions": [
            "Why is it important for people to have hobbies?",
            "How have people's leisure activities changed in the digital age?",
            "Do you think people work too much and relax too little?",
            "Should employers provide more leisure facilities for workers?"
        ],
        "preparationTime": 60
    }
},

"cam19_test3": {
    "part1": [
        {"question": "Do you like taking photographs?", "followUp": "What do you usually take photos of?"},
        {"question": "Do you prefer taking photos with a phone or a camera?", "followUp": "What do you do with the photos you take?"},
        {"question": "How important are photographs in preserving memories?", "followUp": "Do you like looking at old photographs?"},
        {"question": "Has social media changed the way people take photos?", "followUp": "Do you share your photos online?"}
    ],
    "part2": {
        "cueCard": "Describe a photograph that you really like.",
        "bulletPoints": [
            "what the photograph shows",
            "when and where it was taken",
            "who took the photograph",
            "and explain why you like this photograph so much"
        ],
        "followUpQuestions": [
            "Why do people enjoy looking at photographs?",
            "How has digital photography changed the way we record our lives?",
            "Do you think professional photography is still important?",
            "Should photography be taught as an art form in schools?"
        ],
        "preparationTime": 60
    }
},

"cam19_test4": {
    "part1": [
        {"question": "How do you usually get to work or school?", "followUp": "How long does your journey take?"},
        {"question": "What is the traffic like in your area?", "followUp": "Has traffic got better or worse in recent years?"},
        {"question": "Do you think public transport is good in your city?", "followUp": "How could public transport be improved?"},
        {"question": "Do you enjoy travelling long distances?", "followUp": "What is the longest journey you have ever taken?"}
    ],
    "part2": {
        "cueCard": "Describe a journey that you remember well.",
        "bulletPoints": [
            "where you went",
            "how you travelled",
            "who you travelled with",
            "and explain why you remember this journey so well"
        ],
        "followUpQuestions": [
            "How has transport changed in the last 50 years?",
            "What are the environmental effects of increased travel?",
            "Do you think people will travel more or less in the future?",
            "How can governments encourage people to use greener transport?"
        ],
        "preparationTime": 60
    }
},

# ==================== cam20 - AI-generated reasonable topics ====================

"cam20_test1": {
    "part1": [
        {"question": "Do you work or are you a student?", "followUp": "What do you hope to achieve in the next five years?"},
        {"question": "What do you do to relax after a long day?", "followUp": "Do you think it is important to have a daily routine?"},
        {"question": "Do you enjoy spending time alone or with others?", "followUp": "How has this preference changed as you have grown older?"},
        {"question": "What is your favourite time of the day?", "followUp": "Do you consider yourself a morning person or a night owl?"}
    ],
    "part2": {
        "cueCard": "Describe a goal that you would like to achieve in the future.",
        "bulletPoints": [
            "what the goal is",
            "when you set this goal",
            "what you need to do to achieve it",
            "and explain why achieving this goal is important to you"
        ],
        "followUpQuestions": [
            "Why is it important for people to have goals?",
            "How can people stay motivated when working towards long-term goals?",
            "Do you think young people today have different goals than their parents?",
            "Should employers help their employees achieve personal goals?"
        ],
        "preparationTime": 60
    }
},

"cam20_test2": {
    "part1": [
        {"question": "What kind of weather do you like best?", "followUp": "How does the weather affect your mood?"},
        {"question": "Do you prefer hot or cold climates?", "followUp": "Would you like to live in a country with a different climate?"},
        {"question": "What do you usually do on rainy days?", "followUp": "Do you think the climate in your country is changing?"},
        {"question": "Are there any outdoor activities you enjoy in good weather?", "followUp": "How do the seasons affect daily life in your country?"}
    ],
    "part2": {
        "cueCard": "Describe a place you know that has been affected by weather or climate.",
        "bulletPoints": [
            "what place it is",
            "how the weather or climate affects it",
            "what changes you have noticed there",
            "and explain how people in this place deal with the weather conditions"
        ],
        "followUpQuestions": [
            "How serious is climate change in your opinion?",
            "What should governments do to address climate change?",
            "How can individuals reduce their impact on the environment?",
            "Do you think international cooperation on climate change is effective?"
        ],
        "preparationTime": 60
    }
},

"cam20_test3": {
    "part1": [
        {"question": "Do you enjoy giving and receiving gifts?", "followUp": "What was the last gift you received?"},
        {"question": "On what occasions do people give gifts in your country?", "followUp": "Do you prefer giving or receiving gifts?"},
        {"question": "How do you choose gifts for people?", "followUp": "Is the value of a gift important?"},
        {"question": "Have you ever received a gift you did not like?", "followUp": "What do you do with gifts you do not need?"}
    ],
    "part2": {
        "cueCard": "Describe a special gift that you gave to someone.",
        "bulletPoints": [
            "what the gift was",
            "who you gave it to",
            "why you chose that particular gift",
            "and explain how the person reacted when they received it"
        ],
        "followUpQuestions": [
            "Has the tradition of gift-giving changed in your country?",
            "Do you think expensive gifts are more meaningful than inexpensive ones?",
            "How do consumer habits affect gift-giving?",
            "Should children be taught about the value of giving rather than receiving?"
        ],
        "preparationTime": 60
    }
},

"cam20_test4": {
    "part1": [
        {"question": "Do you like animals?", "followUp": "Did you have any pets when you were growing up?"},
        {"question": "What is your favourite animal?", "followUp": "Have you ever been to a zoo or wildlife park?"},
        {"question": "How important is it to protect endangered species?", "followUp": "What can people do to help protect animals?"},
        {"question": "Are there any animals that are special in your culture?", "followUp": "How do people in your country feel about keeping pets?"}
    ],
    "part2": {
        "cueCard": "Describe an animal that you find interesting.",
        "bulletPoints": [
            "what animal it is",
            "where it lives",
            "what you know about its behaviour",
            "and explain why you find this animal interesting"
        ],
        "followUpQuestions": [
            "How important are zoos in protecting animals?",
            "Should wild animals be kept as pets?",
            "How has human activity affected wildlife?",
            "What can be done to protect endangered species more effectively?"
        ],
        "preparationTime": 60
    }
},

}

for test_id, test_data in SPEAKING_TESTS.items():
    test_data["id"] = test_id
    filepath = os.path.join(DATA_DIR, f"{test_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"  Created: {filepath}")

print(f"\nDone! Generated {len(SPEAKING_TESTS)} speaking test files.")
