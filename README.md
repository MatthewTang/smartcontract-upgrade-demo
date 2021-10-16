### notes
- we use initialiser instead of constructor for implementation contract
- we call our initialiser function when the proxyAdmin call the upgradeAndCall ( transparentUpgradeableProxy, _data (our initialiser function in byte ) ) 

test  
1   
2 
3
---
hex zero is "0x"  
repo reference: https://github.com/PatrickAlphaC/upgrades-mix
