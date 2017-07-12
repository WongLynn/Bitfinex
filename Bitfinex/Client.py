#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 11:56:29 2017

@author: Daniel
"""
# Bitfinex.com
#  Limited order commision 0.1%
# Market order commision 0.2%
#PYTHON 3.4
import requests
import json
import base64
import hashlib
import time
import hmac
import csv
import datetime

class Endpoints:

    def __init__(self):
        self.URL = 'https://api.bitfinex.com/v1'
        self.KEY = 'YOUR API KEY'
        self.SECRET = b'YOUR SECRET KEY' 
        pass
    
    def _hash_it(self,j):
        p = base64.standard_b64encode(j.encode('utf8'))
        m = hmac.new(self.SECRET, p, hashlib.sha384)
        m = m.hexdigest()
        return  m
    
    @property
    def _nonce(self):
        return str(time.time() * 100000)
    
    def _Sign(self,Object):
        
        Object_json = json.dumps(Object)
        m = self._hash_it(Object_json)
        headers = {
          'X-BFX-APIKEY' : self.KEY,
          'X-BFX-PAYLOAD' : base64.b64encode(bytes(Object_json, "utf-8")),
          'X-BFX-SIGNATURE' : m
          }
        return headers
    
    def Order(self,Symbol,Amount,Price,Side,Type): # Function to place a new order
        
        # Symbols:  BTCUSD (Bitcoin/US Dollar)
        # Amount: Int
        # Pride: Int, random if market order
        # Side: "buy" or "sell"
        # Type: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders)
       
        Address = '/order/new'
        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'symbol':Symbol,
                'amount':Amount,
                'price':Price,
                'exchange':'bitfinex',
                'side':Side,
                'type':Type
                }
        
        head = self._Sign(payload)
        r = requests.post(self.URL + Address, data={}, headers=head)
        return print(r.json())
    
    
    def CancelOrder(self,Oder_ID): # Function to cancel a order
        
        # Order_ID: the id of the order.
        Address = '/order/cancel'

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'id':Oder_ID
                }

        head = self._Sign(payload)
        r = requests.post(self.URL + Address, data={}, headers=head)
        return print(r.json())

        
    def CancelAllOrders(self): # Function to cancel ALL order
        Address = '/order/cancel/all'

        payload = {
            'request':'/v1' + Address,
            'nonce':self._nonce
            }
        
        head = self._Sign(payload)
        r = requests.post(self.URL + Address, data={}, headers=head)
        return print(r.json())
    
        
    def ReplaceOrder(self,Order_ID,Symbol,Amount,Price,Side,Type):
              
        # Order_ID: the id of the order.
        # Symbols:  BTCUSD (Bitcoin/US Dollar)
        # Amount: Int
        # Pride: Int, random if market order
        # Side: "buy" or "sell"
        # Type: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders)
        Address = '/order/cancel/replace'
        payload = {
                'request':'/v1' + Address,
                'nonce':self._nonce,
                'symbol':Symbol,
                'amount':Amount,
                'price':Price,
                'exchange':'bitfinex',
                'side':Side,
                'type':Type
                }
        head = self._Sign(payload)
        r = requests.post(self.URL + Address, data={}, headers=head)
        return print(r.json())
    
    def BalanceHistory(self,Currency,SinceTemp="01/01/2010",UntilTemp="01/01/2300",Limit=1000,Wallet="exchange"):
        
        # Currency: string
        # Since: DD/MM/YYYY
        # Until: DD/MM/YYYY
        # Limit: Limit number of printed history elements
        # Wallet: “trading”, “exchange”, “deposit”.
 
        Since = str(time.mktime(datetime.datetime.strptime(SinceTemp, "%d/%m/%Y").timetuple()))
        Until = str( time.mktime(datetime.datetime.strptime(UntilTemp, "%d/%m/%Y").timetuple()))

        Address = "/history"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'currency':Currency,
                'since':Since,
                'until':Until,
                'limit':Limit,
                'wallet': Wallet
                }
        
        head = self._Sign(payload)
        r = requests.post(self.URL + Address, data={}, headers=head)
        
        # Write automatically a csv file with the balance history !
        BalanceHistoryJSON = r.json()
        f = csv.writer( open("FOLDER ADDRESS/BalanceHistory_" + Currency + ".csv", "w",newline=''))
        f.writerow( [ 'amount','balance','currency','description','timestamp'])
        for i in range(len(BalanceHistoryJSON)):
            f.writerow([BalanceHistoryJSON[i]['amount'],
                       BalanceHistoryJSON[i]['balance'],
                       BalanceHistoryJSON[i]['currency'],
                       BalanceHistoryJSON[i]['description'],
                       BalanceHistoryJSON[i]['timestamp']])
        
        return r.json()
    
    def Ticker(self,Symbol):
        
        Address = "/pubticker/" + Symbol

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'symbol':Symbol
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        
        return r.json()
    
    def Orderbook(self,Symbol):
        
        Address = "/book/" + Symbol

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'symbol':Symbol
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        
        return r.json()
    
    def Trades(self,Symbol):
    
        Address = "/trades/" + Symbol

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce,
                'symbol':Symbol
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        
        return r.json()
    
    def Symbols(self):
        
        Address = "/symbols"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        return r.json()
    
    def AccountInfo(self):
         
        Address = "/account_infos"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        return r.json()  
    
    def AccountFees(self):
        
        Address = "/account_fees"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        return r.json() 
    
    def Summary(self):
        Address = "/summary"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        return r.json()
    
    def WalletBalances(self):
        Address = "/balances"

        payload = {
                'request':'/v1'+Address,
                'nonce':self._nonce
                }
        head = self._Sign(payload)
        r = requests.get(self.URL + Address, data={}, headers=head)
        return r.json()
        


