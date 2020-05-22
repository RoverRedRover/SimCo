#! usr/bin/python3

""" SIMCOMPANIES WHOLESALER ASSISTANT
    Developed by RoverRedRover, April-May 2020.

    Give the wholesaling player ready access 
    to functions and data he can use on 
    desktop or mobile that will give him 
    confidence he is pricing his products
    for profit.

    No integrated UI; use with a REPL.

    Check out Sim Companies at
        https://www.simcompanies.com
"""


__TITLE__ = 'SimCompanies Wholesaler Assistant'
__VERSION__ = '0.5'
__AUTHOR__ = 'RoverRedRover'


# IMPORTS
from requests import get
from json import loads

class Product:


    # CONSTANTS
    XPT_MULT = {
        "water": 0, 
        "seeds": 0.1,
        "apples": 1,
        "oranges": 1,
        "grapes": 1,
        "grain": 0.1,
        "sugarcane": 0.1,
        "cotton": 0.5,
        "wood": 1
    }

    XPT_COST = 0.342
    EXC_PCT = 0.03
    OBJ_LIST = {}

    # CONSTANTS: API
    BASE_URL = 'https://www.simcompanies.com/'
    API_URL = ('api/v1/market-ticker/'
                '2020-05-11T04:05:52.191Z')
    MY_PRODUCTS = { # todo merge XPT_MULT?
        2: "water",  
        3: "apples",
        4: "oranges",
        5: "grapes",
        6: "grain",
        13: "transport",
        29: "plant research",
        40: "cotton",
        66: "seeds",
        72: "sugarcane",
        106: "wood"
    }
    MY_RESULTS = {}
    PAUSE_TIME = 10    # minutes
    MAX_RUNTIME = 240  # minutes
  


    # STATIC METHODS
    @staticmethod
    def calc_price(
         src_cost, freight, tgt_mgn):
        ''' Return exchange & contract prices
            given source & freight costs and
           desired gross margin.
        '''

        # calc exchange price
        exch_price = (
            (src_cost + freight) /
            (1 - Product.EXC_PCT - tgt_mgn))

        # calc contract price
        contr_price = (
            (src_cost + freight / 2) /
            (1 - tgt_mgn))

        return exch_price, contr_price



    @staticmethod
    def calc_margin(
        exch_cogs, contr_cogs, price):
        """ Returns GPM, given cogs, price.
            See also CLI-friendly public 
            method 'cm'.
        """
        
        exch_mgn = (
            (price - exch_cogs) 
                / price * 100)

        contr_mgn = (
            (price - contr_cogs) 
                / price * 100)

        return exch_mgn, contr_mgn



    @staticmethod
    def fv(pv, i, n, t):
        ''' todo return future value of
            a given amount of money
            held presently
        '''
        # fv = pv * (1 + (i/n))**(n*t)
        return
   


    # CLASS METHODS
    @classmethod
    def api_get(cls):
        ''' Return current Exchange prices
            using SimCompanies' API.
        '''

        market_state = loads(get(
            cls.BASE_URL + cls.API_URL)
                .content)
            # list of dicts; ea dict is
                # data re one prod.

        # todo kill nested loops yuck
        for entry in market_state:

            for product in \
                cls.MY_PRODUCTS.values():

                if product in entry['image']:

                    cls.MY_RESULTS[product] \
                        = entry['price']



    @classmethod
    def load_products(cls):
        ''' Load previously saved Product
            objects using pickle.
        '''
        
        from pickle import load
        from os import name

        load_file = "products.pkl" if name \
            == "posix" else "products_win.pkl"

        try:
            cls.OBJ_LIST = (
                load(open(load_file, 'rb')))
            print('Objects loaded '
                'successfully.')

        except:
            print('Object loading failed.')


         
    @classmethod
    def save_products(cls):
        ''' Pickle previously Product
            objects for later use.
        '''

        from pickle import dump
        from os import name

        save_file = "products.pkl" if name \
            == "posix" else "products_win.pkl"

        try:
            dump(cls.OBJ_LIST,
                open(save_file, 'wb'))
            print('Objects saved '
                'successfully.')

        except:
            print('Object pickling '
                'failed.')
    


    @staticmethod
    def print_exch_data():
        ''' Pretty-print latest Exchange data
        '''

        from time import ctime
        from prettytable import PrettyTable
        
        Product.api_get()
        load_time = ctime()
        
        # Set up the basic table parameters.
        t = PrettyTable(
            ['PROD', 'PRC', 'COGS', 'GPM'])
        t.title = ('EXCHANGE @ '
            f'{load_time}')
        t.align['PROD'] = 'l'
        t.align['PRC'] = 'r'
        t.align['COGS'] = 'r'
        t.align['GPM'] = 'r'

        next_row = []

        # Populate table with data from JSON
        # import.
        for key in Product.MY_RESULTS:

            next_row.append(key.capitalize())

            price = Product.MY_RESULTS[key]

            next_row.append(f'${price:,.3f}')
            
            cogs = 'N/A'
            gpm = 'N/A'
            
            if key in Product.OBJ_LIST:
                cogs = (Product.OBJ_LIST[key].
                    exch_cogs)
                cogs = f'${cogs:,.3f}'
                gpm, _ = (
                    Product.OBJ_LIST[key].
                    cm(Product.MY_RESULTS
                    [key]))
                gpm = f'{gpm:,.1f}%'
            
            next_row.append(cogs)
            next_row.append(gpm)
            t.add_row(next_row)
            next_row.clear()

        t.sortby = 'GPM'
        
        print(t)


 
    # DUNDERS
    def __init__(self, prod_type, src_cost,
            tgt_mgn=0.03):

        if prod_type.lower() in \
            Product.XPT_MULT:

            self.prod_type = prod_type
            self.src_cost = src_cost
            self.tgt_mgn = tgt_mgn

            self.eval_attrs()

            Product.OBJ_LIST[
                self.prod_type] = self

            self.list_options(0.5)

        else:
            print("Invalid product selection.")



    # REGULAR METHODS
    def eval_attrs(self):
        ''' calc freight as well as price and 
            COGS for both exchange and contract
            Needs to be re-run whenever 
            instance variables are changed.
        '''

        self.freight = (
            Product.XPT_COST * 
            Product.XPT_MULT[self.prod_type])

        # calc exchange, contract prices
        self.exch_price, self.contr_price  = (
            Product.calc_price(
                self.src_cost,
                self.freight,
                self.tgt_mgn))

        # calc cost of goods sold (cogs)
        self.exch_cogs = (
            self.src_cost +
            self.freight +
            self.exch_price * 0.03)

        self.contr_cogs = (
            self. src_cost + 
            self.freight / 2)


    
    def list_options(self, mult, 
            lbound=1, ubound=11):
        ''' Provides a list of prices for both
            Exchange and contract by GPM.
        '''

        # print header rows
        print()
        print("Gross profit margins for",
                self.prod_type)
        print("-------------------------")
        print("Pct\t" "Exch\t" "Contr")
        print("-------------------------")


        # print data table
        for gpm in range(lbound, ubound):
            
            gpm *= mult

            exc, con = (
                Product.calc_price(
                    self.src_cost,
                    self.freight,
                    gpm/100))
            
            print(
                f"{gpm:,.2f}%".rjust(3),
                "\t"
                f"${exc:,.2f}\t"
                f"${con:,.2f}\t")

        print()



    def cm(self, price):
        ''' Calc margin on self. Easier to
            use on a CLI than the static
            method 'calc_margin' (WET).
        '''

        exch_mgn, contr_mgn = \
                Product.calc_margin(
                    self.exch_cogs,
                    self.contr_cogs,
                    price)

        return exch_mgn, contr_mgn


    
    def cp(self, margin):
        ''' Calc price on self.  Easier to
            use on a CLI than the static
            method 'calc_price' (WET).
        '''
        # todo 
    

if __name__ == "__main__":

    Product.load_products()

    Product.print_exch_data()

    print("ready for use in interpreter")

