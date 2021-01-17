import requests, re, time
import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# test url
# https://www.smythstoys.com/uk/en-gb/toys/great-value-toys-/flocked-dartboard/p/183407

# profile
email = ''
firstname = ''
lastname = ''
mobilenumber = ''
post_code = ''
del1 = ''
del2 = ''
city = ''
county = ''
chrome_driver_path = '' # use \\ instead of \ for chrome_driver_path
#

h = {"authority": 'www.smythstoys.com',
      "method": 'GET',
      "user-agen": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

####
base_url = 'https://www.smythstoys.com'
atc_url = 'https://www.smythstoys.com/uk/en-gb/cart/add'
pre_check_url_1 = 'https://www.smythstoys.com/uk/en-gb/cart/checkout'
pre_check_url_2 = 'https://www.smythstoys.com/uk/en-gb/login/checkout'
####

product_url = input('Enter product url: ')
sku = str(input('Enter SKU: '))

path_split = product_url.split(base_url)
path = path_split[1]

with requests.Session() as s:
    r = s.get(base_url, headers=h)
    cookies = r.cookies
    csrf = re.findall(r"SRFToken = \"(.*?)\"", r.text)[0]

    sh = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '//uk//en-gb//cart//add',
          "x-requested-with": 'XMLHttpRequest',
          "upgrade-insecure-requests": '1',
          "scheme": 'https',
          "origin": base_url,
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": product_url,
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'empty',
          "sec-fetch-mode": 'cors',
          "sec-fetch-site": 'same-origin'
    }
    
    d = {"gty": '1',
          "preOrder": 'false',
          "productCodePost": sku,
          "deliveryType": 'homeDelivery',
          "storeId": '8796224587768',
          "storeName": 'Leeds Birstall',
          "brand": '',
          "category": '',
          "currency": 'GBP',
          "CSRFToken": csrf
        }

    atc = False
    while not atc:
        try:
            r = s.post(atc_url, headers=sh, data=d, cookies=cookies)        
        except:
            print('Cannot reach /cart/add')
        if r.status_code == 200:
            print('Added to cart')
            cart_cookies = r.cookies
            atc = True
        elif r.status_code == 403:
            print('Error adding to cart...')
            time.sleep(7)
        else:
            print('Error adding to cart [1]...')
            time.sleep(7)

    th = {"authority": 'www.smythstoys.com',
          "method": 'GET',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/login/checkout',
          "upgrade-insecure-requests": '1',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/cart',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "sec-fetch-user": '?1',
          
    }
    # get checkout 
    checkout_login = False
    while not checkout_login:
        r = s.get(pre_check_url_2, headers=th, cookies=cart_cookies, allow_redirects=True)
        if r.url == 'https://www.smythstoys.com/uk/en-gb/login/checkout':
            checkout_login = True
            print('Getting checkout')
        else:
            print('Error getting checkout previews')
            time.sleep(3)

    # submit temp email for guest

    fh = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/login/checkout/checkuser',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/cart',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'empty',
          "sec-fetch-mode": 'cors',
          "sec-fetch-site": 'same-origin',
          "x-requested-with": 'XMLHttpRequest'
    }

    check_email_data = {
        "email": email,
        "confirmEmail": email,
        "CSRFToken": csrf
        }

    check_user_bool = False
    while not check_user_bool:
        check_user_url = 'https://www.smythstoys.com/uk/en-gb/login/checkout/checkuser'
        r = s.post(check_user_url, headers=fh, data=check_email_data)
        if r.status_code == 200:
            check_user_bool = True
            print('Submitting details')
        else:
            print('Error getting checkout previews')
            time.sleep(3)
            

    fih = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/login/checkout/guest',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/login/checkout',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "upgrade-insecure-requests": '1',
          "origin": 'https://www.smythstoys.com'
    }

    guest_checkout_bool = False
    while not guest_checkout_bool:
        guest_checkout = 'https://www.smythstoys.com/uk/en-gb/login/checkout/guest'
        r = s.post(guest_checkout, headers=fih, data=check_email_data, allow_redirects=True)
        if r.status_code == 200 or r.status_code == 302:
            guest_checkout_bool = True
            print('Submitting Address')
        else:
            pass

    sh = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/checkout/multi/delivery-address/add',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-address/add',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "upgrade-insecure-requests": '1',
          "origin": 'https://www.smythstoys.com'
    }
    
    add_delivery_payload = {
        "deviceType": 'Mobile',
        "pudoId": '',
        "pudoSelected": 'false',
        "pudoAvailable": '',
        "deliveryChannel": 'HOME_DELIVERY',
        "customerType": 'Guest',
        "addNewAddressClick": '',
        "editAddressClick": '',
        "showSaveAddressAfterErrorsOnEdit": 'false',
        "useThisAddressClick": '',
        "klarnaReAuthToken": '',
        "klarnaEmailId": '',
        "klarnaAddressId": '',
        "klarnaDeliveryAddressChanged": 'false',
        "address.addressId": '',
        "address.emailNotAvailable": 'false',        
        "address.firstName": firstname,
        "address.lastName": lastname,
        "address.phone": mobilenumber,
        "address.findPostCode": '',
        "address.pudoStoreName": '',
        "address.line1": del1,
        "address.line2": del2,
        "address.townCity": city,
        "address.county": county,
        "address.postcode": post_code,
        "address.countryIso": 'GB',
        "address.saveInAddressBook": 'true',
        "_address.saveInAddressBook": 'on',
        "CSRFToken": csrf
        }

    add_delivery_bool = False
    while not add_delivery_bool:
        add_delivery_url = 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-address/add'
        r = s.post(add_delivery_url, headers=sh, data=add_delivery_payload)

        if r.url == 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-method/choose':
            add_delivery_bool = True
            print('Submitted delivery information')
        else:
            print('Error submitting delivery information')
            time.sleep(5)

    
    seh = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/checkout/multi/delivery-address/add',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '198',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-address/add',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "upgrade-insecure-requests": '1',
          "origin": 'https://www.smythstoys.com'
    }

    select_del_payload = {
        "delivery_method": 'STANDARD_REGULAR',
        "deviceType": 'Mobile',
        "CSRFToken": csrf
        }

    select_delivery_url = 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-method/select'
    select_bool = False
    while not select_bool:
        r = s.post(select_delivery_url, headers=seh, data=select_del_payload, allow_redirects=True)
        if r.url == 'https://www.smythstoys.com/uk/en-gb/checkout/multi/summary/view?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options':
            print('Added delivery method')
            select_bool = True
        else:
            print('Error selecting delivery method')

    # get cc previews
    date_time_unfilt = datetime.datetime.now()
    time1 = re.findall(r" (.*?).", str(date_time_unfilt))[0]
    nh = {"authority": 'www.smythstoys.com',
          "method": 'POST',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/checkout/multi/payment-method/paymentPreProcess',
          "scheme": 'https',
          "accept": '*/*',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "content-length": '668',
          "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
          "referer": 'https://www.smythstoys.com/uk/en-gb/checkout/multi/summary/view?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "x-requested-with": 'XMLHttpRequest',
          "origin": 'https://www.smythstoys.com'
    }

    cc_to_send_data = f'bill_to_forename={firstname},bill_to_surname={lastname},bill_to_email={email},bill_to_address_line1={del1},bill_to_address_line2={del2},bill_to_address_city={city},bill_to_address_state={county},bill_to_address_country=GB,bill_to_address_postal_code={post_code}'

    temp = datetime.datetime.now()
    uuidstart = '149197772'
    uuid2 = temp.isoformat(timespec='minutes')
    final_uuid = uuidstart + uuid2 + 'Z'
    f_uuid = uuid2 + 'Z'

    # refresh to get checkout previews again to scrape checkout data

    cc_check_h = {"authority": 'www.smythstoys.com',
          "method": 'GET',
          "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
          "path": '/uk/en-gb/checkout/multi/payment-method/add?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options',
          "scheme": 'https',
          "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          "accept-encoding": 'gzip, deflate, br',
          "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
          "cache-control": 'max-age=0',
          "referer": 'https://www.smythstoys.com/uk/en-gb/checkout/multi/delivery-method/choose',
          "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
          "sec-ch-ua-mobile": '?0',
          "sec-fetch-dest": 'document',
          "sec-fetch-mode": 'navigate',
          "sec-fetch-site": 'same-origin',
          "sec-fetch-user": '?1',
          "upgrade-insecure-requests": '1'
    }
    
    cc_scrape = 'https://www.smythstoys.com/uk/en-gb/checkout/multi/payment-method/add?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options'
    r = s.get(cc_scrape, headers=cc_check_h, allow_redirects=True)

    # hybrid checkout
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options,
                                  executable_path=chrome_driver_path)
    
    driver.get('https://www.smythstoys.com/uk/en-gb/checkout/multi/summary/view?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options')
    for c in s.cookies :
        driver.add_cookie({'name': c.name, 'value': c.value})
    driver.get('https://www.smythstoys.com/uk/en-gb/checkout/multi/payment-method/add?siteName=UK+Site&isCirculatorScriptEnable=true&pageTitle=Checkout+Delivery+Options')







    
