import math


class CardPack:
    # 1 - 5th root of (1-0.02), number_of_cards = 5, rarity=0.02
    equation = "1 - {number_of_cards}th root of (1-{rarity})"

    def __init__(self, _name, _num_cards, legendary, rare, uncommon_to_common_split_percentage):
        """ All chances should be passed in as decimal values, not percentage. eg: 0.2 (20%)
            All perecentages should come in as decimal values as well. """
        self.name = _name
        self.number_of_cards = _num_cards

        self.per_pack_rarity_perecent = dict(legendary=legendary, rare=rare)
        self.per_card_roll_perecent = dict(legendary=-1, rare=-1, uncommon=-1, common=-1)

        self.split = uncommon_to_common_split_percentage  # this is the % leftover after calculating rarities

        self.calculate_uncommon_and_common_chances()

    def __str__(self):
        return "{} \n\t{} cards \n"\
               "\tRarities: {}\n" \
               "\tCard Rolls (checksum={}):\n\t\t{} \n" \
                .format(self.name, self.number_of_cards,
                    str(self.per_pack_rarity_perecent),
                    self.sum_rolls,
                    str(self.per_card_roll_perecent),
                    )

    def calculate_uncommon_and_common_chances(self):
        """ percent chances of non-rare cards needs calculating as a % of the remaining cards left after rarities
        percentages are calcualted. Eg: 1% legendary, 2% rare means there's 97% of cards left over to be split up
        between uncommon and common.  A split value of .70 means 70% of remaining cards go to uncommon chance,
        and """
        legendary = self.calculate_per_card_roll_percentage(self.per_pack_rarity_perecent['legendary'])
        rare = self.calculate_per_card_roll_percentage(self.per_pack_rarity_perecent['rare'])

        self.per_card_roll_perecent['legendary'] = legendary
        self.per_card_roll_perecent['rare'] = rare

        remaining_allocation = 1 - (legendary + rare)

        # We use remaining allocation to determine the per card roll percents for uncommon and common
        uncommon = remaining_allocation * self.split
        common = remaining_allocation * (1 - self.split)

        self.per_card_roll_perecent['uncommon'] = uncommon
        self.per_card_roll_perecent['common'] = common

        self.sum_rolls = self.sum_per_card_rolls()

    def calculate_per_card_roll_percentage(self, rarity):
        "1 - {number_of_cards}th root of (1-{rarity})"
        nth_root = self.nth_root((1 - rarity), self.number_of_cards)
        return 1 - nth_root

    def sum_per_card_rolls(self):
        sum = 0
        for key in self.per_card_roll_perecent:
            sum += self.per_card_roll_perecent[key]
        return sum

    def nth_root(self, number, root):
        value = number ** (1. / float(root))
        if number < 0:
            value = -1 * value
        return value


if __name__ == '__main__':
    pack = CardPack("Dry Whisker Pack", 1, .01, .02, .75)
    print(pack)

    pack = CardPack("Frisky Cat Pack", 5, .02, .05, .50)
    print(pack)

    pack = CardPack("Fancier Feast Pack", 11, .03, .08, .60)
    print(pack)

    pack = CardPack("I Am Not A Cat Pack", 15, .06, .10, .70)
    print(pack)




