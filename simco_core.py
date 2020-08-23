#! usr/bin/python3

""" SIMCOMPANIES WHOLESALER ASSISTANT
    RoverRedRover, April-May 2020.

    Provide the SimCompanies player with a
    suite of easy-to-use utilities that will
    assist him in running his company.

    From command line/terminal:
        cd <directory where simco is located>
        python -i simco_core.py

    GitHub:
    github.com/RoverRedRover/
        SimCompanies-Price-Calculator

    Check out Sim Companies at
        https://www.simcompanies.com
"""

__TITLE__ = 'SimCompanies Wholesaler Assistant'
__VERSION__ = '0.5'
__AUTHOR__ = 'RoverRedRover'


class Product:


    # CONSTANTS
    XPT_MULT = {
        # arranged in same sequence as warehouse screen
        # to make using Product.update_all() easier
        "seeds": 0.1,
        "apples": 1,
        "oranges": 1,
        "grapes": 1,
        "grain": 0.1,
        "cotton": 0.5,
        "sugarcane": 0.1,
        "wood": 1,
        "power": 0,
        "water": 0,
        "transport": 0,
        "leather": 1,
        "underwear": 1,
        "leather": 1,
        "fabric": 0.5,
    }

    OBJ_LIST = {}

    XPT_COST = 0.331

    DEFAULT_DATA_FILE = (
        'dev_products.pkl'
        # r'/mnt/c/Users/dvcas/OneDrive/'
        # r'Programming/Python/_PROJECTS/simco/'
        # r'dev_products.pkl'
    )

    # CONSTANTS: API
    BASE_URL = 'https://www.simcompanies.com/'
    API_URL = ('api/v1/market-ticker/'
                '2020-05-11T04:05:52.191Z')
    MY_PRODUCTS = { # todo merge XPT_MULT? maybe an orderedtuple?
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
    # PAUSE_TIME = 10    # minutes
    # MAX_RUNTIME = 240  # minutes



    # DUNDERS
    def __init__(self, prod_type, src_cost,
            tgt_mgn=0.03):

        if prod_type.lower() in \
            Product.XPT_MULT:

            self.prod_type = prod_type
            self.src_cost = src_cost
            self.tgt_mgn = tgt_mgn    # todo kill this attr

            self.eval_attrs()

            Product.OBJ_LIST[
                self.prod_type] = self

        else:
            print("Invalid product selection.")



    # STATIC METHODS
    @staticmethod
    def calc_price(src_cost, freight, tgt_mgn):
        ''' Return exchange & contract prices
            given source & freight costs and
           desired gross margin.
        '''

        # calc exchange price
        exch_price = (
            (src_cost + freight) /
            (1 - 0.03 - tgt_mgn))

        # calc contract price
        contr_price = (
            (src_cost + freight / 2) /
            (1 - tgt_mgn))

        return exch_price, contr_price



    @staticmethod
    def calc_margin(exch_cogs, contr_cogs,
        price):
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
    def first_time_use(cls):
        ''' Or whenever you fuck up your products file.'''

        for product in cls.MY_PRODUCTS.values():
            src_cost = float(input(f'Enter source cost for {product}: '))
            Product(product, src_cost)

        cls.save_products()



    @classmethod
    def print_exch_data(cls):
        ''' Pretty-print latest Exchange data
        '''

        from time import ctime
        from prettytable import PrettyTable

        cls.api_get()
        load_time = ctime()

        # Set up the basic table parameters.
        t = PrettyTable(
            ['PROD', 'PRC', 'COGS', 'GPM'],
            max_table_width=47,
            sortby = 'GPM')
        t.title = ('EXCHANGE @ '
            f'{load_time}')
        t.align['PROD'] = 'l'
        t.align['PRC'] = 'r'
        t.align['COGS'] = 'r'
        t.align['GPM'] = 'r'

        next_row = []

        # Populate table with data from JSON
        # import.
        for key in cls.MY_RESULTS:

            next_row.append(key.capitalize())

            price = cls.MY_RESULTS[key]

            next_row.append(f'${price:,.3f}')

            cogs = 'N/A'
            gpm = 'N/A'

            if key in cls.OBJ_LIST:
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

        #t.sortby = 'GPM'

        print(t.get_string(sortby='GPM',
            reversesort=False))



    @classmethod
    def api_get(cls):
        ''' Return current Exchange prices
            using SimCompanies' API.
        '''

        from json import loads
        from requests import get

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
    def load_products(cls, file=DEFAULT_DATA_FILE):
        ''' Load previously saved Product
            objects using pickle.
        '''

        # # test
        # print(f'Product.OBJ_LIST before loading products: '
        #       f'{hex(id(Product.OBJ_LIST))}')

        from pickle import load
        from os import name

        # load_file = "dev_products.pkl" if dev \
        #     else "products.pkl" if name == \
        #     "posix" else "products_win.pkl"

        # todo- first time use
        try:
            cls.OBJ_LIST = (
                load(open(file, 'rb')))

        except Exception as error:
            return error

        # print('Product data loaded '
        #     f'successfully from {file}.')

        return None

        # # test
        # print(f'Product.OBJ_LIST after loading products: '
        #       f'{hex(id(Product.OBJ_LIST))}')


    @classmethod
    def save_products(cls, file=DEFAULT_DATA_FILE):
        ''' Pickle current Product instances. '''

        from pickle import dump
        from os import name

        # save_file = "products.pkl" if name \
        #     == "posix" else "products_win.pkl"

        try:
            dump(cls.OBJ_LIST,
                open(file, 'wb'))
            #print('Product data saved '
            #    f'successfully to {file}.')

        except:
            print('Product data could not '
                    ' be saved.')



    @classmethod
    def print_prod_attrs(cls):
        ''' Print src_cost, exch_cogs,
            contr_cogs for all products
            in Product.OBJ_LIST
        '''

        from time import ctime
        from prettytable import PrettyTable

        # to make life a little easier
        products = cls.OBJ_LIST

        # initialize PrettyTable object
        t = PrettyTable(
            ['PROD', 'SRC CST',
            'exCOGS','ctCOGS'],
            max_table_width = 47)
        t.title = ('Warehouse @ '
                f'{ctime()}')
        t.align['PROD'] = 'l'
        t.align['SRC CST'] = 'r'
        t.align['exCOGS'] = 'r'
        t.align['ctCOGS'] = 'r'

        # list initialized for use in next loop
        next_row = []

        for key in products:
            # create a list of columns for next row
            # and print

            # todo can i use a with statement here?
            # assigning to local variables just
            # lets me pack my code into <= 47 cols
            srccst = (
                products[key].src_cost)
            exCOGS = (
                products[key].exch_cogs)
            ctCOGS = (
                products[key].contr_cogs)

            # put the list together for printing
            next_row.append(key.capitalize())
            next_row.append(f'${srccst:,.3f}')
            next_row.append(f'${exCOGS:,.3f}')
            next_row.append(f'${ctCOGS:,.3f}')

            # attach list to prettytable object
            t.add_row(next_row)

            next_row.clear()

        t.sortby = 'PROD'

        print(t)



    @classmethod
    def update_all(cls, attr='src_cost'):

        for product in cls.XPT_MULT:

            if product in cls.OBJ_LIST.keys():

                print(f'current {attr} of '
                    f'{product}: '
                    f'{getattr(cls.OBJ_LIST[product], attr)}'
                    )
                new_val = float(
                    input(
                    'set new value for '
                    f'{product}: '
                    ))

                setattr(cls.OBJ_LIST[product],
                    attr, new_val)

                cls.OBJ_LIST[
                    product].eval_attrs()

        cls.save_products()



    @classmethod
    def getp(cls, prod):

        return cls.OBJ_LIST[prod]



    @classmethod
    def check_for_aged_data(cls):
        ''' todo Let user know which objects need to be updated '''

        # from time import time

        pass



    # REGULAR METHODS
    def eval_attrs(self):
        ''' calc freight as well as price and
            COGS for both exchange and contract
            Needs to be re-run whenever
            instance variables are changed.
        '''

        # test
        # print()
        # print('Values within eval_attrs')
        # print(f'Product.OBJ_LIST: {hex(id(Product.OBJ_LIST))}')
        # #print(f'objs: {hex(id(objs))}') #iaccessible
        # print(f'self.OBJ_LIST: {hex(id(self.OBJ_LIST))}')

        self.freight = 0
        no_xpt = ['transport','power','water']

        # Freight cost if selling on the Exchange (div by 2 for contract)
        if self.prod_type not in no_xpt:
            self.freight = (
                Product.OBJ_LIST['transport'].
                src_cost *
                Product.XPT_MULT[
                    self.prod_type])

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

        from time import ctime
        self.last_update = ctime()



    def coherency_test(self):
        ''' test for things like...
            ZERO FREIGHT... UGH
        '''
        pass



    def list_options(self, mult,
        lbound=1, ubound=11):
        ''' Provides a list of prices for both
            Exchange and contract by GPM.
        '''

        # todo - refactor to use prettytable
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

        return Product.calc_margin(
                self.exch_cogs,
                self.contr_cogs,
                price)



    def cp(self, margin):
        ''' Calc price on self.  Easier to
            use on a CLI than the static
            method 'calc_price' (WET).
        '''

        return Product.calc_price(
                self.src_cost,
                self.freight,
                margin)



    def update(self, attr=None, val=0, file=DEFAULT_DATA_FILE):
        ''' Update any of a product's
            attribs., then re-calc its
            cogs and freight. Save.
        '''

        if attr:
            setattr(self, attr, val)

        self.eval_attrs()
        self.save_products(file)



def startup_routine():

    # Talk to me, Goose!
    print(f'\n{__TITLE__} v{__VERSION__}.\n'
            f'{__AUTHOR__}, May 2020.')

    print('Note:  At terminal or command line'
            ', type "python -i simco_core.py".')

    print('Loading past product data...')
    Product.load_products(dev=False)

    print('\nLoading latest Exchange data '
            'from SimCompanies.com...')

    Product.print_exch_data()
    print('Exchange data loaded '
            'successfully.')

    print('\nReady for use in interpreter.')


    # # test
    # print()
    # print('Product.OBJ_LIST in "startup_routine": '
    #         f'{len(Product.OBJ_LIST)}\n'
    #         f'Memory address: {hex(id(Product.OBJ_LIST))}')
    #
    # # test
    # print()
    # print('Product.OBJ_LIST["cotton"].OBJ_LIST in "startup_routine": '
    #         f'{len(Product.OBJ_LIST["cotton"].OBJ_LIST)}\n'
    #         f'Memory address: {hex(id(Product.OBJ_LIST["cotton"].OBJ_LIST))}')


if __name__ == "__main__":
    ''' ... then give me my goddamn ball... '''
    startup_routine()

    # Some assignments and functions to ease
    # use with REPL / interpreter
    objs = Product.OBJ_LIST

    # # test
    # print()
    # print('Product.OBJ_LIST in "if name is main": '
    #         f'{len(Product.OBJ_LIST)}\n'
    #         f'Memory address: {hex(id(Product.OBJ_LIST))}')
    #
    # # test
    # print()
    # print('objs in "if name is main": '
    #         f'{len(objs)}\n'
    #         f'Memory address: {hex(id(objs))}')
    #
    # # test
    # print()
    # print('Product.OBJ_LIST["cotton"].OBJ_LIST in "if name is main": '
    #         f'{len(Product.OBJ_LIST["cotton"].OBJ_LIST)}\n'
    #         f'Memory address: {hex(id(Product.OBJ_LIST["cotton"].OBJ_LIST))}')

    exc = Product.print_exch_data

    def update(prod, src_cost):
#         objs[prod].update(attr='src_cost',
#                 val=src_cost)
        # test
        # print()
        # print('Product.OBJ_LIST in function "update":'
        #       f'{len(Product.OBJ_LIST)}\n'
        #       f'Memory address: {hex(id(Product.OBJ_LIST))}')
        #
        # #test
        # print()
        # print('objs in function "update":'
        #       f'{len(objs)}\n'
        #       f'Memory address: {hex(id(objs))}')
        #
        # #test
        # print()
        # print('Product.OBJ_LIST["cotton"].OBJ_LIST in function "update":'
        #       f'{len(Product.OBJ_LIST["cotton"].OBJ_LIST)}\n'
        #       f'Memory address: {hex(id(Product.OBJ_LIST["cotton"].OBJ_LIST))}')
        Product.OBJ_LIST[prod].update(
            attr='src_cost', val=src_cost)
