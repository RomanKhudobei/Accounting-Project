database = {}

# account is special, if it doesn't have sub_account
SPECIAL_ACCOUNTS = ['01', '03', '05', '06', '08', '09', '22', '23', '24',
                    '25', '26', '27', '38', '39', '43', '46', '54', '55',
                    '69', '76', '79', '84', '85', '91', '92', '93', '98']

# valid accounts of accounting (3 digits)
# to avoid entering accounts like '999' or any mistakes in entering
# and it's a lot easier to validate account
VALID_ACCOUNTS = ['100', '101', '102', '103', '104', '105', '106', '107', 
                  '108', '109', '111', '112', '113', '114', '115', '116', 
                  '117', '121', '122', '123', '124', '125', '127', '131', 
                  '132', '133', '134', '135', '141', '142', '143', '151', 
                  '152', '153', '154', '155', '161', '162', '163', '164', 
                  '165', '166', '181', '182', '183', '184', '191', '193', 
                  '201', '202', '203', '204', '205', '206', '207', '208', 
                  '209', '211', '212', '213', '281', '282', '283', '284', 
                  '285', '286', '301', '302', '311', '312', '313', '314', 
                  '315', '316', '331', '332', '333', '334', '335', '341', 
                  '342', '351', '352', '361', '362', '363', '364', '371', 
                  '372', '373', '374', '375', '376', '377', '378', '379', 
                  '401', '402', '403', '404', '411', '412', '413', '414', 
                  '421', '422', '423', '424', '425', '441', '442', '443', 
                  '451', '452', '453', '471', '472', '473', '474', '475', 
                  '476', '477', '478', '481', '482', '483', '484', '491', 
                  '492', '493', '494', '495', '496', '501', '502', '503', 
                  '504', '505', '506', '511', '512', '521', '522', '523', 
                  '531', '532', '601', '602', '603', '604', '605', '606', 
                  '611', '612', '621', '622', '631', '632', '633', '641', 
                  '642', '643', '644', '651', '652', '654', '655', '661', 
                  '662', '663', '671', '672', '680', '681', '682', '683', 
                  '684', '685', '701', '702', '703', '704', '705', '710', 
                  '711', '712', '713', '714', '715', '716', '717', '718', 
                  '719', '721', '722', '723', '731', '732', '733', '740', 
                  '741', '742', '744', '745', '746', '791', '792', '793', 
                  '801', '802', '803', '804', '805', '806', '807', '808', 
                  '809', '811', '812', '813', '814', '815', '816', '821', 
                  '824', '831', '832', '833', '901', '902', '903', '904', 
                  '940', '941', '942', '943', '944', '945', '946', '947', 
                  '948', '949', '951', '952', '961', '962', '963', '970', 
                  '971', '972', '974', '975', '976', '977', '021', '021', 
                  '022', '023', '024', '025', '041', '042', '071', '072']

def check_valid_account(account):
    '''Checks account. If it's not valid - throw according exception.
    If it's valid - nothing happens.'''
    assert type(account) == str, 'Account has to be str type.'

    try:
        int(account)
    except:
        # to raise error with message
        assert str == int, 'Account should be a number str type.'

    if account in SPECIAL_ACCOUNTS:
        pass
    elif account in VALID_ACCOUNTS:
        pass
    else:
        # to raise error with message
        assert account in SPECIAL_ACCOUNTS, 'You entered invalid account.'

def check_in(account, start_remainder=0):
    '''Check out if account already in database 
    and if it's not - creates data structure for it.
    '''
    check_valid_account(account)
    if account in SPECIAL_ACCOUNTS:
        if account not in database:
            database[account] = {
                'start_remainder': start_remainder, 
                'debit': {}, 
                'credit': {}
            }
        return account, None
    else:
        # e.g. if given argument account is 301, than 
        # account = 30, sub_account = 301
        sub_account, account = account, account[0:2]
        if account not in database:
            database[account] = {
                sub_account: {
                    'start_remainder': start_remainder, 
                    'debit': {}, 
                    'credit': {}
                    }
                }
        elif sub_account not in database[account]:
            database[account].update({
                sub_account: {
                    'start_remainder': start_remainder, 
                    'debit': {}, 
                    'credit': {}
                    }
                })
        return account, sub_account

