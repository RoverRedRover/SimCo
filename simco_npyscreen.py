#! usr/bin/python3

""" Blah blah forthcoming docstring. Blah.
"""

import npyscreen
from simco_core import Product
PICKLE_FILENAME = "dead/dev_products.pkl"
Product.load_products(PICKLE_FILENAME)

class SimcoTUI_App(npyscreen.NPSAppManaged):
    """ npyscreen's native application manager """

    def onStart(self):

        self.addForm(
            'LOAD_PICKLE_FILE',
            LoadPickleFile,
            name = 'LOAD YOUR USER PROFILE',
            columns = 47,
        )

        self.addForm(
            'MAIN',
            ViewEditProducts,
            name = 'VIEW/EDIT PRODUCTS',
            columns = 47,
        )

        self.addForm(
            'ADD_PRODUCT',
            AddProduct,
            name = 'Add Product',
            columns = 47
        )



class LoadPickleFile(npyscreen.Form):
    """ The form that allows the user to select the pickle file from which the
        Product objects will be loaded.
    """

    OK_BUTTON_TEXT = 'LOAD & CONTINUE'
    # CANCEL_BUTTON_TEXT = 'EXIT APPLICATION'
    OK_BUTTON_BR_OFFSET = (5, 6)
    # CANCEL_BUTTON_BR_OFFSET = (3, 6)

    def create(self):

        # FORM HEADING
        self.add(
            npyscreen.Textfield,
            w_id = 'form_heading_main',
            value = 'SELECT USER PROFILE',
            editable = False,
        )

        self.nextrely += 1

        # Allow user to select the file he wants to read from.
        self.pkl_file = self.add(
            npyscreen.TitleFilenameCombo,
            name = 'Select .pkl: ',
            value = self.get_local_file(),
            # max_width = 47,
        )


    def get_local_file(self):
        """ Search the local file path for a .pkl file and return
            the first one you see
        """
        from sys import path
        from os import walk
        from os.path import splitext, join

        for parent, folders, files in walk(path[0]):

            # npyscreen.notify_confirm(
            #     parent,'Content of the parent variable')

            for file in files:
                if splitext(file)[1] == '.pkl':
                    return join(parent, file)

        return ''


    def try_loading_pickle(self):
        """ Attempt to load selected .pkl file and report result """

        global Product

        if Product.load_products(file = self.pkl_file.value):
            npyscreen.notify_confirm('Failed to load this data file. '
                'Please try again!', 'That didn\'t work...')
        else:
            npyscreen.notify_confirm('File loaded successfully. Click'
                ' "OK" to continue.',
                'Success!')


    def on_ok(self):
        self.try_loading_pickle()


    def afterEditing(self):
        self.parentApp.setNextForm('VIEW_EDIT_PRODUCTS')



