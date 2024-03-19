# This script processes a given text file to produce a required output.
# 
# Created for the AiCore Hackathon.
#
# Requires the input.txt in the same folder as the script to be run.
#
# Daniel Killen 17/03/2024

auctions = {}

def update_bid(tick):
    """
    Updates an existing auction with a new bid
    """
    # confirm bid is within time limit
    if int(tick[0]) < auctions[tick[3]]["end_time"]:
        # confirm new bid is higher
        if float(tick[4]) > auctions[tick[3]]["current_bid"]:
            # set last price
            auctions[tick[3]]["previous_bid"]=auctions[tick[3]]["current_bid"]
            # update latest price
            auctions[tick[3]]["current_bid"]=float(tick[4])
            # update winning user
            auctions[tick[3]]["winning_user"]=tick[1]
            # update if reserve met
            if float(tick[4]) > auctions[tick[3]]["reserve_price"]:
                auctions[tick[3]]["reserve_met"]=True
    return


def create_auction(tick):
    """
    Creates a new auction
    """
    auctions[tick[3]] = {
        "reserve_price": float(tick[4]),
        "current_bid": 0,
        "previous_bid": 0,
        "reserve_met": False,
        "winning_user": "",
        "end_time": int(tick[5])
        }
    return     


with open('input.txt','r') as input_file:
    input = input_file.readlines()

for i in input:
    tick = i.strip().split('|')
    # check if heartbeat
    if len(tick) == 1:
        pass
    # check if sell
    elif tick[2] == "SELL":
        create_auction(tick)
    # check if bid
    elif tick[2] == "BID":
        update_bid(tick)

for i, key in enumerate(auctions):
    close_time=auctions[key]['end_time']
    item = key       
    if auctions[key]['reserve_met'] == True:
        status= 'SOLD'
        user_id=auctions[key]['winning_user']
        price_paid=auctions[key]['previous_bid']
    else:
        status = 'UNSOLD'
        user_id=""
        price_paid=0.00

    print(f"{close_time}|{item}|{user_id}|{status}|{price_paid:.2f}")
