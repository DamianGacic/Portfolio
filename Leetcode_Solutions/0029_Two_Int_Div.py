'''
Given two integers dividend and divisor, divide two integers without using multiplication, division and mod operator.

Return the quotient after dividing dividend by divisor.

The integer division should truncate toward zero, which means losing its fractional part.
For example, truncate(8.345) = 8 and truncate(-2.7335) = -2.

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = truncate(3.33333..) = 3.
Example 2:

Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = truncate(-2.33333..) = -2.
Note:

Both dividend and divisor will be 32-bit signed integers.
The divisor will never be 0.
Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−2^31,  2^31 − 1].
For the purpose of this problem, assume that your function returns 2^31 − 1 when the division result overflows.
'''
class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        a, b, res = abs(dividend), abs(divisor), 0
        
        while a >= b:
            x = 0
            while a - (b << 1 << x) >= 0:
                x += 1
            res += 1 << x
            a -= b << x
            
        if not (dividend >= 0) is (divisor >= 0):
            res = -res

        return min(max(-2 ** 31, res), 2 ** 31 - 1)
