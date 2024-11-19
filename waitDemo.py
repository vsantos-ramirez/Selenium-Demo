import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
driver.implicitly_wait(5)
text = "co"


#  Test to validate the number of suggestions when Co is typed
def test1_how_many(inp):
    driver.find_element(By.CSS_SELECTOR, ".search-keyword").send_keys(inp)
    time.sleep(3)
    how_many = driver.find_elements(By.XPATH, "//div[@class='products']/div")
    if len(how_many) != 2:
        raise Exception("number of items must be 2")
    else:
        print(len(how_many))
        return print("Test of suggestions # Passed\n")

#  Test to confirm the items suggested when Co is typed
def test2_items():
    options = ["Corn - 1 Kg", "test - 100 Kg", "Brocolli - 1 Kg"]
    for products in options:
        try:
            scan = driver.find_element(By.XPATH, f"//h4[text()='{products}']").text
            print(scan)
        except Exception:
            print(f"Fail suggestion {products} not found\n")
            break


#  Test to add items to cart and its confirmation
def test3_addtocart():
    button = driver.find_elements(By.XPATH, "//div[@class='products']/div")
    items_added = []
    items_in_cart = []
#  Adding items to cart, but two items for corn
    for adding in button:
        product = adding.find_element(By.XPATH, "h4[@class='product-name']").text
        if product in "Corn - 1 Kg":
            adding.find_element(By.XPATH, "div/a[@class='increment']").click()
            adding.find_element(By.XPATH, "div/button").click()
            print(f"adding 2 {product} to cart")
        else:
            adding.find_element(By.XPATH, "div/button").click()
            print(f"adding {product} to cart")
        items_added.append(product)
    driver.find_element(By.CSS_SELECTOR, ".cart-icon").click()
#  Confirm that items added are in cart with correct quantity and amount
    for added in [1, 2]:
        item_in_cart = driver.find_element(
            By.XPATH, f"(//div/p[@class='product-name'])[{added}]").text
        quantity = driver.find_element(
            By.XPATH, f"(//div/p[@class='quantity'])[{added}]").text
        amount = driver.find_element(
            By.XPATH, f"(//div/p[@class='amount'])[{added}]").text
        if "Corn - 1 Kg" == item_in_cart:
            assert quantity == "2 Nos."
            assert amount == "150"
        elif "Brocolli - 1 Kg" == item_in_cart:
            assert quantity == "1 No."
            assert amount == "120"
        items_in_cart.append(item_in_cart)
    assert items_in_cart == items_added
    return print("Test to add to cart Passed\n")

def checkout():
    driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()
    driver.find_element(By.CSS_SELECTOR, ".promoCode").send_keys("rahulshettyacademy")
    driver.find_element(By.CSS_SELECTOR, ".promoBtn").click()

# Sum validation using CSS
    prices = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(5) p")
    total = int(driver.find_element(By.CSS_SELECTOR, ".totAmt").text)
    sum = 0
    for price in prices:
        sum = sum + int(price.text)
    print(f"this is the total {sum}")
    assert total == sum

#  Example of how to declare an explicit wait for certain scenarios
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".promoInfo")))
    promo = driver.find_element(By.CSS_SELECTOR, ".promoInfo").text
    assert promo == "Code applied ..!"

# Example of chaining when you have already a part of a path store in a variable
    driver.find_element(By.XPATH, "//button[text()='Place Order']").click()
    dropdown = Select(driver.find_element
                      (By.CSS_SELECTOR, "div[class='wrapperTwo'] div select"))
    dropdown.select_by_visible_text("Mexico")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, ".chkAgree").click()
    driver.find_element(By.XPATH, "//div[@class='wrapperTwo']/button").click()


test1_how_many(text)
test2_items()
test3_addtocart()
checkout()
time.sleep(15)
