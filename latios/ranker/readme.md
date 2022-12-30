# 2 early 4 deep models

Rnn model
```
0 -> 0.577464759349823
1 -> 0.5492957830429077
2 -> 0.5704225301742554
```
Classic
```
{'max_features': 100}
XGBRegressor -> accuracy: 0.5985915492957746
XGBRegressor -> accuracy: 0.6056338028169014
RandomForestRegressor -> accuracy: 0.6338028169014085
RandomForestRegressor -> accuracy: 0.6126760563380281
RandomForestRegressor -> accuracy: 0.6056338028169014
SVR -> accuracy: 0.676056338028169

{'max_features': 150}
XGBRegressor -> accuracy: 0.6267605633802817
XGBRegressor -> accuracy: 0.6197183098591549
RandomForestRegressor -> accuracy: 0.6971830985915493
RandomForestRegressor -> accuracy: 0.6126760563380281
RandomForestRegressor -> accuracy: 0.6197183098591549
SVR -> accuracy: 0.676056338028169 
```

SVR + tfidf is winner
