from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()                # Load the first page
        bot.dismiss_sign_in_info()           # Dismiss the pop-up (if present)
        bot.change_currency(currency='USD')  # Change currency to USD
        bot.select_place_to_go('New York')   # Set destination
        bot.select_dates(check_in_date='2024-12-19', check_out_date='2024-12-25')  # Set travel dates
        bot.select_adults(1)                 # Set number of adults
        bot.click_search()                   # Click search button
        bot.apply_filtrations()
        bot.refresh() # A workaround to let our bot to grab the data properly
        bot.report_results()              # Apply filters like star rating and price sorting

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line.\n'
            'Please add your Selenium Drivers to PATH.\n'
            'For Windows:\n'
            '    set PATH=%PATH%;C:\\path-to-your-folder\n\n'
            'For Linux:\n'
            '    PATH=$PATH:/path/to/your/folder/\n'
        )
    else:
        raise
