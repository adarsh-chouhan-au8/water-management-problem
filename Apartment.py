from Constants import Constants
from sympy import symbols, Eq, solve
import math


class Apartment:
    def __init__(self, bhk_type, corporation_is_to_borewell_ratio):
        self.total_no_of_guests = 0

        if bhk_type == Constants.TWO_BHK:
            self.total_no_of_tenants = Constants.TENTANTS_IN_2_BHK
        else:
            self.total_no_of_tenants = Constants.TENTANTS_IN_3_BHK

        self.monthly_water_consumption_allowance = self.total_no_of_tenants * \
            Constants.CONSUMPTION_OF_A_PERSON_PER_DAY*Constants.NO_OF_DAYS_IN_A_MONTH
        self.coorporation_water_allocated = 0
        self.borewell_water_allocated = 0
        self.total_water_consumption = self.monthly_water_consumption_allowance
        self.total_bill = 0
        self.allot_water(corporation_is_to_borewell_ratio)

    def add_guests(self, no_of_guests):
        self.total_no_of_guests += no_of_guests
        self.total_water_consumption += no_of_guests * \
            Constants.CONSUMPTION_OF_A_PERSON_PER_DAY*Constants.NO_OF_DAYS_IN_A_MONTH

    def get_allocation(self, corporation_is_to_borewell_ratio):

        [bw_multiplier, cw_multiplier] = corporation_is_to_borewell_ratio.split(
            ':')

        CW, BW = symbols('CW,BW')

        eq1 = Eq((CW+BW), self.monthly_water_consumption_allowance)
        eq2 = Eq((CW*int(cw_multiplier)), BW*int(bw_multiplier))

        result = solve((eq1, eq2), (CW, BW))
        return result.values()

    def get_cost_by_corporate(self):
        cost = self.coorporation_water_allocated*Constants.CORPORATION_WATER_RATE
        return cost

    def get_cost_by_borewell(self):
        cost = self.borewell_water_allocated*Constants.BOREWELL_WATER_RATE
        return cost

    def get_cost_by_tank(self, water_quantity):
        total = 0
        brackets = [
            [Constants.TANKER_SLAB_0_TO_500L_MAX,
                Constants.TANKER_SLAB_0_TO_500L_RATE],
            [Constants.TANKER_SLAB_501_TO_1500L_MAX-Constants.TANKER_SLAB_0_TO_500L_MAX,
                Constants.TANKER_SLAB_501_TO_1500L_RATE],
            [Constants.TANKER_SLAB_1501_TO_3000L_MAX-Constants.TANKER_SLAB_501_TO_1500L_MAX,
                Constants.TANKER_SLAB_1501_TO_3000L_RATE]
        ]

        for bracket in brackets:
            max_value_of_bracket = bracket[0]
            bracket_rate = bracket[1]
            if max_value_of_bracket <= water_quantity:
                total += bracket_rate*max_value_of_bracket
                water_quantity -= max_value_of_bracket
            else:
                total += bracket_rate*water_quantity
                water_quantity = 0
                break

        if water_quantity != 0:
            total += (water_quantity)*Constants.TANKER_SLAB_3001_PLUS_RATE
        return total

    def calculate_billings(self):
        total = 0

        total += self.get_cost_by_corporate() + self.get_cost_by_borewell()

        additional_water_used = self.total_water_consumption - \
            self.monthly_water_consumption_allowance

        total += self.get_cost_by_tank(additional_water_used)
        self.total_bill = math.ceil(total)

    def allot_water(self, corporation_is_to_borewell_ratio):

        [coorporation_water_allocated, borewell_water_allocated] = self.get_allocation(
            corporation_is_to_borewell_ratio)

        self.borewell_water_allocated = borewell_water_allocated
        self.coorporation_water_allocated = coorporation_water_allocated
