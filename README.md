# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129888944077447

path, amountIn, amountOut

B->A : 5, 5.655321988655323

A->D : 5.655321988655323, 2.458781317097934

D->C : 2.458781317097934, 5.0889272933015155

C->B : 5.0889272933015155, 20.129888944077447

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

Slippage in AMM refers to the difference between the expected price of a trade and the price at which the trade is actually executed. 

Uniswap V2 allows users to set a maximum slippage tolerance when they make a trade. If the price changes beyond this tolerance by the time the transaction is executed, the transaction will fail, and the user's funds will not be traded.

```
def get_output_amount(input_amount, input_reserve, output_reserve, max_slippage):
    input_amount_with_fee = input_amount * 0.997
    numerator = input_amount_with_fee * output_reserve
    denominator = input_reserve + input_amount_with_fee
    output_amount = numerator / denominator

    # Calculate minimum output amount based on max slippage
    min_output_amount = output_amount * (1 - max_slippage)

    return {
        "output_amount": output_amount,
        "min_output_amount": min_output_amount,
        "slippage": output_reserve / (output_reserve - output_amount) - 1
    }

# Example usage:
input_amount = 100
input_reserve = 1000
output_reserve = 5000
max_slippage = 0.01

result = get_output_amount(input_amount, input_reserve, output_reserve, max_slippage)
print(result)
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

The rationale behind subtracting a minimum liquidity amount upon the initial liquidity minting is to prevent the possibility of someone owning an entire pool by being the first liquidity provider. If the first liquidity provider could own all the liquidity tokens, they could manipulate the pool's prices or potentially drain the reserves through arbitrage. By subtracting and permanently locking away a small amount of liquidity, Uniswap ensures that no single participant can ever own 100% of the pool's liquidity tokens.


## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

The intention behind this formula is to maintain the constant product formula ( x * y = k ). This ensures that the relative value of each liquidity token remains constant with respect to the pool's reserves. The formula prevents dilution of existing liquidity providers' share in the pool and ensures fair distribution of LP tokens based on the current reserve ratios.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

When a user initiates a swap with a slippage tolerance that allows for price variation, an attacker can spot this transaction in the mempool before it's confirmed. The attacker then places a buy order for the same asset with a higher gas fee to have it executed first, increasing the asset's price. After the user's transaction is executed at this inflated price, the attacker sells the asset at a profit, causing the user to receive fewer tokens than expected. This impacts users by reducing the efficiency and cost-effectiveness of their trades.