def set_start_remainder(account, start_remainder):
    '''Rewrites start_remainder, even if it already exist.'''
    account, sub_account = check_in(account)
    if sub_account == None:
        database[account]['start_remainder'] = start_remainder
    else:
        database[account][sub_account]['start_remainder'] = start_remainder

def add_debit_operation(number, debit, amount, description):
    '''Adds operation to debit account. If it's already exist - 
    rewrites it.'''
    account, sub_account = check_in(debit)
    if sub_account == None:
        database[account]['debit'].update({
            number: {
                'amount': amount, 
                'description': description
            }
        })
    else:
        database[account][sub_account]['debit'].update({
            number: {
                'amount': amount, 
                'description': description
            }
        })

def add_credit_operation(number, credit, amount, description):
    '''Adds operation to credit account. If it's already exist -
    rewrites it.'''
    account, sub_account = check_in(credit)
    if sub_account == None:
        database[account]['credit'].update({
            number: {
                'amount': amount, 
                'description': description
            }
        })
    else:
        database[account][sub_account]['credit'].update({
            number: {
                'amount': amount, 
                'description': description
            }
        })

def add_operation(number, debit, credit, amount, description=None):
    '''Adds operation to accounting database.'''
    assert type(number) == str, 'Number of operation has to be a str type.'
    assert type(description) == str or description == None, 'Description has to be a str type'
    assert amount >= 0, 'Amount has to be greater or equal to zero.'

    try:
        int(number)
    except:
        assert str == int, 'Number of operation has to be number str type.'

    add_debit_operation(number, debit, amount, description)
    add_credit_operation(number, credit, amount, description)

def calculate_debit_turnover(account, sub_account=None):
    '''The summ of all debit/credit operations is called turnover.
    This function calculate debit turnover.'''
    if account in database:  # additional checking for case if function invoked alone
        turnover = 0
        if account in SPECIAL_ACCOUNTS:
            operations = database[account]['debit']
            for operation in operations:
                turnover = turnover + operations[operation]['amount']
            return turnover
        else:
            if sub_account in database[account]:
                operations = database[account][sub_account]['debit']
                for operation in operations:
                    turnover = turnover + operations[operation]['amount']
                return turnover

def calculate_credit_turnover(account, sub_account=None):
    '''The summ of all debit/credit operations is called turnover.
    This function calculate credit turnover.'''
    if account in database:  # additional checking for case if function invoked alone
        turnover = 0
        if account in SPECIAL_ACCOUNTS:
            operations = database[account]['credit']

            for operation in operations:
                turnover = turnover + operations[operation]['amount']

            return turnover
        else:
            if sub_account in database[account]:
                operations = database[account][sub_account]['credit']

                for operation in operations:
                    turnover = turnover + operations[operation]['amount']

                return turnover

def sumbit_turnover():
    '''Caltulates and sets debit/credit turnover for each account.'''
    for account in database:
        if account in SPECIAL_ACCOUNTS:
            database[account]['debit']['turnover'] = calculate_debit_turnover(account, None)
            database[account]['credit']['turnover'] = calculate_credit_turnover(account, None)
        else:
            for sub_account in database[account]:
                database[account][sub_account]['debit']['turnover'] = calculate_debit_turnover(account, sub_account)
                database[account][sub_account]['credit']['turnover'] = calculate_credit_turnover(account, sub_account)

def sumbit_end_remainder():
    '''Calculates and sets end remainder for each account.'''
    for account in database:
        if account in SPECIAL_ACCOUNTS:
            assert 'turnover' in database[account]['debit'], 'You have to invoke sumbit_turnover at first.'

            start_remainder = database[account]['start_remainder']
            debit_turnover = database[account]['debit']['turnover']
            credit_turnover = database[account]['credit']['turnover']

            end_remainder = start_remainder + debit_turnover - credit_turnover
            database[account]['end_remainder'] = end_remainder
        else:
            assert 'turnover' in database[account][sub_account]['debit']

            for sub_account in database[account]:

                start_remainder = database[account][sub_account]['start_remainder']
                debit_turnover = database[account][sub_account]['debit']['turnover']
                credit_turnonver = database[account][sub_account]['credit']['turnover']

                end_remainder = start_remainder + debit_turnover - credit_turnonver
                database[account][sub_account]['end_remainder'] = end_remainder