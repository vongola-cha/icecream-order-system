from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset, SlotSet

import re

FLAVOR_CHOICE = ['chocolate', 'matcha', 'coconut', ' ', 'lychee rose', 'pineapple']
SIZE_CHOICE = [6, 8, 12, 24]


class ValidateIceCreamForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ice_cream_form"

    def validate_flavor(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `actionType` value."""
        print(slot_value)
        if slot_value.lower() not in FLAVOR_CHOICE:
            dispatcher.utter_message(text="Sorry we don't have that. Here are our menu:")
            for i in FLAVOR_CHOICE:
                dispatcher.utter_message(text=f"{i}")
            return {"flavor": None}
        topping = tracker.slots.get("toppingsList")
        # not only say flavor
        if topping:
            dispatcher.utter_message(text=f"ok, {slot_value} icecream with {topping}. ")
            return {"flavor": slot_value, "need_toppings": True, "toppingsList": topping}
        dispatcher.utter_message(text=f"ok, {slot_value} icecream. ")
        return {"flavor": slot_value}

    def validate_size(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `actionType` value."""

        # pick up number only from slot (size)
        size_numOnly = re.findall(r"\d+", slot_value)[0]
        size_numOnly = int(size_numOnly)
        # outof category
        if size_numOnly not in SIZE_CHOICE:
            dispatcher.utter_message(text=f"Sorry, we don't have {size_numOnly} oz. Please tell me again.")
            return {"size": None}
        # get size successfully
        dispatcher.utter_message(text=f"ok, {slot_value} . ")
        return {"size": slot_value}

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict"
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("need_toppings") == False:
            updated_slots.remove("toppingsList")

        if tracker.slots.get("need_drinks") == False:
            updated_slots.remove("drinksList")
        return updated_slots

    def validate_toppingsList(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # need drink
        dispatcher.utter_message(text=f"ok, {slot_value} . ")
        return {"toppingsList": slot_value}

    def validate_drinksList(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # need drink
        dispatcher.utter_message(text=f"ok, {slot_value} . ")
        return {"drinksList": slot_value}


class ShowOrder(Action):
    def name(self):
        return "action_show_order"

    def run(self, dispatcher, tracker, domain):
        flavor = tracker.slots.get("flavor")
        sizeslot = tracker.slots.get("size")
        size = int(re.findall(r"\d+", sizeslot)[0])
        dispatcher.utter_message(text=" ")
        dispatcher.utter_message(text="Please check your order:")
        dispatcher.utter_message(text="--------------------------------------")
        dispatcher.utter_message(text=f"One {size} oz {flavor} ice cream.")
        if tracker.slots.get("need_toppings"):
            toppings = tracker.slots.get("toppingsList")
            dispatcher.utter_message(text=f"Toppings: {toppings}")
        else:
            dispatcher.utter_message(text=f"Without toppings.")
        if tracker.slots.get("need_drinks"):
            drinks = tracker.slots.get("drinksList")
            dispatcher.utter_message(text=f"Drinks: {drinks}")
        else:
            dispatcher.utter_message(text=f"Without drink.")
        dispatcher.utter_message(text="--------------------------------------")
        return []


class ResetAllSlots(Action):
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        submit = tracker.slots.get("comfirm_submit")
        if submit:
            dispatcher.utter_message(text="Thank you, your order has been successfully completed! Enjoy！:)")
        else:
            dispatcher.utter_message(text="OK, your order has been canceled. See you next time!")
        return [AllSlotsReset()]



#---------------HW2---------------------
class ShowRecommendation(Action):
    fruit= {'Coconut', 'Pineapple', 'Pineapple Salted Egg Yolk', 'Peach Sweet Tea', 'Lychee Rose', 'Mango'}
    mix={'Pineapple Salted Egg Yolk','Peach Sweet Tea','Coffee Caramel Butter',
         'Vanilla With Chocolate','Lychee Rose','Green Tea Pistachio'}
    salty={'Pineapple Salted Egg Yolk','Green Tea Pistachio'}
    chocolate={'Chocolate','Vanilla With Chocolate'}
    special={'Pineapple Salted Egg Yolk','Lychee Rose','Green Tea'}
    coffee={'Tiramisu','Coffee Caramel Butter'}
    tea={'Peach Sweet Tea','Green Tea','Green Tea Pistachio'}
    def name(self):
        return "action_show_recommendation"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text=" ")
        dispatcher.utter_message(text="Generate Recommendation ... ... ")
        # generate
        love_fruit=tracker.slots.get("love_fruit")
        love_mix=tracker.slots.get("love_mix")
        love_chocolate=tracker.slots.get("love_chocolate")
        love_special=tracker.slots.get("love_special")
        love_coffee=tracker.slots.get("love_coffee")
        love_salty=tracker.slots.get("love_salty")
        love_tea=tracker.slots.get("love_tea")
        total=self.fruit|self.fruit| self.mix| self.salty| self.chocolate| self.special| self.coffee| self.tea
        # total = list(set(self.fruit).union(self.fruit, self.mix, self.salty, self.chocolate, self.special, self.coffee, self.tea))
        temp={'Raw Milk'}
        # print(total)
        answer = total | temp
        if not love_fruit:
            answer-=self.fruit
        if not love_mix:
            answer-=self.mix
        if not love_salty:
            answer-=self.salty
        if not love_chocolate:
            answer-=self.chocolate
        if not love_coffee:
            answer-=self.coffee
        if not love_tea:
            answer-=self.tea
        dispatcher.utter_message(text=" ")
        dispatcher.utter_message(text="Great! I have customized an personalized tasting menu for you!")
        if not love_special:
            answer-=self.special
            for i in answer:
                dispatcher.utter_message(text=f"{i}")
        else:
            listspecialty=self.special&answer
            if listspecialty is not []:
                dispatcher.utter_message(text="I highly recommend you try these! ")
                for i in listspecialty:
                    dispatcher.utter_message(text=f"{i}")
                dispatcher.utter_message(text=" ")
                dispatcher.utter_message(text="Other choices:")
                answer-=listspecialty
            for i in answer:
                dispatcher.utter_message(text=f"{i}")
            if listspecialty is []:
                dispatcher.utter_message(text=" ")
                dispatcher.utter_message(text="Since you want to try our specialty ice cream, here some other recommendations:")
                for i in self.special:
                    dispatcher.utter_message(text=f"{i}")
        return [AllSlotsReset()]