class ViewEditProducts(npyscreen.ActionFormWithMenus):       # npyscreen.Form,
    """ The form that allows the user to easily change product
        source cost info
    """

    OK_BUTTON_TEXT = 'SAVE'
    CANCEL_BUTTON_TEXT = 'QUIT'
    #OK_BUTTON_BR_OFFSET = (2, 2)
    #CANCEL_BUTTON_BR_OFFSET = (3, 6)

    def create(self):

        Product.load_products(
            file ='dead/dev_products.pkl')

        # FORM HEADING
        self.add(
            npyscreen.Textfield,
            w_id = 'form_heading_main',
            value = 'SELECT PRODUCT TO VIEW',
            editable = False,
        )

        self.nextrely += 1

        # Allow user to select the product he wants to edit
        self.prod_list = self.add(
            npyscreen.TitleCombo,
            name = 'Select prod:',
            values = [x.capitalize() for x in Product.OBJ_LIST],
            value = 0,
            value_changed_callback = self.when_prod_updated,
        )

        self.nextrely += 1

        # FORM HEADING
        self.add(
            npyscreen.Textfield,
            w_id = 'form_heading_sub1',
            value = 'Current product attributes:',
            editable = False,
        )

        self.nextrely += 1

        self.prod_selected = self.prod_list.values[
            self.prod_list.value].lower()
        # a string like 'grain', 'sugarcane', 'seeds', etc.

        # Display product's current source cost
        self.old_src_cost = self.add(
            npyscreen.TitleText,
            name = 'SOURCE COST:',
            value = f'${Product.OBJ_LIST[self.prod_selected].src_cost:,.3f}',
            w_id = 'old_src_cost',
            editable = False,
            )
        # Display product's current Exchange cost of goods sold (COGS)
        self.old_exch_cogs = self.add(
            npyscreen.TitleText,
            name = 'BEP - EXCH:',
            value = f'${Product.OBJ_LIST[self.prod_selected].exch_cogs:,.3f}',
            w_id = 'old_exch_cogs',
            editable = False,
            )

        # Display product's current contract COGS
        self.old_cntr_cogs = self.add(
            npyscreen.TitleText,
            name = 'BEP - CONT:',
            value = f'${Product.OBJ_LIST[self.prod_selected].contr_cogs:,.3f}',
            w_id = 'old_cntr_cogs',
            editable = False,
            )

        self.nextrely += 1

        ### !!! USER-EDITABLE AREA BEGINS HERE !!! ###

        # FORM HEADING
        self.add(
            npyscreen.Textfield,
            w_id = 'form_heading_sub2',
            value = 'New product attributes:',
            editable = False,
        )

        self.nextrely += 1

        # Allow user to change the products source cost
        self.new_src_cost = self.add(
            npyscreen.TitleText,
            name = 'New src cst:',
            value = '',
            editable = True,
        )

        self.nextrely += 1

        # self.add(
        #     npyscreen.Pager,
        #     values=[
        #         'Remember!',
        #         'The break-even prices shown above will',
        #         'not be accurate unless the unit cost of ',
        #         'transportation is up-to-date.',
        #     ],
        #     max_height = 4,
        # )

        # MENU BAR OPTIONS

        self.menu = self.new_menu(name = 'Options')

        self.menu.addItem(
            'Add new product to lineup',
            self.add_product,
            'a',
        )



    def add_product(self):

        self.parentApp.switchForm('ADD_PRODUCT')



    def refresh_prod_attrs(self, product_selected):
        """ Refresh the read-only attributes presented on-npyscreen
            for the object currently selected in the TitleCombo widget
        """

        # Obtain current src_cost, freight, exch_cogs and contr_cogs
        # from Product.OBJ_LIST for the currently selected value in
        # the self.product_selected dropdown menu.
        curr_src_cst   = Product.OBJ_LIST[product_selected].src_cost
        curr_frgt_cst  = Product.OBJ_LIST[product_selected].freight
        curr_exch_be   = Product.OBJ_LIST[product_selected].exch_cogs
        curr_cntr_be   = Product.OBJ_LIST[product_selected].contr_cogs

        self.old_src_cost.value  = f'${curr_src_cst:,.3f}'
        self.old_exch_cogs.value = f'${curr_exch_be:,.3f}'
        self.old_cntr_cogs.value = f'${curr_cntr_be:,.3f}'

        self.new_src_cost.value = ''

        self.display()



    def when_prod_updated(self, widget=None):
        """ Update source cost TitleText widget when user changes
            value in prod_list TitleCombo widget
        """

        npyscreen.blank_terminal()
        # self.display()

        self.prod_selected = widget.values[widget.value].lower()
            # >> a string like 'grain', 'sugarcane', 'seeds', etc.

        self.refresh_prod_attrs(self.prod_selected)



    def on_ok(self):
        """ Execute Product.eval_attrs based on new source cost
            as 'OK' button is being re-purposed here as 'SAVE'
        """

        # Set .editing attribute to True aborts exiting the screen,
        # which is otherwise the default behavior of the ActionForm's
        # OK button. In other words, the user continues working.
        # This is only necessary if .afterEditing is overriden and
        # self.parentApp.setNextForm is set to None therein.
        # self.editing = True

        try:
            idx = 1 if self.new_src_cost.value[0] == '$' else 0
            new_src_cost = float(self.new_src_cost.value[idx:])
        except ValueError:
            npyscreen.notify_confirm(
            'I\'m so sorry, but your Arabic is hard to understand.\n'
            'Please enter an Arabic numeral and try again. Thanks!',
            'This is embarrassing')
            return
        except IndexError:
            npyscreen.notify_confirm(
            'Yeah, um, you might want to actually enter something '
            'in the "New Source Cost" field before trying to update '
            'your products? Hello?',
            'WOW... what a loser...'
            )
            return

        Product.OBJ_LIST[self.prod_selected].update(
            attr='src_cost', val=new_src_cost)

        npyscreen.notify_confirm(
            f'{self.prod_selected.capitalize()} updated successfully '
            f'based on new source cost ${new_src_cost:,.3f}.',
            'All your base are belong to us'
        )

        self.refresh_prod_attrs(self.prod_selected)



    def on_cancel(self):
        """ When user clicks "QUIT" """

        self.parentApp.setNextForm(None)
        # will hopefully go next to afterEditing - it fkg worked!



    # def afterEditing(self):
    #     self.parentApp.setNextForm(None)
    # I have chosen not to use this as any setting installed here
    # will be normative for the entire Form, regardless of
    # circumstance.



class AddProduct(npyscreen.ActionForm):
    """ Enable user to add new products to the lineup """

    # Product.load_products()

    OK_BUTTON_TEXT = "SAVE"
    CANCEL_BUTTON_TEXT = "BACK"

    def create(self):

        self.product_type = self.add(npyscreen.TitleText,
            name = 'Product name',
            value = '',
        )

        self.product_src_cost = self.add(npyscreen.TitleText,
            name = "Source cost",
            value = '',
        )

    def on_ok(self):

        self.editing = True

        try:
            # instantiate instance of Product
            Product(
                self.product_type.value,
                float(self.product_src_cost.value.lower())
                )
            Product.save_products(file = PICKLE_FILENAME)
            npyscreen.notify_confirm('Product added successfully!', 'Success')

        except:
            npyscreen.notify_confirm("That didn't work... :(", "Oops")


    def on_cancel(self):
        self.parentApp.setNextForm('MAIN')



if __name__ == "__main__":
    Product.load_products()
    simcotui = SimcoTUI_App()
    simcotui.run()
