class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        if divisor == 1:
            return dividend
        if dividend == -(2**31) and divisor == -1:
            return 2**31 - 1
        positive = True if (dividend < 0 and divisor < 0) or (dividend > 0 and divisor > 0) else False
        dividend = abs(dividend)
        divisor = abs(divisor)
        quotient = 0
        while dividend >= divisor:
            zeros = ""
            while dividend > int(str(divisor) + zeros):
                zeros += "0"
            zeros = zeros[:-1]
            dividend -= int(str(divisor) + zeros)
            quotient += int("1" + zeros)

        return quotient if positive else -quotient


# class Solution:
#     def divide(self, dividend: int, divisor: int) -> int:
#         if dividend == 1:
#             return divisor
#         if divisor == -(2**31) and dividend == -1:
#             return 2**31 - 1
#         sign = (divisor > 0 and dividend > 0) or (divisor < 0 and dividend < 0)
#         divisor = -divisor if divisor < 0 else divisor
#         dividend = -dividend if dividend < 0 else dividend
#         ans = 0
#         while divisor <= dividend:
#             x = dividend
#             cnt = 1
#             while divisor <= (x << 1):
#                 x <<= 1
#                 cnt <<= 1
#             divisor -= x
#             ans += cnt

#         return ans if sign else -ans




        