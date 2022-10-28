# icecream-order-system
Icecream order system and ice cream recommendation system.  Use RASA.

# Instructions 
# Icecream order system

To build this architecture, two forms with 7 slots are used. It need a form to combine all the
ice cream information, which contains 6 slots (what flavor, whether need toppings, what
toppings, what size, whether need drinks, what drink). Another form is used for submit
request, which contains a boolean slot to catch whether the user want to submit this order.

## To start
To start this system, you can use either a ‘greet’ intent such as hello and hey, or an
‘ask_icecream’ intent such as May I have an ice cream?.
If you start with ‘great’ intent, after several back-and-forth conversations, don’t forget to
continue to ask for order ice cream. The ice cream order form can only be activated by an
‘ask_icecream’ intent.

## During Order
### - How to reply
When being asked what flavor, the user can reply only one flavor or reply the flavor with
toppings (see the example in Design Idea). This system can accept a variety of utterances,
ranging from single responses to longer utterances. chocolate and may I get one tiramisu ice cream? are both accepted in this system. All reply in affirm intent, such as yes, y and sure can
all enable a boolean slot to True. Details can be seen in the ‘hw2_p1\data\nlu.yml’
### - Flavor not in the menu
The system might response you that it is not in the menu. But when the system has no
response( It haven’t been trained that this word or phrase is a flavor), it is just waiting for a
right answe, you can say chocolate or other flavors in the menu to continue this order. - Yes/no
All questions in this system support multiple kinds of ‘affirm’ and ‘deny’. If it do not
response, the reason might be that your reply is neither in the ‘affirm’ intent nor the ‘deny’
intent.

## Unhappy Path
The more unhappy paths it supports, the more stories needs to be written. Therefore, the
system only support recieving unhappy paths between the ‘what flavor’ and ‘what toppings’
questions. Example are:
- Can you add two flavors together?
- Can I book a table?
Becasue of time, other situations have not been written in the story.yml.

## Submit Order and Order again
This system can support ordering ice cream for more than one times. For example, if you
deny to submit the order at the end, you can then call ‘ask_icecream’ intent to start a new
order.


# icecream recommendation system

## To start
To start this system, you can use either a ‘greet’ intent such as hello and hey, or an
‘need_recommendation’ intent, for example Could you recommend some flavors to me?

If you start with ‘great’ intent, after several back-and-forth conversations, don’t forget to
continue to ask for recommendation. The recommendation system can only be activated by a
‘need_recommendation’ intent.

## During Recommendation
### - How to reply
Multiple kinds of ‘affirm’ and ‘deny’ are supported during the survey. For example:
Yes / Y / That sounds good / Sure / Yes I love that / Yep
No / N / Don't like that / No I don’t like that
The reply Maybe is also supported. At this time, The system will treat it as if you don't dislike
this feature and automatically classify it as a like.
### - Multiple ways to recommendations
This system can generate recommendations in multiple ways. It depends on whether the user
wants to try the specialties, and whether there have common features between the user’s
preference and specialties. ‘Highly recommend’ means there are specialties that match the
user’s preference.

## Unhappy Path
Two new unhappy paths are added. Similar with the system in part 1, unhappy paths can only
be supported between the first and second question (fruit and mix).
### Case 1: No preference
This happens in the recommendation part. When being ask whether you like fruit, you can
say:
- I have no preference.
- Both ok
### Case 2: Recommendation when Ordering Ice Cream
This happens in the order part. After say some words like I want an ice cream, when being
ask what kind of flavor you want, you can say:
- I have no favourite flavor
- Any recommendation?
