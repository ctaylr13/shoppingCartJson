import json, ast

class Shopping:
    # Read in JSON convert to Dictionaries
    products = json.loads(open('products.json').read())
    cart = json.loads(open('sample_cart.json').read())

    # Remove the unicode characters
    products = ast.literal_eval(json.dumps(products))
    cart = ast.literal_eval(json.dumps(cart))

    # reduce the to list
    products = products.values()
    cart = cart['cart']['lineItems']

    # return a list of tags in the cart
    def cartTags(cart):
        cartTags = {}
        for x in cart:
            a = x["tags"]
            i = []
            for y in a: 
                y = y.replace('-', " ")
                i.append(y)
                cartTags[x["id"]] = i
        return cartTags


    #remove items IDs from inventory that are in cart
    def possibleSuggestions(product, cart):
        productIDs = []
        for x in product:
            productIDs.append(x['id'])

        cartIDs = []
        for x in cart: 
            cartIDs.append(x['id'])

        for item in productIDs:
            for item1 in cartIDs:
                if item == item1:
                    productIDs.remove(item)

        return productIDs

    # JSON list of possible remaining inventoery
    def reduceProductJson(product, ids):
        reducedList = []
        for x in product:
            for y in ids:
                if x['id'] == y:
                    reducedList.append(x)
        return reducedList

    # matches cart to tags to return suggestions 
    # returns dictionary of cart id with id's that are suggestions 
    def matchTags(products, cart):
        prodNoDash = {}
        for x in cart:
            for y in products:
                i = 0
                dashArray = []
                while(i < len(y['tags'])):
                    a = y['tags'][i].replace('-', ' ')
                    dashArray.append(a)
                    prodNoDash[y["id"]] = dashArray
                    i += 1

        suggestion = {}
        for key in cart.keys():
            holder = []
            for tag in cart[key]:
                for item in prodNoDash:
                    for itemTag in prodNoDash[item]:
                        if itemTag == tag and item not in holder:
                            holder.append(item)
            suggestion[key] = holder
        return suggestion 
   

    # returns json of cart with suggestion field added 
    # suggestion field includes suggestion json for item
    def backtoJson(matches, products):
        newJson = {}
        
        for key in matches: 
            holder = {}
            matchesHolder = []
            for item in products: 
                if key == item['id']:
                    holder = item
                elif item['id'] in matches[key]:
                    matchesHolder.append(item)
                newJson[key] = holder
                newJson[key]["upsell"] = matchesHolder

        return newJson

    def freeShipping(cart):
        cartPrices = []
        status = ''
        for x in cart:
            cartPrices.append(x['price']) 

        results = list(map(int, cartPrices))
        results_sum = sum(results)
        if results_sum > 10000:
            status = "this cart is eligible for free shipping"
        else:
            remaining = 10000 - results_sum
            remainingStr = str(remaining)
            status = "add "+remainingStr+ " for this cart to be eligible for free shipping" 
            
            
        return status                       
    
    # List of Product IDs
    productIDs = possibleSuggestions(products, cart)
    # List of possible inventory
    reducedProduct = reduceProductJson(products, productIDs)
    # returns cart ids and tags
    possibleTags = cartTags(cart)  
    # return ids of matching tags
    matchIds = matchTags(reducedProduct, possibleTags)
    # converts to json
    jsonList = backtoJson(matchIds, products)
    # determines if item is eligible for free shipping
    shippingStatus = freeShipping(cart)
    print(freeShipping(cart))
    print(jsonList)
   
    

customerCart = Shopping




